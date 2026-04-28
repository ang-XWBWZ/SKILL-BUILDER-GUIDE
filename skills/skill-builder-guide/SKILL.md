---
name: skill-builder-guide
description: >-
  AI Agent Skills 创建方法论与执行管线。当需要为项目创建技能体系、
  生成专属技能、理解技能模板、模型分治或验证技能准确性时触发。
  This is a META skill — it creates other skills as its output.
model_tier: L1
skill_tier: meta
composes:
  - planning: delegation
  - functional: change-model
  - atomic: example-dev
  - atomic: example-code-map
  - atomic: example-delegation
composed_by: []
context_budget:
  l1_metadata: 120
  l2_body: 4800
  l3_references: 20000
version: 2.0.0
status: active
review_by: 2026-07-28
trust_level: internal
requires_network: false
requires_file_write: true
compatibility: requires git, python3, pyyaml
allowed_tools: Bash Read Write Edit Grep Glob Agent
evolution:
  usage_count: 0
  last_corrections: []
  stale_markers: []
---

# Skill Builder Guide — 技能创建元技能

> **定位**: **meta 层技能**——它的输出不是业务代码，而是**新的技能文件**（SKILL.md + openai.yaml）。
>
> **核心能力**: 分析目标项目 → 扫描代码提取风格 → 按模板生成专属技能 → 验证准确性 → 用户确认。
>
> **组合关系**: 本技能编排 [code-map](../example-code-map/SKILL.md)、[dev](../example-dev/SKILL.md)、[delegation](../example-delegation/SKILL.md) 作为 atomic 支撑。
>
> **规范参考**: 完整规范见 [references/](references/) 目录；快速入门见项目根目录 `docs/quick-start.md`。

## 触发条件

- 为项目创建技能体系
- "创建技能" / "生成专属技能" / "技能模板"
- "模型分级" / "L0 下放" / "技能验证"
- "技能打包" / "技能目录" / "skill builder"
- "openai.yaml" / "frontmatter 规范"
- 需要理解双轴分级（执行轴 + 组合轴）

## 关联技能

- [变更模型](../change-model/SKILL.md) — functional 层变更报告
- [开发规范](../example-dev/SKILL.md) — atomic 层规范模板
- [代码地图](../example-code-map/SKILL.md) — atomic 层文件定位 [L0]
- [分治规则](../example-delegation/SKILL.md) — atomic 层分治模板

---

## 一、技能体系架构

### 1.1 双轴分级模型

每个技能在**两个独立维度**上定义：

| | 执行轴 (model_tier) | 组合轴 (skill_tier) |
|--|-------------------|---------------------|
| **问题** | 谁执行？ | 在组合图中处于什么位置？ |
| **决策依据** | 认知负载 | 依赖关系与抽象层级 |
| **值域** | L0 / L1 / L2 / L3 | meta / planning / functional / atomic |

**两轴正交。** atomic + L0 = 纯查表（Haiku 执行）；functional + L1 = 多步推理（Sonnet 执行）。两个决策互不替代。

### 1.2 组合轴定义

| Tier | 职责 | 允许的组合操作 |
|------|------|--------------|
| **meta** | 创建其他技能 | 编排 planning + functional + atomic |
| **planning** | 任务拆解与模型路由 | 编排 functional + atomic |
| **functional** | 可复用的多步子例程 | 编排 atomic |
| **atomic** | 单一信息源或工具 | 不编排其他技能 |

### 1.3 执行轴定义

| 等级 | 模型 | 典型任务 | 下放策略 |
|:----:|------|---------|:--------:|
| **L0** | Haiku | 文件查找、信息查阅、命令执行 | **强制下放** |
| **L1** | Sonnet | 单模块修改、窄范围搜索 | 按需 |
| **L2** | Sonnet/Opus | 跨模块实现、根因诊断 | 主模型处理 |
| **L3** | Opus | 架构决策、安全审计 | 主模型处理 |

---

## 二、技能类型决策

根据目标项目特征选择技能组合。

| 项目特征 | 推荐数量 | 技能组合 |
|---------|:------:|---------|
| 小型项目 (Bug修复) | 2 | 规范(atomic) + 流程(functional) |
| 中型项目 (新增页面) | 3 | 规范 + 地图(atomic) + 流程 |
| 大型项目 (新增模块) | 4 | 规范 + 地图 + 流程 + 变更模型(functional) |
| 复杂项目 (多服务) | 5-6 | 以上 + 调用链(functional) + 脚本(atomic) + 分治(planning) |

默认模型等级速查：

| 技能类型 | 执行层 | 组合层 |
|---------|:--:|:--:|
| 规范技能 (dev) | L1 | atomic |
| 地图技能 (code-map) | L0 | atomic |
| 流程技能 (workflow) | L1 | functional |
| 脚本技能 (scripts) | L0 | atomic |
| 调用链技能 (call-chain) | L1 | functional |
| 变更模型技能 (change-model) | L1 | functional |
| 分治技能 (delegation) | L1 | planning |

完整选择矩阵见 [references/skill-types-catalog.md](references/skill-types-catalog.md)。

---

## 三、五阶段执行管线

### 管线总览

```
Phase 1: ANALYZE ──→ Phase 2: SCAN ──→ Phase 3: GENERATE ──→ Phase 4: VALIDATE ──→ Phase 5: CONFIRM
    (L1-Sonnet)        (L0-Haiku)         (L1-Sonnet)           (L0-Haiku)            (L1-Sonnet)
         │                  │                   │                    │                     │
    技能规划方案        代码样本             技能文件              验证报告               approved /
                                                                                       revise / reject
```

