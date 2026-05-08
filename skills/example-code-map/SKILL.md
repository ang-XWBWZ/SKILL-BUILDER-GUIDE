---
name: example-code-map
description: >-
  Code map skill template. Used to guide creation of project-specific
  code map skills. Triggered when asking about file locations, directory
  structure, component navigation, or route mapping.
  L0 — Must be executed by Haiku, pure file path lookup.
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

# Code Map Skill Template

> **Position**: Atomic tier / L0 execution tier — pure file path mapping, **no reasoning required, must be executed by Haiku**. Composed by [change-model](../change-model/SKILL.md) (functional), [delegation](../delegation/SKILL.md) (planning), [skill-builder-guide](../skill-builder-guide/SKILL.md) (meta).
>
> **Usage**: Scan the project directory, then fill in actual paths following this template structure.

## Trigger Conditions

- Creating a code map skill
- Asking about file locations, directory structure
- Asking "where to develop", "which file has the component"
- Asking about page routes, route mapping

## Related Skills

- [Dev Standards](../example-dev/SKILL.md) — tech stack info
- [Delegation](../example-delegation/SKILL.md) — model delegation rules

---

## 1. Project Structure (Template)

> AI scans the project and replaces `{placeholder}` with actual directory layout.

```
{project}/
├── {source_dir}/
│   ├── {entry_file}
│   ├── {config_dir}/
│   ├── {api_layer_dir}/
│   ├── {service_layer_dir}/
│   └── {data_layer_dir}/
├── {resource_dir}/
│   └── {config_file}
└── {frontend_dir}/          # if present
    └── {pages_dir}/
```

---

## 2. Quick Lookup (Template)

> AI fills in actual paths after scanning the project.

| Need | Lookup Method |
|------|----------|
| Modify API | `{api_layer_dir}/{module}*.{ext}` |
| Modify business logic | `{service_layer_dir}/{module}*.{ext}` |
| Modify data access | `{data_layer_dir}/{module}*.{ext}` |
| Modify config | `{config_dir}/{config_file}` |
| Modify frontend page | `{frontend_dir}/{pages_dir}/*.{ext}` |

---

## 3. Routes & Pages (Template)

| Path | File | Description |
|------|------|------|
| / | `{file_path}` | Homepage |
| /{path} | `{file_path}` | {description} |

---

## 4. Model Tier

**L0 — Haiku / atomic tier**: Pure file path lookup, zero reasoning required. Main model must not directly execute this skill — **must delegate to Haiku**.
