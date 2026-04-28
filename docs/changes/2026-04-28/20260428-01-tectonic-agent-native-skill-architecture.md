# Tectonic — Agent-Native Skill Architecture v2.0 变更报告

> **变更标识**: `20260428-01`
> **变更类型**: 架构重构
> **影响等级**: L1 — 内部变更（技能体系全面升级，外部调用方不受影响）

---

## 第一层：WHY — 变更背景与需求

### 1. 变更背景

| 要素 | 说明 |
|------|------|
| **需求来源** | 2026 年 Agent Skill 领域五项关键理论评估 |
| **触发原因** | 项目为静态文档体系，不是可被 agent 动态执行的技能系统 |
| **期望目标** | 从"人读文档"升级为"agent 可执行架构" |

### 2. 需求分析

**核心矛盾**：SKILL-BUILDER-GUIDE 是一个"教人创建技能"的指南，而不是"自己能创建技能"的元技能系统。

**理论输入**：

| 理论 | 来源 | 核心贡献 |
|------|------|---------|
| Progressive Disclosure | agentskills.io 标准 (2025.12) | 四层加载：L1元数据→L2指令体→L3参考→L4脚本 |
| SkillX 三层技能层级 | arXiv 2604.04804 (2026.04) | Planning/Functional/Atomic 组合层级 |
| MCE 元上下文工程 | arXiv 2601.21557 (2026.01) | 双层进化：Meta-Agent 进化技能 + Base-Agent 执行 |
| SSL 结构化表示 | arXiv 2604.24026 (2026.04) | Scheduling/Structural/Logical 三表示 |
| Context-as-Budget | Anthropic benchmark (2026) | 从 20K→120K tokens 任务完成率下降 28% |
| Hermes GEPA | ICLR 2026 Oral | 闭环学习循环 + 遗传算法驱动的技能进化 |
| Hermes 三层记忆 | Nous Research (2026.02) | Episodic/Persistent/Skill 记忆体系 |

**判断逻辑**：

```
输入: 当前项目状态
  ├─ CLAUDE.md 3000+ tokens 全量索引
  ├─ 64KB 单体核心指南
  ├─ 6 个平铺技能，无层级语义
  ├─ 无 Progressive Disclosure
  └─ 无进化机制

判断条件:
  - 五项理论均指向同一方向 → 必须做架构升级
  - Hermes GEPA 完整闭环不可行 → 折中为三态模型
  - 不改方法论内容 → Phase 1 只做结构手术

输出: Tectonic v2.0 架构
```

---

## 第二层：WHAT — 影响与风险

### 3. 影响分析

| 维度 | 影响说明 | 影响程度 |
|------|----------|:--------:|
| **上游调用方** | CLAUDE.md 极简化，agent 路由行为不变 | 无 |
| **下游依赖** | 6 个技能全部升级 frontmatter，交叉引用更新 | 低 |
| **相关文件** | CLAUDE.md / 6×SKILL.md / 6×openai.yaml / skills/README.md | — |
| **新增文件** | 11 个 references/ + scripts/check-skill-health.py | — |

### 4. 风险评估

| 风险项 | 级别 | 说明 | 缓解措施 |
|--------|:----:|------|----------|
| 交叉引用断裂 | L1 | composes/composed_by 双向不一致 | 审计验证已全部闭合 |
| 死链 | L1 | reference 文件引用但未创建 | 已清理，所有 19 处引用指向已存在文件 |
| 旧链接失效 | L0 | SKILL-BUILDER-GUIDE.md 未删除，旧路径仍可访问 | 无外部依赖此路径 |
| 验证工具不识别新字段 | L1 | validate-skills.py 不检查 evolution 等新增字段 | 脚本正常运行，新字段为可选 |

---

## 第三层：HOW — 设计与实现

### 5. 设计方案

#### 双轴分级模型

```
每个技能在两条独立轴上定义：

执行轴 (model_tier):       组合轴 (skill_tier):
  L3 — Opus                  meta — 创建其他技能
  L2 — Sonnet/Opus           planning — 任务拆解与路由
  L1 — Sonnet                functional — 可复用多步子例程
  L0 — Haiku (强制下放)      atomic — 单一信息源/工具

两轴正交。code-map = L0 + atomic；change-model = L1 + functional。
```

#### 四层 Progressive Disclosure

```
L1: openai.yaml         ← 永远加载 (~100 tokens/skill)
L2: SKILL.md            ← 触发时加载 (≤5000 tokens)
L3: references/         ← 按需加载 (≤8000 tokens)
L4: scripts/            ← 零 token 进入上下文
```

#### 三态技能进化

```
Tier 1: 运行时信号收集
  evolution.usage_count / last_corrections / stale_markers
  部署: agent 使用技能后顺手递增，零推理，~10 tokens/次

Tier 2: 离线扫描
  scripts/check-skill-health.py
  部署: Haiku 执行，纯规则分析，零 LLM 调用

Tier 3: 手动重生
  用户说"优化这个技能" → skill-builder-guide 五阶段管线
  部署: Sonnet 完整技能创建流程
```

