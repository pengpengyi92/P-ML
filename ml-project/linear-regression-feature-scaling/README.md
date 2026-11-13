# Feature scaling and gradient descent in linear regression

**Question:** With the same learning rate and update budget, does scaling the larger feature prevent full-batch gradient descent from diverging on this fixture?

This experiment extends the original [linear-regression notes](../../models/linear_regression/readme.md). The deterministic target is `y = 1 + 2x + 0.03z`. Training uses four combinations of `x = ±1` and `z = ±100`; holdout uses four different combinations of `x = ±0.5` and `z = ±50`. There is no random seed. All gradient-descent runs start at zero, fit an intercept, and have a 200-update budget. Scaling divides the second feature by its maximum absolute **training** value and applies the same transform to the holdout. The closed-form OLS reference exploits this fixture's orthogonal columns; it is not a general-purpose solver.

From this directory, with Python 3.11+ and no third-party dependencies:

```sh
python experiment.py
python -m unittest discover -v
```

Measured on Python 3.12.14:

| Condition | Updates | Training MSE | Holdout MSE | Diverged |
| --- | ---: | ---: | ---: | --- |
| Closed-form OLS reference | — | 0 | 0 | No |
| Raw features, rate 0.05 | 2 | 8.96405e12 | 2.24101e12 | Yes |
| Raw features, rate 0.00005 | 200 | 4.80394 | 1.92158 | No |
| Scaled features, rate 0.05 | 200 | 6.96838e-18 | 2.1154e-18 | No |

Divergence here means crossing the preset training-MSE threshold of `1e12`; the displayed errors for that row are at the stop. Scaling changed the convergence behavior in this controlled problem, not the class of linear functions the model can represent. The noiseless holdout comes from the same equation. This is not a benchmark for real-world prediction, optimizer rankings, or speed.
