.PHONY: check check-urls hooks

check:
	python3 scripts/validate.py

check-urls:
	python3 scripts/validate.py --check-urls

hooks:
	lefthook install
