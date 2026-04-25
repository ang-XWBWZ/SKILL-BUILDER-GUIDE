# Skill Builder Guide — 技能模板

用于 standalone use（复制后直接编辑）。

## 使用方式

1. 复制本文件到 `skills/{your-skill-name}/SKILL.md`
2. 替换 `{project}` 占位符为实际项目名
3. 按需增删章节

---

```markdown
---
name: {project}-{skill-type}
description: {项目名}{技能用途}。当{触发场景}时触发。
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
