# P-ML · From Catalog to Experiment

**Title:** Same question, fixed evidence, appropriate metric.
**Date:** 2026-11-15, Asia/Shanghai. All studies below are **PROPOSED / NOT_RUN**.

## Shared minimum contract

Each new project records question, hypothesis, independent baseline, authorized data or
synthetic fixture, data availability times, split, preprocessing fit scope, seeds, metric,
budget, exact versions/commands and negative controls before tuning. Keep failed runs.

1. Separate training, model selection and final testing. Group related entities and near
   duplicates before splitting; use temporal splits for time-dependent deployment.
2. Fit scalers, imputers, tokenizers, encoders, samplers and feature selectors only where
   the protocol permits. Resampling before split leaks information. Freeze final tests.
3. Use equal data, selection budgets and compute envelopes for comparisons. Record both
   unsuccessful and successful trials, actual wall time, hardware, memory and model/data
   rights. Reusing an official test during repeated development creates adaptive leakage.
4. Include a weak/simple baseline, shuffled/random-label negative control when appropriate,
   a known-correct small oracle, ablations and uncertainty across independent seeds/groups.
5. Test export/reload and train/eval behavior separately. Timing separates data loading,
   compilation, warmup and steady state; synchronize asynchronous hardware if timing it.
6. Report the actual result even if worse. No guessed speedup, SOTA, profitability,
   fairness certification or production-readiness claim from a toy or synthetic fixture.

## Task-specific scorecards

| Task | First baseline | Evaluate | Essential negative control / split |
| --- | --- | --- | --- |
| Regression | mean predictor / OLS | MAE/RMSE; optionally calibration for predictive intervals | train-only scaling; random labels should not predict independent holdout |
| Binary classification | prior / logistic regression | ROC-AUC + PR-AUC for imbalance, log loss/calibration, threshold costs | holdout/group/temporal policy; dummy baseline and train-fold-only resampling |
| Multiclass classification | prior / linear model | macro-F1, balanced accuracy, log loss, class-wise errors | rare classes, duplicate subjects and unavailable classes |
| Clustering | declared k-means/PCA baseline | stability/noise/coverage, silhouette with caveats; ARI/NMI only with independent labels | label permutation invariance; do not tune against hidden external labels |
| Representation learning | untrained/frozen simple features | fixed linear probe or retrieval Recall@k/nDCG | no pretraining/evaluation overlap; same probe budget |
| Half-labelled learning | same labelled subset, supervised-only | fixed-label-budget holdout metric | labelled/unlabelled/test pools disjoint; no test-derived pseudo-labels |
| Detection/segmentation | simple known baseline / fixed frozen model | task-specific mAP/IoU, per-class errors | subject/session split, empty masks/objects, fixed IoU conventions |
| Speech recognition | declared fixed baseline | WER/CER, timestamp/error audit, per-language/noise breakdown | speaker/session split; silence/noise hallucination check |
| Generative models | frozen reference + matched prompt/seed policy | task-defined quality/diversity + human review and actual cost | no cherry-picking; include failure prompts; no universal quality scalar |
| Reinforcement learning | random policy + small reference agent | independent episode returns, success/safety and variance | fixed environment version; separate train/eval seeds; termination vs truncation |
| Probabilistic inference | analytic toy / simple distribution | posterior predictive, convergence diagnostics, calibration | prior sensitivity, divergent chains and misspecified model |
| Time series | last value / seasonal naive | rolling-origin MAE/RMSE, horizon-specific errors | point-in-time covariates; zero future-label access |
| Graph prediction | feature-only/simple graph baseline | declared node/edge/graph metric | inductive vs transductive choice, edge/node/temporal leakage |
| Deployment | original eager/fp32 model | prediction tolerance + cold/hot latency, throughput, memory | unsupported operators, precision failures, wrong batching, resource limits |

## Do not invent one universal f(x,y,z)

Different tasks do not share a meaningful universal score. Keep a vector such as
`quality, calibration, latency, memory, cost, failure rate`. If an operational decision
really needs a composite score, pre-register weights, units, normalization bounds and
hard vetoes; fit/tune only on development data. Show the raw components and sensitivity
analysis. A higher weighted score is not evidence that every objective improved.

## First bounded study

Extend the existing feature-scaling experiment with declared noise/conditioning fixtures,
three seeds and fixed train/selection/test groups. Compare OLS, a dummy predictor and
gradient descent under an equal step budget. Add random-target and invalid-data controls.
This is a proposed bridge, not a newly measured result. Review dependencies and resource
budget before installing any selected framework or downloading weights.

Each study uses **Baseline → Change → Measure → Result → Trade-off → Next Action**.
