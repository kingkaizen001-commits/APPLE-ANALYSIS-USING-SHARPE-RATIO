"""Runtime API sanity checks for Bridgaton AI.

Usage:
  python scripts/api_sanity_check.py --base-url http://localhost:8000/api/v1 --api-key change-me
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request


def req(
    method: str,
    url: str,
    api_key: str | None = None,
    bearer_token: str | None = None,
    payload: dict | None = None,
) -> tuple[int, str]:
    body = None
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(url=url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")


def assert_status(name: str, status: int, expected: int) -> None:
    if status != expected:
        raise RuntimeError(f"{name} expected status {expected}, got {status}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000/api/v1")
    parser.add_argument("--api-key", default="change-me")
    args = parser.parse_args()

    s, _ = req("GET", f"{args.base_url}/health")
    assert_status("health", s, 200)

    s, _ = req("GET", f"{args.base_url}/meta/platform")
    assert_status("meta/platform", s, 200)

    s, _ = req("GET", f"{args.base_url}/meta/architecture")
    assert_status("meta/architecture", s, 200)

    # login
    s, body = req(
        "POST",
        f"{args.base_url}/auth/login",
        payload={"username": "admin@bridgaton.ai", "password": "admin123"},
    )
    assert_status("auth/login", s, 200)
    token = json.loads(body)["access_token"]

    # rejects missing auth
    s, _ = req(
        "POST",
        f"{args.base_url}/forecast",
        api_key=args.api_key,
        payload={"sku": "SKU-001", "horizon_days": 5, "confidence_level": 0.9},
    )
    assert_status("forecast_without_bearer", s, 401)

    s, _ = req(
        "POST",
        f"{args.base_url}/forecast",
        api_key=args.api_key,
        bearer_token=token,
        payload={"sku": "SKU-001", "horizon_days": 5, "confidence_level": 0.9},
    )
    assert_status("forecast_with_auth", s, 200)

    s, _ = req(
        "POST",
        f"{args.base_url}/decision/from-history",
        api_key=args.api_key,
        bearer_token=token,
        payload={
            "sku": "SKU-001",
            "current_inventory": 120,
            "lead_time_days": 7,
            "holding_cost_per_unit": 1.5,
            "stockout_cost_per_unit": 10,
            "order_cost_fixed": 200,
            "unit_margin": 4,
            "service_level": 0.95,
            "daily_demands": [90, 95, 110, 105, 120, 98, 102, 108],
            "simulation_runs": 300,
        },
    )
    assert_status("decision/from-history", s, 200)

    s, _ = req(
        "POST",
        f"{args.base_url}/reports/decision-summary",
        api_key=args.api_key,
        bearer_token=token,
        payload={
            "organization_id": 1,
            "period_start": "2026-01-01",
            "period_end": "2026-01-31",
            "sku_count": 10,
            "stockout_probabilities": [0.1, 0.2, 0.3],
            "profit_delta_pcts": [2.4, 1.1, 3.2],
        },
    )
    assert_status("reports/decision-summary", s, 200)

    print("PASS: api sanity checks complete")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
