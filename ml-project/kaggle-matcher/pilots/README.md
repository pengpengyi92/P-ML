# Kaggle CPU and T4 pilot measurements

Measured on 2026-11-19. Both pilots finished in Kaggle using only the official
labeled `train.csv`. Kaggle kernels were launched private and offline, with a
300-second timeout each, no paid accelerator, and no competition submission.
Only aggregate metrics are published; no dataset rows, models or predictions.

| Fixed workload | Script wall time (v0.1.0 plan) | Peak process RAM (plan) | Peak per-device VRAM (plan) |
| --- | --- | --- | --- |
| Titanic CPU, logistic regression | **5.35 s** (6-60 min) | **180.92 MiB / 0.177 GiB** (2-8 GiB) | Not used (0 GiB) |
| Digit Recognizer, small CNN on one T4 | **29.88 s** (30-240 min) | **1.494 GiB** (8-20 GiB) | **215 MiB / 0.210 GiB** (4-10 GiB) |

The matcher returned `likely_for_pilot` for both workloads; both completed well
within the planning budgets. **The numeric ranges overestimated these runs.**
No generic budget was tightened on the basis of one sample per workload. Both
containers reported four CPU cores in affinity/quota and a 30 GiB cgroup memory
limit, with two configured compute threads. Compare consumption, not allocated
container capacity, to the estimated RAM numbers.

## Fixed protocol and receipts

- **Titanic CPU v1:** stratified seed-42 split of 891 rows (712 fit, 179 held out);
  train-only imputation, scaling and one-hot encoding; scikit-learn logistic
  regression. Fit 0.047 s, 144/179 correct (80.45%). [Raw receipt](evidence/titanic.json).
- **Digit Recognizer T4 v2:** read all 42,000 training rows; seed-42 stratified
  sample of 12,000 fit and 3,000 held-out examples. Two-convolution CNN, Adam
  at 0.001, 3 epochs, batch 128, `cuda:0` on a dual-T4 session. Fit 7.33 s,
  2,839/3,000 correct (94.63%). [Raw receipt](evidence/digit-recognizer.json).
- Wall time is monotonic script time from entry through data fingerprinting, imports,
  loading, model training and holdout scoring; excludes queue, container startup,
  artifact rendering and upload. Fit times exclude loading and scoring. Host RAM
  is Linux `ru_maxrss` for the script process, not the whole container.
- GPU peak used is `nvidia-smi` per-card memory, sampled 95 times at roughly 0.2 s
  intervals; transient peaks may be missed. GPU 0 reached 215 MiB and GPU 1 3 MiB.
  PyTorch also reported 61.77 MiB peak allocated tensors and 72 MiB peak reserved
  by its allocator. These are different counters and are not added.
- **Failed trial retained:** Digit v1 hit `RuntimeError: Invalid device argument`
  at the peak reset before CUDA allocation. v2 moved the reset to after model
  transfer to initialize CUDA. No change in data, model, batch, epochs, or policy.
  The CPU path is unchanged; its historical source hash is pinned in the comparator.
- Kaggle status was read back for CPU v1 and GPU v2. The latest metadata confirmed
  private/offline, one matching competition source, CPU (`None`) and `NvidiaTeslaT4`
  respectively. CPU image digest: `7de5e1496c568335455c8bb1f86f5c36f0591e87e92e9aa9f0eefcd07f227c66`;
  GPU image digest: `fc720c15545eb096a510e1f085b17fc118387a007599424d953a4f327b71cacf`.
- Holdout scores are smoke checks, not leaderboard scores. Random stratification
  does not enforce family groups or image sources. Results are single runs, not
  variance estimates or evidence for full training, sweeps, or larger models.

Official inputs: [Titanic](https://www.kaggle.com/competitions/titanic/data) and
[Digit Recognizer](https://www.kaggle.com/competitions/digit-recognizer/data).

## Reproduce

Recompute the comparison locally from the recorded receipts. This needs no Kaggle
account, credentials, dataset, or GPU:

```sh
python ml-project/kaggle-matcher/pilots/compare.py
```

To re-run the measurement scripts with your own free Kaggle quota and competition
access, choose a fresh suffix per trial. The packager does not upload anything.
Push starts a private script run, **not** a competition submission.

```sh
python ml-project/kaggle-matcher/pilots/prepare.py --owner YOUR_USERNAME --suffix myrun1 --out .local/pilots-myrun1
kaggle kernels push -p .local/pilots-myrun1/cpu --timeout 300
kaggle kernels push -p .local/pilots-myrun1/gpu --timeout 300 --accelerator NvidiaTeslaT4
```

Check each exact kernel version with `kaggle kernels status`. Download just
`pilot-metrics.json` using `kaggle kernels output` and pass those paths to
`compare.py --cpu ... --gpu ...`. Kaggle runtimes and hardware availability can
change; the receipt records actual versions and validates the dual-T4 profile.
