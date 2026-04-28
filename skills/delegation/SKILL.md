---
name: delegation
description: >-
  分治驱动技能。定义任务拆解、模型分级路由、子任务派发的原则与方法。
  当需要拆解复杂任务、确定模型等级、派发子Agent时触发。
model_tier: L1
skill_tier: planning
composes:
  - functional: change-model
  - atomic: example-dev
  - atomic: example-code-map
composed_by:
  - meta: skill-builder-guide
context_budget:
  l1_metadata: 105
  l2_body: 3200
  l3_references: 6000
version: 1.1.0
status: active
review_by: 2026-07-28
trust_level: internal
requires_network: false
requires_file_write: false
compatibility: universal
allowed_tools: Agent Bash Read Grep Glob
evolution:
  usage_count: 0
  last_corrections: []
  stale_markers: []
---

# 分治驱动 — 任务拆解与模型路由

> **定位**: Planning 层技能——不直接执行业务任务，而是决定任务如何拆解、路由到哪个模型、如何派发子Agent。
>
> **组合关系**: 本技能编排 [code-map](../example-code-map/SKILL.md) 和 [dev](../example-dev/SKILL.md) 作为 L0 信息收集的 atomic 技能。
>
> **模板参考**: 为其他项目创建分治技能时，参照 [example-delegation](../example-delegation/SKILL.md)。
>
> **深入参考**: 升级策略细节见 [references/upgrade-escalation.md](references/upgrade-escalation.md)。

## 触发条件

- 任务包含多个子目标
- 需要判断模型等级（L0/L1/L2/L3）
- 需要拆解复杂任务并派发子Agent
- 询问"该不该下放"、"用什么模型"、"怎么拆任务"
- 混合操作类型（分析+实现、实现+验证）

## 关联技能

- [技能构建指南](../skill-builder-guide/SKILL.md) — meta 层技能创建
- [变更模型](../change-model/SKILL.md) — functional 层变更驱动
- [分治规则模板](../example-delegation/SKILL.md) — atomic 层参考

---

## 一、核心原则

```
主模型（高能力）
  ├── 拆解 → 路由 → 派发
  ├── 整合 → 冲突检测 → 再决策
  └── 不执行 L0 工作
        │
        ├─ L0 子模型（轻量）：读、查、跑、验
        ├─ L1 子模型（标准）：有界实现、窄搜索
        └─ L2+ 主模型自身处理
```

**三句话原则**：
1. 主模型编排，子模型执行
2. L0 任务默认下放
3. 子任务一目标一验证

---

## 二、双轴分级

每个任务在**两个独立轴**上评估：

| | 执行轴 (model_tier) | 组合轴 (skill_tier) |
|--|-------------------|---------------------|
| **问题** | 谁来执行？ | 在组合图中处于什么位置？ |
| **决策依据** | 认知负载 | 依赖关系 |
| **值域** | L0 / L1 / L2 / L3 | meta / planning / functional / atomic |

### 执行轴：模型分级路由

| 等级 | 复杂度 | 推荐模型 | 做什么 | 下放建议 |
|:----:|--------|----------|------|----------|
| **L0** | 执行级 | Haiku（轻量） | 文件查找、信息查阅、命令执行、静态追踪、机械编辑 | **默认下放** |
| **L1** | 有界级 | Sonnet（标准） | 单模块修改、窄范围搜索、格式修复 | 按需 |
| **L2** | 推理级 | Sonnet/Opus | 多步骤规划、根因诊断、跨模块修改、结果整合 | 主模型处理 |
| **L3** | 战略级 | Opus | 架构决策、安全审计、系统重设计 | 主模型处理 |

**L0 下放的核心理由**：L0 是机械操作，主模型执行消耗 5-15x token，与轻量模型结果等价。

### 组合轴：技能层级

| Tier | 职责 | 本体系中的技能 |
|------|------|--------------|
| **meta** | 创建其他技能 | skill-builder-guide |
| **planning** | 编排与路由 | delegation |
| **functional** | 可复用的多步子例程 | change-model |
| **atomic** | 单一工具/查表 | dev, code-map, delegation-template |

---

## 三、何时拆解任务

满足**任一条件**即建议拆解：

