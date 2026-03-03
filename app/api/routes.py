from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import USER_STORE, create_access_token, get_current_user, require_roles
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
    JobStatusResponse,
    LoginRequest,
    LoginResponse,
    ReportRequest,
)
from app.services.alerts import AlertEngine
from app.services.data_quality import summarize_ingestion
from app.services.forecasting import ForecastEngine
from app.services.optimization import InventoryOptimizer
from app.services.reporting import ReportingService
from app.tasks.celery_app import celery_app, generate_forecast, train_model_for_sku

router = APIRouter()
secure_router = APIRouter(dependencies=[Depends(require_api_key)])
forecast_engine = ForecastEngine()
optimizer = InventoryOptimizer()
alert_engine = AlertEngine()
reporting_service = ReportingService()


@router.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    record = USER_STORE.get(payload.username)
    if not record or record["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        username=payload.username,
        role=record["role"],
        organization_id=record["organization_id"],
    )
    return LoginResponse(
        access_token=token,
        role=record["role"],
        organization_id=record["organization_id"],
    )


@router.get("/meta/platform")
def platform_meta() -> dict:
    return {
        "product_name": PRODUCT_NAME,
        "api_version": API_VERSION,
        "modules": [
            "auth_rbac",
            "ingestion",
            "forecasting",
            "optimization",
            "simulation",
            "alerts",
            "reporting",
            "ml_training",
        ],
    }


@router.get("/meta/architecture")
def architecture_meta() -> dict:
    return {
        "status": "baseline_ready",
        "implemented": [
            "fastapi_api",
            "postgres_schema_baseline",
            "celery_redis_tasks",
            "forecast_quantiles",
            "monte_carlo_decision_path",
            "alerts_endpoint",
            "reporting_endpoint",
            "docker_stack",
            "jwt_like_auth_rbac",
            "job_status_endpoint",
        ],
    }


@secure_router.post("/ingestion/validate", response_model=IngestionSummary)
def validate_ingestion(
    payload: IngestionRequest,
    _user=Depends(require_roles("admin", "analyst")),
) -> IngestionSummary:
    return summarize_ingestion(payload.records)


@secure_router.post("/forecast", response_model=ForecastResponse)
def forecast(
    payload: ForecastRequest,
    _user=Depends(require_roles("admin", "analyst", "viewer")),
) -> ForecastResponse:
    return forecast_engine.forecast(payload)


@secure_router.post("/forecast/async")
def forecast_async(
    payload: ForecastRequest,
    _user=Depends(require_roles("admin", "analyst")),
) -> dict:
    job = generate_forecast.delay(payload.sku, payload.horizon_days)
    return {"task_id": job.id, "status": "submitted"}


@secure_router.post("/ml/train")
def ml_train(
    sku: str,
    _user=Depends(require_roles("admin")),
) -> dict:
    job = train_model_for_sku.delay(sku)
    return {"task_id": job.id, "status": "submitted", "sku": sku}


@secure_router.get("/jobs/{task_id}", response_model=JobStatusResponse)
def job_status(
    task_id: str,
    _user=Depends(require_roles("admin", "analyst", "viewer")),
) -> JobStatusResponse:
    async_result = celery_app.AsyncResult(task_id)
    result_payload = async_result.result if isinstance(async_result.result, dict) else None
    return JobStatusResponse(task_id=task_id, status=async_result.status, result=result_payload)


@secure_router.post("/decision", response_model=DecisionResponse)
def decision(
    payload: DecisionRequest,
    _user=Depends(require_roles("admin", "analyst")),
) -> DecisionResponse:
    return optimizer.recommend(payload)


@secure_router.post("/decision/from-history", response_model=DecisionResponse)
def decision_from_history(
    payload: HistoryDecisionRequest,
    _user=Depends(require_roles("admin", "analyst")),
) -> DecisionResponse:
    return optimizer.recommend_from_history(payload)


@secure_router.post("/alerts/evaluate", response_model=AlertResponse)
def evaluate_alerts(
    payload: AlertRequest,
    _user=Depends(require_roles("admin", "analyst", "viewer")),
) -> AlertResponse:
    return alert_engine.evaluate(payload)


@secure_router.post("/reports/decision-summary", response_model=DecisionSummaryReport)
def decision_summary_report(
    payload: ReportRequest,
    user=Depends(require_roles("admin", "analyst", "viewer")),
) -> DecisionSummaryReport:
    if payload.organization_id != user.organization_id:
        raise HTTPException(status_code=403, detail="organization mismatch")
    return reporting_service.build_decision_summary(payload)


router.include_router(secure_router)
