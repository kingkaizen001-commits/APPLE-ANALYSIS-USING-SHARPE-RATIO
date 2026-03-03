# Bridgaton AI — What Next (Execution Plan)

## Goal for next 14 days
Move from scaffold to deployable alpha with real persistence, auth, and observability.

## Sprint 1 (Days 1–4): Persistence + migrations
1. Add SQLAlchemy models mapped to `db/schema.sql` entities.
2. Add Alembic migrations and bootstrap command.
3. Persist ingestion summaries and decision outputs in PostgreSQL.
4. Add repository layer for forecasts/decisions.

**Definition of done**
- Ingestion and decision endpoints write records to DB.
- Local migration up/down works.

## Sprint 2 (Days 5–8): Auth + multi-tenancy
1. Replace static API key with JWT auth (`access` + `refresh`).
2. Add organization scoping middleware (`organization_id` enforced on every query).
3. Add role checks (`admin`, `analyst`, `viewer`) for write endpoints.

**Definition of done**
- User from org A cannot read/write org B data.
- Auth tests cover role permissions.

## Sprint 3 (Days 9–11): Async orchestration + status APIs
1. Add `POST /forecast/async` persistence of task metadata.
2. Add `GET /jobs/{task_id}` endpoint for task state/result retrieval.
3. Add retry/backoff policy for Celery jobs.

**Definition of done**
- Submitted async job has durable status transitions.

## Sprint 4 (Days 12–14): Reliability + release readiness
1. Add structured logs to JSON format for deployment collectors.
2. Add health checks for Redis/Postgres dependencies.
3. Add CI checks (compile + smoke + schema consistency).
4. Publish deployment runbook for Docker/EC2.

**Definition of done**
- One-command smoke verification passes.
- Release checklist complete.

## KPI targets for this cycle
- API p95 latency < 300ms for sync endpoints.
- Decision endpoint success rate > 99.5%.
- Forecast async job completion success > 98%.
- Zero cross-tenant access violations.
