from datetime import date

import pytest

from acme_harvest.lots import Lot
from acme_harvest.traceability import BrokenChainError, chain, origin

HARVESTED = date(2026, 11, 18)


def make_lot(trace_id: str, parent: str | None = None) -> Lot:
    return Lot(trace_id, "Green Valley", "mango", 10.0, HARVESTED, parent)


def make_lots(*lots: Lot) -> dict[str, Lot]:
    return {lot.trace_id: lot for lot in lots}


def abc() -> tuple[dict[str, Lot], Lot, Lot, Lot]:
    a = make_lot("A")
    b = make_lot("B", parent="A")
    c = make_lot("C", parent="B")
    return make_lots(a, b, c), a, b, c


def test_chain_single_intake_lot_returns_only_itself() -> None:
    a = make_lot("A")
    assert chain(make_lots(a), "A") == [a]


def test_chain_returns_ancestors_newest_first() -> None:
    lots, a, b, c = abc()
    assert chain(lots, "C") == [c, b, a]


def test_chain_raises_on_missing_parent() -> None:
    lots = make_lots(make_lot("B", parent="X"))
    with pytest.raises(BrokenChainError, match="missing lot X"):
        chain(lots, "B")


def test_chain_raises_on_unknown_start_id() -> None:
    lots, *_ = abc()
    with pytest.raises(BrokenChainError, match="missing lot unknown"):
        chain(lots, "unknown")


def test_broken_chain_error_is_a_lookup_error() -> None:
    with pytest.raises(LookupError):
        chain({}, "unknown")


def test_chain_raises_on_loop() -> None:
    lots = make_lots(make_lot("A", parent="B"), make_lot("B", parent="A"))
    with pytest.raises(BrokenChainError, match="loop at"):
        chain(lots, "A")


def test_origin_returns_intake_lot() -> None:
    lots, a, _, _ = abc()
    assert origin(lots, "C") is a


def test_origin_of_intake_lot_is_itself() -> None:
    lots, a, _, _ = abc()
    assert origin(lots, "A") is a
