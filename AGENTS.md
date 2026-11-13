# Working on P-ML

P-ML is a public, continuously maintained machine learning research and learning repository. Welcome community Discussions, original ML algorithms, experiments, replications, corrections, and curated resources.

## History and direction

- **2025-04-17:** The project began as **ML-Architectures**, a small teaching and learning repository about model internals, losses, and optimization. Its linear-regression notes remain under `models/`.
- **2026-11-14T03:16:18+08:00:** The renamed **P-ML** adopts a broader public research remit: continue teaching the foundations, conduct original experiments, reproduce and critique existing work, and curate papers, projects, repositories, and websites. See the [dated statement](update/2026-11-14-p-ml-research-statement.md).

## Where to work

- Start in [Discussions](https://github.com/pengpengyi92/P-ML/discussions), or suggest a resource at [the standing call for contributions](https://github.com/pengpengyi92/P-ML/issues/1). Look for existing threads before opening a new one. Agents are welcome to help prepare proposals or PRs with human authorization; this file does not grant posting permissions.

- Put citations and paper notes in `ml-paper/`, runnable work in `ml-project/`, source-repository entries in `ml-repo/`, and learning-site entries in `ml-website/`.
- Use `update/` for dated statements and milestone records. Preserve the original timestamp and statement text when archiving a launch statement.
- Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a public contribution. A Discussion is for exploration; an Issue proposes or tracks work; a PR delivers the actual change.

## Evidence and release rules

- State the question, baseline, dataset or fixtures, split, metric, configuration, and reproduction command. Record seeds when randomness is involved. Report runtime or compute cost when measured, and document limitations and negative results.
- Distinguish a proposal, a reading note, a reproduced result, and an original measured result. Use `UNMEASURED` for unrun evaluations. Do not imply broader performance from a toy experiment.
- **P University is private.** Only cite or adapt Department of CSDSAI material explicitly cleared for public release. Cite a public artifact or an approved public attribution, not a private path, URL, draft, dataset, or conversation. If permission or provenance is unclear, leave the material out.
- Check source links, licenses, and duplicate entries. Do not copy papers, vendor other projects, add real credentials, or commit private or generated data. Keep changes scoped and report what was not tested.
