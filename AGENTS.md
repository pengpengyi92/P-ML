# Working on P-ML

P-ML is a public, continuously maintained machine learning research and learning repository. Welcome community Discussions, original ML algorithms, experiments, replications, corrections, and curated resources.

## History and direction

- **2025-04-17:** The project began as **ML-Architectures**, a small teaching and learning repository about model internals, losses, and optimization. Its linear-regression notes remain under `models/`.
- **2026-11-14T03:16:18+08:00:** The renamed **P-ML** adopts a broader public research remit: continue teaching the foundations, conduct original experiments, reproduce and critique existing work, and curate papers, projects, repositories, and websites. See the [dated statement](update/2026-11-14-p-ml-research-statement.md).

## Where to work

- Start at [ML/DL/RL intake #2](https://github.com/pengpengyi92/P-ML/issues/2) or the [Research Exchange / curated index #3](https://github.com/pengpengyi92/P-ML/discussions/3); [general contributions #1](https://github.com/pengpengyi92/P-ML/issues/1) remains open. Search for duplicates, keep one original thread per work, and preserve canonical URLs and author/submitter credit.
- Route public Kaggle artifacts to [Kaggle intake #4](https://github.com/pengpengyi92/P-ML/issues/4) and method discussions to the [Kaggle Hub #5](https://github.com/pengpengyi92/P-ML/discussions/5). Use point-in-time source links and separate validation from leaderboard claims. Do not run submissions or transfer assets, private notebooks, or restricted data as part of curation.
- Welcome agent-assisted research organization, source checks and contribution drafts. Disclose assistance, original authorship and evidence boundaries. A human reviews and authorizes public posts; this guide is not posting permission or permission to auto-install/run submissions.

- Put citations and paper notes in `ml-paper/`, runnable work in `ml-project/`, source-repository entries in `ml-repo/`, and learning-site entries in `ml-website/`.
- `repo/README.md` is a navigation alias, not a duplicate catalog. New source cards belong in `ml-repo/`, with project-specific reasons, source pins, license/data limits and observed PR states. Run `python -m unittest discover -s tests -v`; keep the original feature-scaling experiment separately reproducible.
- Use `update/` for dated statements and milestone records. Preserve the original timestamp and statement text when archiving a launch statement.
- Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a public contribution. A Discussion is for exploration; an Issue proposes or tracks work; a PR delivers the actual change.

## Evidence and release rules

- State the question, baseline, dataset or fixtures, split, metric, configuration, and reproduction command. Record seeds when randomness is involved. Report runtime or compute cost when measured, and document limitations and negative results.
- Distinguish a proposal, a reading note, a reproduced result, and an original measured result. Use `UNMEASURED` for unrun evaluations. Do not imply broader performance from a toy experiment.
- **P University is private.** Only cite or adapt Department of CSDSAI material explicitly cleared for public release. Cite a public artifact or an approved public attribution, not a private path, URL, draft, dataset, or conversation. If permission or provenance is unclear, leave the material out.
- Check source links, licenses, and duplicate entries. Do not copy papers, vendor other projects, add real credentials, or commit private or generated data. Keep changes scoped and report what was not tested.
