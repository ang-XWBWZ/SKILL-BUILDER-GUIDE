# Skill Builder Guide

AI Agent Skills 创建指南与模板体系。

> **定位**：本指南用于**指导创建项目专属技能**，不是直接复制使用的成品。
> **快速入门**：[docs/quick-start.md](docs/quick-start.md) — 5分钟掌握 Change Model 驱动开发

---

## 强制分治规则

主模型不得执行 L0 任务。所有文件操作、脚本执行、格式转换必须派 Haiku。

---

## 技能路由

| 技能 | 执行层 | 组合层 | 触发场景 |
|------|:------:|:------:|----------|
| [delegation](skills/delegation/) | L1 | planning | 拆解任务、模型路由、L0下放 |
| [skill-builder-guide](skills/skill-builder-guide/) | L1 | **meta** | 创建技能、技能模板、模型分级 |
| [change-model](skills/change-model/) | L1 | functional | 变更报告、DiffLog、归档存档、Git分析 |
| [example-dev](skills/example-dev/) | L1 | atomic | 技术栈、代码规范、API规范 |
| [example-code-map](skills/example-code-map/) | **L0** | atomic | 文件位置、组件定位、目录结构 |
| [example-delegation](skills/example-delegation/) | L1 | atomic | 分治规则模板、下放格式 |

---

## 关键文件

| 文件 | 说明 |
|------|------|
| `docs/quick-start.md` | 5分钟快速入门 |
| `templates/skill-template.md` | 技能模板 |
| `templates/change-model-template.md` | 变更模型模板 |
| `scripts/validate-skills.py` | 技能验证工具 |
