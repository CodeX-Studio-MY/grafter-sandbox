from acme_harvest.grading import Grade, grade, price


def test_clean_sweet_fruit_is_grade_a() -> None:
    assert grade(defect_pct=2, brix=12) == Grade.A


def test_price_applies_grade_factor() -> None:
    assert price(4.0, 100, Grade.B) == 320.0
