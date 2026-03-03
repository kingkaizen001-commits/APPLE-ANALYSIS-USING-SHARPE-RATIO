.PHONY: check compile smoke sanity

compile:
	python -m compileall app

smoke:
	python scripts/smoke_check.py

sanity:
	python scripts/api_sanity_check.py --base-url http://localhost:8000/api/v1 --api-key change-me

check: compile smoke
