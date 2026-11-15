# CV / DL / RL · Fixed-Protocol Study Plan

**Date:**2026-11-15, Asia/Shanghai. All new studies below **PROPOSED / NOT_RUN**.
Reuse the [shared experiment protocol](../ecosystem/EXPERIMENT_PROTOCOL.md); this is an
incremental specialization, not a second universal scoring system.

## CV protocol

Start with synthetic, non-identifying images or clearly licensed data. Fix subjects,
sessions, videos, time ranges and near-duplicate groups before splitting. Do not randomly
split adjacent frames from the same video. Fit transforms only on permitted training data.

| Study | Independent baseline/oracle | Metric | Negative control |
| --- | --- | --- | --- |
| Geometry/image transform | synthetic checkerboard, known affine transform or identity | coordinate/pixel tolerance, inverse consistency | wrong units/axes/dtype must fail the oracle |
| Classification | dummy/linear or frozen reference under same split/budget | macro-F1, calibration and per-class errors | shuffled labels and duplicate-subject leakage audit |
| Detection/segmentation | fixed known predictor and independent synthetic boxes/masks | mAP/IoU/Dice with fixed definitions | empty masks, wrong class mapping, coordinate reversal |
| Tracking/video | frozen reference, declared train/test sequences | IDF1/HOTA or declared task metric, identity switches | scene-cut, missing detections, no adjacent-frame contamination |
| 3D/rendering | known camera/geometry and held-out viewpoints | geometry tolerance, fixed-view quality and cost | wrong handedness/scale, hidden training viewpoints |

Prompted segmentation/grounding must record where prompts came from. Human-provided
ground truth prompts cannot silently count as autonomous zero-shot localization.

## DL protocol

1. **Gradient:** compare hand calculation/finite differences to a small autodiff graph.
   Check branch accumulation, repeated variables, zero gradient and invalid inputs.
2. **Training:** fixed synthetic data and train/validation/test split; compare dummy/OLS
   or a simple reference under equal step/selection budgets. Keep all failed runs.
3. **State:** compare uninterrupted training to checkpoint/restore, including optimizer,
   scheduler, random generator and data-loader position. Declare nondeterministic kernels.
4. **Scale:** compare one eager baseline and one proposed precision/parallel change.
   Fix effective batch, tokens, losses, model/data versions and device counts; record peak
   memory, cold/warm wall time and actual communication cost. No assumed speedup.
5. **Export:** reload/export prediction tolerance before any throughput claim. Distinguish
   software dependencies, model weights, data rights and external service conditions.

The first proposed DL study is a finite-difference gradient fixture. This does not authorize
installing unreviewed packages, downloading weights or spending on GPU/cloud services.

## RL protocol

| Mode | Baseline | Budget and holdout | What to measure |
| --- | --- | --- | --- |
| Online | random/simple policy + one fixed algorithm | equal environment interactions; separate train/evaluation seeds | return, success, failures, episode length and seed variance |
| Offline | behavior cloning/simple fixed offline reference | same trajectories; isolated evaluation; no extra online data | declared return and uncertainty; exact dataset/normalization/version |
| Multi-agent | random/scripted agents + fixed opponent pool | fixed agent population, role mapping and opponent holdout | joint/individual rewards, fairness of evaluation and failure rate |
| Model-based | model-free or simple dynamics reference | count real environment interactions and planning/model-training work separately | dynamics error, return, uncertainty and planning cost |

Distinguish `terminated` from `truncated`; handle episode resets and bootstrapping according
to the algorithm's actual protocol. Multi-agent death/entry and AEC/Parallel semantics must
be explicit. Do not leak future transition data across replay or offline evaluation splits.

Simulation throughput, physics accuracy, reward hacking, policy return and real-world
safety are different outcomes. A good simulator benchmark is not evidence that a learned
policy works or is safe outside the simulator. Old D4RL normalized scores must not be
compared blindly with recreated Minari tasks/versions.

## Decision record

Use **Baseline → Change → Measure → Result → Trade-off → Next Action** with source/data
versions, seeds, exact commands, hardware, elapsed time and actual costs. Show the metric
vector, failures and uncertainty; no post-hoc weighted score or leaderboard cherry-picking.
All performance, learning gains and production readiness remain **UNMEASURED** until run.
