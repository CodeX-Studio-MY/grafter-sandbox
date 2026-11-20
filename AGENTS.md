# AcmeHarvest API — context for agents (fictional example)

## Architecture
- `src/acme_harvest/lots.py` — harvest intake, traceability IDs, lot splits
- `src/acme_harvest/grading.py` — quality grades and price factors
- `src/acme_harvest/traceability.py` — walks a lot back to its intake
- `src/acme_harvest/invoices.py` — invoices (protected: never edited by Grafter)

## Conventions
- Python 3.12, standard library only. Tests use pytest in `tests/`, one file per module.
- Pass `today` explicitly; never call `date.today()` in domain code.
- Raise the module's own error type (`IntakeError`, `BrokenChainError`, `InvoiceError`).

## Domain terms
- **Lot** — produce from one harvest intake; its `trace_id` follows it to the invoice.
- **Split** — dividing a lot for packing; children keep `parent` so the chain never breaks.
- **Brix** — sugar content in degrees; below `min_brix` lowers the grade.
