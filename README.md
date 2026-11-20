# AcmeHarvest API (fictional)

A tiny, deliberately under-tested postharvest API. It exists only so Grafter can be tested
end to end before it touches a real solution. Nothing here is a real product.

```bash
pip install -e ".[dev]"
pytest --cov
```

Coverage is kept low on purpose (about 35%). Grafter's first job type writes tests for it.
`src/acme_harvest/invoices.py` is protected in `grafter.charter.yaml`, so Grafter must never edit it.
