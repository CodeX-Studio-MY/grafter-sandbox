import pytest

from acme_harvest.grading import Grade, grade, price


def test_clean_sweet_fruit_is_grade_a() -> None:
    assert grade(defect_pct=2, brix=12) == Grade.A


def test_price_applies_grade_factor() -> None:
    assert price(4.0, 100, Grade.B) == 320.0


@pytest.mark.parametrize("defect_pct", [-1, 101])
def test_out_of_range_defect_pct_raises(defect_pct: float) -> None:
    with pytest.raises(ValueError, match="defect_pct must be between 0 and 100"):
        grade(defect_pct, brix=12)


def test_negative_brix_raises() -> None:
    with pytest.raises(ValueError, match="brix cannot be negative"):
        grade(defect_pct=2, brix=-0.1)


@pytest.mark.parametrize(("defect_pct", "brix"), [(30, 12), (2, 6.9)])
def test_reject_when_defects_or_brix_too_low(defect_pct: float, brix: float) -> None:
    assert grade(defect_pct, brix) == Grade.REJECT


@pytest.mark.parametrize(("defect_pct", "brix"), [(8, 12), (3, 9)])
def test_grade_b_for_moderate_defects_or_low_brix(defect_pct: float, brix: float) -> None:
    assert grade(defect_pct, brix) == Grade.B


def test_grade_c_for_high_but_acceptable_defects() -> None:
    assert grade(defect_pct=20, brix=12) == Grade.C


@pytest.mark.parametrize(("base", "weight"), [(-1.0, 10), (4.0, -1)])
def test_price_rejects_negative_inputs(base: float, weight: float) -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        price(base, weight, Grade.A)
