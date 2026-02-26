# AI Inventory & Demand Intelligence Engine — Startup Execution Blueprint

## Technical self-assessment (honest)
- **Math depth:** **9/10**
- **Python depth:** **10/10**

I can fully support implementation across probability/statistics, stochastic optimization, forecasting, and simulation, including production FastAPI + async task orchestration.

## Recommended baseline for execution
To de-risk delivery, we should assume a practical founder baseline of:
- **Math:** 4–5/10
- **Python:** 5–6/10

This gives us the right learning + build cadence.

## 12-week parallel build plan (product + math)

### Weeks 1–2: Platform foundation
- FastAPI service scaffold
- PostgreSQL schema for SKUs, sales, inventory, lead times, suppliers
- Celery + Redis async job queue
- Data validation and ingestion API
- Math track: probability distributions, expectation, variance, standard deviation

### Weeks 3–4: Data quality + feature engine
- Missing-value imputation pipeline
- Outlier detection module
- Feature engineering (lags, rolling windows, promo flags, seasonality)
- Stationarity checks (ADF)
- Math track: inferential statistics, confidence intervals, regression residuals

### Weeks 5–6: Forecasting engine v1
- SARIMA + Prophet + XGBoost forecast models
- Rolling-origin validation by SKU
- Auto model selection (MAPE/RMSE)
- Quantile output scaffold (P10/P50/P90)
- Math track: time-series decomposition, autocorrelation/PACF

### Weeks 7–8: Probabilistic layer + optimization v1
- Demand distribution estimation
- Prediction intervals + stock-out probability computation
- Safety stock + EOQ + Newsvendor implementation
- Decision API (reorder qty/day, confidence)
- Math track: optimization under uncertainty, service-level math

### Weeks 9–10: Monte Carlo simulation engine
- 10,000-path demand simulation
- Policy evaluation per simulation (stock-out, holding, lost sales, profit)
- Objective optimization (maximize expected profit vs service-level target)
- Cash-flow impact projections
- Math track: simulation convergence, scenario analysis

### Weeks 11–12: Production hardening + GTM readiness
- Model monitoring + retraining triggers
- Explainability (feature importance/SHAP for ML models)
- Tiered product packaging (10 SKU / 200 SKU / multi-location)
- API docs + Dockerized deployment baseline
- Math track: review + capstone implementation

## MVP decision output contract
Each SKU/location decision response should include:
- recommended reorder quantity and reorder date
- stock-out probability
- expected profit delta
- cash tied in inventory
- confidence score
- model provenance (selected model + validation metrics)

## Immediate next build actions (this sprint)
1. Create FastAPI project skeleton with `app/api`, `app/services`, `app/models`.
2. Define PostgreSQL schema + migrations for core entities.
3. Implement ingestion endpoint + validation checks.
4. Add first forecasting interface (pluggable model adapter pattern).
5. Stand up Celery worker and async forecast job flow.

## Success metrics for first 30 days
- Data ingestion reliability > 99%
- At least 3 forecasting models operational per SKU
- Automated rolling validation active
- Decision API returns reorder recommendation + uncertainty
- Pilot dataset simulation report generated
