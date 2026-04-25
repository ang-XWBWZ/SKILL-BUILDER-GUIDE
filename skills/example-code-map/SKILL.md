---
name: example-code-map
description: 示例项目代码地图。询问文件位置、目录结构、组件导航时触发。
status: active
version: 1.0.0
updatedAt: 2026-04-25
---

# 示例项目代码地图

## 触发条件

- 询问项目结构、目录结构
- 询问"在哪里开发"
- 询问文件位置、组件位置

## 关联技能

- [开发规范](../example-dev/SKILL.md) — 技术栈信息
- [分治驱动](../example-delegation/SKILL.md) — 模型分治规则

---

## 一、项目结构

```
myproject/
├── src/main/java/com/example/myproject/
│   ├── MyprojectApplication.java
│   ├── config/
│   ├── controller/
│   ├── service/
│   └── repository/
├── src/main/resources/
│   └── application.yml
└── frontend/
    └── src/
        ├── App.vue
        └── api/
```

## 二、快速定位

| 需求 | 文件 |
|------|------|
| 修改 API | `controller/UserController.java` |
| 修改业务逻辑 | `service/UserService.java` |
| 修改前端页面 | `frontend/src/App.vue` |
| 修改配置 | `application.yml` |

## 三、模型等级

**L0 — Haiku**：纯文件路径查表，无推理需求。
