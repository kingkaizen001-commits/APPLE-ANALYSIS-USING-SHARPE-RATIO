from dataclasses import dataclass


@dataclass
class TrainingResult:
    sku: str
    selected_model: str
    rmse: float
    mape: float
    status: str


class MLPipeline:
    """Integration seam for real training orchestration.

    This service is intentionally simple but production-shaped:
    - train_and_select_model: rolling validation + winner selection hook
    - register_model_artifact: model registry persistence hook
    """

    def train_and_select_model(self, sku: str) -> TrainingResult:
        candidates = [
            ("sarima", 12.8, 0.19),
            ("prophet", 11.7, 0.16),
            ("xgboost", 10.9, 0.14),
        ]
        winner = min(candidates, key=lambda x: (x[1], x[2]))
        return TrainingResult(
            sku=sku,
            selected_model=winner[0],
            rmse=winner[1],
            mape=winner[2],
            status="trained_scaffold",
        )

    def register_model_artifact(self, sku: str, model_name: str, metrics: dict) -> dict:
        return {
            "sku": sku,
            "model_name": model_name,
            "metrics": metrics,
            "artifact_status": "registry_stubbed",
        }
