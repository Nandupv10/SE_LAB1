# L6_L7_45 — Mobile Data Plan

Lab 6: Code and Branch Coverage

## About

A small Python module that works out data overage charges by plan, usage, roaming and loyalty, checks whether a recharge is allowed and reports plan validity status.

## Files

| File | Description |
|------|-------------|
| `mobile_data_plan.py` | The module under test |
| `test_mobile_data_plan.py` | Comprehensive test suite targeting 100% statement and branch coverage |
| `coverage_report.txt` | Pytest and branch coverage execution output |

Keep all your Lab 6 work in this `LAB6` folder. Lab 7 will be added to this repo later.

## Running Tests and Coverage

To run the test suite and verify branch coverage:

```bash
python -m pytest test_mobile_data_plan.py --cov=mobile_data_plan --cov-branch --cov-report=term-missing
```

## Coverage Summary

```text
============================= test session starts =============================
platform win32 -- Python 3.12.0, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\pvnan\OneDrive\Desktop\SE_LAB1\L6_L7_45_mobile_data_plan\Lab 6
plugins: platformdirs-4.12.3, cov-7.1.0
collected 16 items

test_mobile_data_plan.py ................                                [100%]

=============================== tests coverage ================================
Name                  Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------
mobile_data_plan.py      37      0     26      0   100%
-----------------------------------------------------------------
TOTAL                    37      0     26      0   100%
============================= 16 passed in 0.24s ==============================
```

- **Statement Coverage:** 100% (37 / 37 statements)
- **Branch Coverage:** 100% (26 / 26 branches, 0 missed, 0 partial)
