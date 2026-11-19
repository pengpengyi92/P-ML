# P-ML relaunch — benchmark card

## Kaggle Competition Matcher v0.1.0 - 2026-11-19

| Step | Evidence |
| --- | --- |
| Baseline | First matching English keyword selects one task. No method, paradigm or resource output. |
| Change | Separate objective, learning paradigm and model family; map to baseline and optional next workload; compare resource ranges to dated Kaggle planning budgets. |
| Measure | Task exact match versus baseline on 24 frozen development descriptions; paradigm exact match for matcher only. Include unsupported, ambiguous and cross-language inputs. |
| Result | Baseline 10/24 task matches; matcher 24/24 task and 24/24 paradigm matches on this development set. [Two Kaggle pilots](ml-project/kaggle-matcher/pilots/README.md) confirm fit for those configurations only: Titanic 5.35 s / 181 MiB RAM; Digit 29.88 s / 1.49 GiB RAM / 215 MiB maximum sampled per-T4 VRAM. |
| Trade-off | Generic ranges substantially overestimated these tiny runs. No held-out routing, broader size calibration, model superiority or user decision quality demonstrated. [EADB](report/2026-11-19-kaggle-matcher-eadb.md). |
| Next Action | Blind-label at least 30 unseen prompts; profile multiple data sizes and accelerators before recalibrating or recommending hardware purchases. |

## CV / DL / RL focus expansion - 2026-11-15

| Step | Evidence |
| --- | --- |
| Baseline |73 primary projects /146 source files and32 catalog tests; original feature-scaling experiment with3 tests. |
| Change |43 non-overlapping primary projects (CV16 /DL11 /RL16),89 new pinned source files, role-based routes, rights/maintenance review and proposed CV/DL/RL studies; combined116 unique repos. |
| Measure |15 new contracts plus32 existing; source/role/non-overlap/permission/path checks, old/new deterministic render, unchanged original experiment and source preservation. Actual final counts/hashes in ml-repo/cv-dl-rl/CHECKS.json. |
| Result |47 catalog tests PASS (15 new +32 retained),3 original experiment tests PASS; old/new rendering deterministic and frozen source/experiment history unchanged. First46/47 run had a case-sensitive protocol keyword false positive, corrected without removing the requirement. No model result inferred from catalog counts. |
| Trade-off |Bounded selection; CORL original/MBRL-Lib archived, other deprecated interfaces and9 API-license exceptions explicit. Upstream runtime, throughput, accuracy, cost, learning benefit and real-world safety NOT_RUN / UNMEASURED. |
| Next Action |One pre-registered synthetic gradient/geometry/environment study; compare an independent baseline under fixed budgets before increasing implementation scope. |

## ML ecosystem catalog - 2026-11-15

| Step | Evidence |
| --- | --- |
| Baseline |10 prior detailed cards and10 offline catalog tests; original feature-scaling experiment with3 tests. |
| Change |73 selected canonical primary repos,15 overlapping routes,146 pinned/byte-verified README/license files, rights/maintenance notes, report and experiment protocols. Old10 are included, not73+10. |
| Measure |Fixed offline evidence contracts; canonical de-duplication, exact source pins, timestamps, privacy, license/HTTP/integrity negative controls, links, deterministic rendering; rerun unchanged experiment separately. |
| Result |32 catalog tests PASS (22 new,10 retained);3 original experiment tests PASS. Source files checked by Git blob and byte length, SHA256 recorded. Actual receipts in ml-repo/ecosystem/CHECKS.json. |
| Trade-off |Bounded curation, not all ML software.2 archives;5 API-license exceptions, including1 explicitly noncommercial reference. No upstream runtime, model accuracy, speed/cost improvement, learning gain or production validation; NOT_RUN / UNMEASURED. |
| Next Action |One pre-registered synthetic study with fixed data/splits/metric/budget, independent baseline and negative controls; judge the result rather than catalog size. |

## Repository catalog — 2026-11-14

| Step | Evidence |
| --- | --- |
| Baseline | No role-specific multi-repository AI reading routes; existing project code and prior indexes preserved. |
| Change |10 project-specific cards, official source pins/PR states, license limits, study plans and catalog-only CI. |
| Measure |10 local catalog tests; 目录10项；既有 feature-scaling 实验3项，分别通过. [Observed delivery](update/2026-11-14-ai-repository-guides.md). |
| Result |Catalog checks PASS; runtime/model/learning/throughput improvements NOT RUN / UNMEASURED, not claimed from curation. |
| Trade-off |Curated bounded sample, changing paths/permissions and PR history; no full ecosystem audit or third-party certification. |
| Next Action |One fixed-fixture study with independent baseline and negative controls; no model/GPU spending without approval. |

**Version:** 2026-11-14 relaunch. [Experiment and commands](ml-project/linear-regression-feature-scaling/).

| Step | Evidence |
| --- | --- |
| Baseline | Raw-feature full-batch gradient descent at fixed rates 0.05 and 0.00005; closed-form OLS as the numerical reference. |
| Change | Divide the large-magnitude feature by the training maximum absolute value. Keep the 0.05 rate, intercept, initialization, fixture, and 200-update budget fixed. |
| Measure | Train and holdout MSE on fixed, disjoint synthetic rows; count updates until budget or the preset divergence threshold. |
| Result | Raw 0.05 diverged after 2 updates; raw 0.00005 reached holdout MSE 1.92158; scaled 0.05 reached 2.1154e-18 after 200 updates. OLS holdout MSE was 0. Three unit tests passed. |
| Trade-off | Scaling adds a fitted preprocessing step. This tiny noiseless fixture isolates conditioning; real-data performance, runtime comparison, and community uptake are **UNMEASURED**. |
| Next Action | Vary conditioning and noise across preregistered fixtures and a declared learning-rate grid. |
