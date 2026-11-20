"""Quality grading at the packhouse."""

from __future__ import annotations

from enum import StrEnum


class Grade(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    REJECT = "reject"


PRICE_FACTOR = {Grade.A: 1.0, Grade.B: 0.8, Grade.C: 0.5, Grade.REJECT: 0.0}


def grade(defect_pct: float, brix: float, min_brix: float = 10.0) -> Grade:
    """Grade by defect share (0-100) and sugar content (degrees Brix)."""
    if not 0 <= defect_pct <= 100:
        raise ValueError("defect_pct must be between 0 and 100")
    if brix < 0:
        raise ValueError("brix cannot be negative")
    if defect_pct > 25 or brix < min_brix * 0.7:
        return Grade.REJECT
    if defect_pct <= 5 and brix >= min_brix:
        return Grade.A
    if defect_pct <= 12:
        return Grade.B
    return Grade.C


def price(base_price_per_kg: float, weight_kg: float, g: Grade) -> float:
    if base_price_per_kg < 0 or weight_kg < 0:
        raise ValueError("price and weight cannot be negative")
    return round(base_price_per_kg * weight_kg * PRICE_FACTOR[g], 2)
