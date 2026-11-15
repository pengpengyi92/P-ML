# P-ML · ML 仓库生态整理报告

**Title:** From ML frameworks to paradigms, tasks and reproducible engineering.
**Date:** 2026-11-15, Asia/Shanghai; source observations are timestamped in
[snapshot.json](../ml-repo/ecosystem/snapshot.json).
**Status:** Public-source catalog and study design; upstream model runs **NOT_RUN**,
quality, learning benefit and cost reduction **UNMEASURED**.

## 1. 本轮做了什么

- 新建 [73库/15路线的生态目录](../ml-repo/ecosystem/README.md)，包括 PyTorch、TensorFlow、
  JAX、Keras、Transformers，以及监督、无监督、自监督/半监督、强化等学习方向。
- 每条有具体用途、学习入口、限制、canonical归属、commit、原始 README/许可入口。
  73个主仓库都取得两类源文件，共146个固定文件，校验 Git blob、字节长度并记录 SHA256。
- 学习方式、任务领域和工程层不是同一维度：多标签是为了交叉阅读，不能把数量加起来。
- 原有10篇详细卡和历史 PR 观察、机器可读旧目录、原有线性回归实验与早期模型笔记保留。
  新73条包含旧10条对应项目；在所记录的 canonical重定向下，合计仍是73个，不是83个。
- 发布原创说明与链接，不复制上游源代码、论文、数据集、模型权重、商业服务或私有研究。

“所有 ML 相关 repo”在工程上没有可穷尽的范围；本轮明确为维护者选择的核心生态，
不是逐一枚举所有组织，更不是互联网全集。未覆盖推荐、因果、联邦/隐私、机器人、
多模态和其他语言等完整分支，后续按真实任务与证据补充。

## 2. 分类结果

| 层面 | 路线 | 标签条数（不可相加作为独立项目数） |
| --- | --- | --- |
| 工程底座 | 数值/数据；深度学习框架 | 6；7 |
| 学习方式 | 监督；无监督/检索；自监督/半监督；强化 | 8；5；5；4 |
| 任务/方法 | Transformer/LLM；视觉；音频；生成 | 10；10；3；3 |
| 任务/方法 | 概率统计；时序/在线；图学习 | 6；5；2 |
| 工程闭环 | 调参/评估/解释；交换/推理/服务 | 9；8 |

### 监督学习：先形成可靠 baseline

scikit-learn 是拆分、Pipeline、传统算法和交叉验证的学习入口。XGBoost、LightGBM、
CatBoost 提供梯度提升树的不同工程实现。AutoGluon 增加受预算约束的模型/集成搜索，
不代表默认公平或总是优于手工方法。imbalanced-learn 的重采样必须放进训练折内部；
River 的在线学习必须按先预测、后更新的顺序评估。

### 无监督/表征：别把“好看”当有效

PCA/聚类可从scikit-learn开始；UMAP的二维图不是独立真值。HDBSCAN要报告噪声比例与
稳定性。Faiss包含相似检索、索引与聚类组件，但不等于完整RAG；检索和聚类分别评估。
BERTopic把表征、聚类、主题表示组合起来，解释仍需要人工检查。

### 自监督/半监督：训练目标与评估协议分开

solo-learn、Lightly、DINOv2、MAE和微软半监督代码提供不同研究入口。自监督不是没有
目标；半监督也不是把测试集当无标签训练数据。预训练、冻结线性探针和完整微调的成绩
不能混成一个指标；要固定标注预算、数据去重和下游选择预算。

### 深度学习与Transformer：架构、框架、库不同

PyTorch/TF/JAX训练的是建模与计算能力，Keras/Flax/Lightning/fastai组织不同层级的建模
或训练接口。Transformer是架构，Transformers是实现多类模型的库。先固定一个问题，
再比较梯度、状态、训练/推理接口；不能为了“全面”同时维护一堆未跑通的技术栈。

