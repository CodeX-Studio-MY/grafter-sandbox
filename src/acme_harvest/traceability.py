"""Traceability: walk a lot back to its harvest intake. The chain must never break."""

from __future__ import annotations

from acme_harvest.lots import Lot


class BrokenChainError(LookupError):
    """A lot points at a parent that does not exist, or the chain loops."""


def chain(lots: dict[str, Lot], trace_id: str) -> list[Lot]:
    """Return the lot and all its ancestors, newest first."""
    out: list[Lot] = []
    seen: set[str] = set()
    current: str | None = trace_id
    while current is not None:
        if current in seen:
            raise BrokenChainError(f"loop at {current}")
        lot = lots.get(current)
        if lot is None:
            raise BrokenChainError(f"missing lot {current}")
        seen.add(current)
        out.append(lot)
        current = lot.parent
    return out


def origin(lots: dict[str, Lot], trace_id: str) -> Lot:
    return chain(lots, trace_id)[-1]
