# Skills — 技能体系

本目录包含技能模板和方法论，用于指导生成项目专属技能。

> **定位**：本目录的技能是模板参考，不是直接复制使用的成品。请参照这些模板为你的项目生成专属技能。

---

## 技能清单（双轴分级）

| 技能 | 执行层 | 组合层 | 用途 |
|------|:------:|:------:|------|
| [delegation](delegation/) | L1 | **planning** | 任务拆解、模型路由、子Agent编排 ★ |
| [skill-builder-guide](skill-builder-guide/) | L1 | **meta** | 技能创建管线（分析→扫描→生成→验证→确认） |
| [change-model](change-model/) | L1 | **functional** | 变更报告、调用链检查、存档归档 |
| [example-dev](example-dev/) | L1 | atomic | 开发规范、分层架构、命名规范 |
| [example-code-map](example-code-map/) | **L0** | atomic | 文件定位、目录结构、路由映射 |
| [example-delegation](example-delegation/) | L1 | atomic | 分治规则模板、下放格式 |

> ★ **planning 层**：所有任务入口先经 delegation 判断拆解与路由
> ★ **meta 层**：skill-builder-guide 输出不是代码，而是**新的技能文件**
> ★ **L0 标注**：必须由 Haiku 执行，主模型不得直接调用

---

## 双轴分级模型

每个技能在两个独立轴上定义：

| | 执行轴 (model_tier) | 组合轴 (skill_tier) |
|--|-------------------|---------------------|
| **问题** | 谁执行？ | 在组合图中处于什么位置？ |
| **决策依据** | 认知负载 | 依赖关系与抽象层级 |
| **值域** | L0 / L1 / L2 / L3 | meta / planning / functional / atomic |

两轴正交。例如 code-map 是 atomic + L0（纯查表，Haiku 执行），change-model 是 functional + L1（多步推理，Sonnet 执行）。

---

## 组合关系

```
skill-builder-guide [meta]
  ├─→ delegation [planning]
  ├─→ change-model [functional]
  ├─→ example-dev [atomic]
  ├─→ example-code-map [atomic]
  └─→ example-delegation [atomic]

delegation [planning]
  ├─→ change-model [functional]
  ├─→ example-dev [atomic]
  └─→ example-code-map [atomic]

change-model [functional]
  ├─→ example-dev [atomic]
  └─→ example-code-map [atomic]
```

---

## 生成专属技能流程

```
用户请求 → skill-builder-guide [meta]
  ├─ Phase 1: ANALYZE — 分析项目确定技能方案
  ├─ Phase 2: SCAN — 派 Haiku 扫描代码 [L0]
  ├─ Phase 3: GENERATE — 按模板生成 SKILL.md + openai.yaml
  ├─ Phase 4: VALIDATE — 执行验证脚本 [L0]
  └─ Phase 5: CONFIRM — 用户确认
```

---

## 目录结构

```
skills/{skill-name}/
├── SKILL.md              # L2: 核心指令体 (≤5000 tokens)
├── agents/
│   └── openai.yaml       # L1: 触发配置
├── references/           # L3: 深入参考（按需加载）
├── scripts/              # L4: 可执行脚本（零token进上下文）
└── assets/               # 静态资源
```
