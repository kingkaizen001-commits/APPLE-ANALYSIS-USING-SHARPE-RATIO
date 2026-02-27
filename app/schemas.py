from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class SalesRecord(BaseModel):
    sku: str = Field(..., min_length=1)
    day: date
    quantity: float = Field(..., ge=0)
    price: Optional[float] = Field(default=None, ge=0)
    promotion_flag: bool = False


class IngestionRequest(BaseModel):
    records: List[SalesRecord] = Field(default_factory=list, min_length=1)

    @field_validator("records")
    @classmethod
    def reject_empty_records(cls, records: List[SalesRecord]) -> List[SalesRecord]:
        if not records:
            raise ValueError("records cannot be empty")
        return records


class IngestionSummary(BaseModel):
    total_records: int
    missing_price_count: int
    outlier_count: int
    by_sku: Dict[str, int]


class ForecastRequest(BaseModel):
    sku: str
    horizon_days: int = Field(default=14, ge=1, le=90)
    confidence_level: float = Field(default=0.9, gt=0.5, lt=0.999)


class ForecastPoint(BaseModel):
    day_index: int
    p10: float
    p50: float
    p90: float


class ForecastResponse(BaseModel):
    sku: str
    selected_model: str
    rmse: float
    mape: float
    points: List[ForecastPoint]


class DecisionRequest(BaseModel):
    sku: str
    current_inventory: float = Field(..., ge=0)
    lead_time_days: int = Field(..., ge=1, le=120)
    holding_cost_per_unit: float = Field(..., ge=0)
    stockout_cost_per_unit: float = Field(..., ge=0)
    order_cost_fixed: float = Field(..., ge=0)
    unit_margin: float = Field(default=1.0, ge=0)
    service_level: float = Field(default=0.95, gt=0.5, lt=0.999)


class HistoryDecisionRequest(DecisionRequest):
    daily_demands: List[float] = Field(..., min_length=7)
    simulation_runs: int = Field(default=3000, ge=200, le=20000)


class DecisionResponse(BaseModel):
    sku: str
    reorder_quantity: float
    reorder_day_offset: int
    stockout_probability: float
    expected_profit_delta_pct: float
    cash_tied_inventory: float
    confidence_score: float
    model_provenance: Dict[str, str]


class AlertRequest(BaseModel):
    sku: str
    stockout_probability: float = Field(..., ge=0, le=1)
    coverage_days: int = Field(..., ge=0)
    overstock_days: int = Field(default=0, ge=0)
    lead_time_variability: float = Field(default=0.0, ge=0)


class AlertItem(BaseModel):
    severity: str
    code: str
    message: str


class AlertResponse(BaseModel):
    sku: str
    total_alerts: int
    alerts: List[AlertItem]


class ReportRequest(BaseModel):
    organization_id: int = Field(..., ge=1)
    period_start: date
    period_end: date
    sku_count: int = Field(..., ge=0)
    stockout_probabilities: List[float] = Field(default_factory=list)
    profit_delta_pcts: List[float] = Field(default_factory=list)


class DecisionSummaryReport(BaseModel):
    organization_id: int
    period_start: date
    period_end: date
    sku_count: int
    average_stockout_probability: float
    average_profit_delta_pct: float
    generated_status: str


class HealthResponse(BaseModel):
    status: str
