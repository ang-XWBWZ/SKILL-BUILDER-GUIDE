# Skills — 技能模板目录

本目录包含创建项目专属技能的**模板和方法论**，用于指导生成专属技能文档。

> **定位**：本目录的技能是模板参考，不是直接复制使用的成品。请参照这些模板为你的项目生成专属技能。

---

## 技能模板清单

| 技能 | 等级 | 用途 | 说明 |
|------|:----:|------|------|
| [delegation](delegation/) | L1 | 任务拆解、模型路由 | **本项目分治中枢** ★ |
| [change-model](change-model/) | L1 | 变更报告、调用链检查 | **核心驱动模板** ★ |
| [skill-builder-guide](skill-builder-guide/) | L1 | 技能创建方法论 | 元技能 |
| [example-dev](example-dev/) | L1 | 开发规范技能模板 | 含分层规范、代码扫描方法 |
| [example-code-map](example-code-map/) | **L0** | 代码地图技能模板 | 文件定位方法论 |
| [example-delegation](example-delegation/) | L1 | 分治规则技能模板 | 供其他项目参照 |

> ★ 分治中枢：所有任务入口先经 delegation 判断拆解与路由
> ★ 核心驱动模板：以 Change Model 四层架构（WHY/WHAT/HOW/VALIDATION）驱动开发流程

---

## 生成专属技能流程

```
用户请求 → AI 分析项目 → 扫描代码 → 提取风格 → 生成专属 SKILL.md
```

**AI 执行步骤**：

1. 分析项目技术栈和分层结构
2. 派 Haiku 扫描各层代码样本（L0 任务）
3. 提取标准写法和兼容写法
4. 生成项目专属的 SKILL.md
5. 用户确认或提供文档调整

---

## 技能关联

```
delegation (分治中枢) ← 任务入口，决定拆解与路由
    │
    └─→ 所有 L0 任务下放 Haiku

change-model (变更驱动)
    │
    ├─ WHY   → 需求分析（主模型）
    │
    ├─ WHAT  → 影响风险（主模型）
    │
    ├─ HOW   → example-dev (查规范)
    │        → example-code-map (查文件) [L0]
    │
    └─ VALIDATION → 调用链检查
                   → 测试验证
                   → 变更报告
```
