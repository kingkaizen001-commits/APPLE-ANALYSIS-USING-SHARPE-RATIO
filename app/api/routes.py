from fastapi import APIRouter, Depends

from app.core.config import API_VERSION, PRODUCT_NAME
from app.core.security import require_api_key
from app.schemas import (
    AlertRequest,
    AlertResponse,
    DecisionRequest,
    DecisionResponse,
    DecisionSummaryReport,
    ForecastRequest,
    ForecastResponse,
    HealthResponse,
    HistoryDecisionRequest,
    IngestionRequest,
    IngestionSummary,
    ReportRequest,
)
from app.services.alerts import AlertEngine
from app.services.data_quality import summarize_ingestion
from app.services.forecasting import ForecastEngine
from app.services.optimization import InventoryOptimizer
from app.services.reporting import ReportingService
from app.tasks.celery_app import generate_forecast, train_model_for_sku

router = APIRouter()
secure_router = APIRouter(dependencies=[Depends(require_api_key)])
forecast_engine = ForecastEngine()
optimizer = InventoryOptimizer()
alert_engine = AlertEngine()
reporting_service = ReportingService()


@router.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/meta/platform")
def platform_meta() -> dict:
    return {
        "product_name": PRODUCT_NAME,
        "api_version": API_VERSION,
        "modules": [
            "ingestion",
            "forecasting",
            "optimization",
            "simulation",
            "alerts",
            "reporting",
            "ml_training",
        ],
    }


@secure_router.post("/ingestion/validate", response_model=IngestionSummary)
def validate_ingestion(payload: IngestionRequest) -> IngestionSummary:
    return summarize_ingestion(payload.records)


@secure_router.post("/forecast", response_model=ForecastResponse)
def forecast(payload: ForecastRequest) -> ForecastResponse:
    return forecast_engine.forecast(payload)


@secure_router.post("/forecast/async")
def forecast_async(payload: ForecastRequest) -> dict:
    job = generate_forecast.delay(payload.sku, payload.horizon_days)
    return {"task_id": job.id, "status": "submitted"}


@secure_router.post("/ml/train")
def ml_train(sku: str) -> dict:
    job = train_model_for_sku.delay(sku)
    return {"task_id": job.id, "status": "submitted", "sku": sku}


@secure_router.post("/decision", response_model=DecisionResponse)
def decision(payload: DecisionRequest) -> DecisionResponse:
    return optimizer.recommend(payload)


@secure_router.post("/decision/from-history", response_model=DecisionResponse)
def decision_from_history(payload: HistoryDecisionRequest) -> DecisionResponse:
    return optimizer.recommend_from_history(payload)


@secure_router.post("/alerts/evaluate", response_model=AlertResponse)
def evaluate_alerts(payload: AlertRequest) -> AlertResponse:
    return alert_engine.evaluate(payload)


@secure_router.post("/reports/decision-summary", response_model=DecisionSummaryReport)
def decision_summary_report(payload: ReportRequest) -> DecisionSummaryReport:
    return reporting_service.build_decision_summary(payload)


router.include_router(secure_router)
