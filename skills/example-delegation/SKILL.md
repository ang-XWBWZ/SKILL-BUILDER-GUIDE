---
name: example-delegation
description: >-
  Delegation rules skill template. Used to guide creation of project-specific
  delegation rules. Defines which tasks must be delegated to Haiku,
  delegation format, and sub-agent output standards.
model_tier: L1
skill_tier: atomic
composes: []
composed_by:
  - meta: skill-builder-guide
context_budget:
  l1_metadata: 100
  l2_body: 1500
  l3_references: 3000
version: 1.1.0
status: active
review_by: 2026-07-28
trust_level: internal
requires_network: false
requires_file_write: false
compatibility: universal
allowed_tools: Agent Read Bash
evolution:
  usage_count: 0
  last_corrections: []
  stale_markers: []
---

# Delegation Rules Skill Template

> **Position**: Atomic tier / L1 execution tier — a **reference template** for other projects to create project-level delegation rules. Composed by [skill-builder-guide](../skill-builder-guide/SKILL.md) (meta).
>
> **Full implementation**: See [delegation](../delegation/SKILL.md) (planning tier) for this project's actual delegation skill.
>
> **Deep reference**: See [references/upgrade-strategy.md](references/upgrade-strategy.md) for upgrade strategy details.

## Trigger Conditions

- Creating delegation rules skill / Defining L0 task delegation rules
- Asking "should this task be delegated"
- Need delegation rules template reference

## Related Skills

- [Delegation](../delegation/SKILL.md) — actual planning-tier delegation skill used by this project
- [Dev Standards](../example-dev/SKILL.md) — L0 info lookup scenarios
- [Code Map](../example-code-map/SKILL.md) — L0 file location scenarios [L0]

---

## 1. Mandatory Delegation Principle

**Main model must not execute L0 tasks.** All L0 tasks must be delegated via `Agent(model: "haiku")`.

## 2. L0 Task Catalog

| Category | Example Tasks | Target Skill |
|------|---------|---------|
| File lookup | Find file location, directory structure | code-map |
| Info lookup | Check version number, API routes | dev |
| Command execution | Deploy, package, service start/stop | scripts |
| Static tracing | Draw dataflow diagram, verify API list | code-map / dev |
| Mechanical edit | Rename variable, update version number | (direct) |

## 3. Standard Delegation Format

```
Agent(
  description: "3-5 word task description",
  model: "haiku",
  prompt: """
    【Task】What specifically to do
    【Files】List of paths to read
    【Output】Conclusion/Basis/Uncertainty format
  """
)
```

## 4. Sub-Agent Output Format

```
Conclusion:   One sentence answering the assigned goal
Basis:        Specific evidence, observations, reasoning path
Uncertainty:  Risks, missing information, failure modes (write "None" if none)
```

Main model does only three things after receiving: extract conclusions → identify conflicts → decide.

## 5. Upgrade / Fallback Strategy

| Trigger | Threshold | Action |
|---------|------|------|
| User repeatedly unsatisfied | Same task ≥2 correction rounds failed | Package context, submit to top-tier model |
| Work rework | Same code repeatedly modified, problem not converging | Stop modifying, re-analyze root cause |

**Upgrade info package**: Original requirements + attempted solutions and failure reasons + current blockers + excluded assumptions.

See [references/upgrade-strategy.md](references/upgrade-strategy.md).

## 6. Model Tier

**L1 — Sonnet / atomic tier**: Rule interpretation and orchestration, requires reasoning. This skill is a template reference. See [delegation](../delegation/SKILL.md) for actual execution.
