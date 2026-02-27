.PHONY: check compile smoke

compile:
	python -m compileall app

smoke:
	python scripts/smoke_check.py

check: compile smoke
