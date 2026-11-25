#!/usr/bin/env python3
"""Validate repository structure, Markdown rules, links, and optionally live URLs."""

from __future__ import annotations

import argparse
import concurrent.futures
import http.client
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FILES = (
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "LICENSE",
    ".github/ISSUE_TEMPLATE/config.yml",
    "docs/validacao-brasil.md",
    "docs/criterios-e-fora-da-lista.md",
    "assets/hero-banner.png",
    "assets/mapa-ecossistema-dark.svg",
    "assets/mapa-ecossistema-light.svg",
)
MAX_MD_LINES = 300
PLACEHOLDER_HOSTS = {"example.com", "example.org", "example.net", "localhost", "127.0.0.1"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_ATTR_RE = re.compile(r'\b(?:src|srcset)="([^"]+)"')
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
SOFT_HTTP_STATUS = {403, 405, 429, 999}
HARD_HTTP_STATUS = {404, 410}


def github_slug(text: str, counts: dict[str, int]) -> str:
    """Return a GitHub-compatible heading anchor slug."""
    cleaned = "".join(ch for ch in text.strip().lower() if ch.isalnum() or ch in (" ", "-"))
    base = cleaned.replace(" ", "-")
    idx = counts.get(base, 0)
    counts[base] = idx + 1
    return base if idx == 0 else f"{base}-{idx}"


def parse_markdown(path: Path) -> tuple[list[str], set[str], list[tuple[int, str, str]]]:
    """Extract lines, heading slugs, and (line_no, section_title, target) links."""
    lines = path.read_text(encoding="utf-8").splitlines()
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    links: list[tuple[int, str, str]] = []
    in_fence = False
    current_h2 = ""

    for lineno, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = HEADING_RE.match(line)
        if heading:
            level, title = heading.groups()
            slugs.add(github_slug(title, counts))
            if len(level) == 2:
                current_h2 = title
        for match in LINK_RE.finditer(line):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            links.append((lineno, current_h2, target))
        for match in HTML_ATTR_RE.finditer(line):
            for part in match.group(1).split(","):
                asset = part.strip().split()[0] if part.strip() else ""
                if asset and not asset.startswith(("https://", "http://", "data:")):
                    links.append((lineno, current_h2, asset))
    return lines, slugs, links


def check_live_url(url: str) -> tuple[str, str]:
    """Check an external URL with HEAD then GET fallback. Returns (level, message)."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return ("ok", f"{resp.status}")
        except urllib.error.HTTPError as exc:
            if exc.code in SOFT_HTTP_STATUS and method == "HEAD":
                continue
            if exc.code in SOFT_HTTP_STATUS:
                return ("warn", f"HTTP {exc.code} (bot/rate check)")
            if exc.code in HARD_HTTP_STATUS:
                return ("error", f"HTTP {exc.code}")
            if method == "HEAD":
                continue
            return ("warn", f"HTTP {exc.code}")
        except urllib.error.URLError as exc:
            return ("error", f"network/DNS error: {exc.reason}")
        except (TimeoutError, http.client.HTTPException, OSError) as exc:
            if method == "HEAD":
                continue
            return ("warn", f"connection issue: {exc}")
    return ("warn", "unverified")


def validate_repo(check_urls: bool) -> int:
    """Run all structural and optional live URL checks."""
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    md_files = sorted(
        p for p in ROOT.rglob("*.md") if ".git" not in p.parts
    )
    parsed: dict[Path, tuple[list[str], set[str], list[tuple[int, str, str]]]] = {}
    for md in md_files:
        parsed[md] = parse_markdown(md)
        lines, _, _ = parsed[md]
        rel = md.relative_to(ROOT)
        if len(lines) >= MAX_MD_LINES:
            errors.append(f"{rel}: {len(lines)} lines (must stay under {MAX_MD_LINES})")
        if rel.as_posix() == "README.md":
            for idx, line in enumerate(lines, start=1):
                if "\u2014" in line:
                    errors.append(f"README.md:{idx}: em-dash is not allowed")

    external_urls: set[str] = set()
    readme_seen_in_section: dict[str, set[str]] = {}

    for md, (_, slugs, links) in parsed.items():
        rel = md.relative_to(ROOT)
        for lineno, section, target in links:
            if any(ch.isspace() for ch in target):
                errors.append(f"{rel}:{lineno}: whitespace in URL: {target}")
                continue
            if target.startswith("http://"):
                errors.append(f"{rel}:{lineno}: insecure http:// URL: {target}")
                continue
            if target.startswith("https://"):
                host = urllib.parse.urlparse(target).hostname or ""
                if not host or host in PLACEHOLDER_HOSTS:
                    errors.append(f"{rel}:{lineno}: invalid/placeholder host in {target}")
                    continue
                external_urls.add(target)
                if rel.as_posix() == "README.md" and section:
                    seen = readme_seen_in_section.setdefault(section, set())
                    if target in seen:
                        errors.append(
                            f"README.md:{lineno}: duplicate URL in section '{section}': {target}"
                        )
                    seen.add(target)
                continue
            if target.startswith("mailto:"):
                continue
            if target.startswith("#"):
                if target[1:] not in slugs:
                    errors.append(f"{rel}:{lineno}: broken anchor '{target}'")
                continue

            path_part, _, frag = target.partition("#")
            resolved = (md.parent / path_part).resolve()
            if not resolved.exists():
                errors.append(f"{rel}:{lineno}: missing relative path '{target}'")
            elif frag and resolved in parsed and frag not in parsed[resolved][1]:
                errors.append(f"{rel}:{lineno}: broken anchor '{target}'")

    for svg in sorted((ROOT / "assets").rglob("*.svg")) if (ROOT / "assets").is_dir() else []:
        try:
            ET.parse(svg)
        except ET.ParseError as exc:
            errors.append(f"{svg.relative_to(ROOT)}: invalid SVG XML ({exc})")

    for png in sorted((ROOT / "assets").rglob("*.png")) if (ROOT / "assets").is_dir() else []:
        header = png.read_bytes()[:8]
        if len(header) < 8 or header != b"\x89PNG\r\n\x1a\n":
            errors.append(f"{png.relative_to(ROOT)}: invalid or empty PNG file")

    if check_urls and not errors:
        urls = sorted(external_urls)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            for url, (level, msg) in zip(urls, pool.map(check_live_url, urls)):
                if level == "error":
                    errors.append(f"Live URL failed ({msg}): {url}")
                elif level == "warn":
                    warnings.append(f"Live URL warning ({msg}): {url}")

    for warn in warnings:
        print(f"WARN: {warn}", file=sys.stderr)
    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)

    print(
        f"Checked {len(md_files)} markdown files and {len(external_urls)} unique external URLs "
        f"({len(errors)} errors, {len(warnings)} warnings)."
    )
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-urls",
        action="store_true",
        help="Verify external HTTPS URLs over the network",
    )
    args = parser.parse_args()
    return validate_repo(check_urls=args.check_urls)


if __name__ == "__main__":
    raise SystemExit(main())
