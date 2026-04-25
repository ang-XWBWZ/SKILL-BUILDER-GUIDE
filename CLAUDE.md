# Skill Builder Guide

AI Agent Skills 创建指南与模板体系。

---

## 强制分治规则

主模型不得执行 L0 任务。所有文件操作、脚本执行、格式转换必须派 Haiku。

## 项目技能

| 技能 | 模型等级 | 路径 | 用途 |
|------|---------|------|------|
| skill-builder-guide | **L1 — Sonnet** | [skills/skill-builder-guide](skills/skill-builder-guide/) | 技能创建方法论 |
| example-dev | **L1 — Sonnet** | [skills/example-dev](skills/example-dev/) | 开发规范示例 |
| example-code-map | **L0 — Haiku** | [skills/example-code-map](skills/example-code-map/) | 代码地图示例 |
| example-delegation | **L1 — Sonnet** | [skills/example-delegation](skills/example-delegation/) | 分治规则示例 |

## 关键文件

| 文件 | 说明 |
|------|------|
| `SKILL-BUILDER-GUIDE.md` | 核心指南 |
| `templates/skill-template.md` | 技能模板 |
| `scripts/validate-skills.py` | 技能验证工具 |
