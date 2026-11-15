# 深度学习框架

**Dimension:** `engineering`. **Selected:** 7; multi-label, not additive.
**Snapshot completed:** `2026-11-15T11:46:35+08:00`; each API observation keeps its own timestamp.

Public-source reading candidates; third-party runtime **NOT_RUN**, quality/cost gains **UNMEASURED**.
Code, data, weights, hosted products and dependencies have separate terms. No installation recommendation or official partnership is implied.

[总目录](README.md) · [实验与防泄漏协议](EXPERIMENT_PROTOCOL.md) · [来源快照](snapshot.json)

| Repository / current owner | 学什么、从哪里开始 | 许可识别与维护状态 | 使用边界 |
| --- | --- | --- | --- |
| [pytorch/pytorch](https://github.com/pytorch/pytorch) | 张量、自动微分、模型与训练状态；[固定 README](https://github.com/pytorch/pytorch/blob/c79633996ebc2114482ae5a4ff3cb409d79a8a9c/README.md)；[版本树](https://github.com/pytorch/pytorch/tree/c79633996ebc2114482ae5a4ff3cb409d79a8a9c) | [NOASSERTION](https://github.com/pytorch/pytorch/blob/c79633996ebc2114482ae5a4ff3cb409d79a8a9c/LICENSE) / needs-license-review / 固定 LICENSE 含 BSD 风格条款及多来源版权声明；不能以 API NOASSERTION 断言无许可，也不能忽略第三方组件。; not archived (not a support promise) | 硬件、算子、随机性和构建条件独立验证。 |
| [tensorflow/tensorflow](https://github.com/tensorflow/tensorflow) | 计算图、自动微分和训练接口；[固定 README](https://github.com/tensorflow/tensorflow/blob/9417b73895fc2c9224bdad8f556db4d178bce700/README.md)；[版本树](https://github.com/tensorflow/tensorflow/tree/9417b73895fc2c9224bdad8f556db4d178bce700) | [Apache-2.0](https://github.com/tensorflow/tensorflow/blob/9417b73895fc2c9224bdad8f556db4d178bce700/LICENSE); not archived (not a support promise) | 与其他框架对照时固定数据、精度和训练预算。 |
| [jax-ml/jax](https://github.com/jax-ml/jax) | 函数变换、自动微分与编译；[固定 README](https://github.com/jax-ml/jax/blob/a4ed83c9cb70611b48c81cff3994ff9ce165c03c/README.md)；[版本树](https://github.com/jax-ml/jax/tree/a4ed83c9cb70611b48c81cff3994ff9ce165c03c) | [Apache-2.0](https://github.com/jax-ml/jax/blob/a4ed83c9cb70611b48c81cff3994ff9ce165c03c/LICENSE); not archived (not a support promise) | JIT 首次编译成本与热运行耗时分开测量。 |
| [keras-team/keras](https://github.com/keras-team/keras) | 高层建模和多后端接口；[固定 README](https://github.com/keras-team/keras/blob/50be564d7d833537b789b0359ec709f5a7267c33/README.md)；[版本树](https://github.com/keras-team/keras/tree/50be564d7d833537b789b0359ec709f5a7267c33) | [Apache-2.0](https://github.com/keras-team/keras/blob/50be564d7d833537b789b0359ec709f5a7267c33/LICENSE); not archived (not a support promise) | 后端、版本与数值等价性不能默认一致。 |
| [google/flax](https://github.com/google/flax) | JAX 模型、参数与训练状态组织；[固定 README](https://github.com/google/flax/blob/204a819c2eb76281b47e4e4a967c578f5615705c/README.md)；[版本树](https://github.com/google/flax/tree/204a819c2eb76281b47e4e4a967c578f5615705c) | [Apache-2.0](https://github.com/google/flax/blob/204a819c2eb76281b47e4e4a967c578f5615705c/LICENSE); not archived (not a support promise) | 不同 Flax API 和状态管理方式不能混为一谈。 |
| [Lightning-AI/pytorch-lightning](https://github.com/Lightning-AI/pytorch-lightning) | 训练循环、checkpoint 与分布式组织；[固定 README](https://github.com/Lightning-AI/pytorch-lightning/blob/84df182f50ab34301aabb3c0eb4031815bfb413d/README.md)；[版本树](https://github.com/Lightning-AI/pytorch-lightning/tree/84df182f50ab34301aabb3c0eb4031815bfb413d) | [Apache-2.0](https://github.com/Lightning-AI/pytorch-lightning/blob/84df182f50ab34301aabb3c0eb4031815bfb413d/LICENSE); not archived (not a support promise) | 便利封装不能消除数据和评估错误。 |
| [fastai/fastai](https://github.com/fastai/fastai) | 高层训练、数据块和迁移学习；[固定 README](https://github.com/fastai/fastai/blob/46231bdc3e88a457c940dd7bde8a03c92fb42901/README.md)；[版本树](https://github.com/fastai/fastai/tree/46231bdc3e88a457c940dd7bde8a03c92fb42901) | [Apache-2.0](https://github.com/fastai/fastai/blob/46231bdc3e88a457c940dd7bde8a03c92fb42901/LICENSE); not archived (not a support promise) | 默认 augmentation、学习率和拆分需要读清楚。 |
