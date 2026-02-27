"""Offline smoke checks for repository readiness.

No third-party dependencies required.
"""

from pathlib import Path
import sys

REQUIRED_FILES = [
    "app/main.py",
    "app/api/routes.py",
    "app/services/forecasting.py",
    "app/services/optimization.py",
    "app/services/ml_pipeline.py",
    "app/services/alerts.py",
    "app/services/reporting.py",
    "app/tasks/celery_app.py",
    "db/schema.sql",
    "docs/NEXT_STEPS_EXECUTION_PLAN.md",
    "docs/ARCHITECTURE_GAP_AUDIT.md",
    "docs/TESTING_PHASE_PLAYBOOK.md",
    "scripts/api_sanity_check.py",
]

REQUIRED_ENDPOINT_MARKERS = [
    '"/health"',
    '"/meta/platform"',
    '"/meta/architecture"',
    '"/forecast"',
    '"/decision"',
    '"/decision/from-history"',
    '"/ml/train"',
    '"/alerts/evaluate"',
    '"/reports/decision-summary"',
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    root = Path(__file__).resolve().parents[1]

    for rel in REQUIRED_FILES:
        p = root / rel
        if not p.exists():
            fail(f"missing required file: {rel}")

    routes = (root / "app/api/routes.py").read_text(encoding="utf-8")
    for marker in REQUIRED_ENDPOINT_MARKERS:
        if marker not in routes:
            fail(f"missing endpoint marker in routes.py: {marker}")

    schema = (root / "db/schema.sql").read_text(encoding="utf-8")
    for table in ["organizations", "users", "demand_history", "forecasts", "decisions"]:
        if f"CREATE TABLE {table}" not in schema:
            fail(f"missing table in schema.sql: {table}")

    print("PASS: smoke checks complete")


if __name__ == "__main__":
    main()
