# 时间序列与在线学习

**Dimension:** `application-domain`. **Selected:** 5; multi-label, not additive.
**Snapshot completed:** `2026-11-15T11:46:35+08:00`; each API observation keeps its own timestamp.

Public-source reading candidates; third-party runtime **NOT_RUN**, quality/cost gains **UNMEASURED**.
Code, data, weights, hosted products and dependencies have separate terms. No installation recommendation or official partnership is implied.

[总目录](README.md) · [实验与防泄漏协议](EXPERIMENT_PROTOCOL.md) · [来源快照](snapshot.json)

| Repository / current owner | 学什么、从哪里开始 | 许可识别与维护状态 | 使用边界 |
| --- | --- | --- | --- |
| [statsmodels/statsmodels](https://github.com/statsmodels/statsmodels) | 统计模型、诊断与参数解释；[固定 README](https://github.com/statsmodels/statsmodels/blob/27e747596049cc1a9b06e113af739fdeec59cecc/README.md)；[版本树](https://github.com/statsmodels/statsmodels/tree/27e747596049cc1a9b06e113af739fdeec59cecc) | [BSD-3-Clause](https://github.com/statsmodels/statsmodels/blob/27e747596049cc1a9b06e113af739fdeec59cecc/LICENSE.txt); not archived (not a support promise) | 显著性、预测力和因果关系不是同一结论。 |
| [online-ml/river](https://github.com/online-ml/river) | 在线学习与流式评估；[固定 README](https://github.com/online-ml/river/blob/115df63c9cd57f904dd3a6d586b6cf32d2c1b2c8/README.md)；[版本树](https://github.com/online-ml/river/tree/115df63c9cd57f904dd3a6d586b6cf32d2c1b2c8) | [BSD-3-Clause](https://github.com/online-ml/river/blob/115df63c9cd57f904dd3a6d586b6cf32d2c1b2c8/LICENSE); not archived (not a support promise) | 必须先预测后更新，不能把未来标签提前学习。 |
| [sktime/sktime](https://github.com/sktime/sktime) | 时间序列预测、变换和评估；[固定 README](https://github.com/sktime/sktime/blob/b5338e0b59de48fa5ace5c52c7007b1c2bc4801b/README.md)；[版本树](https://github.com/sktime/sktime/tree/b5338e0b59de48fa5ace5c52c7007b1c2bc4801b) | [BSD-3-Clause](https://github.com/sktime/sktime/blob/b5338e0b59de48fa5ace5c52c7007b1c2bc4801b/LICENSE); not archived (not a support promise) | 使用时间顺序/滚动切分，不套用普通随机 CV。 |
| [sktime/pytorch-forecasting](https://github.com/sktime/pytorch-forecasting) | 深度时序模型和 covariate 数据组织；[固定 README](https://github.com/sktime/pytorch-forecasting/blob/519f05dd975a74bb1de105a4c1b92a760ee95c96/README.md)；[版本树](https://github.com/sktime/pytorch-forecasting/tree/519f05dd975a74bb1de105a4c1b92a760ee95c96) | [MIT](https://github.com/sktime/pytorch-forecasting/blob/519f05dd975a74bb1de105a4c1b92a760ee95c96/LICENSE); not archived (not a support promise) | known-future 与 observed-only 变量必须真实可用。 |
| [unit8co/darts](https://github.com/unit8co/darts) | 多类预测模型和回测接口；[固定 README](https://github.com/unit8co/darts/blob/e679f7bea284734b15961c9ee3c4e4fc3fcd7fd2/README.md)；[版本树](https://github.com/unit8co/darts/tree/e679f7bea284734b15961c9ee3c4e4fc3fcd7fd2) | [Apache-2.0](https://github.com/unit8co/darts/blob/e679f7bea284734b15961c9ee3c4e4fc3fcd7fd2/LICENSE); not archived (not a support promise) | 标准化、外生变量及预测起点遵守 point-in-time。 |
