---
name: skill-builder-guide
description: >-
  AI Agent Skills creation methodology and execution pipeline. Triggered when
  creating skill systems for projects, generating project-specific skills,
  understanding skill templates, model delegation, or validating skill accuracy.
  This is a META skill — it creates other skills as its output.
model_tier: L1
skill_tier: meta
composes:
  - planning: delegation
  - functional: change-model
  - atomic: example-dev
  - atomic: example-code-map
  - atomic: example-delegation
composed_by: []
context_budget:
  l1_metadata: 120
  l2_body: 4000
  l3_references: 20000
version: 2.0.0
status: active
review_by: 2026-07-28
trust_level: internal
requires_network: false
requires_file_write: true
compatibility: requires git, python3, pyyaml
allowed_tools: Bash Read Write Edit Grep Glob Agent
evolution:
  usage_count: 0
  last_corrections: []
  stale_markers: []
---

# Skill Builder Guide — Meta-Skill for Skill Creation

> **Position**: **meta tier skill** — output is not business code, but **new skill files** (SKILL.md + openai.yaml).
>
> **Core capability**: Analyze target project → scan code to extract patterns → generate project-specific skills from templates → validate accuracy → user confirmation.
>
> **Composition**: Orchestrates [code-map](../example-code-map/SKILL.md), [dev](../example-dev/SKILL.md), [delegation](../example-delegation/SKILL.md) as atomic supports.
>
> **Full spec**: `SKILL-BUILDER-GUIDE.md` (project root) · Quick start: `docs/quick-start.md`

## Trigger Conditions

- Creating a skill system for a project
- "create skill" / "generate project-specific skill" / "skill template"
- "model tier" / "L0 delegation" / "skill validation"
- "skill packaging" / "skill directory" / "skill builder"
- "openai.yaml" / "frontmatter spec"

## Related Skills

- [Change Model](../change-model/SKILL.md) — functional tier change reports
- [Dev Standards](../example-dev/SKILL.md) — atomic tier standards template
- [Code Map](../example-code-map/SKILL.md) — atomic tier file location [L0]
- [Delegation Rules](../example-delegation/SKILL.md) — atomic tier delegation template

---

## 1. Skill System Architecture

Every skill is defined on **two independent dimensions**, orthogonal to each other:

| | Execution Axis (model_tier) | Composition Axis (skill_tier) |
|--|-------------------|---------------------|
| **Question** | Who executes? | Where in the composition graph? |
| **Values** | L0/L1/L2/L3 | meta/planning/functional/atomic |

**Execution axis**: L0=Haiku mechanical · L1=Sonnet bounded implementation · L2=Sonnet/Opus multi-step reasoning · L3=Opus architectural decisions

**Composition axis**: meta=creates skills · planning=task decomposition & routing · functional=reusable multi-step routines · atomic=single information source

> atomic+L0 = pure lookup (Haiku); functional+L1 = multi-step reasoning (Sonnet)

## 2. Skill Type Decision

| Project Profile | Count | Skill Combo |
|---------|:--:|---------|
| Small | 2 | standards + workflow |
| Medium | 3 | + code-map |
| Large | 4 | + change-model |
| Complex | 5-6 | + call-chain + scripts + delegation |

Default model tier quick reference:

| Skill Type | Execution | Composition |
|---------|:--:|:--:|
| Standards (dev) | L1 | atomic |
| Code Map (code-map) | **L0** | atomic |
| Workflow (workflow) | L1 | functional |
| Scripts (scripts) | **L0** | atomic |
| Call-Chain (call-chain) | L1 | functional |
| Change Model (change-model) | L1 | functional |
| Delegation (delegation) | L1 | planning |

Full selection matrix: [references/skill-types-catalog.md](references/skill-types-catalog.md).

---

## 3. Five-Phase Execution Pipeline

```
Phase 1: ANALYZE ──→ Phase 2: SCAN ──→ Phase 3: GENERATE ──→ Phase 4: VALIDATE ──→ Phase 5: CONFIRM
    (L1-Sonnet)        (L0-Haiku)         (L1-Sonnet)           (L0-Haiku)            (L1-Sonnet)
         │                  │                   │                    │                     │
    Skill plan        Code samples        Skill files         Validation report     approved/revise
```

### Phase 1: ANALYZE — Project Analysis

- **Executor**: Sonnet (L1)
- **Output**: `{ skill_plan: [{ name, skill_tier, model_tier, reason }] }`