HF工具还包括Tokenizer、Datasets、Evaluate、PEFT、TRL、Sentence Transformers和
Safetensors。它们分别涉及输入、数据、指标、微调、后训练、表征和存储，不是可互相替代
的“模型”。对话模板、特殊token、loss mask、权重来源和检索负样本都可能改变结论。

### 扩展任务：使用任务自己的判据

视觉的分类、检测、分割用不同标签和指标；语音按说话人/会话切分并检查静音幻觉。
概率模型要看采样/后验诊断，时序要滚动评估和point-in-time，图学习要明确
inductive/transductive，强化学习要固定环境、训练/评估种子和episode结束语义。
部署则先验证导出/加载数值等价，再测冷启动、热延迟、内存与并发。

## 3. 来源核查带来的具体修正

1. 当前canonical地址：`microsoft/LightGBM` → `lightgbm-org/LightGBM`；
   `huggingface/safetensors` → `safetensors/safetensors`；
   `pytorch/captum` → `meta-pytorch/captum`。旧详细卡是历史观察，不篡改其日期/来源。
2. MAE和微软半监督仓库当前已归档。保留研究价值，但不能作为活跃维护/生产支持证据。
3. MAE固定LICENSE明确为 **CC BY-NC4.0**。它是带非商业限制的研究参考，不能因为
   公开可见或API显示NOASSERTION就宣传成可无条件商用的开源实现。
4. NumPy/PyTorch的固定LICENSE含BSD风格条款；CleanRL含MIT主体及改编文件通知；
   PyMC声明Apache2.0并说明AePPL的MIT代码。这些API未识别项不能全部写成“没有许可”，
   也不能只看一个标签忽略文件级和组件条款。
5. TorchAudio固定README明确进入maintenance phase，部分功能自2.8弃用并在2.9移除。
   未归档不等于接口仍持续扩张；集成前应复核当前版本与迁移说明。

以上事实在各分类页指向固定原始README/LICENSE，完整来源见[快照](../ml-repo/ecosystem/snapshot.json)。
代码许可、权重许可、训练/评估数据、第三方依赖与托管服务条款必须分别核查。

## 4. 如何让目录产生实际价值

先挑一条任务闭环，而不是安装73个库。例如：固定表格任务 → dummy/线性baseline →
一个树模型 → 合法的调参/留出 → 错误分析/校准 → reload或推理等价。

第二阶段可以依次选择深度梯度小算例、聚类稳定性、冻结表征检索、时序滚动预测、强化
环境契约、概率后验检查等独立小实验。每个实验都要有固定fixture、独立oracle或baseline、
负对照、版本、实际命令和预算，而不是从“项目被收录”跳到“已经掌握或证明更强”。

[统一实验协议](../ml-repo/ecosystem/EXPERIMENT_PROTOCOL.md)提供14类任务的baseline、
指标和防泄漏要求。不构造跨所有任务的万能f分数；确需复合指标时预先固定权重、单位、
归一化和硬约束，并同时公开原始指标，避免调权重制造提升。

## 5. 验证和交付边界

[检查回执](../ml-repo/ecosystem/CHECKS.json)记录实际命令、哈希、失败与限制；
[日志](../log/2026-11-15-ml-ecosystem.md)记录选择过程。新增离线测试覆盖去重、来源、
重定向、时区、权限、许可、归档、链接与采集器负对照，旧10项测试保留不弱化。
原有线性回归3项单元测试单独重跑，结果不推广到本目录其他模型。

实际本地验证：32项目录测试（新增22项、保留10项）和3项既有实验测试通过，分类页重新
生成后哈希不变。原有10篇详细卡、旧来源/PR记录、实验代码、模型笔记及旧测试的Git差异
为空。检查回执含命令、代码/快照/原始本地日志哈希；远端CI在发布后单独核验。

没有安装/执行73个上游软件、下载权重、训练模型、调用收费推理/GPU、接入客户资料或
发布外部issue/PR/discussion。没有声称新SOTA、性能提升、投资回报、生产可用或学习收益。
后续维护首先关注真实实验，而不是持续扩大链接数。
