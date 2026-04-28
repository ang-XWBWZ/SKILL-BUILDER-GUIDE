# frontmatter 完整字段规范

## 必填字段

| 字段 | 类型 | 约束 | 示例 |
|------|------|------|------|
| `name` | string | 1-64 chars, 小写字母+数字+中划线。与目录名一致。 | `myproject-dev` |
| `description` | string | 1-1024 chars。做什么 + 何时触发。含触发关键词。 | 见下方编写规范 |

## description 编写规范

必须包含两个要素：
1. **做什么**（技能的功能定位）
2. **何时触发**（触发场景/关键词）

```yaml
# ✅ 好的 description
description: >-
  MyProject 开发规范查询。当用户询问技术栈、代码规范、
  API规范、配置项或开发规范时触发。

# ❌ 太短
description: 开发规范

# ❌ 缺少触发信息
description: 提供项目开发规范和编码风格参考
```

## 双轴分级字段（新增）

| 字段 | 类型 | 值域 | 说明 |
|------|------|------|------|
| `model_tier` | string | L0 / L1 / L2 / L3 | 执行轴：谁执行这个技能 |
| `skill_tier` | string | meta / planning / functional / atomic | 组合轴：在组合图中的层级 |

**一致性约束**：
- L0 + meta → 非法（meta 需理解项目结构，不能是纯机械操作）
- L0 + planning → 非法（planning 需编排推理）
- L0 + functional → 不推荐（functional 含多步推理）
- L0 + atomic → 合法（纯查表）

## 组合关系字段（新增）

| 字段 | 类型 | 说明 |
|------|------|------|
| `composes` | list | 本技能编排哪些下层技能。格式：`[{skill_tier}: {skill_name}]` |
| `composed_by` | list | 本技能被哪些上层技能编排。格式：`[{skill_tier}: {skill_name}]` |

**闭合检查**：如果 A.composes 包含 B，则 B.composed_by 必须包含 A。

## 上下文预算字段（新增）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `context_budget.l1_metadata` | int | ≤150 | name + description 的 token 预算 |
| `context_budget.l2_body` | int | ≤5000 (硬约束) | SKILL.md 正文 token 上限 |
| `context_budget.l3_references` | int | ≤10000 | references/ 目录总 token 上限 |

**验证规则**：脚本可对 L2 body 做 token 估算（中文字符/1.5 + 英文单词/1.3）。

## 生命周期字段

| 字段 | 类型 | 值域 | 说明 |
|------|------|------|------|
| `version` | semver | x.y.z | 语义化版本 |
| `status` | string | draft / active / deprecated / superseded | 技能状态 |
| `review_by` | date | YYYY-MM-DD | 建议复核日期，过期后验证工具告警 |
| `superseded_by` | string | 技能名 | 仅 status=superseded 时需要 |

## 安全字段（新增）

| 字段 | 类型 | 值域 | 说明 |
|------|------|------|------|
| `trust_level` | string | internal / community / verified | 来源信任级别 |
| `requires_network` | bool | — | 脚本是否需要网络访问 |
| `requires_file_write` | bool | — | 脚本是否需要文件写入 |

**trust_level 影响自动执行权限**：
- `internal`：项目自有技能，完全信任
- `verified`：经过代码审查的第三方技能
- `community`：社区贡献，需用户逐次确认

## 兼容性字段（来自 agentskills.io）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `compatibility` | string | ≤500 chars | 环境要求（如 `requires git, python3`） |
| `allowed_tools` | string | 空格分隔 | 技能允许使用的工具白名单 |

## 进化信号字段（Tier 1：运行时收集，零推理成本）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `evolution.usage_count` | int | ≥0 | 每次使用此技能时 +1 |
| `evolution.last_corrections` | list | 最多 3 条 | 用户纠正记录，每条格式：`"YYYY-MM-DD: 一句话"` |
| `evolution.stale_markers` | list | 每条 ≤100 chars | agent 发现内容可能过时的地方 |

**使用方式**：agent 执行任务后顺手更新，不触发任何 LLM 推理。Tier 2 离线扫描器（`scripts/check-skill-health.py`）定期分析这些信号，生成改进建议。

**设计哲学**：信号收集内联化（~10 tokens/次），信号处理离线化（一次 Haiku 调用），避免在会话中做技能进化（否则上下文成本不可控）。
