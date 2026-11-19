# EADB delivery: Kaggle Competition Matcher v0.1.0

**2026-11-19 | Scope:** first offline matcher release and two bounded Kaggle pilots.
This is the matcher's version, not a new version of the full research catalog.

## Contract and design

For a new competition, choose a model and a small, affordable experiment before
committing compute. Accept a known public Kaggle URL/slug or a short English/Chinese
description. Return the task, learning paradigm, model family, starter method,
validation guidance, resource ranges and an indicative Kaggle fit. An unknown
link requests a description; insufficient task evidence must abstain from picking
a workload. The matcher itself does not train, execute notebooks, download data
or submit. Separate, explicitly authorized pilots exercise two suggested routes.

Decision: use local rules plus a dated six-entry public-source catalog instead of
scraping, an LLM or a Kaggle credential. The flow is identity/description -> task
and learning evidence -> independent method plans -> per-plan budget comparison.
The [application README](../ml-project/kaggle-matcher/README.md) documents the schema,
resource unit and source, examples, and triage states. Catalog keys are unique slugs;
the task and learning values have distinct meanings. Unknown competition metrics
stay null; a known metric and rules are attributed to the official contest, even
when a pasted description selects a different route.

## Test protocol and observed results

- Question: does evidence-aware routing beat first-keyword routing on the fixed
  development set and correctly abstain on its insufficient-evidence controls?
- [24 fixed descriptions and expected labels](../ml-project/kaggle-matcher/eval_cases.json)
  combine six real-task paraphrases with 18 constructed scenarios. They are not
  a held-out or randomly sampled set. Both methods get the same text, with no
  slugs, network, training, random seeds or per-case interpretation at scoring time.
- [Baseline](../ml-project/kaggle-matcher/benchmark.py) takes the first substring
  match in a fixed keyword order. Measure exact task agreement for both; additionally
  compare learning paradigm for the matcher only. Acceptance: no regression on
  the fixed expected labels; invalid input returns a controlled error; missing
  evidence returns no plans; a per-device 20 GiB demand does not fit the T4 plan.
- Python 3.11.3, Windows: **16 matcher tests, 4 pilot receipt tests, 47 existing
  catalog tests and 3 existing feature-scaling tests passed**. Task scores: baseline **10/24**,
  matcher **24/24**. Matcher learning paradigm: **24/24**. Baseline misses include
  a prize-only prompt classified as RL and an image-only prompt with no objective.
  The benchmark script emits the complete miss list.

```sh
python -m unittest discover -s tests -v
python -m unittest discover -s ml-project/linear-regression-feature-scaling -v
python ml-project/kaggle-matcher/benchmark.py
python ml-project/kaggle-matcher/pilots/compare.py
python ml-project/kaggle-matcher/matcher.py digit-recognizer --plan next --vram-gib 20
```

The last command produced supervised image classification, a classical CPU
baseline `likely_for_pilot`, and a deep-learning candidate `above_planning_budget`
for `vram_gib` on T4x2. The matcher does not claim to measure that invocation.

## Kaggle pilot acceptance

Freeze v0.1.0 estimates and question: will the suggested CPU baseline and T4
CNN fit their planning envelopes? Pass only if both authorized Kaggle runs finish,
return exact workload and accelerator evidence, and stay below CPU configuration,
host RAM, per-device VRAM and time budgets without making a submission.

**Observed:** Titanic CPU v1 complete in **5.35 s**, **0.177 GiB** peak process RAM,
no accelerator. Digit CNN v2 complete in **29.88 s**, **1.494 GiB** peak process RAM,
**215 MiB** peak sampled use on the active T4. Both 4-core sessions used two
configured compute threads. Both `likely_for_pilot` predictions held; both time and
RAM observations, and the T4 VRAM observation, were below the original lower bound.
This is scoped fit evidence, not interval calibration. Exact commands, inputs,
units, raw receipts and the pre-training GPU v1 failure are documented in the
[pilot report](../ml-project/kaggle-matcher/pilots/README.md). No submission was made.

## EADB G0-G9

Gate statuses follow the Engineering Artifact Delivery Benchmark v1.0. These are
scoped outcomes, not an aggregate score or a production certification.

| Gate | Verdict | Deliverable or remaining limit |
| --- | --- | --- |
| G0 Opportunity and permissions | PASS | Owner-requested public app and two private, offline pilots; only official labeled data in Kaggle. Public repo contains source, fixtures and aggregate receipts, not data/model copies or credentials. |
| G1 Requirements | PASS | Known/unknown input, model suggestions, fit estimates, explicit abstention and invalid-input contracts above. |
| G2 Design | PASS | Deterministic local pipeline, versioned catalog with sources, task/model separation and per-device planning budgets. |
| G3 Implementation | PASS | Python 3.11+ CLI, importable inference function, text/JSON, no additional dependencies. |
| G4 Tests | PASS, scoped | 70 local tests, 24-case benchmark, receipt comparison, and successful CPU/T4 Kaggle runs. GPU v1 failure retained. |
| G5 Self-review | PASS, scoped | Reviewed provenance and estimates separately from observations, GPU initialization fix, receipt guards, privacy and diff scope. |
| G6 Independent review | NOT RUN | Author second pass is not human peer review. Request review on route precedence, abstention and resource assumptions. |
| G7 Release and rollback | PASS for offline release | Merge PR #6 after current CI, exact receipt checks and owner authorization; no migration or deployment. Revert the PR merge to roll back; no state or prior experiment to migrate. |
| G8 Docs and demo | PASS | Root feature entry, local quickstart, schema/units, benchmarks and concrete demo. |
| G9 Acceptance and learning | PASS, fixed scope | Offline routing and two small Kaggle workloads fit. Numeric intervals over-budget these runs; use more samples before recalibrating. |

## Limits and next decision

Accuracy on unseen tasks, model superiority, runtime variance, full-scale resource
needs, submission compliance and adoption are **UNMEASURED**. Text rules can misread
negation, objective conflicts and unsupported domains; Kaggle limits can change.
Next, independently label at least 30 unseen descriptions and profile several
workload sizes before broadening rules or tightening the budgets. No leaderboard
submission is needed.
