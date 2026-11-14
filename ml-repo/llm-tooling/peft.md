# PEFT — P-ML 视角

**Last reviewed:** 2026-11-14 (Asia/Shanghai). **Profile:** ml.

[官方仓库](https://github.com/huggingface/peft) · [固定提交 README](https://github.com/huggingface/peft/blob/66a7c305bac9d7f8183b1f158280b77be971a3d4/README.md).
来源提交：`66a7c305bac9d7f8183b1f158280b77be971a3d4`；逐条时间与公开元数据见 [catalog.json](../catalog.json)。

## 用途

参数高效微调与 adapter 相关工具。

## 为何在本仓库收录

学习 LoRA/adapter 的实现和实验隔离，避免把参数更少误写成效果更优。 这是目录编者的选题理由，不是已测量的优越性或官方背书。

## 源码入口

以下路径已在上述固定 Git tree 中核对；路径存在不等于本轮完成源码审计。

1. [源码入口 1](https://github.com/huggingface/peft/blob/66a7c305bac9d7f8183b1f158280b77be971a3d4/src/peft/peft_model.py)：`src/peft/peft_model.py`。
2. [源码入口 2](https://github.com/huggingface/peft/blob/66a7c305bac9d7f8183b1f158280b77be971a3d4/src/peft/tuners/lora/model.py)：`src/peft/tuners/lora/model.py`。

## 学习路线

先读官方 README 与许可，再按上述入口追踪一个输入、状态变化和输出；对照其测试，写下问题：**是否只更新了实验声明中的参数？**

## 练习（未执行）

先检查冻结/可训练参数、adapter 保存与加载边界，列出受控 ablation；未训练模型。 本轮新增练习的实测效果、性能和学习收益均为 **NOT RUN / UNMEASURED**，不沿用旧 PR 的局部测试冒充新实验。

## 贡献证据

本轮按本项目、作者 pengpengyi92、public PR 做有界检索，未捕获可列出的 PR。此条定位为 **官方来源核对后的阅读候选**，不声称曾提交、被采用或已独立复现。

## 许可与限制

GitHub 许可证信号：**Apache-2.0**。 阅读 [上游许可](https://github.com/huggingface/peft/blob/66a7c305bac9d7f8183b1f158280b77be971a3d4/LICENSE)；API 分类不替代许可原文、第三方依赖、数据/模型权重和商用条件。
本次没有安装/运行此库、调用收费服务、下载模型、签署新 CLA/DCO 或提交上游改动。公开 PR 仅作学习案例；不构成就业、团队合作或生产采用声明。

[分类路线](README.md) · [本目录总入口](../README.md) · [学习与证据模板](../HOW_TO_STUDY.md)
