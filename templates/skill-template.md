# Skill Builder Guide — 技能模板

> **定位**：本模板用于**指导创建**项目专属技能，不是直接复制使用的成品。使用时替换 `{placeholder}` 为项目实际内容，按需增删章节。

## 使用方式

1. 参照本模板结构，理解各章节的目的
2. 将 `{project}`、`{skill-type}` 等占位符替换为项目实际名称
3. 根据项目需要增删章节，不用照搬
4. 保存到 `skills/{your-skill-name}/SKILL.md`

---

```markdown
---
name: {project}-{skill-type}
description: {项目名}{技能用途}。当{触发场景}时触发。
status: active
reviewBy: {review-date}
version: 1.0.0
updatedAt: {date}
---

# {项目名}{技能名}

## 触发条件

- {触发场景1}
- {触发场景2}
- {触发场景3}

## 关联技能

- [关联技能](../{skill-path}/SKILL.md) — 关联说明

---

## 一、{章节标题}

### 1.1 {子标题}

| 列1 | 列2 | 说明 |
|-----|-----|------|
| {内容} | {内容} | {说明} |

## 二、{章节标题}

{内容}

## 三、模型等级

**L0/L1/L2 — 模型名**：{原因说明}
```
