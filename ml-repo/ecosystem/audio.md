# 音频与语音

**Dimension:** `application-domain`. **Selected:** 3; multi-label, not additive.
**Snapshot completed:** `2026-11-15T11:46:35+08:00`; each API observation keeps its own timestamp.

Public-source reading candidates; third-party runtime **NOT_RUN**, quality/cost gains **UNMEASURED**.
Code, data, weights, hosted products and dependencies have separate terms. No installation recommendation or official partnership is implied.

[总目录](README.md) · [实验与防泄漏协议](EXPERIMENT_PROTOCOL.md) · [来源快照](snapshot.json)

| Repository / current owner | 学什么、从哪里开始 | 许可识别与维护状态 | 使用边界 |
| --- | --- | --- | --- |
| [pytorch/audio](https://github.com/pytorch/audio) | 音频 I/O、变换与模型；[固定 README](https://github.com/pytorch/audio/blob/9b19155e6fce04a83704eadc85d3dfe99e520c0c/README.md)；[版本树](https://github.com/pytorch/audio/tree/9b19155e6fce04a83704eadc85d3dfe99e520c0c) | [BSD-2-Clause](https://github.com/pytorch/audio/blob/9b19155e6fce04a83704eadc85d3dfe99e520c0c/LICENSE) / 固定 README 明确处于 maintenance phase，部分功能已从2.8弃用并在2.9移除；不是当前特性持续扩展承诺。; not archived (not a support promise) | 检查维护阶段、后端迁移和版本支持，不默认功能持续扩展。 |
| [speechbrain/speechbrain](https://github.com/speechbrain/speechbrain) | 语音训练、识别和相关研究配方；[固定 README](https://github.com/speechbrain/speechbrain/blob/c0241278f93ef02cd5191f03caf4e5f8e1292bf6/README.md)；[版本树](https://github.com/speechbrain/speechbrain/tree/c0241278f93ef02cd5191f03caf4e5f8e1292bf6) | [Apache-2.0](https://github.com/speechbrain/speechbrain/blob/c0241278f93ef02cd5191f03caf4e5f8e1292bf6/LICENSE); not archived (not a support promise) | 按说话人/会话隔离并核对语料及权重条款。 |
| [openai/whisper](https://github.com/openai/whisper) | 语音识别与转录；[固定 README](https://github.com/openai/whisper/blob/86098128c0b4f24f0e2aa2994de830614b474227/README.md)；[版本树](https://github.com/openai/whisper/tree/86098128c0b4f24f0e2aa2994de830614b474227) | [MIT](https://github.com/openai/whisper/blob/86098128c0b4f24f0e2aa2994de830614b474227/LICENSE); not archived (not a support promise) | 语言、噪声、时间戳与幻觉错误须按固定样本评估。 |
