# Bridgaton AI — Readiness Status

## Requested readiness areas

### 1. Database schema (PostgreSQL)
**Status:** ✅ Ready as baseline.
- Multi-tenant core entities and analytical tables are defined in `db/schema.sql`.
- Includes organizations, users, SKUs, locations, demand history, forecasts, decisions.

### 2. Module endpoints + inputs/outputs
**Status:** ✅ Ready as API contract baseline.
- Endpoints cover ingestion, forecasting, optimization, simulation-based decisioning,
  alert evaluation, reporting summary, auth login, and async job status retrieval.
- Input/output schemas are versioned through Pydantic models.

### 3. ML model pipeline integration
**Status:** 🟡 Integrated as production-shaped seam.
- `MLPipeline` and async `ml.train` task are implemented as integration hooks.
- Real training persistence/model registry needs next implementation sprint.

### 4. Simulation engine structure
**Status:** ✅ Ready as first functional structure.
- Monte Carlo policy search exists in optimizer (`/decision/from-history`) with candidate evaluation and stock-out/profit metrics.

### 5. Alerts + report pipeline
**Status:** ✅ Ready as functional scaffold.
- Alerts engine evaluates risk thresholds.
- Reporting service produces decision summary report outputs.

## Applied from docs/plans in code
- Added auth login endpoint and bearer-token RBAC dependencies.
- Added async job status endpoint (`GET /jobs/{task_id}`).
- Added organization-level mismatch guard on reporting endpoint.
- Updated runtime sanity checks to validate login + bearer flow.

## What is still required for full production launch
1. Real DB persistence layer (ORM + migrations + repository pattern).
2. DB-backed auth/JWT refresh-token lifecycle and rotation.
3. Global tenant middleware enforced on all paths (not only report guard).
4. Model registry + artifact storage integration.
5. End-to-end integration tests against Postgres/Redis in CI.
