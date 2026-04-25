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

不需要 Skills 的时候：
- AI 每次都要重新理解项目 → **输出不稳定**
- 每个问题都要手动描述上下文 → **效率低**
- 模型处理所有任务不分级 → **token 浪费 5-15x**

---

## 快速开始

```bash
# 1. 克隆本仓库
git clone https://github.com/your-org/skill-builder-guide.git
cd skill-builder-guide

# 2. 阅读创建指南
#    SKILL-BUILDER-GUIDE.md

# 3. 复制示例技能到你的项目
cp -r skills/example-dev /path/to/your/project/skills/
cp -r skills/example-code-map /path/to/your/project/skills/

# 4. 按指南修改为你的项目信息

# 5. 验证技能准确性
python scripts/validate-skills.py /path/to/your/project/skills/
```

---

## 项目结构

```
skill-builder-guide/
├── SKILL-BUILDER-GUIDE.md      ← 核心指南（必读）
├── README.md                   ← 本文件
├── CLAUDE.md                   ← 项目自身 CLUADE.md
├── LICENSE
│
├── skills/                     ← 示例技能目录（可直接复制使用）
│   ├── skill-builder-guide/    ← 本指南自身作为 Claude Code 技能
│   ├── example-dev/            ← 开发规范技能示例
│   ├── example-code-map/       ← 代码地图技能示例
│   └── example-delegation/     ← 模型分治技能示例
│
├── templates/                  ← 可复用的模板
│   ├── skill-template.md
│   └── openai-template.yaml
│
├── scripts/                    ← 工具脚本
│   ├── validate-skills.py      ← 验证技能与实际代码的一致性
│   ├── package-skill.py        ← 打包技能为 .zip
│   └── README.md
│
└── .github/workflows/
    └── validate.yml            ← CI: 自动验证技能健康度
```

---

## 核心概念

### 六大技能类型

| 类型 | 用途 | 典型问题 |
|------|------|---------|
| **规范技能** (dev) | 技术栈、代码规范、API 规范 | "用什么技术？怎么组织？" |
| **地图技能** (code-map) | 文件定位、组件导航 | "在哪写？哪个文件？" |
| **流程技能** (workflow) | 开发步骤、检查清单 | "按什么顺序？从哪开始？" |
| **脚本技能** (scripts) | 部署回滚、日常运维 | "怎么运行？怎么部署？" |
| **调用链技能** (call-chain) | 数据流追踪、类型验证 | "数据怎么传？终点在哪？" |
| **分治技能** (delegation) | 模型路由、L0 强制下放 | "谁来做？该不该派 Haiku？" |

### 模型分级路由

| 等级 | 模型 | 任务类型 | 必须下放？ |
|------|------|---------|-----------|
| **L0** | Haiku（轻量） | 文件查找、信息查阅、命令执行 | **是** |
| **L1** | Sonnet（标准） | 有界实现、单模块修改 | 可选 |
| **L2** | Sonnet/Opus（高能力） | 根因诊断、跨模块实现 | 主模型级别 |
| **L3** | Opus（顶级） | 架构决策、安全审计 | 主模型级别 |

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
policy:
  allow_implicit_invocation: false
triggers:
  - 开发规范
  - 技术栈
```

---

## 谁在用这个？

- **独立开发者** — 为自己的项目创建 Skills，减少重复描述
- **团队** — 统一 AI 协作规范，新人快速上手
- **开源项目** — 为贡献者提供 AI 友好的开发指引
- **AI Agent 开发者** — 构建自定义技能生态

---

## Roadmap

- [x] 核心指南 v1.0
- [x] 6 种技能模板
- [x] 模型分级路由（L0-L3）
- [x] H-ADMC 主从编排模式
- [x] 技能验证协议
- [ ] 技能自动生成 CLI 工具
- [ ] VS Code 扩展支持
- [ ] 技能市场（社区共享）
- [ ] 多 Agent 框架适配（Cursor、Copilot）

---

## 贡献

欢迎提交 PR 和 Issue！请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)（如有）。

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
"# SKILL-BUILDER-GUIDE" 
"# SKILL-BUILDER-GUIDE" 