### Phase 1: ANALYZE — 项目分析与技能规划

**执行者**: Sonnet (L1)
**输入**: 目标项目路径 + 项目类型提示（如 `--stack spring-boot --type fullstack`）
**输出**: 技能规划方案 `{ skill_plan: [{ name, skill_tier, model_tier, reason }] }`

```
Agent(
  description: "分析项目确定技能方案",
  model: "sonnet",
  prompt: """
    【任务】分析目标项目，确定应创建哪些技能
    【项目路径】{project_path}
    【类型提示】{project_type_hint}
    【分析维度】
      1. 项目类型（前端/后端/全栈/微服务）
      2. 技术栈（语言、框架、数据库、中间件）
      3. 模块结构（业务模块、技术模块）
      4. 团队规模
    【输出格式】
      Conclusion: 推荐创建 N 个技能，类型为 [...]
      Basis: 每个技能的创建理由（项目特征 → 技能类型映射）
      Uncertainty: 需要用户确认的假设（如"假设数据库为 MySQL"）
  """
)
```

### Phase 2: SCAN — 代码扫描

**执行者**: Haiku (L0) — **必须下放**
**输入**: 技能规划 + 文件匹配模式
**输出**: 各层代码样本，含关键模式识别

扫描维度与记录格式见 [references/pipeline/phase-2-scan.md](references/pipeline/phase-2-scan.md)。

核心扫描检查清单：

| 层级 | 扫描目标 | 记录项 |
|------|---------|--------|
| 接口层 | 路由声明、参数校验、响应封装 | `{方式}`、`{类/函数名}` |
| 业务层 | 抽象接口、一致性管理、参数转换 | `{有/无}`、`{方式}` |
| 数据层 | ORM方式、查询组织、分页方式 | `{框架}`、`{方式}` |
| 集成层 | 远程调用、消息队列、定时任务 | `{列表}`、`{配置}` |

### Phase 3: GENERATE — 生成技能文件

**执行者**: Sonnet (L1)
**输入**: 技能规划 + 代码样本 + 匹配的模板
**输出**: `skills/{name}/SKILL.md` + `skills/{name}/agents/openai.yaml`

生成规则：
1. **frontmatter 字段**：按 [references/frontmatter-spec.md](references/frontmatter-spec.md) 填写完整
2. **触发条件**：从项目代码中提取实际术语作为触发词
3. **技术栈表**：填入扫描到的实际版本号
4. **代码示例**：使用扫描到的实际代码片段（脱敏后）
5. **双轴标注**：model_tier 和 skill_tier 必须填写

详细 prompt 模板见 [references/pipeline/phase-3-generate.md](references/pipeline/phase-3-generate.md)。

### Phase 4: VALIDATE — 验证技能准确性

**执行者**: Haiku (L0) — **必须下放**
**输入**: 生成的技能路径
**输出**: 验证报告 `{ pass_rate, unmatched: [{file, expected, actual}] }`

```bash
# 格式 + 结构验证
python scripts/validate-skills.py skills/{skill-name}

# 语义验证（Phase 3 后可用）
python scripts/validate-skills.py skills/{skill-name} --semantic
```

验收标准：

| 验证层 | 通过条件 |
|--------|---------|
| V1 格式 | frontmatter 完整、trigger ≥5、YAML 有效 |
| V2 结构 | 双轴等级一致、组合图闭合、预算不超限 |
| V3 语义 | 文件路径 ≥95%、方法名 ≥90%、版本号 100% |

验证协议详见 [references/validation-protocol.md](references/validation-protocol.md)。

### Phase 5: CONFIRM — 用户确认

**执行者**: Sonnet (L1)
**输出**: `approved` | `revise({feedback})` | `reject`

确认要点：
1. 技术栈版本是否正确
2. 标准写法是否符合预期
3. 兼容写法原因是否准确
4. 是否有用户文档需要合并（以用户文档为准）

---

## 四、目录结构规范

```
{project}/skills/{skill-name}/
├── SKILL.md              # L2: 核心指令体 (≤5000 tokens)
├── agents/
│   └── openai.yaml       # L1: 触发配置（元数据 + 触发词）
├── references/           # L3: 深入参考，按需加载 (≤8000 tokens total)
├── scripts/              # L4: 可执行脚本（零token进入上下文）
└── assets/               # 静态资源（模板、图片）
```

CLAUDE.md 集成规范：极简路由表（≤500 tokens），只放强制分治规则 + 技能路由表，不包含完整技能描述。

---

## 五、核心规范速查

| 规范 | 参考文件 |
|------|---------|
| frontmatter 完整字段定义 | [references/frontmatter-spec.md](references/frontmatter-spec.md) |
| 8 种技能类型完整目录 | [references/skill-types-catalog.md](references/skill-types-catalog.md) |
| 技能验证协议 | [references/validation-protocol.md](references/validation-protocol.md) |
| 完整创建流程与验收标准 | `SKILL-BUILDER-GUIDE.md` 第九章 |
| 技能打包与分发 | `SKILL-BUILDER-GUIDE.md` 第十八章 |
| 维护与生命周期管理 | `SKILL-BUILDER-GUIDE.md` 第十章 |

---

## 六、模型等级

**L1 — Sonnet / meta tier**：需理解项目结构、提取代码风格、按模板生成结构化技能文档、根据验证反馈迭代。扫描子任务派 L0 — Haiku。
