from app.schemas import AlertItem, AlertRequest, AlertResponse


class AlertEngine:
    def evaluate(self, req: AlertRequest) -> AlertResponse:
        alerts: list[AlertItem] = []

        if req.stockout_probability >= 0.25:
            alerts.append(
                AlertItem(
                    severity="high",
                    code="STOCKOUT_RISK",
                    message=f"SKU {req.sku} stock-out risk is {req.stockout_probability:.1%}",
                )
            )

        if req.coverage_days <= 3:
            alerts.append(
                AlertItem(
                    severity="high",
                    code="LOW_COVERAGE",
                    message=f"SKU {req.sku} has only {req.coverage_days} days of coverage",
                )
            )

        if req.overstock_days >= 45:
            alerts.append(
                AlertItem(
                    severity="medium",
                    code="OVERSTOCK",
                    message=f"SKU {req.sku} has potential overstock ({req.overstock_days} days)",
                )
            )

        if req.lead_time_variability >= 0.35:
            alerts.append(
                AlertItem(
                    severity="medium",
                    code="SUPPLIER_VARIABILITY",
                    message="Supplier lead-time variability is elevated",
                )
            )

        return AlertResponse(sku=req.sku, total_alerts=len(alerts), alerts=alerts)
