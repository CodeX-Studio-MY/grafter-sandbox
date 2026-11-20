from datetime import date

import pytest

from acme_harvest.lots import IntakeError, intake, make_trace_id, split

TODAY = date(2026, 11, 20)


def test_intake_assigns_trace_id() -> None:
    lot = intake("Green Valley", "Mango", 120.5, date(2026, 11, 18), 7, TODAY)
    assert lot.trace_id == "AH-20261118-GRE-0007"
    assert lot.produce == "mango"


def test_intake_rejects_unknown_produce() -> None:
    with pytest.raises(IntakeError):
        intake("Green Valley", "banana", 10, date(2026, 11, 18), 1, TODAY)


def test_intake_rejects_non_positive_weight() -> None:
    with pytest.raises(IntakeError):
        intake("Green Valley", "apple", 0, date(2026, 11, 18), 1, TODAY)


def test_intake_rejects_future_harvest_date() -> None:
    with pytest.raises(IntakeError):
        intake("Green Valley", "pear", 10, date(2026, 11, 21), 1, TODAY)


def test_make_trace_id_rejects_short_grower_code() -> None:
    with pytest.raises(IntakeError):
        make_trace_id("A-B", date(2026, 11, 18), 1)


@pytest.mark.parametrize("seq", [0, 10000])
def test_make_trace_id_rejects_sequence_out_of_range(seq: int) -> None:
    with pytest.raises(IntakeError):
        make_trace_id("Green Valley", date(2026, 11, 18), seq)


def test_split_children_keep_parent_link() -> None:
    lot = intake("Green Valley", "mango", 100, date(2026, 11, 18), 7, TODAY)
    children = split(lot, [60, 40])
    assert [c.trace_id for c in children] == [
        "AH-20261118-GRE-0007.1",
        "AH-20261118-GRE-0007.2",
    ]
    assert all(c.parent == lot.trace_id for c in children)
    assert [c.weight_kg for c in children] == [60, 40]


def test_split_rejects_weights_not_matching_lot_weight() -> None:
    lot = intake("Green Valley", "mango", 100, date(2026, 11, 18), 7, TODAY)
    with pytest.raises(IntakeError):
        split(lot, [60, 30])
