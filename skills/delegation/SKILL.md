---
name: delegation
description: >-
  Decomposition-driven skill. Defines the principles and methods for task decomposition, model tier routing, and sub-task dispatch.
  Trigger when decomposing complex tasks, determining model tiers, or dispatching sub-agents.
model_tier: L1
skill_tier: planning
composes:
  - functional: change-model
  - atomic: example-dev
  - atomic: example-code-map
composed_by:
  - meta: skill-builder-guide
context_budget:
  l1_metadata: 105
  l2_body: 3200
  l3_references: 6000
version: 1.1.0
status: active
review_by: 2026-07-28
trust_level: internal
requires_network: false
requires_file_write: false
compatibility: universal
allowed_tools: Agent Bash Read Grep Glob
evolution:
  usage_count: 0
  last_corrections: []
  stale_markers: []
---

# Delegation Driver — Task Decomposition and Model Routing

> **Positioning**: Planning tier skill — does not directly execute business tasks; instead determines how tasks should be decomposed, routed to which model, and dispatched to sub-agents.
>
> **Composition**: This skill orchestrates [code-map](../example-code-map/SKILL.md) and [dev](../example-dev/SKILL.md) as L0 information-gathering atomic skills.
>
> **Template Reference**: When creating delegation skills for other projects, reference [example-delegation](../example-delegation/SKILL.md).
>
> **In-Depth Reference**: For upgrade strategy details, see [references/upgrade-escalation.md](references/upgrade-escalation.md).

## Trigger Conditions

- Task contains multiple sub-goals
- Requires determining model tier (L0/L1/L2/L3)
- Requires decomposing complex tasks and dispatching sub-agents
- Questions about "should I delegate", "which model to use", "how to decompose tasks"
- Mixed operation types (analysis + implementation, implementation + verification)

## Related Skills

- [Skill Builder Guide](../skill-builder-guide/SKILL.md) — meta tier skill creation
- [Change Model](../change-model/SKILL.md) — functional tier change driver
- [Delegation Rule Template](../example-delegation/SKILL.md) — atomic tier reference

---

## I. Core Principles

```
Main Model (high capability)
  ├── Decompose → Route → Dispatch
  ├── Integrate → Conflict Detection → Re-decide
  └── Does NOT execute L0 work
        │
        ├─ L0 Sub-model (lightweight): read, search, run, verify
        ├─ L1 Sub-model (standard): bounded implementation, narrow search
        └─ L2+ Handled by main model itself
```

**Three Governing Rules**:
1. Main model orchestrates, sub-models execute
2. L0 tasks are delegated by default
3. One sub-task, one goal, one verification

---

## II. Dual-Axis Classification

Each task is evaluated on **two independent axes**:

| | Execution Axis (model_tier) | Composition Axis (skill_tier) |
|--|-----------------------------|-------------------------------|
| **Question** | Who executes? | Where does it sit in the composition graph? |
| **Decision Criterion** | Cognitive load | Dependency relationships |
| **Value Domain** | L0 / L1 / L2 / L3 | meta / planning / functional / atomic |

### Execution Axis: Model Tier Routing

| Tier | Complexity | Recommended Model | What It Does | Delegation Advice |
|:----:|------------|--------------------|--------------|-------------------|
| **L0** | Execution-level | Haiku (lightweight) | File lookup, information retrieval, command execution, static tracing, mechanical edits | **Delegate by default** |
| **L1** | Bounded-level | Sonnet (standard) | Single-module changes, narrow-scope search, format fixes | On demand |
| **L2** | Reasoning-level | Sonnet/Opus | Multi-step planning, root cause diagnosis, cross-module changes, result integration | Main model handles |
| **L3** | Strategic-level | Opus | Architecture decisions, security audits, system redesign | Main model handles |

**Core Rationale for L0 Delegation**: L0 tasks are mechanical operations; main model execution consumes 5-15x tokens for equivalent results to the lightweight model.

### Composition Axis: Skill Tiers

| Tier | Responsibility | Skills in This System |
|------|---------------|-----------------------|
| **meta** | Creates other skills | skill-builder-guide |
| **planning** | Orchestration and routing | delegation |
| **functional** | Reusable multi-step sub-routines | change-model |
| **atomic** | Single tool / table lookup | dev, code-map, delegation-template |

---

## III. When to Decompose Tasks

Decomposition is recommended if **any** condition is met:

