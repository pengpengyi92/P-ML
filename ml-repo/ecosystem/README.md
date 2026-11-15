# P-ML · Machine Learning Repository Map

**Title:** 从学习方式到工程闭环的机器学习仓库地图。
**Review date:** 2026-11-15, Asia/Shanghai. 每个来源的实际观察时间、commit 和文件哈希见
[snapshot.json](snapshot.json)。

这一版按明确选题整理 **73 个主项目、15 条交叉路线**。不是整个互联网 ML 软件的穷尽
清单，也不是73个算法或软件质量排名。只发布公开链接、版本元数据与原创导读，不镜像
上游代码、模型权重、数据集或文档。既有10篇详细卡及历史观察原样保留。

## 1. 三种维度，不混为一个分类

- **学习方式**：监督、无监督、自监督/半监督、强化学习。无监督不等于无损失函数，
  自监督通常用数据构造训练目标，强化学习以环境交互和回报为核心。
- **任务/模型领域**：视觉、语音、NLP、生成、概率、时序、图学习。任务领域可采用不同
  学习方式；Transformer 是模型架构，Hugging Face Transformers 是软件库。
- **工程层**：数组/数据 → 框架 → 训练/调参 → 评估/解释 → 导出/服务。框架不是模型效果，
  检索索引不是完整 RAG，模型服务也不是完整训练系统。

一个项目可以多标签收录，统计按 canonical repo 去重，不能把各路线数量相加。

## 2. 分类入口

| 路线 | 关键对象 | 进入方式 |
| --- | --- | --- |
| [数值与数据底座](foundations.md) | NumPy、SciPy、pandas、Polars、Dask、Datasets | 数值/shape、数据可用时间、fit 与 transform 边界 |
| [深度学习框架](frameworks.md) | PyTorch、TensorFlow、JAX、Keras、Flax、Lightning、fastai | 梯度、参数、训练状态、checkpoint；固定同一算例对照 |
| [监督学习](supervised.md) | scikit-learn、XGBoost、LightGBM、CatBoost、AutoGluon、River | 回归/分类、树、类别、失衡、在线更新与严格留出 |
| [无监督与检索](unsupervised.md) | PCA/聚类入口、UMAP、HDBSCAN、Faiss、BERTopic | 数据结构发现；不把二维展示当真值，检索单独评估 |
| [自监督与半监督](self-semi-supervised.md) | solo-learn、Lightly、DINOv2、MAE、Semi-supervised-learning | 预训练目标、标签预算、线性探针、冻结评估与许可 |
| [Transformer / LLM](transformers-llm.md) | Transformers、Tokenizers、PEFT、TRL、Sentence Transformers | token、loss mask、训练/推理一致性、检索与后训练 |
| [计算机视觉](vision.md) | torchvision、timm、MMDetection、MMSegmentation、Detectron2、Kornia | 分类/检测/分割各自的数据拆分、增强和指标 |
| [音频与语音](audio.md) | TorchAudio、SpeechBrain、Whisper | 音频采样、说话人隔离、识别、错误与幻觉检查 |
| [生成与扩散](generative.md) | Diffusers、Latent Diffusion、教学实现 | scheduler、去噪与采样；质量和成本分开量化 |
| [强化学习](reinforcement.md) | Gymnasium、Stable-Baselines3、RLlib/Ray、CleanRL | 环境契约、回报、episode 边界和独立评估种子 |
| [概率与统计](probabilistic.md) | Pyro、NumPyro、PyMC、GPyTorch、SciPy、statsmodels | 先验、后验、采样诊断和校准，不只看点预测 |
| [时序与在线](time-series.md) | sktime、PyTorch Forecasting、Darts、River | 时间切分、滚动预测、外生变量、先预测后更新 |
| [图学习](graph.md) | PyG、DGL | 节点/边/图任务，inductive 与 transductive 协议 |
| [调参、评估与解释](evaluation.md) | Optuna、MLflow、SHAP、Captum、Evidently、Fairlearn | 搜索预算、实验追踪、sanity check、分群和漂移 |
| [交换、推理与服务](deployment.md) | ONNX、ONNX Runtime、BentoML、vLLM、Triton | 数值等价、精度、冷/热延迟、并发与隔离 |

表内每个项目都链接固定版本的原始 README、许可文件和版本树，并有独立用途与边界。
归档、API 许可未识别和当前规范归属均显式保留，不由知名度推断。

## 3. 四条可执行的阅读顺序

1. **传统/表格 ML**：NumPy/pandas → scikit-learn Pipeline → XGBoost/LightGBM/CatBoost
   → Optuna → 校准、分群和误差分析。先用简单 baseline，再给复杂度找证据。
2. **深度学习基础**：PyTorch → 同一线性模型的梯度与状态 → 视觉/音频一个固定任务
   → checkpoint 和推理等价。JAX/TF 是可选对照，不要求同时熟练全部框架。
3. **表征学习/LLM**：数据/分词 → 表征或预训练目标 → 冻结特征评估 → PEFT/后训练
   → 独立留出；不要用已见任务/答案冒充零样本泛化。
4. **研究到服务**：固定数据/协议 → 训练 → 评估 → 权重来源/格式 → 导出/服务 →
   数值误差与成本。API 返回200、图像好看和目录测试通过都不证明模型有效。

## 4. 许可、维护与复现边界

代码许可、模型权重、数据集、第三方组件和托管服务必须分别核查。GitHub 的 SPDX 分类
是发现信号而非法律结论；`NOASSERTION` 不等于没有任何许可，也不等于自由复用。
归档可保留学习价值，但不是当前可维护/可部署的承诺。本轮未批准任何付费服务、GPU
训练、模型下载或未审阅代码执行。

所有第三方训练、效果/吞吐比较、数值等价、生产安全与学习收益：**NOT_RUN / UNMEASURED**。
既有线性回归实验的实测结果仍只属于其原始固定算例，不能推广到这73个项目。

## 5. 更新和贡献

```sh
python scripts/collect_ml_ecosystem.py --collect --render --review-dir .local/ml-source-review
python -m unittest discover -s tests -v
python -m unittest discover -s ml-project/linear-regression-feature-scaling -v
```

从项目根目录运行，Python3.11+、已认证的 `gh`；仅需公开 GitHub 读取权限，不打印凭据。
采集器按小批量 GraphQL 获取元数据、固定 commit 的源文件，并验证每个文件的 Git blob
与字节大小。原始文本/缓存只落在忽略的 `.local/`，公开快照仅保留元数据和原创说明。
失败则停止，不把403/超时当成“无许可”；显式 `--resume` 保留缓存原观察时间。

- [选题清单](selection.json) · [来源快照](snapshot.json) · [检索方法](SEARCH_PROTOCOL.md)
- [实验与反泄漏协议](EXPERIMENT_PROTOCOL.md) · [检查回执](CHECKS.json)
- [综合报告](../../report/2026-11-15-ml-ecosystem.md) · [原有10篇详细导读](../README.md)
- [贡献规范](../../CONTRIBUTING.md)：新增条目先查重，提交来源、学习价值、具体入口与边界。

后续按真实任务补充推荐系统、因果、联邦、隐私、机器人、多模态、JVM/R/C++等分支；
当前未覆盖不等于这些领域没有开源实现，也不应随意宣称“所有 ML 仓库已经收齐”。
