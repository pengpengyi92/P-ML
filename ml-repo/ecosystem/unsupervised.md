# 无监督、聚类、降维与检索

**Dimension:** `learning-paradigm`. **Selected:** 5; multi-label, not additive.
**Snapshot completed:** `2026-11-15T11:46:35+08:00`; each API observation keeps its own timestamp.

Public-source reading candidates; third-party runtime **NOT_RUN**, quality/cost gains **UNMEASURED**.
Code, data, weights, hosted products and dependencies have separate terms. No installation recommendation or official partnership is implied.

[总目录](README.md) · [实验与防泄漏协议](EXPERIMENT_PROTOCOL.md) · [来源快照](snapshot.json)

| Repository / current owner | 学什么、从哪里开始 | 许可识别与维护状态 | 使用边界 |
| --- | --- | --- | --- |
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | Pipeline、传统模型、聚类、降维与交叉验证；[固定 README](https://github.com/scikit-learn/scikit-learn/blob/ee56c8b5d809dc7b970a140ed501269b63c69cf8/README.rst)；[版本树](https://github.com/scikit-learn/scikit-learn/tree/ee56c8b5d809dc7b970a140ed501269b63c69cf8) | [BSD-3-Clause](https://github.com/scikit-learn/scikit-learn/blob/ee56c8b5d809dc7b970a140ed501269b63c69cf8/COPYING); not archived (not a support promise) | 预处理只能在训练集或训练折拟合。 |
| [lmcinnes/umap](https://github.com/lmcinnes/umap) | 邻域保持与非线性降维；[固定 README](https://github.com/lmcinnes/umap/blob/5113b770a4ca109b21e51edd5c88bf981a1702e3/README.rst)；[版本树](https://github.com/lmcinnes/umap/tree/5113b770a4ca109b21e51edd5c88bf981a1702e3) | [BSD-3-Clause](https://github.com/lmcinnes/umap/blob/5113b770a4ca109b21e51edd5c88bf981a1702e3/LICENSE.txt); not archived (not a support promise) | 二维图好看不等于簇真实或预测有效。 |
| [scikit-learn-contrib/hdbscan](https://github.com/scikit-learn-contrib/hdbscan) | 密度聚类、噪声和稳定性；[固定 README](https://github.com/scikit-learn-contrib/hdbscan/blob/a06a8042e9d49f3a5bbfcfe928ba7113d8cf5c76/README.rst)；[版本树](https://github.com/scikit-learn-contrib/hdbscan/tree/a06a8042e9d49f3a5bbfcfe928ba7113d8cf5c76) | [BSD-3-Clause](https://github.com/scikit-learn-contrib/hdbscan/blob/a06a8042e9d49f3a5bbfcfe928ba7113d8cf5c76/LICENSE); not archived (not a support promise) | 标签编号无语义，比较时处理噪声与标签置换。 |
| [facebookresearch/faiss](https://github.com/facebookresearch/faiss) | 稠密向量相似检索、索引和聚类组件；[固定 README](https://github.com/facebookresearch/faiss/blob/ebab8f784c1d177129602269d5ad966c525fbdcb/README.md)；[版本树](https://github.com/facebookresearch/faiss/tree/ebab8f784c1d177129602269d5ad966c525fbdcb) | [MIT](https://github.com/facebookresearch/faiss/blob/ebab8f784c1d177129602269d5ad966c525fbdcb/LICENSE); not archived (not a support promise) | 并非通用无监督框架或完整 RAG；召回、聚类质量和资源开销须分别评估。 |
| [MaartenGr/BERTopic](https://github.com/MaartenGr/BERTopic) | embedding、聚类和主题表示；[固定 README](https://github.com/MaartenGr/BERTopic/blob/9036123c97aaa9a6cc4bec4a6db1a7caf9209df6/README.md)；[版本树](https://github.com/MaartenGr/BERTopic/tree/9036123c97aaa9a6cc4bec4a6db1a7caf9209df6) | [MIT](https://github.com/MaartenGr/BERTopic/blob/9036123c97aaa9a6cc4bec4a6db1a7caf9209df6/LICENSE); not archived (not a support promise) | 主题解释、离群项及外部 embedding 权重要单独验证。 |
