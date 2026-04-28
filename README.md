# Skill Builder Guide

> **Agent-Native Skill Architecture v2.0** — 从人读文档到 agent 可执行架构

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 这是什么？

**Skill Builder Guide** 是一套用于构建 AI Agent Skills 的指南、模板和工具体系。基于 2026 年五项关键理论（Progressive Disclosure / SkillX / MCE / SSL / Context-as-Budget）重新设计为 **agent 可执行架构**。

### 三个核心概念

| # | 概念 | 一句话 |
|:--:|------|--------|
| 1 | **双轴分级** | 每个技能同时在执行轴（L0-L3，谁执行）和组合轴（meta/planning/functional/atomic，在哪层）上定义 |
| 2 | **四层渐进披露** | L1元数据永远加载 → L2指令体触发时加载 → L3参考按需加载 → L4脚本零token进上下文 |
| 3 | **三态进化** | 运行时顺手收集信号（~10t/次）→ 离线Haiku扫描分析 → 用户手动触发技能重生 |

---

## 架构全景

```
CLAUDE.md (~500t)              ← 路由器，不是百科全书
  │
  ├─ delegation [planning, L1] ← 编排中枢
  │   └─ composes: change-model + example-dev + example-code-map
  │
  ├─ skill-builder-guide [meta, L1] ← 元技能: 创建其他技能
  │   └─ composes: delegation + change-model + 所有atomic
  │
  ├─ change-model [functional, L1] ← 变更报告 WHY/WHAT/HOW/VALIDATION
  │   └─ composes: example-dev + example-code-map
  │
  ├─ example-dev [atomic, L1]     ← 技术栈 / 规范
  ├─ example-code-map [atomic, L0] ← 文件定位 (必须派Haiku)
  └─ example-delegation [atomic, L1] ← 分治模板

每个技能:
  SKILL.md          ← L2: 核心指令体 (≤5000 tokens)
  agents/openai.yaml ← L1: 触发元数据
  references/        ← L3: 深入参考 (按需加载)
  scripts/           ← L4: 可执行脚本 (零token进上下文)
```

---

## 快速开始

> 5 分钟入门：[docs/quick-start.md](docs/quick-start.md)

### 为你的项目创建专属技能

```
在 Claude Code 中:
"为我的 {项目名} 创建技能体系"
```

skill-builder-guide (meta) 自动执行五阶段管线：分析项目 → 扫描代码(L0 Haiku) → 生成技能 → 验证 → 确认。

### 启动技能健康检查

```bash
python scripts/check-skill-health.py skills/     # Tier 2 离线扫描
python scripts/validate-skills.py skills/        # V1+V2 格式+结构验证
```

---

## 项目结构

```
SKILL-BUILDER-GUIDE/
├── CLAUDE.md                       ← 极简路由表 (~500 tokens)
├── README.md                       ← 本文件
├── SKILL-BUILDER-GUIDE.md          ← 核心指南 (人类参考，18章)
│
├── docs/
│   ├── quick-start.md              ← 5分钟入门
│   └── changes/                    ← 变更报告存档
│
├── skills/                         ← 技能体系 (6个)
│   ├── delegation/                 ← [planning] 分治中枢
│   ├── skill-builder-guide/        ← [meta] 技能创建管线
│   ├── change-model/               ← [functional] 变更报告
│   ├── example-dev/                ← [atomic, L1] 开发规范模板
│   ├── example-code-map/           ← [atomic, L0] 代码地图模板
│   ├── example-delegation/         ← [atomic, L1] 分治规则模板
│   └── README.md                   ← 技能索引 + 组合关系图
│
├── templates/                      ← 可复用模板
│   ├── skill-template.md
│   ├── change-model-template.md
│   └── openai-template.yaml
│
├── scripts/                        ← 工具脚本
│   ├── validate-skills.py          ← V1+V2 格式+结构验证
│   ├── check-skill-health.py       ← Tier 2 健康度扫描
│   └── package-skill.py            ← 技能打包
│
└── workflows/
    └── validate.yml                ← CI: 自动验证
```

---

## 技能双轴分级速查

| 技能 | 执行层 | 组合层 | 用途 |
|------|:------:|:------:|------|
| delegation | L1 | planning | 拆解任务、模型路由、子Agent编排 |
| skill-builder-guide | L1 | meta | 技能创建五阶段管线 |
| change-model | L1 | functional | WHY/WHAT/HOW/VALIDATION 变更报告 |
| example-dev | L1 | atomic | 技术栈规范、分层架构、命名惯例 |
| example-code-map | **L0** | atomic | 文件定位、目录结构 (**派Haiku**) |
| example-delegation | L1 | atomic | 分治规则模板、下放格式 |

---

## Roadmap

- [x] 双轴分级模型 (model_tier × skill_tier)
- [x] 四层渐进披露 (L1→L2→L3→L4)
- [x] CLAUDE.md 极简化 (3000t → 500t)
- [x] skill-builder-guide 元技能管线 (五阶段)
- [x] 三态技能进化 (Tier1信号收集 → Tier2离线扫描 → Tier3重生管线)
- [x] V1+V2 技能验证 + 健康度检查
- [ ] V3 语义验证（代码级事实核查，即将支持）
- [ ] 技能自动生成 CLI 工具
- [ ] 多 Agent 框架适配

---

## 贡献

```bash
# 验证所有技能
python scripts/validate-skills.py skills/

# 健康度检查
python scripts/check-skill-health.py skills/

# 打包发布
python scripts/package-skill.py skills/skill-builder-guide
```

---

## License

MIT
