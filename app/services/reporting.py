from app.schemas import DecisionSummaryReport, ReportRequest


class ReportingService:
    def build_decision_summary(self, req: ReportRequest) -> DecisionSummaryReport:
        average_stockout_probability = (
            sum(req.stockout_probabilities) / len(req.stockout_probabilities)
            if req.stockout_probabilities
            else 0.0
        )
        average_profit_delta_pct = (
            sum(req.profit_delta_pcts) / len(req.profit_delta_pcts)
            if req.profit_delta_pcts
            else 0.0
        )

        return DecisionSummaryReport(
            organization_id=req.organization_id,
            period_start=req.period_start,
            period_end=req.period_end,
            sku_count=req.sku_count,
            average_stockout_probability=average_stockout_probability,
            average_profit_delta_pct=average_profit_delta_pct,
            generated_status="generated_scaffold",
        )
