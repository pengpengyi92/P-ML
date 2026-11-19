# EADB delivery: Kaggle Competition Matcher v0.1.0

**2026-11-19 | Scope:** first offline application release candidate for P-ML.
This is the matcher's version, not a new version of the full research catalog.

## Contract and design

For a new competition, choose a model and a small, affordable experiment before
committing compute. Accept a known public Kaggle URL/slug or a short English/Chinese
description. Return the task, learning paradigm, model family, starter method,
validation guidance, resource ranges and an indicative Kaggle fit. An unknown
link requests a description; insufficient task evidence must abstain from picking
a workload. No model training, notebook execution, automatic download or submission.

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
- Python 3.11.3, Windows: **16 new matcher tests, 47 existing catalog tests and
  3 existing feature-scaling tests passed**. Exact task scores: baseline **10/24**,
  matcher **24/24**. Matcher learning paradigm: **24/24**. Baseline misses include
  a prize-only prompt classified as RL and an image-only prompt with no objective.
  The benchmark script emits the complete miss list.

```sh
python -m unittest discover -s tests -v
python -m unittest discover -s ml-project/linear-regression-feature-scaling -v
python ml-project/kaggle-matcher/benchmark.py
python ml-project/kaggle-matcher/matcher.py digit-recognizer --plan next --vram-gib 20
```

The last command produced supervised image classification, a classical CPU
baseline `likely_for_pilot`, and a deep-learning candidate `above_planning_budget`
for `vram_gib` on T4x2. All runtime fields remained `UNMEASURED`.

## EADB G0-G9

Gate statuses follow the Engineering Artifact Delivery Benchmark v1.0. These are
scoped outcomes, not an aggregate score or a production certification.

| Gate | Verdict | Deliverable or remaining limit |
| --- | --- | --- |
| G0 Opportunity and permissions | PASS | Owner-requested app for public P-ML; only public competition metadata and original fixtures; no data/model copies or credentials. |
| G1 Requirements | PASS | Known/unknown input, model suggestions, fit estimates, explicit abstention and invalid-input contracts above. |
| G2 Design | PASS | Deterministic local pipeline, versioned catalog with sources, task/model separation and per-device planning budgets. |
| G3 Implementation | PASS | Python 3.11+ CLI, importable inference function, text/JSON, no additional dependencies. |
| G4 Tests | PASS, local | 66 tests and 24-case benchmark; exact commands above. Hardware estimates were not tested on live jobs. |
| G5 Self-review | PASS, scoped | Checked URL versus arbitrary text, override and limit provenance, numeric validation, and diff scope. Separated model family from VRAM and added a conflicting-description test. |
| G6 Independent review | NOT RUN | Author second pass is not human peer review. Request review on route precedence, abstention and resource assumptions. |
| G7 Release and rollback | Demo only | Reviewable PR; no migration or deployment. Before merge, close the PR to withdraw; after merge, revert the feature as one change. No existing experiment, catalog or stored data needs rollback. |
| G8 Docs and demo | PASS | Root feature entry, local quickstart, schema/units, benchmarks and concrete demo. |
| G9 Acceptance and learning | PASS, fixed scope | Local routing and pilot-triage contracts demonstrated; external validity and user decision quality not established. |

## Limits and next decision

Real classification performance, impact on model quality, peak RAM/VRAM, wall time,
monetary cost, submission compliance and adoption are **UNMEASURED**. Text rules can
misread negation, objective conflicts and unsupported domains. Account quotas and
competition rules can change. Keep this offline prototype until independent labels
on at least 30 new descriptions and two separately approved CPU/GPU micro-pilots
justify expanding the language and sizing rules. No leaderboard submission is needed.
