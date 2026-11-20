from datetime import date

import pytest

from acme_harvest.lots import IntakeError, intake

TODAY = date(2026, 11, 20)


def test_intake_assigns_trace_id() -> None:
    lot = intake("Green Valley", "Mango", 120.5, date(2026, 11, 18), 7, TODAY)
    assert lot.trace_id == "AH-20261118-GRE-0007"
    assert lot.produce == "mango"


def test_intake_rejects_unknown_produce() -> None:
    with pytest.raises(IntakeError):
        intake("Green Valley", "banana", 10, date(2026, 11, 18), 1, TODAY)
