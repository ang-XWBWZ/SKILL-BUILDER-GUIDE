# Skills — Skill System

This directory contains skill templates and methodology for guiding the creation of project-specific skills.

> **Position**: Skills in this directory are template references, not ready-to-use products. Use these templates to generate project-specific skills.

---

## Skill Inventory (Dual-Axis)

| Skill | Execution Tier | Composition Tier | Purpose |
|------|:------:|:------:|------|
| [delegation](delegation/) | L1 | **planning** | Task decomposition, model routing, sub-agent orchestration |
| [skill-builder-guide](skill-builder-guide/) | L1 | **meta** | Skill creation pipeline (Analyze→Scan→Generate→Validate→Confirm) |
| [change-model](change-model/) | L1 | **functional** | Change reports, call-chain checks, archive |
| [example-dev](example-dev/) | L1 | atomic | Dev standards, layered architecture, naming conventions |
| [example-code-map](example-code-map/) | **L0** | atomic | File location, directory structure, route mapping |
| [example-delegation](example-delegation/) | L1 | atomic | Delegation rule template, dispatch format |

> **planning tier**: All task entry points go through delegation for decomposition and routing decisions.
> **meta tier**: skill-builder-guide's output is not code, but **new skill files**.
> **L0 marked**: Must be executed by Haiku — main model must not call directly.

---

## Dual-Axis Model

Each skill is defined on two independent axes:

| | Execution Axis (model_tier) | Composition Axis (skill_tier) |
|--|-------------------|---------------------|
| **Question** | Who executes? | Where in the composition graph? |
| **Decision basis** | Cognitive load | Dependencies and abstraction level |
| **Values** | L0 / L1 / L2 / L3 | meta / planning / functional / atomic |

The two axes are orthogonal. Example: code-map is atomic + L0 (pure lookup, Haiku executes), change-model is functional + L1 (multi-step reasoning, Sonnet executes).

---

## Composition Graph

```
skill-builder-guide [meta]
  ├─→ delegation [planning]
  ├─→ change-model [functional]
  ├─→ example-dev [atomic]
  ├─→ example-code-map [atomic]
  └─→ example-delegation [atomic]

delegation [planning]
  ├─→ change-model [functional]
  ├─→ example-dev [atomic]
  └─→ example-code-map [atomic]

change-model [functional]
  ├─→ example-dev [atomic]
  └─→ example-code-map [atomic]
```

---

## Generating Project-Specific Skills

```
User request → skill-builder-guide [meta]
  ├─ Phase 1: ANALYZE — Analyze project, determine skill plan
  ├─ Phase 2: SCAN — Dispatch Haiku to scan code [L0]
  ├─ Phase 3: GENERATE — Generate SKILL.md + openai.yaml from templates
  ├─ Phase 4: VALIDATE — Run validation scripts [L0]
  └─ Phase 5: CONFIRM — User confirmation
```

---

## Directory Structure

```
skills/{skill-name}/
├── SKILL.md              # L2: Core instruction body (≤5000 tokens)
├── agents/
│   └── openai.yaml       # L1: Trigger configuration
├── references/           # L3: Deep reference (loaded on demand)
├── scripts/              # L4: Executable scripts (zero tokens in context)
└── assets/               # Static resources
```
