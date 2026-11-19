# Kaggle Competition Matcher v0.1.0

Decide what to try first: the learning paradigm, a baseline and optional next model,
how to validate them, and whether a **small pilot** can likely fit a Kaggle Notebook.
Python 3.11+ and its standard library are the only requirements. No Kaggle credentials,
downloads, model training, submissions or network access.

## Run from the P-ML repository root

```sh
python ml-project/kaggle-matcher/matcher.py --list
python ml-project/kaggle-matcher/matcher.py https://www.kaggle.com/competitions/digit-recognizer
python ml-project/kaggle-matcher/matcher.py --description "Cluster unlabeled tabular data to identify customer segments."
python ml-project/kaggle-matcher/matcher.py digit-recognizer --plan next --vram-gib 20 --json
```

For a competition not in [`catalog.json`](catalog.json), provide `--description` or
`--description-file path.txt` (UTF-8, up to 32,000 characters). Include the target,
modalities, available training labels, and, for a simulator, the environment and
agent actions. English and Chinese task descriptions are supported. Start with the
task summary rather than a whole page including incentives, FAQs, and suggested methods.
An unsupported slug without a description exits with code 2. A valid description
with insufficient signals returns `unknown` without guessing a task or hardware.

| Example | Task and learning | Starter route | Next route |
| --- | --- | --- | --- |
| Titanic | Tabular classification; supervised | Logistic regression on CPU | Tree boosting on CPU |
| House Prices | Tabular regression; supervised | Median and ridge on CPU | Tree boosting on CPU |
| Store Sales | Forecasting; supervised | Seasonal naive on CPU | Lag features and boosting on CPU |
| Digit Recognizer | Image classification; supervised | Logistic regression on CPU | Small CNN or transfer learning on a GPU |
| LLM Detect AI Generated Text | Text classification; supervised | TF-IDF and logistic regression on CPU | Compact encoder on a GPU |
| Connect X | Sequential decision; RL optional | Rules or minimax on CPU | Small-policy/self-play pilot on CPU |
| Unlabeled customer segments (synthetic) | Clustering; unsupervised | Mini-batch k-means on CPU | Compare PCA + k-means and HDBSCAN |

## Read the output

- `task`, `learning`, `modalities`, and plan `family` are distinct. Deep learning is
  a model family, so supervised classification can have both classical and deep plans.
  Sequential decisions can have a search baseline without training an RL policy.
- `basis` is `curated_snapshot` or `description_rules`. The latter returns local
  matched terms, not an asserted official metric. With both slug and description,
  the latter selects the route; any known metric/rules still describe the official contest.
- `plans.baseline` and optional `plans.next` carry CPU core targets, host RAM and
  **per-device** VRAM in GiB, and hours. These conservative planning ranges are
  not measured minimum requirements. If you know better, use `--cpu-cores`, `--ram-gib`,
  `--vram-gib`, or `--hours` on `--plan baseline` (default) or `--plan next`.
- `likely_for_pilot` means every range fits the planning envelope;
  `pilot_required` means a range crosses it; `above_planning_budget` means a lower
  bound already exceeds it. Try smaller batches or streaming before provisioning
  more resources. The last label does not rule out a different Kaggle configuration.
- `--submission-hours` compares the same estimated workload against a separate
  competition limit, only relevant for steps rerun in the submission. It does not
  certify internet, disk, external assets, accelerator, or per-action constraints.

The 2026-11-19 planning envelopes are 4 CPU cores, 24 GiB host RAM, and 10 hours
for CPU and T4×2, plus 14 GiB usable VRAM **per T4** in the GPU profile. The margins
are deliberate heuristics below the published capacities, not official quotas. A
single allocation cannot assume both GPUs' memory is pooled. Kaggle's [Notebook
specifications](https://www.kaggle.com/docs/notebooks) and [P100 retirement notice](https://www.kaggle.com/product-announcements/735239)
inform the profiles. Check your live session, quota, disk and competition rules.

## Verify

```sh
python -m unittest discover -s tests -p test_kaggle_matcher.py -v
python ml-project/kaggle-matcher/benchmark.py
```

See [Kaggle pilot measurements](pilots/README.md) and the
[EADB report](../../report/2026-11-19-kaggle-matcher-eadb.md) for test protocol,
observed metrics, limitations, and rollback. Both tested plans ran within Kaggle's
planning budgets, well below the generic RAM/time ranges. The CLI does not train or
measure the workload in a user's invocation and still marks that as `UNMEASURED`.
