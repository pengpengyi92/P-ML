# P-ML — AI Repository Guide Delivery

**Date:** 2026-11-14 (Asia/Shanghai). **Owner:** Pengyi Peng. Prepared with Codex assistance.

## Scope and baseline

Base HEAD: `ec8575e0b52e747c1b9b5ae460344cccd3858066`. First batch: **10 project-specific cards**.
Across P-ML/P-Research/P-CSDSAI there are27 unique official repositories and32
cards; cross-listed repositories are not counted as extra research experiments
or upstream contributions. This is a selected starting inventory, not the whole
ML/AI ecosystem or all historical contributions.

模型方法、训练、预处理、数据切分、指标和可复现实验。先 scikit-learn / XGBoost / LightGBM 建立 tabular baseline；再用 PyTorch / TensorFlow 理解梯度与状态；最后读 Transformers / PEFT，并把 Datasets、Evaluate、Safetensors 放进同一个复现协议。

[Catalog](../ml-repo/README.md) · [Study guide](../ml-repo/HOW_TO_STUDY.md) ·
[Source metadata](../ml-repo/catalog.json).

## What changed

- Classified entries with original, per-project inclusion reasons, questions,
  fixed source HEADs, two verified code entry paths, and unrun study exercises.
- Re-read bounded public author PR metadata; MERGED / OPEN / CLOSED_UNMERGED
  remain separate. No PR found means a reading candidate, not a fake contribution.
- Added an independent stdlib-only catalog validator and read-only GitHub CI job.
- Updated README/agent navigation, TODO and benchmark records. No model training,
  inference serving, pricing logic, application runtime or deployment changes.

P-ML keeps ml-repo/ canonical with a repo/ bridge; P-Research is AI-first with
Quant × AI retained as an application branch; P-CSDSAI emphasizes systems.
Historical statements and project snapshots are not rewritten. Existing
LLMQuant guides, imported Socratic Tutor, synthetic quant cases and P-Trust code
are preserved where present. Different project perspectives are linked, not
passed off as separate validated model improvements.

## Actual validation

Environment: Windows, Python3.12.14; Node24.18.0 for the existing P-Trust checks.
Catalog SHA-256: `be9c40eb0d55f28fec5f2411f425f17308acf206b54eac7f32e98f8e88217ec0`.

| Check | Observed result | Boundary |
| --- | --- | --- |
| `python -m unittest discover -s tests -p test_repo_catalog.py -v` |10 passed, exit0 | Public source pins, card content/links, PR state semantics, permissions and no workstation/credential material |
| Existing scoped checks |目录10项；既有 feature-scaling 实验3项，分别通过 | No third-party model execution or learning-effect evidence |
| `git diff --check` |PASS | Authored changes only |

Legacy command: run `python -m unittest discover -v` from
`ml-project/linear-regression-feature-scaling/`:3 passed, exit0. Root catalog
suite has10 tests; these are separate scopes, not a new measured ML result.

第三方库、模型和 GPU NOT RUN；原有合成实验仅复跑其3个测试。

No new GPU job, model/dataset download, paid API call, investment or upstream
PR/comment/CLA/DCO action. Context7 returned a quota limit; official upstream
GitHub documents and metadata were used instead. Initial guessed paths in some
HKUDS repositories did not match their current layouts; corrected entries were
verified against the same pinned Git trees, not invented or tested by execution.

Remote CI is separate from local evidence and is not claimed green before it
is observed. The catalog cannot validate software safety, model claims,
benchmark scores, partnerships or employment. Learning benefit, real model
quality and performance gains remain **UNMEASURED**.

## License and publication boundary

Only public metadata, links and original commentary are published. No upstream
source/license mirrors or private research notes/logs/datasets/strategies are
exported. License classifiers are not legal permission: PyTorch/VideoRAG require
reading their texts; VideoRAG and dependencies/model weights have separate terms;
AutoMemory lacks a captured root license and stays NEEDS_PERMISSION/reference-only.
No particular code/data/weight reuse or commercial use is authorized by listing.

## Next action

Choose one small fixed fixture from a card. Record question, baseline, split,
metric/tolerance, cost and negative controls before execution. Keep model/method,
AI research protocol and systems-engineering results separate, linking an
existing artifact when the same work is relevant to more than one project.
