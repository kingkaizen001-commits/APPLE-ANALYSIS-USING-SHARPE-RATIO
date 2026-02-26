from collections import Counter
from typing import Iterable

from app.schemas import IngestionSummary, SalesRecord


def detect_iqr_outliers(values: Iterable[float]) -> set[int]:
    vals = list(values)
    if len(vals) < 4:
        return set()

    sorted_vals = sorted(vals)
    q1 = sorted_vals[len(sorted_vals) // 4]
    q3 = sorted_vals[(len(sorted_vals) * 3) // 4]
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return {idx for idx, v in enumerate(vals) if v < lower or v > upper}


def summarize_ingestion(records: list[SalesRecord]) -> IngestionSummary:
    missing_price_count = sum(1 for r in records if r.price is None)
    by_sku = dict(Counter(r.sku for r in records))
    outlier_idx = detect_iqr_outliers([r.quantity for r in records])

    return IngestionSummary(
        total_records=len(records),
        missing_price_count=missing_price_count,
        outlier_count=len(outlier_idx),
        by_sku=by_sku,
    )
