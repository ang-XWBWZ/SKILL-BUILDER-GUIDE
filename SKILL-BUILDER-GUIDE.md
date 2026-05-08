# Agent Skills Creation Guide v2.1 — Live

Methodology and execution pipeline for creating Claude Code project-specific skill systems.

> **Purpose**: Guides creation of project-specific skills. Template reference in `skills/`. Quick start: [docs/quick-start.md](docs/quick-start.md).

---

## Contents

1. [Five-Phase Execution Pipeline](#1-five-phase-execution-pipeline) ← action spine for skill creation
2. [Dual-Axis Model](#2-dual-axis-model)
3. [Directory Structure & Deployment Paths](#3-directory-structure--deployment-paths)
4. [Core Specs Quick Reference](#4-core-specs-quick-reference)
5. [Skill Template Quick Reference](#5-skill-template-quick-reference)
6. [Model Tier Routing](#6-model-tier-routing)
7. [CLAUDE.md Integration](#7-claudemd-integration)
8. [H-ADMC Decomposition Criteria](#8-h-admc-decomposition-criteria)
9. [Sub-Agent Output Standards](#9-sub-agent-output-standards)
10. [Validation Protocol](#10-validation-protocol)
11. [Delegation Engine](#11-delegation-engine)
12. [Script Directory](#12-script-directory)
13. [Maintenance & Evolution](#13-maintenance--evolution)
14. [Packaging & Distribution](#14-packaging--distribution)
**Appendix**: [Template Index](#appendix-template-index) · [Skill Quick Select](#appendix-skill-quick-select) · [Practice Quick Reference](#appendix-practice-quick-reference)

---

## 1. Five-Phase Execution Pipeline

The single execution path for skill creation. Each phase has an explicit executor, input, output, and gate.

```
Phase 1: ANALYZE ──→ Phase 2: SCAN ──→ Phase 3: GENERATE ──→ Phase 4: VALIDATE ──→ Phase 5: CONFIRM
    (L1-Sonnet)        (L0-Haiku)         (L1-Sonnet)           (L0-Haiku)            (L1-Sonnet)
         │                  │                   │                    │                     │
    Skill plan        Code samples        Skill files          Validation report     approved/revise
```

### Phase 1: ANALYZE — Project Analysis

- **Executor**: Sonnet (L1)
- **Output**: `{ skill_plan: [{ name, skill_tier, model_tier, reason }] }`

Analyze project type, tech stack, module structure, team size → determine skill count (2-6) and type combination. Default model tiers:

| Skill Type | Execution | Composition |
|---------|:--:|:--:|
| Standards (dev) | L1 | atomic |
| Code Map (code-map) | **L0** | atomic |
| Workflow (workflow) | L1 | functional |
| Scripts (scripts) | L0 | atomic |
| Call-Chain (call-chain) | L1 | functional |
| Change Model (change-model) | L1 | functional |
| Delegation (delegation) | L1 | planning |

> **Gate**: Phase 1 must pause after completion. Wait for user confirmation of the skill plan. Do NOT proceed to Phase 2 without approval.

### Phase 2: SCAN — Code Scanning

- **Executor**: Haiku (L0) — **must delegate**
- **Output**: Code samples per layer with key pattern identification

| Layer | Scan Target | Record |
|------|---------|--------|
| API Layer | Route declarations, param validation, response wrapping | `{method}`, `{class/function name}` |
| Service Layer | Abstract interfaces, consistency management, param conversion | `{yes/no}`, `{method}` |
| Data Layer | ORM approach, query organization, pagination | `{framework}`, `{method}` |
| Integration Layer | Remote calls, message queues, scheduled tasks | `{list}`, `{config}` |

### Phase 3: GENERATE — Generate Skill Files

- **Executor**: Sonnet (L1)
- **Output**: `.claude/skills/{name}/SKILL.md` + `.claude/skills/{name}/agents/openai.yaml` (default auto-load path; use `skills/{name}/` for template projects)

Hard rules (all mandatory):
1. Fill frontmatter completely per §4, including dual-axis fields
2. Extract trigger words from project code (5-15, covering action + query types)
3. Fill actual version numbers from scan — **no placeholders allowed**
4. Use actual scanned code snippets (sanitized)
5. Cross-reference related skills with relative paths
6. SKILL.md body ≤5000 tokens

Generated skills default to concise, accurate **English** content.

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
| V2 Structure | Dual-axis consistent, composition graph closed, budget within limits |
| V3 Semantic | File paths ≥95%, method names ≥90%, version numbers 100% |

Skills below this standard must not be published.

### Phase 5: CONFIRM — User Confirmation

- **Executor**: Sonnet (L1)
- **Output**: `approved` | `revise({feedback})` | `reject`

Confirm: version numbers correct, standard patterns match expectations, compatibility patterns accurately explained, user docs merged (user docs take precedence).

---

## 2. Dual-Axis Model

Every skill is defined on **two independent dimensions**. The axes are orthogonal — decisions on one do not replace decisions on the other.

| | Execution Axis (model_tier) | Composition Axis (skill_tier) |
|--|-------------------|---------------------|
| **Question** | Who executes? | Where in the composition graph? |
| **Decision basis** | Cognitive load | Dependencies & abstraction level |
| **Values** | L0 / L1 / L2 / L3 | meta / planning / functional / atomic |

**Execution axis**: L0=Haiku mechanical · L1=Sonnet bounded implementation · L2=Sonnet/Opus multi-step reasoning · L3=Opus architectural decisions

**Composition axis**: meta=creates skills · planning=task decomposition & routing · functional=reusable multi-step routines · atomic=single information source

> atomic+L0 = pure lookup (Haiku executes); functional+L1 = multi-step reasoning (Sonnet executes)

### Skill Count Decision

| Project Profile | Count | Skill Combo |
|---------|:--:|---------|
| Small (bug fixes) | 2 | standards + workflow |
| Medium (new pages) | 3 | + code-map |
| Large (new modules) | 4 | + change-model |
| Complex (multi-service) | 5-6 | + call-chain + scripts + delegation |

---

## 3. Directory Structure & Deployment Paths

### Production Projects (Recommended — Auto-Loaded)

```
{project}/.claude/skills/{skill-name}/    ← Claude Code auto-injects
├── SKILL.md              # L2: Core instruction body (≤5000 tokens)
├── agents/
│   └── openai.yaml       # L1: Trigger config
├── references/           # L3: Deep reference, loaded on demand
├── scripts/              # L4: Executable scripts (zero tokens in context)
└── assets/               # Static resources
```

### Template/Methodology Projects (Not Auto-Loaded)

```
{project}/skills/{skill-name}/           ← Requires explicit CLAUDE.md routing
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/
└── assets/
```

### Path Selection

| Path | Use Case | Auto-Load | Slash Cmd |
|------|---------|:---:|:---:|
| `.claude/skills/` | Production project skills | ✅ | ✅ |
| `skills/` | Template/methodology projects | ❌ | ❌ |
| `~/.claude/skills/` | Global cross-project skills | ✅ | ✅ |

> Production projects must use `.claude/skills/`. `skills/` is for template projects only.

### Naming Convention

| Rule | Correct | Wrong |
|------|------|------|
| Project prefix | `myproject-dev` | `dev` |
| Hyphen separator | `myproject-change-workflow` | `myproject_change_workflow` |
| All lowercase | `myproject-dev` | `Myproject-Dev` |
| Dir = skill name | `myproject-dev/` | `dev/` |

---

## 4. Core Specs Quick Reference

### 4.1 Frontmatter (Required for SKILL.md)

```yaml
---
name: [skill-name]                        # Required: matches directory name
description: [30-50 words, purpose + trigger] # Required
model_tier: L0|L1|L2|L3                   # Required: execution axis
skill_tier: meta|planning|functional|atomic # Required: composition axis
status: active                            # draft|active|deprecated|superseded
review_by: [YYYY-MM-DD]                   # Suggested review date
context_budget:                           # Required
  l1_metadata: 120
  l2_body: 5000
  l3_references: 20000
version: 1.0.0
---
```

### 4.2 openai.yaml (Required)

```yaml
skill: [skill-name]                       # Matches directory name
description: [one-liner, matches SKILL.md]
triggers:                                 # Required: 5-15 trigger words
  - [action trigger 1]
  - [query trigger 2]
```

Trigger rules: 5-15 items, 2-8 words each, cover action type (create/modify/query/build) + query type (where/which/how/locate). Avoid semantic duplicates and overly generic terms.

### 4.3 Required SKILL.md Sections

**Trigger Conditions** (required) — List all trigger scenarios (5-10), distinguish action vs. query triggers.

**Related Skills** (required) — Reference 2-3 related skills, ordered upstream→downstream, using relative paths.

Optional sections: Project architecture, tech stack, directory structure, component inventory, page routes, workflow overview, checklists, report templates — choose based on skill type.

---

## 5. Skill Template Quick Reference

Each skill type needs only frontmatter + required section skeleton. Full templates in corresponding `skills/` directories.

### Standards (dev) — L1 / atomic

```yaml
name: {project}-dev
description: {Project} development standards. Triggered when asking about tech stack, code standards, API conventions.
model_tier: L1
skill_tier: atomic
```
Required sections: Tech stack (version numbers from code scan), layered architecture, code standards, API conventions, config & environment
Reference: [skills/example-dev/](skills/example-dev/)

### Code Map (code-map) — L0 / atomic

```yaml
name: {project}-code-map
description: {Project} code map. Triggered when asking about file locations, directory structure, component positions.
model_tier: L0
skill_tier: atomic
```
Required sections: Directory structure, route mapping, component inventory
Reference: [skills/example-code-map/](skills/example-code-map/)

### Workflow (workflow) — L1 / functional

```yaml
name: {project}-change-workflow
description: {Project} development workflow. Triggered when describing dev requirements or asking about dev steps.
model_tier: L1
skill_tier: functional
```
Required sections: Workflow overview (phase→input→steps→output), checklists

### Change Model (change-model) — L1 / functional

```yaml
name: {project}-change-model
description: Change report skill. Triggered when generating change reports, recording changes, or checking call chains.
model_tier: L1
skill_tier: functional
```
Required sections: WHY/WHAT/HOW/VALIDATION four-layer architecture, call-chain check template, archive path
Reference: [skills/change-model/](skills/change-model/) · Quick start: [docs/quick-start.md](docs/quick-start.md)

### Call-Chain (call-chain) — L1 / functional

```yaml
name: {project}-call-chain
description: {Project} call-chain checking. Triggered when tracing API call chains, checking data flow, or verifying type matching.
model_tier: L1
skill_tier: functional
```
Required sections: Call-chain tracing method, data type checking, final-call checklist

### Scripts (scripts) — L0 / atomic

```yaml
name: {project}-scripts
description: {Project} script tools. Triggered when running maintenance scripts or batch operations.
model_tier: L0
skill_tier: atomic
```
Required sections: Script inventory table, execution flow, output report (JSON) format, error handling

### Delegation (delegation) — L1 / planning

```yaml
name: {project}-delegation
description: Task decomposition & model routing. Triggered when needing delegation, task breakdown, or model dispatch.
model_tier: L1
skill_tier: planning
```
Required sections: 6 decomposition criteria, model tier routing table, 3 delegation patterns, output standards
Reference: [skills/delegation/](skills/delegation/)

---

## 6. Model Tier Routing

### Tier Framework

| Tier | Cognitive Load | Model | Typical Tasks |
|:----:|---------|---------|---------|
| **L0** | None (mechanical) | Haiku | File lookup, info query, command execution |
| **L1** | Low-Medium | Sonnet | Single-module changes, narrow search |
| **L2** | Medium-High | Sonnet/Opus | Root cause diagnosis, cross-module implementation |
| **L3** | High | Opus | Architectural decisions, security audits |

### Mandatory Delegation Rule

**L0 tasks must be executed by lightweight models. Main model must not directly handle L0 tasks. One violation ≈ 5-15x token cost.**

| Task Category | Example | Delegate To |
|---------|------|---------|
| File lookup | "Where is the entry file" | L0 Haiku |
| Info query | "What framework version" | L0 Haiku |
| Command exec | "Run deploy script" | L0 Haiku |
| Static tracing | "Draw dataflow diagram" | L0 Haiku |
| Mechanical edit | "Update version number" | L0 Haiku |

Exception: Inline single-file reads as context for downstream reasoning may be done directly by the main model.

### Upgrade / Fallback

| Trigger | Threshold | Action |
|---------|------|------|
| User repeatedly unsatisfied | ≥2 correction rounds failed | Package context, upgrade model |
| Work rework | Same code ≥3 modifications, not converging | Stop, re-analyze root cause |
| Problem not converging | 3 rounds without narrowing scope | Upgrade to re-diagnose |

---

## 7. CLAUDE.md Integration

CLAUDE.md is the root entry point for the skill system. Its role depends on where skills are stored:

| Skill Path | Routing Table | Notes |
|-------------|:--:|------|
| `.claude/skills/` | **Optional** | Skills auto-loaded, routing table is documentation only |
| `skills/` | **Required** | Only trigger path |

### Version A: Skills in `.claude/skills/` (Recommended)

```markdown
# {Project Name}

## Mandatory Delegation Rules (Highest Priority)

> One violation ≈ 5-15x token cost. Main model must not execute L0 tasks.
> All file ops, script execution, format conversion must delegate to Haiku.

## Available Skills

> Auto-loaded from `.claude/skills/`, supports `/skill-name` invocation.

| Skill | Execution | Composition | Purpose |
|------|:------:|:------:|------|
| `{project}-dev` | L1 | atomic | Tech stack, standards |
| `{project}-code-map` | **L0** | atomic | File location [delegate to Haiku] |
| `{project}-change-model` | L1 | functional | Change reports, call-chain checks |
```

### Version B: Skills in `skills/` (Explicit Routing Required)

```markdown
# {Project Name}

## Mandatory Delegation Rules (Highest Priority)

> Main model must not execute L0 tasks.

| Category | Criterion | Example |
|------|---------|------|
| File lookup | Purpose is path retrieval | "Where is the entry file" |
| Info query | Purpose is a definite value | "Framework version" |
| Command exec | Fixed steps, no branching | "One-click deploy" |

## Skill Routing Table (Required — skills/ not auto-loaded)

| Skill | Execution | Composition | Trigger Scenario |
|------|:------:|:------:|----------|
| [dev](skills/{project}-dev/) | L1 | atomic | Tech stack, code standards |
| [code-map](skills/{project}-code-map/) | **L0** | atomic | File location [delegate to Haiku] |
```

---

## 8. H-ADMC Decomposition Criteria

**H** = Decompose → **A** = Assign → **D** = Execute → **M** = Merge → **C** = Check

Main model orchestrates. Sub-models execute. L0 must be delegated.

### Six Decomposition Criteria

If ANY criterion is met, decomposition is mandatory:

1. **Multiple sub-goals** — task contains >1 distinct goal
2. **Mixed operation types** — requires both analysis and generation
3. **Cannot close in one pass** — cannot complete + verify in one pass
4. **Risk isolation** — independent verification reduces overall risk
5. **Parallel opportunity** — sub-tasks can run concurrently
6. **L0 sub-tasks present** — non-trivial tasks almost always contain L0 work

### Sub-Agent Constraint Template

Every dispatched sub-agent prompt must include:

```
Constraints:
1. Goal is fixed — do not redefine or expand it
2. State assumptions explicitly
3. Do the minimum necessary work
4. Produce verifiable output, not completion claims
5. Report uncertainty when evidence is incomplete
6. Use structured output format
```

Non-convergence handling: Do not repeat execution. Return to decomposition layer, change task structure, re-decompose and re-dispatch.

---

## 9. Sub-Agent Output Standards

All dispatched sub-agents must return in this structured format. Free-form narration is forbidden:

```
Conclusion: (One sentence answering the assigned goal)
Basis: (Specific evidence, observations, reasoning path)
Uncertainty: (Risks, missing info, failure modes; write "None" if none)
```

Main agent integration: extract conclusions → identify conflicts → advance decision. Main agent must not perform local reasoning on behalf of sub-agents.

Standard dispatch format:

```
Agent(
  description: "3-5 word task description",
  model: "haiku",
  prompt: """
    【Task】What specifically to do
    【Files】List of paths to read
    【Output】Return in Conclusion/Basis/Uncertainty format
  """
)
```

---

## 10. Validation Protocol

### Validation Commands

```bash
# Format + structure validation (supports both paths)
python scripts/validate-skills.py .claude/skills/{skill-name}
python scripts/validate-skills.py skills/{skill-name}

# Semantic validation
python scripts/validate-skills.py .claude/skills/{skill-name} --semantic
```

### Acceptance Criteria (Hard)

| Declaration Type | Verification Method | Pass Rate |
|---------|---------|:---:|
| File paths | Glob/Read to confirm existence | ≥95% |
| Method names | Grep source code to confirm | ≥90% |
| Version numbers | Read dependency config files | 100% |
| API routes | Read route config to confirm | ≥90% |

Below standard = must not publish. Agent must code-level fact-check every acceptance item — verify each declaration with tools, not by trusting document content.

### Periodic Verification

| Timing | Scope |
|------|---------|
| At creation | All declarations |
| After refactor | Affected skills |
| Quarterly | All skills |

---

## 11. Delegation Engine

The delegation skill is a meta-skill managing main/sub model division of labor. It does not participate directly in business development.

```
skills/delegation/
├── SKILL.md                    # Decomposition principles, model routing, patterns, output standards
├── agents/
│   └── openai.yaml             # Triggers: delegation, task breakdown, model dispatch, L0, H-ADMC
└── references/
```

Core triggers: delegation, task breakdown, model dispatch, model tier, L0 tasks, dispatch to Haiku, sub-agent, H-ADMC

Deployment: Global delegation skill in `~/.claude/skills/delegation/`. Project-level rules in CLAUDE.md mandatory block. Dual-layer combination recommended.

---

## 12. Script Directory

Skills may include executable scripts for automating repetitive operations:

```
.claude/skills/{skill-name}/scripts/     # or skills/{skill-name}/scripts/
├── deploy.sh
└── health-check.sh
```

Script execution rules:
- Executed by L0 sub-model (Haiku)
- Output structured results (JSON or Conclusion/Basis/Uncertainty)
- **Never** inline script content in SKILL.md (reference path only)

Use cases: verify declarations, manage environments, package & distribute, automated testing.

---

## 13. Maintenance & Evolution

### When to Update

| Scenario | Update |
|------|---------|
| Tech stack change | Standards skill, code-map skill |
| New module added | Code-map skill |
| Workflow optimization | Workflow skill |
| Systematic errors found | Related skills |

Update flow: detect change → assess impact → update skills → validate → commit

### Lifecycle

```
draft → active → deprecated → (removed)
                  ↓
             superseded → point to replacement
```

Status in frontmatter `status` field. Superseded skills use `supersededBy` to point to replacement.

### Quarterly Health Check

- [ ] Tech stack still current
- [ ] Directory structure matches reality
- [ ] Trigger words still match user intent
- [ ] Workflow still covers dev scenarios
- [ ] Model tier annotations correct
- [ ] Declarations pass code-level verification

---

## 14. Packaging & Distribution

### Path Summary

| Path | Purpose | Auto-Load |
|------|------|:---:|
| `{project}/.claude/skills/` | Production project skills | ✅ |
| `{project}/skills/` | Template/methodology reference | ❌ |
| `~/.claude/skills/` | Global cross-project skills | ✅ |
| `~/.claude/skills-dist/` | Zip archive repository | — |

### Install Commands

```bash
# Package
zip -r my-skill.zip my-skill/

# Install globally
python scripts/zip_extract.py my-skill.zip ~/.claude/skills/ my-skill

# Install to project (production)
cp -r my-skill/ {project}/.claude/skills/my-skill/
```

---

## Appendix: Template Index

| Template | Tier | Reference |
|------|:----:|---------|
| Standards (dev) | L1 / atomic | `skills/example-dev/` · §5 |
| Code Map (code-map) | **L0** / atomic | `skills/example-code-map/` · §5 |
| Workflow (workflow) | L1 / functional | Main guide §8.3 template |
| Change Model (change-model) | L1 / functional | `skills/change-model/` · §5 · `docs/quick-start.md` |
| Call-Chain (call-chain) | L1 / functional | §5 · Main guide §8.4 template |
| Scripts (scripts) | L0 / atomic | §5 · Main guide §8.5 template |
| Delegation (delegation) | L1 / planning | `skills/delegation/` · §11 |
| CLAUDE.md | — | §7 |

---

## Appendix: Skill Quick Select

| Project Profile | Recommended Combo |
|---------|-------------|
| Simple frontend | standards + workflow |
| Complex frontend | standards + code-map + workflow |
| Simple backend | standards + workflow + scripts |
| Complex backend | standards + workflow + scripts + call-chain |
| Full-stack | standards + code-map + workflow + change-model + delegation |
| Microservices | standards + workflow + call-chain + change-model + delegation |

| Scenario | Recommended Skills |
|------|----------|
| New hire onboarding | code-map + workflow |
| Daily development | standards + code-map |
| Change release | change-model + call-chain |
| Issue investigation | call-chain + standards |

---

## Appendix: Practice Quick Reference

### Import Steps for Existing Projects

```
① Analyze → ② Gap analysis → ③ Create skills → ④ Validate & iterate
```

1. Analyze: Identify project type, tech stack, module structure, team size
2. Gap: Check against quick-select table, inspect `.claude/skills/` and `skills/`
3. Create: Choose deployment path per §3 (production→`.claude/skills/`), generate per §5 templates
4. Validate: Test slash commands + natural language triggers, invite team trial

### Conflict Resolution

When multiple skill triggers overlap: project-specific > generic · `required` > `recommended` · exact match > broad match · `active` > `deprecated`

### Version Management

Semantic Versioning: MAJOR.MINOR.PATCH. Commit: `feat|fix|docs(skills): {description}`

### Security Red Lines

- Code examples in skill files must be sanitized (IPs, passwords, tokens → placeholders)
- Reference project skills (e.g. `skills/example-dev/`) must not contain original project sensitive info
- Main model L2+ must not directly execute L0 tasks
