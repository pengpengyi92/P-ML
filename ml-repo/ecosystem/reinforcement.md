# 强化学习与环境

**Dimension:** `learning-paradigm`. **Selected:** 4; multi-label, not additive.
**Snapshot completed:** `2026-11-15T11:46:35+08:00`; each API observation keeps its own timestamp.

Public-source reading candidates; third-party runtime **NOT_RUN**, quality/cost gains **UNMEASURED**.
Code, data, weights, hosted products and dependencies have separate terms. No installation recommendation or official partnership is implied.

[总目录](README.md) · [实验与防泄漏协议](EXPERIMENT_PROTOCOL.md) · [来源快照](snapshot.json)

| Repository / current owner | 学什么、从哪里开始 | 许可识别与维护状态 | 使用边界 |
| --- | --- | --- | --- |
| [Farama-Foundation/Gymnasium](https://github.com/Farama-Foundation/Gymnasium) | 环境 API、状态和 episode 边界；[固定 README](https://github.com/Farama-Foundation/Gymnasium/blob/68c3f95def1b9d91922db5363a28dc1d4a83a960/README.md)；[版本树](https://github.com/Farama-Foundation/Gymnasium/tree/68c3f95def1b9d91922db5363a28dc1d4a83a960) | [MIT](https://github.com/Farama-Foundation/Gymnasium/blob/68c3f95def1b9d91922db5363a28dc1d4a83a960/LICENSE); not archived (not a support promise) | 环境本身不是 RL 算法，terminated 与 truncated 要区分。 |
| [DLR-RM/stable-baselines3](https://github.com/DLR-RM/stable-baselines3) | 常用强化学习算法与训练；[固定 README](https://github.com/DLR-RM/stable-baselines3/blob/0cdcd200deef06b9ad0af72f6ddfb07c06c6df39/README.md)；[版本树](https://github.com/DLR-RM/stable-baselines3/tree/0cdcd200deef06b9ad0af72f6ddfb07c06c6df39) | [MIT](https://github.com/DLR-RM/stable-baselines3/blob/0cdcd200deef06b9ad0af72f6ddfb07c06c6df39/LICENSE); not archived (not a support promise) | 独立环境种子、评估 episode 和 reward 口径必须固定。 |
| [ray-project/ray](https://github.com/ray-project/ray) | 分布式任务、调参与 RL 工具链；[固定 README](https://github.com/ray-project/ray/blob/76d004dab6f68ee515f9472866aa41489ca7a7e9/README.md)；[版本树](https://github.com/ray-project/ray/tree/76d004dab6f68ee515f9472866aa41489ca7a7e9) | [Apache-2.0](https://github.com/ray-project/ray/blob/76d004dab6f68ee515f9472866aa41489ca7a7e9/LICENSE); not archived (not a support promise) | Ray 核心、RLlib 和托管服务不同；集群成本另测。 |
| [vwxyzjn/cleanrl](https://github.com/vwxyzjn/cleanrl) | 单文件强化学习实现；[固定 README](https://github.com/vwxyzjn/cleanrl/blob/fe8d8a03c41a7ef5b523e2e354bd01c363e786bb/README.md)；[版本树](https://github.com/vwxyzjn/cleanrl/tree/fe8d8a03c41a7ef5b523e2e354bd01c363e786bb) | [NOASSERTION](https://github.com/vwxyzjn/cleanrl/blob/fe8d8a03c41a7ef5b523e2e354bd01c363e786bb/LICENSE) / needs-license-review / 固定 LICENSE 主体为 MIT，另列改编代码的 Apache 及其他通知；按文件检查，不把 NOASSERTION 当作无许可。; not archived (not a support promise) | 简洁实现不等于跨环境可直接复用结果。 |
