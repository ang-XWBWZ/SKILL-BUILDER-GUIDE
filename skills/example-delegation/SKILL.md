---
name: example-delegation
description: 示例模型分治规则。定义哪些任务必须下放 Haiku、下放格式、主模型不得越界执行的强制约束。
status: active
version: 1.0.0
updatedAt: 2026-04-25
---

# 示例模型分治规则

## 触发条件

- 任何任务开始时自动激活
- 遇到 L0 任务但主模型未下放时触发纠正
- 询问"这个任务该不该下放"

## 关联技能

- [开发规范](../example-dev/SKILL.md) — L0 信息查阅场景
- [代码地图](../example-code-map/SKILL.md) — L0 文件定位场景

---

## 一、强制分治原则

**主模型不得执行 L0 任务。** 所有 L0 任务必须通过 `Agent(model: "haiku")` 下放。

## 二、L0 任务清单

| 类别 | 任务举例 | 目标技能 |
|------|---------|---------|
| 文件查找 | 查文件在哪、目录结构 | code-map |
| 信息查阅 | 查版本号、API 路由 | dev |
| 命令执行 | 部署、打包、服务启停 | scripts |

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
Conclusion: (一句话)
Basis: (具体证据)
Uncertainty: (局限或风险)
```

## 五、模型等级

**L1 — Sonnet**：规则解释与编排，需推理判断。
