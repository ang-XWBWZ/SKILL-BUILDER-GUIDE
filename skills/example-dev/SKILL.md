---
name: example-dev
description: 示例项目开发规范。询问技术栈、API规范、代码规范时触发。
version: 1.0.0
updatedAt: 2026-04-25
---

# 示例项目开发规范

## 触发条件

- 询问技术栈、依赖版本
- 询问代码规范、API 规范
- 新功能开发前的规范确认

## 关联技能

- [代码地图](../example-code-map/SKILL.md) — 文件位置、组件定位
- [分治驱动](../example-delegation/SKILL.md) — 模型分治规则

---

## 一、技术栈

| 依赖 | 版本 | 说明 |
|------|------|------|
| Spring Boot | 3.2.0 | Web 框架 |
| Java | 17 | 编程语言 |
| Vue 3 | ^3.4.0 | 前端框架 |
| MySQL | 8.0 | 数据库 |

## 二、代码规范

### 包结构

```
com.example.myproject/
├── config/       # 配置类
├── controller/   # API 控制器
├── service/      # 业务逻辑
└── repository/   # 数据访问
```

### 命名规范

| 类型 | 命名 | 示例 |
|------|------|------|
| Controller | XxxController | UserController |
| Service | XxxService | UserService |
| DTO | XxxRequest/Response | UserRequest |

## 三、API 规范

| 方法 | 路由 | 说明 |
|------|------|------|
| GET | /api/users | 用户列表 |
| POST | /api/users | 创建用户 |
| GET | /api/users/{id} | 用户详情 |

## 四、模型等级

**L1 — Sonnet**：含规范理解和推理，非纯查表。