1. **Multiple sub-goals** — task contains more than one distinct goal
2. **Mixed operation types** — requires both analysis and generation, implementation and verification
3. **Cannot close the loop in a single pass** — cannot complete and verify within one pass
4. **Risk isolation** — independent verification reduces overall risk
5. **Parallelism opportunity** — sub-tasks can run concurrently
6. **Contains L0 work** — non-trivial tasks almost always include L0 work

**Cases NOT requiring decomposition**: single goal, single-pass closure, pure reasoning tasks (no file/command operations).

---

## IV. Sub-Task Design

Each sub-task satisfies:
- **One goal** — unambiguous, not multi-intent
- **Clear input** — file paths, search patterns, commands to execute
- **Expected output** — return in output specification format
- **Verification condition** — what counts as "done"
- **Minimal dependencies** — as independent and parallelizable as possible

### Design Comparison

| Bad (vague, multi-goal) | Good (clear, single-goal) |
|--------------------------|----------------------------|
| "Analyze the business layer and fix issues" | "Read {filename}, extract all public method signatures, output as a list" |
| "Check service health status" | "Check if backend process is running, database is reachable, API responds 200" |

---

## V. Common Delegation Patterns

### Pattern A: L0 Information Gathering (most common)

```
User Requirement
  │
Main Model (L2): Understand requirement, determine what information is needed
  ├── L0: Locate files         → code-map
  ├── L0: Look up tech specs   → dev
  ├── L0: Read existing code   → extract patterns
  └── Main Model: Integrate information, execute implementation
```

### Pattern B: Parallel L0 Batch

```
Main Model: Decompose into N independent checks
  ├── L0: Check A
  ├── L0: Check B
  ├── L0: Check C
  └── Main Model: Collect results, output summary
```

### Pattern C: Complex Investigation

```
Main Model (L2): Analyze problem, locate clues
  ├── L0: Read key code files
  ├── L0: Check git log change history
  └── Main Model: Synthesize evidence, diagnose root cause
```

---

## VI. Sub-Agent Output Specification

Each sub-agent returns a structured three-element response:

```
Conclusion:    One-sentence answer to the assigned goal
Basis:         Concrete evidence, observations, reasoning path
Uncertainty:   Risks, missing information, failure modes (write "None" if none)
```

After receiving, the main model only does three things:
1. Extract each sub-agent's conclusion
2. Identify conflicts or gaps
3. Decide: continue / re-decompose / complete

**The main model MUST NOT substitute sub-agent local reasoning.**

### Standard Dispatch Command Format

```
Agent(
  description: "3-5 word task description",
  model: "haiku",
  prompt: """
    【Task】What specifically to do
    【Files】List of file paths to read
    【Output Requirements】Return in Conclusion/Basis/Uncertainty format
  """
)
```

---

## VII. Upgrade Strategy

When the following occurs on the same task, **escalate to reasoning/top-tier model**:

| Trigger Condition | Threshold | Action |
|-------------------|-----------|--------|
| User repeatedly dissatisfied | Same task, ≥2 rounds of corrections not passing | Package context, submit to top-tier model |
| Rework loops | Same code section modified ≥3 times, issue not converging | Stop modifying, re-analyze root cause |
| Issue not converging | 3 rounds of conversation, issue scope still not narrowing | Escalate to higher-tier model for re-diagnosis |

**Escalation Information Package**: original requirements + attempted solutions with failure reasons + current blocker + eliminated hypotheses.

See [references/upgrade-escalation.md](references/upgrade-escalation.md) for details.

---

## VIII. Skill Evolution Signal Collection (Tier 1)

**At the end of every task, update the `evolution` field of the skills used**. This is a zero-reasoning-cost metadata update — no LLM invocation, no additional context loaded.

```
End of task:
  skill.evolution.usage_count += 1

  IF user made corrections:
    skill.evolution.last_corrections.append("YYYY-MM-DD: [one-liner]")
    (keep only the most recent 3)

  IF skill content found inconsistent with reality:
    skill.evolution.stale_markers.append("[one-liner]")
```

Tier 2 offline scanner (`scripts/check-skill-health.py`) periodically analyzes these signals. Tier 3 is triggered by the user explicitly invoking "optimize this skill" to enter the five-phase regeneration pipeline.

---

## IX. Model Tier

**L1 — Sonnet / planning tier**: Rule explanation and orchestration; must determine decomposition and routing strategy based on task characteristics.
