---
name: skill-builder-guide
description: AI Agent Skills 创建方法论。当需要为项目创建技能体系、学习技能模板、理解模型分治或验证技能准确性时触发。
status: active
version: 1.0.0
updatedAt: 2026-04-25
---

# Skill Builder Guide — 技能创建方法论

## 触发条件

- 需要为项目创建技能体系
- 询问"怎么创建 Skills"
- 需要技能模板
- 需要理解模型分治和 L0-L3 路由
- 需要验证 Skills 是否准确
- 需要技能打包分发

## 关联技能

- [变更模型模板](../change-model/SKILL.md) — 变更报告技能模板
- [示例-开发规范](../example-dev/SKILL.md) — 规范技能模板
- [示例-代码地图](../example-code-map/SKILL.md) — 地图技能模板
- [示例-分治驱动](../example-delegation/SKILL.md) — 分治元技能模板

---

## 一、核心指南

完整指南见 `SKILL-BUILDER-GUIDE.md`（项目根目录）。

### 快速导航

| 章节 | 内容 |
|------|------|
| 二、技能数量规划 | 根据项目类型决定技能数量（2-6个） |
| 三、目录结构规范 | 标准化技能目录布局 |
| 六、agents/openai.yaml 规范 | 触发词设计与模型等级标注 |
| 八、技能模板 | 8种技能类型的指南模板 |
| 十一、模型分级路由 | L0-L3 分级、强制下放规则 |
| 十二、H-ADMC 主从编排 | 拆解→派发→整合的完整模式 |
| 十三、技能验证协议 | 代码级事实核查方法 |

## 二、创建步骤总结

```
① 项目分析 → 确定技能类型 + 标注模型等级
② 创建目录结构
③ 编写 SKILL.md（按模板）
④ 编写 agents/openai.yaml（标注 L0/L1/L2）
⑤ 技能验证（代码级事实核查）
⑥ 编写 README.md + CLAUDE.md
```

## 三、模型等级标注速查

| 技能类型 | 默认等级 | 说明 |
|---------|---------|------|
| 规范技能 (dev) | L1 — Sonnet | 含规范推理，非纯查表 |
| 地图技能 (code-map) | L0 — Haiku | 纯文件路径映射 |
| 流程技能 (workflow) | L1 — Sonnet | 多步骤编排需判断 |
| 脚本技能 (scripts) | L0 — Haiku | 固定命令执行 |
| 调用链技能 (call-chain) | L1 — Sonnet | 需要理解数据流 |
| 分治技能 (delegation) | L1 — Sonnet | 规则解释与编排 |
