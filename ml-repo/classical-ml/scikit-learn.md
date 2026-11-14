# scikit-learn — P-ML 视角

**Last reviewed:** 2026-11-14 (Asia/Shanghai). **Profile:** ml.

[官方仓库](https://github.com/scikit-learn/scikit-learn) · [固定提交 README](https://github.com/scikit-learn/scikit-learn/blob/ee56c8b5d809dc7b970a140ed501269b63c69cf8/README.rst).
来源提交：`ee56c8b5d809dc7b970a140ed501269b63c69cf8`；逐条时间与公开元数据见 [catalog.json](../catalog.json)。

## 用途

经典机器学习、预处理与模型选择。

## 为何在本仓库收录

建立传统 ML 的 baseline、split、pipeline 和评估习惯，再谈复杂模型。 这是目录编者的选题理由，不是已测量的优越性或官方背书。

## 源码入口

以下路径已在上述固定 Git tree 中核对；路径存在不等于本轮完成源码审计。

1. [源码入口 1](https://github.com/scikit-learn/scikit-learn/blob/ee56c8b5d809dc7b970a140ed501269b63c69cf8/sklearn/linear_model/_base.py)：`sklearn/linear_model/_base.py`。
2. [源码入口 2](https://github.com/scikit-learn/scikit-learn/blob/ee56c8b5d809dc7b970a140ed501269b63c69cf8/sklearn/model_selection/_split.py)：`sklearn/model_selection/_split.py`。

## 学习路线

先读官方 README 与许可，再按上述入口追踪一个输入、状态变化和输出；对照其测试，写下问题：**如何避免预处理和交叉验证泄漏？**

## 练习（未执行）

固定合成分类样本，预处理只在训练集拟合；比较 Pipeline 与错误全样本预处理的差异。 本轮新增练习的实测效果、性能和学习收益均为 **NOT RUN / UNMEASURED**，不沿用旧 PR 的局部测试冒充新实验。

## 贡献证据

本轮按本项目、作者 pengpengyi92、public PR 做有界检索，未捕获可列出的 PR。此条定位为 **官方来源核对后的阅读候选**，不声称曾提交、被采用或已独立复现。

## 许可与限制

GitHub 许可证信号：**BSD-3-Clause**。 阅读 [上游许可](https://github.com/scikit-learn/scikit-learn/blob/ee56c8b5d809dc7b970a140ed501269b63c69cf8/COPYING)；API 分类不替代许可原文、第三方依赖、数据/模型权重和商用条件。
本次没有安装/运行此库、调用收费服务、下载模型、签署新 CLA/DCO 或提交上游改动。公开 PR 仅作学习案例；不构成就业、团队合作或生产采用声明。

[分类路线](README.md) · [本目录总入口](../README.md) · [学习与证据模板](../HOW_TO_STUDY.md)
