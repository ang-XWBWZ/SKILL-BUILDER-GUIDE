---
name: example-code-map
description: >-
  代码地图技能模板。用于指导创建项目专属的代码地图技能。
  当询问文件位置、目录结构、组件导航、路由映射时触发。
  L0 — 必须由 Haiku 执行，纯文件路径查表。
model_tier: L0
skill_tier: atomic
composes: []
composed_by:
  - functional: change-model
  - planning: delegation
  - meta: skill-builder-guide
context_budget:
  l1_metadata: 95
  l2_body: 800
  l3_references: 0
version: 1.1.0
status: active
review_by: 2026-07-28
trust_level: internal
requires_network: false
requires_file_write: false
compatibility: universal
allowed_tools: Read Glob
evolution:
  usage_count: 0
  last_corrections: []
  stale_markers: []
---

# 代码地图技能模板

> **定位**: Atomic 层 / L0 执行层——纯文件路径映射，**无推理需求，必须由 Haiku 执行**。被 [change-model](../change-model/SKILL.md) (functional)、[delegation](../delegation/SKILL.md) (planning)、[skill-builder-guide](../skill-builder-guide/SKILL.md) (meta) 编排调用。
>
> **使用方式**: 参照本模板的结构，扫描项目目录后填充实际路径。

## 触发条件

- 创建代码地图技能
- 询问文件位置、目录结构
- 询问"在哪里开发"、"组件在哪个文件"
- 询问页面路由、路由映射

## 关联技能

- [开发规范](../example-dev/SKILL.md) — 技术栈信息
- [分治驱动](../example-delegation/SKILL.md) — 模型分治规则

---

## 一、项目结构（模板）

> AI 扫描项目后替换 `{placeholder}` 为实际目录布局。

```
{project}/
├── {源码目录}/
│   ├── {入口文件}
│   ├── {配置目录}/
│   ├── {接口层目录}/
│   ├── {业务层目录}/
│   └── {数据层目录}/
├── {资源目录}/
│   └── {配置文件}
└── {前端目录}/          # 如有
    └── {页面目录}/
```

---

## 二、快速定位（模板）

> AI 扫描项目后填充实际路径。

| 需求 | 定位方式 |
|------|----------|
| 修改接口 | `{接口层目录}/{业务模块}*.{扩展名}` |
| 修改业务逻辑 | `{业务层目录}/{业务模块}*.{扩展名}` |
| 修改数据访问 | `{数据层目录}/{业务模块}*.{扩展名}` |
| 修改配置 | `{配置目录}/{配置文件}` |
| 修改前端页面 | `{前端目录}/{页面目录}/*.{扩展名}` |

---

## 三、路由与页面（模板）

| 路径 | 文件 | 说明 |
|------|------|------|
| / | `{文件路径}` | 首页 |
| /{path} | `{文件路径}` | {说明} |

---

## 四、模型等级

**L0 — Haiku / atomic tier**：纯文件路径查表，零推理需求。主模型不得直接执行此技能——**必须下放 Haiku**。
