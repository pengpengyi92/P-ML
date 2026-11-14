# Machine Learning — 模型、数据与评估

**Last reviewed:** 2026-11-14 (Asia/Shanghai). 首批 **10** 个项目视角档案；选题范围：模型方法、训练、预处理、数据切分、指标和可复现实验。

这不是整个生态的全量清单、星数排名或安装建议。历史公开 PR 已重新读回；无 PR 的项目标为阅读候选，不编造贡献或复现。每篇档案都有独立收录理由、固定源码入口、学习路线、未执行练习、许可与贡献状态。

## 分类路线

- [Classical ML / 表格数据与 baseline](classical-ml/README.md)
- [Deep Learning / 张量、梯度与训练](deep-learning/README.md)
- [LLM Tooling / 模型接口与微调](llm-tooling/README.md)
- [Data & Evaluation / 数据、指标与权重](data-and-evaluation/README.md)

## 收录索引

| 项目 | 本仓库为何收录 | 档案 |
| --- | --- | --- |
| PyTorch | 学习模型、梯度、损失和训练状态的基础，不把框架熟悉度当成模型效果。 | [阅读](deep-learning/pytorch.md) |
| scikit-learn | 建立传统 ML 的 baseline、split、pipeline 和评估习惯，再谈复杂模型。 | [阅读](classical-ml/scikit-learn.md) |
| TensorFlow | 与 PyTorch 对照训练/自动微分概念，保留不同框架的接口和构建条件。 | [阅读](deep-learning/tensorflow.md) |
| Transformers | 研究模型接口、tokenization、loss mask 与训练/推理一致性。 | [阅读](llm-tooling/transformers.md) |
| Datasets | 把数据版本、split、shuffle、预处理和泄漏控制视为模型实验的一部分。 | [阅读](data-and-evaluation/datasets.md) |
| Evaluate | 学习指标定义、分类不平衡与评估接口，而非只优化单一排行榜数值。 | [阅读](data-and-evaluation/evaluate.md) |
| PEFT | 学习 LoRA/adapter 的实现和实验隔离，避免把参数更少误写成效果更优。 | [阅读](llm-tooling/peft.md) |
| Safetensors | 把权重序列化、dtype 与模型复现连接起来。 | [阅读](data-and-evaluation/safetensors.md) |
| XGBoost | 提供经典 tabular ML 对照，研究 loss、树复杂度与早停。 | [阅读](classical-ml/xgboost.md) |
| LightGBM | 研究树学习实现与复杂度控制，保留与其他 tabular baseline 的同口径比较。 | [阅读](classical-ml/lightgbm.md) |

## 怎么开始

先 scikit-learn / XGBoost / LightGBM 建立 tabular baseline；再用 PyTorch / TensorFlow 理解梯度与状态；最后读 Transformers / PEFT，并把 Datasets、Evaluate、Safetensors 放进同一个复现协议。

[学习与证据模板](HOW_TO_STUDY.md) · [机器可读来源与状态](catalog.json)。所有新模型/Agent/GPU/性能实验 **NOT RUN**；目录校验不是第三方软件验收，学习收益与性能改进 **UNMEASURED**。

## 权限和来源

只发布原创说明、公开元数据与链接，不镜像上游源码、许可证或模型。代码、模型权重和数据许可分开看；NOASSERTION/未识别不是免费复用授权。AutoMemory 如出现在本目录，许可未明确，仅作参考；VideoRAG 需核对组件和第三方模型条款。条目不代表官方合作或雇佣关系。

## 相关目录

- [P-ML / 模型与方法](https://github.com/pengpengyi92/P-ML/tree/main/ml-repo)
- [P-Research / AI 研究](https://github.com/pengpengyi92/p-research/tree/main/repo)
- [P-CSDSAI / AI 系统与数据](https://github.com/pengpengyi92/p-csdsai/tree/main/repo)

Recommend a repository via [CONTRIBUTING.md](../CONTRIBUTING.md).
