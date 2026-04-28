---
name: example-delegation
description: >-
  分治规则技能模板。用于指导创建项目专属的分治规则。
  定义哪些任务必须下放 Haiku、下放格式、子Agent输出规范。
model_tier: L1
skill_tier: atomic
composes: []
composed_by:
  - meta: skill-builder-guide
context_budget:
  l1_metadata: 100
  l2_body: 1500
  l3_references: 3000
version: 1.1.0
status: active
review_by: 2026-07-28
trust_level: internal
requires_network: false
requires_file_write: false
compatibility: universal
allowed_tools: Agent Read Bash
evolution:
  usage_count: 0
  last_corrections: []
  stale_markers: []
---

# 分治规则技能模板

> **定位**: Atomic 层 / L1 执行层——供其他项目参照创建项目级分治规则的**指南模板**。被 [skill-builder-guide](../skill-builder-guide/SKILL.md) (meta) 编排调用。
>
> **完整实现**: 本项目实际使用的分治技能见 [delegation](../delegation/SKILL.md) (planning 层)。
>
> **深入参考**: 升级策略细节见 [references/upgrade-strategy.md](references/upgrade-strategy.md)。

## 触发条件

- 创建分治规则技能 / 定义 L0 任务下放规则
- 询问"这个任务该不该下放"
- 需要分治规则模板参考

## 关联技能

- [分治驱动](../delegation/SKILL.md) — 本项目实际使用的 planning 层分治技能
- [开发规范](../example-dev/SKILL.md) — L0 信息查阅场景
- [代码地图](../example-code-map/SKILL.md) — L0 文件定位场景 [L0]

---

## 一、强制分治原则

**主模型不得执行 L0 任务。** 所有 L0 任务必须通过 `Agent(model: "haiku")` 下放。

## 二、L0 任务清单

| 类别 | 任务举例 | 目标技能 |
|------|---------|---------|
| 文件查找 | 查文件在哪、目录结构 | code-map |
| 信息查阅 | 查版本号、API 路由 | dev |
| 命令执行 | 部署、打包、服务启停 | scripts |
| 静态追踪 | 画数据流图、核对API清单 | code-map / dev |
| 机械编辑 | 修改变量名、更新版本号 | (直接操作) |

## 三、下放标准格式

```
Agent(
  description: "3-5词描述任务",
  model: "haiku",
  prompt: """
    【任务】具体要做什么
    【文件】需要读取的路径列表
    【输出要求】Conclusion/Basis/Uncertainty 格式
  """
)
```

## 四、子Agent输出格式

```
结论 (Conclusion):   一句话回答分配的目标
依据 (Basis):        具体证据、观察、推理路径
不确定性 (Uncertainty): 风险、缺失信息、失败模式（无则写"无"）
```

主模型收到后只做三件事：提取结论 → 识别冲突 → 决策。

## 五、升级/兜底策略

| 触发条件 | 阈值 | 动作 |
|---------|------|------|
| 用户多次不满意 | 同一任务 ≥2 轮修正未通过 | 打包上下文，提交顶级模型 |
| 工作返工 | 同段代码反复修改，问题未收敛 | 停止修改，重新分析根因 |

**升级信息包**：原始需求 + 已尝试方案及失败原因 + 当前阻塞点 + 已排除假设。

详见 [references/upgrade-strategy.md](references/upgrade-strategy.md)。

## 六、模型等级

**L1 — Sonnet / atomic tier**：规则解释与编排，需推理判断。本技能为模板参考，实际执行参考 [delegation](../delegation/SKILL.md)。
