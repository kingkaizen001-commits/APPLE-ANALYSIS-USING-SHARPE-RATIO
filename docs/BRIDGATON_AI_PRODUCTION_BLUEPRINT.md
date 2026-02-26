# Bridgaton AI — Production-Ready Backend Blueprint

## 1) Product identity
- **Product name:** Bridgaton AI
- **Positioning:** AI Inventory & Demand Intelligence Engine
- **Core promise:** Probabilistic forecasts + optimization recommendations with measurable financial impact.

## 2) Backend architecture
- **API Layer:** FastAPI (sync APIs + async orchestration triggers)
- **State + System of Record:** PostgreSQL (multi-tenant schema)
- **Task Queue:** Celery + Redis (forecast retraining, Monte Carlo jobs, alert generation)
- **Model Layer:**
  - Time series: SARIMA / Prophet
  - Gradient boosting: XGBoost / LightGBM
  - Deep models (phase 2): LSTM / TFT
- **Storage:** S3 for batch uploads, artifacts, model files
- **Infra:** Docker containers on AWS EC2/ECS, RDS Postgres, ElastiCache Redis

## 3) Modules and contracts

### A. User & Organization module
- JWT authentication, RBAC (`admin`, `analyst`, `viewer`)
- Multi-tenant isolation via `organization_id`

### B. Data ingestion module
- Input channels: CSV upload + API feed
- Processing: schema checks, missing value handling, outlier detection, feature generation
- Core endpoint:
  - `POST /api/v1/ingestion/validate`

### C. Forecasting module
- Ensemble candidates: SARIMA, Prophet, XGBoost
- Rolling validation and model auto-selection by SKU/location
- Output: `p10`, `p50`, `p90`, `rmse`, `mape`
- Endpoints:
  - `POST /api/v1/forecast`
  - `POST /api/v1/forecast/async`

### D. Optimization + simulation module
- Deterministic baseline: safety stock + EOQ
- Stochastic policy search: Monte Carlo with historical demand distribution
- Endpoints:
  - `POST /api/v1/decision`
  - `POST /api/v1/decision/from-history`

### E. Alerts & recommendations module (next implementation step)
- Stockout risk thresholds
- Overstock detection
- Supplier-lead-time risk alerts

### F. Reporting/API integration module (next implementation step)
- ERP/POS sync endpoints
- CSV/Excel export jobs
- Scheduled decision reports

## 4) Data model baseline
- SQL schema file: `db/schema.sql`
- Entities included:
  - organizations, users, skus, locations
  - demand_history, inventory_snapshots, supplier_profiles
  - forecasts, decisions

## 5) Algorithm pipeline
1. Ingest and validate demand/inventory data
2. Generate feature sets (lags, rolling stats, seasonality/promo flags)
3. Evaluate candidate forecast models with rolling windows
4. Persist probabilistic forecast quantiles
5. Run optimization (baseline or Monte Carlo policy search)
6. Persist decisions + provenance + confidence
7. Trigger alert engine and reporting jobs

## 6) Security and compliance checklist
- Tenant-level authorization on every read/write path
- Password hashing + JWT rotation policy
- TLS everywhere (API + DB + Redis in production)
- Audit logging for decision and model outputs
- Data retention policy per organization

## 7) Immediate build sequence (engineering)
1. Add auth and tenant middleware.
2. Add SQL migrations from `db/schema.sql`.
3. Wire persistence for ingestion and decision outputs.
4. Add async forecast retraining task and status endpoint.
5. Add alert rules engine with Celery scheduler.
6. Add model-monitoring endpoint (RMSE/MAPE drift).
