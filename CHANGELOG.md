# Changelog

Todas as mudanças relevantes deste repositório são documentadas neste arquivo, seguindo o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [Unreleased]

### Added

- Hero banner ilustrado em alta resolução (`assets/hero-banner.png`).
- Diagrama visual adaptativo claro/escuro de 3 colunas (`assets/mapa-ecossistema-light.svg` e `assets/mapa-ecossistema-dark.svg`) mostrando o fluxo entre comprovantes no Brasil, plataformas validadoras e benefícios.
- Árvore de decisão Mermaid em `docs/validacao-brasil.md`, checklist rápido copiável e alertas de renovação no `README.md`.
- Arquivos de governança open source: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md` e `.editorconfig`.
- Configuração de formulários em `.github/ISSUE_TEMPLATE/config.yml` e atualizações automáticas do Dependabot em `.github/dependabot.yml`.
- Workflow semanal `.github/workflows/check-urls.yml` para detectar links quebrados (`404`/`410`).
- Verificação de assets HTML locais, assinatura de PNGs e integridade XML de SVGs em `scripts/validate.py`.

## [2026-11-24]

### Added

- Lista inicial curada de benefícios para estudantes no Brasil (`README.md`) com foco em GitHub Student Pack, IA, cloud, dev, design, produtividade, streaming, hardware, cursos e direitos brasileiros (DNE/CIE e ID Jovem).
- Guia de validação estudantil no Brasil (`docs/validacao-brasil.md`) cobrindo `.edu.br`, declaração de matrícula, SheerID, UNiDAYS Brasil, Goodstack e alertas de cobrança automática.
- Lista de critérios e serviços excluídos (`docs/criterios-e-fora-da-lista.md`) separando programas encerrados, restritos ao exterior e planos já gratuitos para qualquer usuário.
- Templates de issue e pull request em português, `CONTRIBUTING.md`, licença `CC0-1.0`, hooks com Lefthook, `Makefile`, `scripts/validate.py` e CI inicial.
