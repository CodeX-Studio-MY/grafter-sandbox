"""Invoices. Invariant: an invoice number is immutable once issued."""

from __future__ import annotations

from dataclasses import dataclass, field


class InvoiceError(ValueError):
    """Invalid invoice operation."""


@dataclass
class Line:
    trace_id: str
    description: str
    amount: float


@dataclass
class Invoice:
    customer: str
    lines: list[Line] = field(default_factory=list)
    number: str | None = None

    def add(self, line: Line) -> None:
        if self.number is not None:
            raise InvoiceError("cannot change an issued invoice")
        if line.amount < 0:
            raise InvoiceError("line amount cannot be negative")
        self.lines.append(line)

    def total(self) -> float:
        return round(sum(line.amount for line in self.lines), 2)

    def issue(self, number: str) -> None:
        if self.number is not None:
            raise InvoiceError(f"invoice already issued as {self.number}")
        if not self.lines:
            raise InvoiceError("cannot issue an empty invoice")
        self.number = number
