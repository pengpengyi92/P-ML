# P-ML · CV / Deep Learning / RL Focus

**Title:** 把计算机视觉、深度学习与强化学习作为重点研究路线。
**Review date:** 2026-11-15, Asia/Shanghai; exact primary-source observations and pins
are in [snapshot.json](snapshot.json).

本轮新增 **43个不重复主仓库**：CV16、DL11、RL16。与原有[73库生态地图](../ecosystem/README.md)
合计 **116个独立主项目**。不是全球全集、软件质量排名或已跑通116个系统的声明。
旧73库快照、详细卡和历史检查回执不改；本目录是明确分开的增量。

## Three priority routes

| 方向 | 本轮重点 | 入口 |
| --- | --- | --- |
| CV | 图像/几何、分类、检测、分割、姿态、跟踪、视频、点云、可微3D、神经渲染、视觉部署 | [16库导读](computer-vision.md) |
| DL | 自动微分、训练原理、GPT学习实现、微调、混合精度、分布式/并行、注意力组件 | [11库导读](deep-learning.md) |
| RL | actor/learner、在线/离线、多智能体、模型式RL、数据、环境和物理仿真 | [16库导读](reinforcement-learning.md) |

### CV：不只“调用一个视觉模型”

- 底层：OpenCV / contrib / scikit-image，用几何、像素、坐标、dtype和形态学建立直觉。
- 感知：MMPreTrain、MMPose、MMTracking、MMRotate、SAM/SAM2、GroundingDINO、YOLO。
- 视频与3D：PyTorchVideo、Open3D、PyTorch3D、Nerfstudio；分别核对时间、视角和坐标。
- 部署：MMDeploy；和[原有ONNX/推理路线](../ecosystem/deployment.md)连接，先测数值等价。
- 原有[视觉10库](../ecosystem/vision.md)中的torchvision、timm、MMDetection、MMSegmentation、
  Detectron2、Kornia及表征学习项目仍然有效，不重复计数。

### DL：原理 → 训练循环 → 训练工程

- 原理：micrograd + D2L；用手算/有限差分验证梯度，教材文本与代码许可分开。
- 训练循环：minGPT / nanoGPT用于历史教学；nanoGPT README已经推荐nanochat作为后继。
- 微调/训练：Accelerate、torchtune；和原有PyTorch、TF、JAX、Flax、Lightning、PEFT联读。
- 规模化：DeepSpeed、torchtitan、Megatron-LM；xFormers是组件，不是完整训练框架。
- DL是长期重点，但不需要同时安装全部工具。设备支持、梯度累积、有效batch、随机状态、
  optimizer、checkpoint恢复和实际内存/通信成本，都要用相同任务和预算验证。

### RL：先认清对象，再比较分数

| 对象 | 例子 | 不能误当成 |
| --- | --- | --- |
| 算法/研究组件 | TorchRL、d3rlpy、CORL、rlkit、MBRL-Lib、Acme | 所有环境上都更强的已验证策略 |
| 环境/API | PettingZoo、Minigrid、Procgen、HighwayEnv | 算法本身或现实安全证明 |
| 数据工具/旧benchmark | Minari、D4RL | 自动授予轨迹使用权或可跨版本直接比较的总分 |
| 物理/具身平台 | MuJoCo、Brax、Habitat-Lab、ML-Agents | 更高仿真FPS就等于更高策略回报 |

原有[Gymnasium、SB3、Ray/RLlib、CleanRL](../ecosystem/reinforcement.md)保留。
训练/评估种子、交互预算、episode结束语义、多智能体生命周期和离线数据来源要显式记录。

## Source findings that change how to use the list

- 原始 `tinkoff-ai/CORL` 已归档；最初候选 `corl-team/CORL` 是fork，未当作另一个独立主项目。
  MBRL-Lib也已归档。历史实现可读，不代表当前维护或兼容性保证。
- D4RL README指向Minari/Gymnasium相关项目迁移；不能把旧环境/归一化分数直接混用。
- Brax README明确自0.13.0仅`brax/training`活跃维护，建议环境/物理使用相应后继接口。
- D2L：教材CC BY-SA4.0；示例/参考代码modified MIT。已固定额外许可文件，不整书复制。
- Ultralytics是AGPL-3.0及另外的商业授权选项，不是“只能非商业”的同义词。
- 本次Minigrid固定LICENSE出现`@@`补丁标记，单列**许可待澄清的阅读参考**，不自动授权复用。
- SAM2的代码/权重/demo、字体和第三方cc_torch分别核对；许可补充文件一并固定。
- DeepSpeed和torchtune的canonical归属已分别解析为`deepspeedai`和`meta-pytorch`。

具体事实、版本与许可入口都在三张分类表，不依靠星数或品牌推定性能与权利。

## Reproduce the catalog, not imaginary ML results

```sh
python scripts/collect_ml_ecosystem.py --catalog-dir ml-repo/cv-dl-rl --collect --render --review-dir .local/cv-dl-rl-sources
python -m unittest discover -s tests -v
python -m unittest discover -s ml-project/linear-regression-feature-scaling -v
```

Python3.11+和认证后的`gh`；仅公开来源读取。原文/缓存只在忽略的`.local/`；不提交源码
镜像、模型、数据集、私有资料或凭据。`--resume`保留原API观察时间。输出限制在本项目
`ml-repo/`的子目录，taxonomy单独维护，不改变原73库默认生成逻辑。

第三方安装、训练、仿真、权重下载、GPU、速度/成本/模型质量比较均 **NOT_RUN / UNMEASURED**。
这次验证的是来源和目录工程，不是模型benchmark。

[实验协议](EXPERIMENT_PROTOCOL.md) · [检索/权利方法](SEARCH_PROTOCOL.md) ·
[选题](selection.json) · [taxonomy](taxonomy.json) · [检查回执](CHECKS.json) ·
[综合报告](../../report/2026-11-15-cv-dl-rl.md) · [全部导读](../README.md)