1. **多个子目标** — 任务包含超过一个不同目标
2. **混合操作类型** — 同时需要分析和生成、实现和验证
3. **无法单次闭环** — 不能在一个 pass 内完成并验证
4. **风险隔离** — 独立验证可降低整体风险
5. **并行机会** — 子任务可同时运行
6. **包含 L0 工作** — 非平凡任务几乎总是包含 L0 工作

**不需要拆解的情况**：单一目标、单次闭环、纯推理任务（无文件/命令操作）。

---

## 四、子任务设计

每个子任务满足：
- **一个目标** — 不模糊、不多义
- **明确输入** — 文件路径、搜索模式、待执行命令
- **预期输出** — 按输出规范格式返回
- **验证条件** — 什么算"完成"
- **最小依赖** — 尽量独立、可并行

### 设计对比

| 差（模糊、多目标） | 好（明确、单目标） |
|------|------|
| "分析业务层并修复问题" | "读取 {文件名}，提取所有公共方法签名，以列表输出" |
| "检查服务健康状态" | "检查后端进程是否运行、数据库是否可连接、API是否响应200" |

---

## 五、常用分治模式

### 模式 A：L0 信息收集（最常用）

```
用户需求
  │
主模型 (L2)：理解需求、确定需要哪些信息
  ├── L0：查文件位置    → code-map
  ├── L0：查技术规范    → dev
  ├── L0：读现有代码    → 提取模式
  └── 主模型：整合信息、执行实现
```

### 模式 B：并行 L0 批量

```
主模型：拆解为 N 个独立检查
  ├── L0：检查 A
  ├── L0：检查 B
  ├── L0：检查 C
  └── 主模型：收集结果、输出总结
```

### 模式 C：复杂调查

```
主模型 (L2)：分析问题、定位线索
  ├── L0：读关键代码文件
  ├── L0：查 git log 变更历史
  └── 主模型：综合证据、诊断根因
```

---

## 六、子Agent输出规范

每个子Agent返回结构化三要素：

```
结论 (Conclusion):   一句话回答分配的目标
依据 (Basis):        具体证据、观察、推理路径
不确定性 (Uncertainty): 风险、缺失信息、失败模式（无则写"无"）
```

主模型收到后只做三件事：
1. 提取各子Agent结论
2. 识别冲突或缺口
3. 决策：继续 / 重新拆解 / 完成

**主模型不得替代子Agent进行局部推理。**

### 派发命令标准格式

```
Agent(
  description: "3-5词描述任务",
  model: "haiku",
  prompt: """
    【任务】具体要做什么
    【文件】需要读取的路径列表
    【输出要求】按 Conclusion/Basis/Uncertainty 格式返回
  """
)
```

---

## 七、升级策略

当同一任务出现以下情况时，**升级至推理/顶级模型处理**：

| 触发条件 | 阈值 | 动作 |
|---------|------|------|
| 用户多次不满意 | 同一任务 ≥2 轮修正未通过 | 打包上下文，提交顶级模型 |
| 工作返工 | 同段代码反复修改 ≥3 次，问题未收敛 | 停止修改，重新分析根因 |
| 问题未收敛 | 3 轮对话后仍未缩小问题范围 | 升级至更高级模型重新诊断 |

**升级信息包**：原始需求 + 已尝试方案及失败原因 + 当前阻塞点 + 已排除假设。

详见 [references/upgrade-escalation.md](references/upgrade-escalation.md)。

---

## 八、技能进化信号收集（Tier 1）

**每个任务结束时，更新所用技能的 `evolution` 字段**。这是零推理成本的 metadata 更新——不触发 LLM 调用，不加载额外上下文。

```
任务结束:
  skill.evolution.usage_count += 1

  IF 用户有纠正:
    skill.evolution.last_corrections.append("YYYY-MM-DD: [一句话]")
    (只保留最近 3 条)

  IF 发现技能内容与实际不符:
    skill.evolution.stale_markers.append("[一句话]")
```

Tier 2 离线扫描器（`scripts/check-skill-health.py`）定期分析这些信号。Tier 3 由用户显式触发"优化这个技能"进入五阶段重生管线。

---

## 九、模型等级

**L1 — Sonnet / planning tier**：规则解释与编排，需根据任务特征判断拆解和路由策略。
