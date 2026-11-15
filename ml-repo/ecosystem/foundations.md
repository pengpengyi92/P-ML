# 数值与数据底座

**Dimension:** `engineering`. **Selected:** 6; multi-label, not additive.
**Snapshot completed:** `2026-11-15T11:46:35+08:00`; each API observation keeps its own timestamp.

Public-source reading candidates; third-party runtime **NOT_RUN**, quality/cost gains **UNMEASURED**.
Code, data, weights, hosted products and dependencies have separate terms. No installation recommendation or official partnership is implied.

[总目录](README.md) · [实验与防泄漏协议](EXPERIMENT_PROTOCOL.md) · [来源快照](snapshot.json)

| Repository / current owner | 学什么、从哪里开始 | 许可识别与维护状态 | 使用边界 |
| --- | --- | --- | --- |
| [numpy/numpy](https://github.com/numpy/numpy) | 数组、shape、dtype 和向量化；[固定 README](https://github.com/numpy/numpy/blob/ebad7c7ca008d222d7fcf2ce18a0d3c253d1a107/README.md)；[版本树](https://github.com/numpy/numpy/tree/ebad7c7ca008d222d7fcf2ce18a0d3c253d1a107) | [NOASSERTION](https://github.com/numpy/numpy/blob/ebad7c7ca008d222d7fcf2ce18a0d3c253d1a107/LICENSE.txt) / needs-license-review / 固定 root LICENSE 为 BSD 三条款式文本；API NOASSERTION 不是无许可。构建/分发组件仍需独立核查。; not archived (not a support promise) | 广播、精度和拷贝语义会改变数值或内存行为。 |
| [scipy/scipy](https://github.com/scipy/scipy) | 科学计算、优化、统计与稀疏矩阵；[固定 README](https://github.com/scipy/scipy/blob/a1ea3167fe271a2950bdc8878a403b2eda592fcb/README.rst)；[版本树](https://github.com/scipy/scipy/tree/a1ea3167fe271a2950bdc8878a403b2eda592fcb) | [BSD-3-Clause](https://github.com/scipy/scipy/blob/a1ea3167fe271a2950bdc8878a403b2eda592fcb/LICENSE.txt); not archived (not a support promise) | 算法收敛和约束可行性须独立检查。 |
| [pandas-dev/pandas](https://github.com/pandas-dev/pandas) | 表格、时间索引与实验数据整理；[固定 README](https://github.com/pandas-dev/pandas/blob/9b9be6d5b979cb984b765026158587c478a9a6f4/README.md)；[版本树](https://github.com/pandas-dev/pandas/tree/9b9be6d5b979cb984b765026158587c478a9a6f4) | [BSD-3-Clause](https://github.com/pandas-dev/pandas/blob/9b9be6d5b979cb984b765026158587c478a9a6f4/LICENSE); not archived (not a support promise) | join、缺失值和时间对齐可能产生泄漏。 |
| [pola-rs/polars](https://github.com/pola-rs/polars) | 列式数据和惰性查询；[固定 README](https://github.com/pola-rs/polars/blob/2d9938dfa3558a89c5d7a05d4ff1b0e5afccfd59/README.md)；[版本树](https://github.com/pola-rs/polars/tree/2d9938dfa3558a89c5d7a05d4ff1b0e5afccfd59) | [MIT](https://github.com/pola-rs/polars/blob/2d9938dfa3558a89c5d7a05d4ff1b0e5afccfd59/LICENSE); not archived (not a support promise) | 不能将查询速度自动解释为模型质量提升。 |
| [dask/dask](https://github.com/dask/dask) | 分块、惰性和分布式数据处理；[固定 README](https://github.com/dask/dask/blob/249a51a1db4261791b93b4ce04e67341729939c3/README.rst)；[版本树](https://github.com/dask/dask/tree/249a51a1db4261791b93b4ce04e67341729939c3) | [BSD-3-Clause](https://github.com/dask/dask/blob/249a51a1db4261791b93b4ce04e67341729939c3/LICENSE.txt); not archived (not a support promise) | 调度开销、分区与集群资源须另测。 |
| [huggingface/datasets](https://github.com/huggingface/datasets) | 数据版本、split 和预处理；[固定 README](https://github.com/huggingface/datasets/blob/efc82474bc990f5872226dca56457536c9a880e9/README.md)；[版本树](https://github.com/huggingface/datasets/tree/efc82474bc990f5872226dca56457536c9a880e9) | [Apache-2.0](https://github.com/huggingface/datasets/blob/efc82474bc990f5872226dca56457536c9a880e9/LICENSE); not archived (not a support promise) | 客户端许可不等于数据集许可或个人数据使用授权。 |
