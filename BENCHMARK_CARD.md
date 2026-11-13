# P-ML relaunch — benchmark card

**Version:** 2026-11-14 relaunch. [Experiment and commands](ml-project/linear-regression-feature-scaling/).

| Step | Evidence |
| --- | --- |
| Baseline | Raw-feature full-batch gradient descent at fixed rates 0.05 and 0.00005; closed-form OLS as the numerical reference. |
| Change | Divide the large-magnitude feature by the training maximum absolute value. Keep the 0.05 rate, intercept, initialization, fixture, and 200-update budget fixed. |
| Measure | Train and holdout MSE on fixed, disjoint synthetic rows; count updates until budget or the preset divergence threshold. |
| Result | Raw 0.05 diverged after 2 updates; raw 0.00005 reached holdout MSE 1.92158; scaled 0.05 reached 2.1154e-18 after 200 updates. OLS holdout MSE was 0. Three unit tests passed. |
| Trade-off | Scaling adds a fitted preprocessing step. This tiny noiseless fixture isolates conditioning; real-data performance, runtime comparison, and community uptake are **UNMEASURED**. |
| Next Action | Vary conditioning and noise across preregistered fixtures and a declared learning-rate grid. |
