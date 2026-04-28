# 技能验证协议

> 对应 `SKILL-BUILDER-GUIDE.md` 第十三章。此文件为 L3 参考。

## 验证三层模型

| 层 | 名称 | 检查内容 | 工具 |
|----|------|---------|------|
| **V1** | 格式验证 | frontmatter 完整性、触发词数量、YAML 语法 | validate-skills.py |
| **V2** | 结构验证 | 双轴等级一致性、组合图闭合、上下文预算 | validate-skills.py --structural |
| **V3** | 语义验证 | 文件路径存在性、方法名匹配、版本号准确 | validate-skills.py --semantic |

## V1：格式验证

| 检查项 | 通过条件 |
|--------|---------|
| SKILL.md 存在 | 文件存在且非空 |
| agents/openai.yaml 存在 | 文件存在且可解析 |
| frontmatter 起止分隔符 `---` | 第一行必须是 `---` |
| name 字段 | 在 frontmatter 中存在 |
| status 字段 | 值为 draft/active/deprecated/superseded |
| superseded 的 supersededBy | status=superseded 时必须存在 |
| review_by 日期 | 格式 YYYY-MM-DD（兼容旧格式 reviewBy） |
| triggers 数量 | 5-15 个 |
| YAML 语法 | 无解析错误 |
| short_description 含等级标注 | 包含 L0/L1/L2/L3 |

## V2：结构验证

| 检查项 | 通过条件 |
|--------|---------|
| 双轴等级一致性 | L0 技能不得包含推理语言关键词 |
| 组合图闭合 | A.composes 包含 B → B.composed_by 必须包含 A |
| 上下文预算 | l1_metadata ≤150, l2_body ≤5000, l3_references ≤20000 |
| 层级约束 | atomic 不能 composes 其他 atomic |
| 命名一致性 | composes/composed_by 中的名称必须匹配目标 SKILL.md 的 name 字段 |
| display_name 对齐 | openai.yaml display_name 必须与 SKILL.md 中的 model_tier+skill_tier 一致 |

## V3：语义验证（计划中）

| 检查项 | 验证方法 | 通过标准 |
|--------|---------|:------:|
| 文件路径 | 检查文件系统 | ≥95% |
| 方法名 | 读取源文件确认 | ≥90% |
| 版本号 | 读取依赖配置 | 100% |
| API 路由 | 读取路由配置 | ≥90% |

## 验收标准

低于此标准的技能不得发布：

```
V1 格式验证通过率： 100%
V2 结构验证通过率： 100%
V3 语义验证通过率： 文件路径≥95% / 方法名≥90% / 版本号100%
```

## 验证时机

| 时机 | 验证范围 | 层级 |
|------|---------|:--:|
| 创建时 | 全部声明 | V1+V2+V3 |
| 代码重构后 | 受影响技能 | V3 |
| 季度检查 | 全部技能 | V1+V2+V3 |
| 用户报告误差 | 相关技能 | V3 |

## 验证记录格式

```
技能名: myproject-code-map
验证日期: 2026-04-28
V1通过率: 100%
V2通过率: 100%
V3通过率: 92%
不匹配项:
  - getPrice() → 实际为 quotePrice()
  - /api/balance 声明GET → 实际为 POST
```
