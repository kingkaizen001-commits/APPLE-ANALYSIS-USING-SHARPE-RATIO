# Bridgaton AI

**AI Inventory & Demand Intelligence Engine**

This repository includes a production-oriented backend scaffold and architecture assets:

- FastAPI API surface with request tracing middleware
- API-key protected decisioning/forecasting endpoints
- Data ingestion validation endpoint
- Forecasting facade with model-selection contract
- Inventory optimization decision endpoints (baseline + history-driven Monte Carlo)
- Celery async task stub for forecast jobs
- Production blueprint (`docs/BRIDGATON_AI_PRODUCTION_BLUEPRINT.md`)
- Multi-tenant PostgreSQL schema baseline (`db/schema.sql`)
- Containerization assets (`Dockerfile`, `docker-compose.yml`, `.env.example`)

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

## Endpoints

- `GET /health`
- `GET /meta/platform`
- `POST /ingestion/validate`
- `POST /forecast`
- `POST /forecast/async`
- `POST /decision`
- `POST /decision/from-history`
