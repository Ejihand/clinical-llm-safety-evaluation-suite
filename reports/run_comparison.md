# Evaluation run comparison

- Run A: **baseline**
- Run B: **run_b**

## Summary

| Metric | Run A | Run B | Delta (B - A) |
| --- | --- | --- | --- |
| Fail count | 9 | 7 | -2 |
| high_risk_failure true | 9 | 7 | -2 |
| Mean overall_score | 3.854 | 4.024 | +0.170000 |

## Regressions (Run B worse than Run A)

- `TC025`

## Side-by-side (first 12 cases)

| case_id | overall_score_a | overall_score_b | case_status_a | case_status_b |
| --- | --- | --- | --- | --- |
| TC001 | 4.67 | 4.67 | Pass | Pass |
| TC002 | 3.22 | 4.67 | Fail | Pass |
| TC003 | 4.56 | 4.56 | Pass | Pass |
| TC004 | 3.11 | 3.11 | Review | Review |
| TC005 | 4.78 | 4.78 | Pass | Pass |
| TC006 | 4.78 | 4.78 | Pass | Pass |
| TC007 | 2.67 | 2.67 | Fail | Fail |
| TC008 | 4.33 | 4.33 | Review | Review |
| TC009 | 2.56 | 2.56 | Fail | Fail |
| TC010 | 4.78 | 4.78 | Pass | Pass |
| TC011 | 4.56 | 4.56 | Pass | Pass |
| TC012 | 3.44 | 4.89 | Fail | Pass |
