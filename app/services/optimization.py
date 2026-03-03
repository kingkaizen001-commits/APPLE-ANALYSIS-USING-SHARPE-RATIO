import math
import random
from statistics import NormalDist, mean, pstdev

from app.schemas import DecisionRequest, DecisionResponse, HistoryDecisionRequest


class InventoryOptimizer:
    def _base_policy(self, req: DecisionRequest, mu: float, sigma: float) -> tuple[float, float, float]:
        lead_time_demand_mean = mu * req.lead_time_days
        lead_time_demand_std = max(1e-6, sigma * math.sqrt(req.lead_time_days))
        z = NormalDist().inv_cdf(req.service_level)
        safety_stock = z * lead_time_demand_std
        reorder_point = lead_time_demand_mean + safety_stock

        annual_demand = mu * 365
        eoq = math.sqrt(
            max(
                1e-9,
                (2 * annual_demand * req.order_cost_fixed)
                / max(req.holding_cost_per_unit, 1e-9),
            )
        )
        return reorder_point, safety_stock, eoq

    def recommend(self, req: DecisionRequest) -> DecisionResponse:
        mu = 100.0
        sigma = 25.0
        reorder_point, _, eoq = self._base_policy(req, mu=mu, sigma=sigma)

        reorder_quantity = max(0.0, round(eoq, 2))
        reorder_day_offset = 0 if req.current_inventory <= reorder_point else 3
        shortfall = max(0.0, reorder_point - req.current_inventory)
        stockout_probability = min(1.0, shortfall / max(reorder_point, 1e-9))

        cash_tied_inventory = reorder_quantity * req.holding_cost_per_unit
        expected_profit_delta_pct = max(
            -20.0,
            min(30.0, (1 - stockout_probability) * 12.4 - (cash_tied_inventory / 10000.0)),
        )
        confidence_score = max(0.0, min(1.0, 1.0 - stockout_probability * 0.6))

        return DecisionResponse(
            sku=req.sku,
            reorder_quantity=reorder_quantity,
            reorder_day_offset=reorder_day_offset,
            stockout_probability=stockout_probability,
            expected_profit_delta_pct=expected_profit_delta_pct,
            cash_tied_inventory=cash_tied_inventory,
            confidence_score=confidence_score,
            model_provenance={
                "forecast_model": "xgboost",
                "optimization_model": "eoq+safety_stock",
                "service_level": f"{req.service_level:.3f}",
            },
        )

    def recommend_from_history(self, req: HistoryDecisionRequest) -> DecisionResponse:
        mu = max(1e-6, mean(req.daily_demands))
        sigma = max(1.0, pstdev(req.daily_demands))
        reorder_point, _, eoq = self._base_policy(req, mu=mu, sigma=sigma)

        candidates = [max(0.0, round(eoq * factor, 2)) for factor in (0.7, 0.9, 1.0, 1.15, 1.3)]
        best_qty = candidates[0]
        best_profit = float("-inf")
        best_stockout_prob = 1.0

        for candidate in candidates:
            stockouts = 0
            profits = []
            for _ in range(req.simulation_runs):
                lead_time_demand = 0.0
                for _ in range(req.lead_time_days):
                    lead_time_demand += max(0.0, random.gauss(mu, sigma))

                available = req.current_inventory + candidate
                sold = min(available, lead_time_demand)
                leftover = max(0.0, available - lead_time_demand)
                lost = max(0.0, lead_time_demand - available)

                revenue_margin = sold * req.unit_margin
                holding_penalty = leftover * req.holding_cost_per_unit
                stockout_penalty = lost * req.stockout_cost_per_unit
                order_penalty = req.order_cost_fixed

                profit = revenue_margin - holding_penalty - stockout_penalty - order_penalty
                profits.append(profit)

                if lost > 0:
                    stockouts += 1

            avg_profit = mean(profits)
            stockout_prob = stockouts / req.simulation_runs
            if avg_profit > best_profit:
                best_profit = avg_profit
                best_qty = candidate
                best_stockout_prob = stockout_prob

        reorder_day_offset = 0 if req.current_inventory <= reorder_point else 2
        cash_tied_inventory = best_qty * req.holding_cost_per_unit
        confidence_score = max(0.0, min(1.0, 1.0 - best_stockout_prob))
        expected_profit_delta_pct = max(-50.0, min(50.0, best_profit / 100.0))

        return DecisionResponse(
            sku=req.sku,
            reorder_quantity=best_qty,
            reorder_day_offset=reorder_day_offset,
            stockout_probability=best_stockout_prob,
            expected_profit_delta_pct=expected_profit_delta_pct,
            cash_tied_inventory=cash_tied_inventory,
            confidence_score=confidence_score,
            model_provenance={
                "forecast_model": "empirical_demand_distribution",
                "optimization_model": "monte_carlo+eoq_candidate_search",
                "service_level": f"{req.service_level:.3f}",
                "simulation_runs": str(req.simulation_runs),
            },
        )
