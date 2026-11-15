# 概率建模、贝叶斯与统计

**Dimension:** `method-family`. **Selected:** 6; multi-label, not additive.
**Snapshot completed:** `2026-11-15T11:46:35+08:00`; each API observation keeps its own timestamp.

Public-source reading candidates; third-party runtime **NOT_RUN**, quality/cost gains **UNMEASURED**.
Code, data, weights, hosted products and dependencies have separate terms. No installation recommendation or official partnership is implied.

[总目录](README.md) · [实验与防泄漏协议](EXPERIMENT_PROTOCOL.md) · [来源快照](snapshot.json)

| Repository / current owner | 学什么、从哪里开始 | 许可识别与维护状态 | 使用边界 |
| --- | --- | --- | --- |
| [scipy/scipy](https://github.com/scipy/scipy) | 科学计算、优化、统计与稀疏矩阵；[固定 README](https://github.com/scipy/scipy/blob/a1ea3167fe271a2950bdc8878a403b2eda592fcb/README.rst)；[版本树](https://github.com/scipy/scipy/tree/a1ea3167fe271a2950bdc8878a403b2eda592fcb) | [BSD-3-Clause](https://github.com/scipy/scipy/blob/a1ea3167fe271a2950bdc8878a403b2eda592fcb/LICENSE.txt); not archived (not a support promise) | 算法收敛和约束可行性须独立检查。 |
| [statsmodels/statsmodels](https://github.com/statsmodels/statsmodels) | 统计模型、诊断与参数解释；[固定 README](https://github.com/statsmodels/statsmodels/blob/27e747596049cc1a9b06e113af739fdeec59cecc/README.md)；[版本树](https://github.com/statsmodels/statsmodels/tree/27e747596049cc1a9b06e113af739fdeec59cecc) | [BSD-3-Clause](https://github.com/statsmodels/statsmodels/blob/27e747596049cc1a9b06e113af739fdeec59cecc/LICENSE.txt); not archived (not a support promise) | 显著性、预测力和因果关系不是同一结论。 |
| [pyro-ppl/pyro](https://github.com/pyro-ppl/pyro) | 概率程序、变分推断和后验检查；[固定 README](https://github.com/pyro-ppl/pyro/blob/a31bc1784707268cd79df77ead4c7a47062f0193/README.md)；[版本树](https://github.com/pyro-ppl/pyro/tree/a31bc1784707268cd79df77ead4c7a47062f0193) | [Apache-2.0](https://github.com/pyro-ppl/pyro/blob/a31bc1784707268cd79df77ead4c7a47062f0193/LICENSE.md); not archived (not a support promise) | 推断收敛与后验预测检查不能省略。 |
| [pyro-ppl/numpyro](https://github.com/pyro-ppl/numpyro) | JAX 概率推断；[固定 README](https://github.com/pyro-ppl/numpyro/blob/3728ea15d04e17346f33899c761525524360090d/README.md)；[版本树](https://github.com/pyro-ppl/numpyro/tree/3728ea15d04e17346f33899c761525524360090d) | [Apache-2.0](https://github.com/pyro-ppl/numpyro/blob/3728ea15d04e17346f33899c761525524360090d/LICENSE.md); not archived (not a support promise) | 设备精度、采样诊断和链间收敛须记录。 |
| [pymc-devs/pymc](https://github.com/pymc-devs/pymc) | 贝叶斯模型与采样诊断；[固定 README](https://github.com/pymc-devs/pymc/blob/bc3904be4119596442d16593745fe4e2894297e9/README.rst)；[版本树](https://github.com/pymc-devs/pymc/tree/bc3904be4119596442d16593745fe4e2894297e9) | [NOASSERTION](https://github.com/pymc-devs/pymc/blob/bc3904be4119596442d16593745fe4e2894297e9/LICENSE) / needs-license-review / 固定 LICENSE 声明 Apache-2.0，含 AePPL 的 MIT 代码及历史声明；按组件检查。; not archived (not a support promise) | 先验敏感性和 posterior predictive 不是点预测精度。 |
| [cornellius-gp/gpytorch](https://github.com/cornellius-gp/gpytorch) | 高斯过程与不确定性；[固定 README](https://github.com/cornellius-gp/gpytorch/blob/e1302d24cbd334649ada70608cbe98e903a47a83/README.md)；[版本树](https://github.com/cornellius-gp/gpytorch/tree/e1302d24cbd334649ada70608cbe98e903a47a83) | [MIT](https://github.com/cornellius-gp/gpytorch/blob/e1302d24cbd334649ada70608cbe98e903a47a83/LICENSE); not archived (not a support promise) | 训练规模、近似和区间校准独立验证。 |
