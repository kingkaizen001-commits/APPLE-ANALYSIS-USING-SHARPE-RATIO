import math
from dataclasses import dataclass

from app.schemas import ForecastPoint, ForecastRequest, ForecastResponse


@dataclass
class ModelScore:
    name: str
    rmse: float
    mape: float


class ForecastEngine:
    """Pluggable forecast facade.

    Current implementation uses deterministic baseline scores and a simple
    demand progression as a scaffold so real models can be swapped in without
    changing API contracts.
    """

    _CANDIDATE_SCORES = [
        ModelScore(name="sarima", rmse=12.8, mape=0.19),
        ModelScore(name="prophet", rmse=11.7, mape=0.16),
        ModelScore(name="xgboost", rmse=10.9, mape=0.14),
    ]

    def forecast(self, req: ForecastRequest) -> ForecastResponse:
        best = min(self._CANDIDATE_SCORES, key=lambda m: (m.rmse, m.mape))
        base = 100.0
        growth = 0.002
        spread = 0.18 * (1.0 - req.confidence_level + 0.1)

        points: list[ForecastPoint] = []
        for d in range(1, req.horizon_days + 1):
            median = base * math.pow(1.0 + growth, d)
            p10 = max(0.0, median * (1.0 - spread))
            p90 = median * (1.0 + spread)
            points.append(ForecastPoint(day_index=d, p10=p10, p50=median, p90=p90))

        return ForecastResponse(
            sku=req.sku,
            selected_model=best.name,
            rmse=best.rmse,
            mape=best.mape,
            points=points,
        )
