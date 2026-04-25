# Skills — 示例技能目录

本目录包含可复用的示例技能，可直接复制到你的项目中修改使用。

## 技能清单

| 技能 | 模型等级 | 用途 |
|------|---------|------|
| [skill-builder-guide](skill-builder-guide/) | L1 — Sonnet | 技能创建方法论（本指南自身） |
| [example-dev](example-dev/) | L1 — Sonnet | 开发规范技能示例 |
| [example-code-map](example-code-map/) | L0 — Haiku | 代码地图技能示例 |
| [example-delegation](example-delegation/) | L1 — Sonnet | 模型分治技能示例 |

## 快速复制到项目

```bash
# 复制需要的技能到你的项目
cp -r skills/example-dev /path/to/your/project/skills/
cp -r skills/example-code-map /path/to/your/project/skills/

# 修改 SKILL.md 中的项目信息
# 修改 agents/openai.yaml 中的触发词

# 验证
python scripts/validate-skills.py /path/to/your/project/skills/
```
