"""Harvest intake: every lot gets a traceability ID that follows it to the invoice."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

KNOWN_PRODUCE = frozenset({"apple", "pear", "mango", "durian", "papaya"})


class IntakeError(ValueError):
    """A lot cannot be accepted at intake."""


@dataclass(frozen=True)
class Lot:
    trace_id: str
    grower: str
    produce: str
    weight_kg: float
    harvested_on: date
    parent: str | None = None


def make_trace_id(grower: str, harvested_on: date, seq: int) -> str:
    code = "".join(ch for ch in grower.upper() if ch.isalnum())[:3]
    if len(code) < 3:
        raise IntakeError(f"grower code too short: {grower!r}")
    if not 1 <= seq <= 9999:
        raise IntakeError(f"sequence out of range: {seq}")
    return f"AH-{harvested_on:%Y%m%d}-{code}-{seq:04d}"


def intake(
    grower: str, produce: str, weight_kg: float, harvested_on: date, seq: int, today: date
) -> Lot:
    produce = produce.strip().lower()
    if produce not in KNOWN_PRODUCE:
        raise IntakeError(f"unknown produce: {produce!r}")
    if weight_kg <= 0:
        raise IntakeError("weight must be positive")
    if harvested_on > today:
        raise IntakeError("harvest date is in the future")
    return Lot(make_trace_id(grower, harvested_on, seq), grower, produce, weight_kg, harvested_on)


def split(lot: Lot, weights: list[float]) -> list[Lot]:
    """Split a lot for packing. Children keep the parent link so the chain never breaks."""
    if len(weights) < 2:
        raise IntakeError("split needs at least two parts")
    if any(w <= 0 for w in weights):
        raise IntakeError("split weights must be positive")
    if abs(sum(weights) - lot.weight_kg) > 0.001:
        raise IntakeError("split weights must add up to the lot weight")
    return [
        Lot(
            trace_id=f"{lot.trace_id}.{i}",
            grower=lot.grower,
            produce=lot.produce,
            weight_kg=w,
            harvested_on=lot.harvested_on,
            parent=lot.trace_id,
        )
        for i, w in enumerate(weights, start=1)
    ]
