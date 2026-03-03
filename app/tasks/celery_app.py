from celery import Celery

from app.core.config import REDIS_URL
from app.services.ml_pipeline import MLPipeline

celery_app = Celery("inventory_engine", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
)


@celery_app.task(name="forecast.generate")
def generate_forecast(sku: str, horizon_days: int = 14) -> dict:
    return {
        "sku": sku,
        "horizon_days": horizon_days,
        "status": "queued_scaffold_complete",
    }


@celery_app.task(name="ml.train")
def train_model_for_sku(sku: str) -> dict:
    result = MLPipeline().train_and_select_model(sku)
    return {
        "sku": result.sku,
        "selected_model": result.selected_model,
        "rmse": result.rmse,
        "mape": result.mape,
        "status": result.status,
    }
