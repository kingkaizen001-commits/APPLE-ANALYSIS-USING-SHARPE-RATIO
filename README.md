# Bridgaton AI

**AI Inventory & Demand Intelligence Engine**

This repository includes a production-oriented backend scaffold and architecture assets:

- FastAPI API surface with request tracing middleware
- API-key protected decisioning/forecasting endpoints
- Data ingestion validation endpoint
- Forecasting facade with model-selection contract
- Inventory optimization decision endpoints (baseline + history-driven Monte Carlo)
- ML training integration seam (`/ml/train`) with Celery task stub
- Alerts evaluation and reporting summary endpoints
- Celery async task stubs for forecast jobs and model training
- Production blueprint (`docs/BRIDGATON_AI_PRODUCTION_BLUEPRINT.md`)
- Readiness status (`docs/READINESS_STATUS.md`)
- Architecture audit (`docs/ARCHITECTURE_GAP_AUDIT.md`)
- Next execution plan (`docs/NEXT_STEPS_EXECUTION_PLAN.md`)
- Testing playbook (`docs/TESTING_PHASE_PLAYBOOK.md`)
- Multi-tenant PostgreSQL schema baseline (`db/schema.sql`)
- Containerization assets (`Dockerfile`, `docker-compose.yml`, `.env.example`)
- CI workflow (`.github/workflows/ci.yml`)

## Configuration

Copy `.env.example` values into your deployment environment and set a strong `API_KEY`.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API base: `http://localhost:8000/api/v1`

## Run with Docker Compose

```bash
docker compose up --build
```

## Security

- Protected endpoints require header: `x-api-key: <API_KEY>`
- Public endpoints:
  - `GET /health`
  - `GET /meta/platform`
  - `GET /meta/architecture`

## Endpoints

- `GET /health`
- `GET /meta/platform`
  - `GET /meta/architecture`
- `POST /ingestion/validate`
- `POST /forecast`
- `POST /forecast/async`
- `POST /ml/train`
- `POST /decision`
- `POST /decision/from-history`
- `POST /alerts/evaluate`
- `POST /reports/decision-summary`

## Quality checks

```bash
make check
```

This runs:
- `python -m compileall app`
- `python scripts/smoke_check.py`

## Runtime sanity check

Start the API first, then run:

```bash
make sanity
```

This executes `scripts/api_sanity_check.py` against `/api/v1`.