Analyze project type, tech stack, module structure, team size. Output plan in Conclusion/Basis/Uncertainty format.

> **Gate**: Phase 1 must pause after completion. Wait for user confirmation of the skill plan. Do NOT proceed to Phase 2 without approval.

### Phase 2: SCAN — Code Scanning

- **Executor**: Haiku (L0) — **must delegate**
- **Output**: Code samples per layer

| Layer | Scan Target | Record |
|------|---------|--------|
| API Layer | Route declarations, param validation, response wrapping | `{method}`, `{class/function name}` |
| Service Layer | Abstract interfaces, consistency mgmt, param conversion | `{yes/no}`, `{method}` |
| Data Layer | ORM approach, query organization, pagination | `{framework}`, `{method}` |
| Integration Layer | Remote calls, message queues, scheduled tasks | `{list}`, `{config}` |

Detailed scan dimensions: [references/pipeline/phase-2-scan.md](references/pipeline/phase-2-scan.md).

### Phase 3: GENERATE — Generate Skill Files

- **Executor**: Sonnet (L1)
- **Output**: `SKILL.md` + `agents/openai.yaml` → default `.claude/skills/{name}/` (template projects use `skills/{name}/`)

Hard rules:
1. Fill frontmatter per [references/frontmatter-spec.md](references/frontmatter-spec.md), include dual-axis fields
2. Extract trigger words from project code (5-15, action + query)
3. Fill actual version numbers from scan — **no placeholders**
4. Use actual scanned code snippets (sanitized)
5. SKILL.md body ≤5000 tokens

Generated skills default to concise, accurate **English** content.

Detailed prompt template: [references/pipeline/phase-3-generate.md](references/pipeline/phase-3-generate.md).

### Phase 4: VALIDATE — Verify

- **Executor**: Haiku (L0) — **must delegate**

```bash
python scripts/validate-skills.py .claude/skills/{skill-name}
python scripts/validate-skills.py skills/{skill-name}
python scripts/validate-skills.py .claude/skills/{skill-name} --semantic
```

| Layer | Pass Condition |
|--------|---------|
| V1 Format | frontmatter complete, triggers ≥5, YAML valid |
| V2 Structure | Dual-axis consistent, composition graph closed |
| V3 Semantic | File paths ≥95%, method names ≥90%, version numbers 100% |

Below standard = must not publish. See [references/validation-protocol.md](references/validation-protocol.md).

### Phase 5: CONFIRM — User Confirmation

- **Executor**: Sonnet (L1)
- **Output**: `approved` | `revise({feedback})` | `reject`

Confirm: version numbers correct, standard patterns match expectations, compatibility patterns accurately explained, user docs merged (user docs take precedence).

---

## 4. Directory Structure

| Path | Use Case | Auto-Load | Slash Cmd |
|------|---------|:---:|:---:|
| `.claude/skills/{name}/` | Production project skills | ✅ | ✅ |
| `skills/{name}/` | Template/methodology reference | ❌ | ❌ |
| `~/.claude/skills/{name}/` | Global cross-project skills | ✅ | ✅ |

```
{skill-name}/
├── SKILL.md              # L2: Core instruction body (≤5000 tokens)
├── agents/
│   └── openai.yaml       # L1: Trigger config
├── references/           # L3: Deep reference, loaded on demand
├── scripts/              # L4: Executable scripts
└── assets/               # Static resources
```

CLAUDE.md integration: Routing table optional with `.claude/skills/`, required with `skills/`. Mandatory delegation rules always at top.

---

## 5. Core Spec Reference

| Spec | Reference File |
|------|---------|
| Full frontmatter fields | [references/frontmatter-spec.md](references/frontmatter-spec.md) |
| 8 skill type catalog | [references/skill-types-catalog.md](references/skill-types-catalog.md) |
| Validation protocol | [references/validation-protocol.md](references/validation-protocol.md) |
| Full creation workflow | `SKILL-BUILDER-GUIDE.md` |
| Packaging & distribution | `SKILL-BUILDER-GUIDE.md` §14 |
| Maintenance & lifecycle | `SKILL-BUILDER-GUIDE.md` §13 |

---

## 6. Model Tier

**L1 — Sonnet / meta tier**: Requires understanding project structure, extracting code patterns, generating structured skill docs from templates, iterating based on validation feedback. Scan sub-tasks delegate to L0 — Haiku.
