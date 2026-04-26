# Skill Builder Guide

> **为 AI Agent 创建专业技能的标准化指南与模板体系**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-8A2BE2)](https://claude.ai/code)

---

## 这是什么？

**Skill Builder Guide** 是一套完整的指南、模板和工具，帮助开发者为任意项目创建专业的 **AI Agent Skills**（技能体系）。

Skills 是 Claude Code 等 AI Agent 的结构化知识库。有了 Skills，AI 可以：

- **精确理解项目结构** — 知道文件在哪、如何命名、遵循什么规范
- **一致性执行开发任务** — 按统一流程编码、测试、部署
- **自动路由到合适模型** — L0 机械任务派 Haiku，L2 推理任务用 Sonnet/Opus

**没有 Skills 的时候**：

| 问题 | 后果 |
|------|------|
| AI 每次重新理解项目 | 输出不稳定 |
| 手动描述上下文 | 效率低 |
| 模型不分级处理 | token 浪费 5-15x |

---

## 快速开始

> **项目定位**：本指南用于**指导创建项目专属技能**，不是直接复制使用的成品。

### 核心理念

```
Change Model 四层架构（驱动开发流程）：

WHY   → 变更背景与需求
WHAT  → 影响与风险
HOW   → 设计与实现
VALIDATION → 调用链检查 + 测试验证
```

### 使用方式

1. **阅读快速入门**：[docs/quick-start.md](docs/quick-start.md)
2. **参照模板结构**：为本指南提供的技能模板和方法论
3. **生成专属技能**：AI 根据你的项目代码生成专属技能文档

---

## 项目结构

```
skill-builder-guide/
├── SKILL-BUILDER-GUIDE.md      ← 核心指南（18章节 + 附录）
├── README.md                   ← 本文件
├── CLAUDE.md                   ← 项目技能入口
├── LICENSE
│
├── docs/                       ← 文档
│   └── quick-start.md          ← 5分钟快速入门
│
├── skills/                     ← 技能模板与方法论
│   ├── delegation/              ← 分治驱动 ★（任务路由中枢）
│   ├── skill-builder-guide/    ← 技能创建方法论
│   ├── change-model/           ← 变更模型技能模板
│   ├── example-dev/            ← 开发规范技能模板
│   ├── example-code-map/       ← 代码地图技能模板 [L0]
│   └── example-delegation/     ← 分治规则技能模板
│
├── templates/                  ← 可复用模板
│   ├── skill-template.md       ← 技能模板
│   └── change-model-template.md ← 变更模型模板
│
├── scripts/                    ← 工具脚本
│   ├── validate-skills.py      ← 验证技能一致性
│   └── package-skill.py        ← 打包技能为 .zip
│
└── .github/workflows/
    └── validate.yml            ← CI: 自动验证技能健康度
```

> ★ 标记为核心驱动技能，建议优先掌握

---

## 核心概念

### 八大技能类型

| 类型 | 等级 | 用途 | 典型问题 |
|------|:----:|------|---------|
| **规范技能** (dev) | L1 | 技术栈、代码规范、API规范 | "用什么技术？怎么组织？" |
| **地图技能** (code-map) | **L0** | 文件定位、组件导航 | "在哪写？哪个文件？" |
| **流程技能** (workflow) | L1 | 开发步骤、检查清单 | "按什么顺序？从哪开始？" |
| **脚本技能** (scripts) | L0 | 部署回滚、日常运维 | "怎么运行？怎么部署？" |
| **调用链技能** (call-chain) | L1 | 数据流追踪、类型验证 | "数据怎么传？终点在哪？" |
| **变更日志技能** (diffs) | L1 | 变更记录、历史追踪 | "改了什么？为什么改？" |
| **变更模型技能** (change-model) | L1 | 结构化变更报告 | "为什么改？影响什么？怎么验证？" |
| **分治技能** (delegation) | L1 | 模型路由、L0 强制下放 | "谁来做？该不该派 Haiku？" |

### 模型分级路由

| 等级 | 模型 | 任务类型 | 必须下放？ |
|:----:|------|---------|:----------:|
| **L0** | Haiku（轻量） | 文件查找、信息查阅、命令执行 | **是** |
| **L1** | Sonnet（标准） | 有界实现、单模块修改 | 否 |
| **L2** | Sonnet/Opus（高能力） | 根因诊断、跨模块实现 | 否 |
| **L3** | Opus（顶级） | 架构决策、安全审计 | 否 |

### 变更模型四层架构

```
┌─────────────────────────────────────┐
│  WHY    — 变更背景与需求             │
│  WHAT   — 影响与风险                 │
│  HOW    — 设计与实现                 │
│  VALIDATION — 验证与交付             │
│    └─ 调用链检查（测试前）           │
└─────────────────────────────────────┘
```

---

## 技能调用流程

### 变更开发流程

```
需求到达
    │
    ▼
┌─ delegation：判断任务复杂度，拆解L0子任务
    │
    ▼
WHY: 需求分析（主模型）
    │
    ▼
HOW: 设计与实现
    ├─ 查技术栈/规范 → example-dev (L1)
    ├─ 查文件位置   → example-code-map (L0) [派Haiku]
    └─ 编码实现     → 主模型处理
    │
    ▼
VALIDATION: 验证
    ├─ 调用链检查   → change-model 调用链检查章节 (L1)
    ├─ 测试验证     → 主模型处理
    └─ 生成变更报告 → change-model (L1)
```

### 技能创建流程

```
创建技能需求
    │
    ▼
┌─ delegation：拆解扫描任务，L0信息收集派Haiku
    │
    ▼
skill-builder-guide (L1)
    ├─ 确定技能类型和数量
    ├─ 选择模板（8种）
    ├─ 标注模型等级
    └─ 验证技能准确性
    │
    ▼
参照模板生成专属技能
    ├─ delegation        → 分治驱动技能
    ├─ change-model      → 变更报告技能
    ├─ example-dev       → 开发规范技能
    ├─ example-code-map  → 代码地图技能
    └─ example-delegation → 分治规则模板
```

---

## 示例：创建你的第一个技能

### 1. 目录结构

```bash
mkdir -p myproject/skills/myproject-dev/agents
```

### 2. SKILL.md

```markdown
---
name: myproject-dev
description: MyProject 开发规范。询问技术栈、API规范时触发。
status: active
version: 1.0.0
---

## 触发条件

- 询问技术栈、依赖版本
- 询问 API 规范、代码规范

## 关联技能

- [代码地图](../myproject-code-map/SKILL.md)

---

## 一、技术栈

| 依赖 | 版本 | 说明 |
|------|------|------|
| Spring Boot | 3.2.0 | Web 框架 |
```

### 3. agents/openai.yaml

```yaml
interface:
  display_name: "L1 — myproject-dev"
  short_description: "L1 — 开发规范查询"
  default_prompt: "Use myproject-dev skill"
policy:
  allow_implicit_invocation: false
triggers:
  - 开发规范
  - 技术栈
  - API规范
```

---

## 谁在用这个？

| 用户类型 | 使用场景 |
|----------|----------|
| **独立开发者** | 为自己的项目创建 Skills，减少重复描述 |
| **团队** | 统一 AI 协作规范，新人快速上手 |
| **开源项目** | 为贡献者提供 AI 友好的开发指引 |
| **AI Agent 开发者** | 构建自定义技能生态 |

---

## Roadmap

- [x] 核心指南 v1.0（18章节）
- [x] 8 种技能模板
- [x] 模型分级路由（L0-L3）
- [x] H-ADMC 主从编排模式（拆解→派发→执行→整合→检查）
- [x] 技能验证协议
- [x] 变更模型技能（WHY/WHAT/HOW/VALIDATION）
- [x] 调用链检查方法论
- [ ] 技能自动生成 CLI 工具
- [ ] VS Code 扩展支持
- [ ] 技能市场（社区共享）
- [ ] 多 Agent 框架适配（Cursor、Copilot）

---

## 贡献

欢迎提交 PR 和 Issue！

### 开发

```bash
# 验证所有示例技能
python scripts/validate-skills.py skills/

# 打包发布
python scripts/package-skill.py skills/skill-builder-guide
```

---

## License

MIT