### 6. 实现映射

#### 变更示意树

```
📁 SKILL-BUILDER-GUIDE/
├── 📄 CLAUDE.md                              ✏️ 修改 — 3000t → 500t 极简化
├── 📄 README.md                              ✏️ 修改 — 双轴架构 + 渐进披露
│
├── 📁 skills/
│   ├── 📄 README.md                          ✏️ 修改 — 组合关系图
│   │
│   ├── 📁 delegation/ [planning]
│   │   ├── 📄 SKILL.md                       ✏️ 修改 — frontmatter 升级 + §八进化信号
│   │   ├── 📁 agents/
│   │   │   └── 📄 openai.yaml               ✏️ 修改 — display_name L1-planning
│   │   └── 📁 references/                   ⭐ 新增
│   │       └── 📄 upgrade-escalation.md      ⭐ 新增
│   │
│   ├── 📁 skill-builder-guide/ [meta]
│   │   ├── 📄 SKILL.md                       ✏️ 修改 — 全重写为五阶段管线
│   │   ├── 📁 agents/
│   │   │   └── 📄 openai.yaml               ✏️ 修改 — display_name L1-meta
│   │   └── 📁 references/                   ⭐ 新增
│   │       ├── 📄 frontmatter-spec.md        ⭐ 新增 — 13字段规范 + evolution
│   │       ├── 📄 skill-types-catalog.md     ⭐ 新增
│   │       ├── 📄 validation-protocol.md     ⭐ 新增 — 三层验证模型
│   │       └── 📁 pipeline/
│   │           ├── 📄 phase-2-scan.md        ⭐ 新增
│   │           └── 📄 phase-3-generate.md    ⭐ 新增
│   │
│   ├── 📁 change-model/ [functional]
│   │   ├── 📄 SKILL.md                       ✏️ 修改 — L3内容分流到references/
│   │   ├── 📁 agents/
│   │   │   └── 📄 openai.yaml               ✏️ 修改 — display_name L1-functional
│   │   └── 📁 references/                   ⭐ 新增
│   │       ├── 📄 archive-design.md          ⭐ 新增
│   │       ├── 📄 archive-workflow.md        ⭐ 新增
│   │       └── 📄 git-analysis.md           ⭐ 新增
│   │
│   ├── 📁 example-dev/ [atomic, L1]
│   │   ├── 📄 SKILL.md                       ✏️ 修改 — 扫描清单分流到references/
│   │   ├── 📁 agents/
│   │   │   └── 📄 openai.yaml               ✏️ 修改
│   │   └── 📁 references/
│   │       └── 📄 code-scanning-guide.md     ⭐ 新增
│   │
│   ├── 📁 example-code-map/ [atomic, L0]
│   │   ├── 📄 SKILL.md                       ✏️ 修改 — frontmatter 升级
│   │   └── 📁 agents/
│   │       └── 📄 openai.yaml               ✏️ 修改 — display_name L0-atomic
│   │
│   └── 📁 example-delegation/ [atomic, L1]
│       ├── 📄 SKILL.md                       ✏️ 修改 — frontmatter 升级
│       ├── 📁 agents/
│       │   └── 📄 openai.yaml               ✏️ 修改
│       └── 📁 references/
│           └── 📄 upgrade-strategy.md        ⭐ 新增
│
└── 📁 scripts/
    └── 📄 check-skill-health.py             ⭐ 新增 — Tier 2 离线扫描

📌 图例: ⭐ 新增 (18) | ✏️ 修改 (15) | 未变更: templates/ / workflows/ / LICENSE
```

#### 变更统计

| 类型 | 数量 |
|------|------|
| 新增文件 | 18 |
| 修改文件 | 15 |
| 新增 references/ 文件 | 11 |
| 新增 scripts/ 文件 | 1 |
| 新增代码行 (Python) | ~200 |
| 净 token 节省 (CLAUDE.md) | -2500 |

---

## 第四层：VALIDATION — 验证与交付

### 7. 调用链检查

| 检查项 | 状态 | 说明 |
|--------|:----:|------|
| composes/composed_by 双向闭合 | ✅ | 全部 13 条边验证闭合 |
| 技能名一致性 | ✅ | composes 中全部使用正式名 |
| reference 文件引用 | ✅ | 19 处引用全部指向已存在文件 |
| display_name 对齐 | ✅ | 6/6 与 frontmatter model_tier+skill_tier 一致 |
| l2_body 预算合规 | ✅ | 6/6 均在其声明预算内 |
| validate-skills.py | ✅ | 0 错误 / 0 警告 |
| check-skill-health.py | ✅ | 正常运行，所有技能 usage_count=0 |

### 8. 交付信息

| 项目 | 值 |
|------|-----|
| **分支** | (本地，未提交) |
| **变更文件** | 33 个 |
| **变更日期** | 2026-04-28 |

### 9. 回滚方案

回退到变更前的 Git 状态即可。所有方法论内容未改动（仅重新组织），无数据丢失。

---

*报告时间: 2026-04-28*
