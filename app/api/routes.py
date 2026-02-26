from fastapi import APIRouter, Depends

from app.core.config import API_VERSION, PRODUCT_NAME
from app.core.security import require_api_key
from app.schemas import (
    DecisionRequest,
    DecisionResponse,
    ForecastRequest,
    ForecastResponse,
    HealthResponse,
    HistoryDecisionRequest,
    IngestionRequest,
    IngestionSummary,
)
from app.services.data_quality import summarize_ingestion
from app.services.forecasting import ForecastEngine
from app.services.optimization import InventoryOptimizer
from app.tasks.celery_app import generate_forecast

router = APIRouter()
secure_router = APIRouter(dependencies=[Depends(require_api_key)])
forecast_engine = ForecastEngine()
optimizer = InventoryOptimizer()


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


@secure_router.post("/decision", response_model=DecisionResponse)
def decision(payload: DecisionRequest) -> DecisionResponse:
    return optimizer.recommend(payload)


@secure_router.post("/decision/from-history", response_model=DecisionResponse)
def decision_from_history(payload: HistoryDecisionRequest) -> DecisionResponse:
    return optimizer.recommend_from_history(payload)


router.include_router(secure_router)
