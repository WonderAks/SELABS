# Lab 7 — Fuzzing for Input Validation Bugs

Fuzz testing the ride-share fare module with [Hypothesis](https://hypothesis.readthedocs.io/).

## Files

| File | Description |
|------|-------------|
| `ride_share_fare.py` | Fixed module: invalid input returns `None` instead of crashing |
| `test_ride_share_fare.py` | Hypothesis tests (12 tests) |
| `ride_share_fare_original_buggy.py` | Original buggy module, kept for reference |
| `PES2UG24CS044_Lab7_Fuzzing_Report.pdf` | Report with screenshots for Steps 2, 4, 5 and 6 |

## Results

- Original code: 9 failed, 3 passed
- Fixed code: 12 passed

## Run

```
pip install hypothesis pytest
python -m pytest test_ride_share_fare.py -v
```
