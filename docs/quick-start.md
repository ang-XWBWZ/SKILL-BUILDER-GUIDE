# 5-Minute Quick Start

AI Agent development workflow driven by **Change Model**.

---

## Core Concept

```
Traditional: Requirements → Code → Test → Deploy
                ↓
           Process is untraceable, changes hard to understand

Change Model: Requirements → WHY → WHAT → HOW → VALIDATION → Deploy
                    ↓      ↓      ↓       ↓
                 Context  Impact  Design  Verify (call-chain check)
                    ↓
              Structured change report, complete causal chain
```

---

## Quick Start

### Scenario: Add a "filter by condition" feature to your project

> **Reading note**: This is a **generic example demonstrating the Change Model workflow**. Replace `{placeholder}` with your project's actual content. Focus on understanding the **four-layer analysis method**, not copying the example text verbatim.

---

### Step 1: WHY — Change Context & Requirements (30s)

**AI Prompt**:

```
Use the change-model skill to analyze the following requirement:

Requirement: {your query endpoint} needs to support filtering by {your filter dimension}.
Currently, it only returns all results.
Goal: Add an optional {your filter parameter} to support {your value range} filtering.
Constraint: Behavior unchanged when {your filter parameter} is not passed. Maintain backward compatibility.
```

**Output**:

```markdown
## Change Context

| Element | Description |
|------|------|
| Requirement source | {requester} |
| Trigger reason | Cannot filter by {filter dimension} |
| Desired outcome | Support {filter parameter} filtering |

## Decision Logic

Input: {required_param} (required), {optional_param} (optional)

Conditions:
- {optional_param} has value → return matching results
- {optional_param} empty → return all results

Output: {result_list}
```

---

### Step 2: WHAT — Impact & Risk (30s)

**AI Prompt**:

```
Continue using change-model to analyze impact and risk
```

**Output**:

```markdown
## Impact Analysis

| Dimension | Impact Description | Severity |
|------|----------|:----:|
| Upstream callers | New optional parameter, behavior unchanged when omitted | None |
| Database | {table_name} read-only query | — |

## Risk Assessment

| Risk | Level | Description | Mitigation |
|--------|:----:|------|----------|
| Compatibility | L0 | New optional parameter | Verified behavior unchanged when omitted |
```

---

### Step 3: HOW — Design & Implementation (2 min)

**AI Prompt**:

```
Use {project}-dev skill to query project tech stack and standards
Use {project}-code-map skill to locate files that need modification

Then generate the call chain and change file checklist
```

**Output**:

```markdown
## Call Chain

Caller
  │ {method} {endpoint}?{required}=xxx[&{optional}=xxx]
  ▼
API Layer ({entry_component})
  │ Parameter validation → calls service layer
  ▼
Service Layer ({service_component})
  │ Business logic: append filter when {optional} has value
  ▼
Data Layer ({data_component})
  │ {query statement with optional condition}
  ▼
Database

## Change File Checklist

| # | Action | File Path | Change Description |
|:----:|:----:|----------|----------|
| 1 | ✏️ | `{input_definition_file}` | Add {optional} field |
| 2 | ✏️ | `{service_file}` | Append filter logic |
| 3 | ✏️ | `{data_file}` | Add optional query condition |
```

**Implementation** (pseudocode):

```
Input struct {
    {required}: {Type}   // Required, validated
    {optional}: {Type}   // Optional
}

ServiceMethod({Input} input):
    If input.{optional} is not empty:
        AppendFilter({optional})
    Return DataLayer.Query(input)
```

---

### Step 4: VALIDATION — Verify & Deliver (1 min)

**AI Prompt**:

```
Use change-model to perform call-chain check, then generate test cases
```

**Output**:

```markdown
## Call-Chain Check

| Check Item | Status | Description |
|--------|:----:|------|
| Entry validation | ✅ | {required} required validation active |
| Type check | ✅ | {optional} type matches, nullable |
| Final call | ✅ | Query conditions correctly assembled |

## Test Verification

| # | Scenario | Input | Expected | Result |
|:-:|------|------|----------|:---:|
| 1 | No optional param | {required}=xxx | Return all results | ✅ |
| 2 | With optional param | {required}=xxx&{optional}=yyy | Return matching only | ✅ |

## Rollback Plan

Remove the {optional} parameter code.
```

---

## What You Get

| Output | Value |
|------|------|
| **Change context doc** | Clear "why changed", traceable |
| **Impact/risk analysis** | Identify problems early, reduce risk |
| **Call chain diagram** | Newcomers quickly understand data flow |
| **Change file checklist** | See what changed at a glance |
| **Call-chain check** | Ensure correctness before testing |
| **Test cases** | Clear verification points, executable |
| **Rollback plan** | Fast recovery if issues arise |

---

## Skill Call Quick Reference

> **Note**: Each skill has two dimensions — **execution tier** (who executes, L0-L3) and **composition tier** (position in the skill graph, meta/planning/functional/atomic). The two axes are orthogonal. See project README for details.

| Phase | Skill | Execution | Composition | Purpose |
|------|----------|:------:|:------:|------|
| WHY | {project}-change-model | L1 | functional | Requirements analysis, decision logic |
| WHAT | {project}-change-model | L1 | functional | Impact analysis, risk assessment |
| HOW | {project}-dev | L1 | atomic | Tech stack, standards lookup |
| HOW | {project}-code-map | **L0** | atomic | File location [delegate to Haiku] |
| VALIDATION | {project}-change-model | L1 | functional | Call-chain check + change report |

---

## Next Steps

1. **Generate project-specific skills using the templates in this guide**

```
In Claude Code:
"Using the skills/example-dev/SKILL.md template structure, scan my project code
 and generate a project-specific {project}-dev development standards skill"

"Using the skills/example-code-map/SKILL.md template structure, analyze my project
 directory and generate a project-specific {project}-code-map code map skill"

"Using the skills/change-model/SKILL.md template structure, adapt to my project's
 tech stack and generate a project-specific {project}-change-model change report skill"
```

2. **Generate skills to `.claude/skills/` (auto-loaded)**

> Skills generated to `.claude/skills/` are auto-discovered by Claude Code and support `/skill-name` invocation.

3. **Create CLAUDE.md (optional — skills are already auto-loaded)**

With auto-loaded skills, CLAUDE.md only needs mandatory delegation rules and common commands. The skill index is documentation only:

```markdown
## Mandatory Delegation Rules

Main model must not execute L0 tasks. File operations must delegate to Haiku.

## Available Skills

> Auto-loaded from `.claude/skills/`, supports `/skill-name` invocation.

| Skill | Execution | Composition | Purpose |
|------|:------:|:------:|------|
| {project}-dev | L1 | atomic | Dev standards, coding style |
| {project}-code-map | **L0** | atomic | File location [delegate to Haiku] |
| {project}-change-model | L1 | functional | Change reports, call-chain checks |
```

4. **Start using**

```
Use {project}-change-model to analyze the following requirement: {your requirement description}
```

---

## FAQ

### Q: Why do call-chain checks before testing?

Testing only verifies "correctness of expected inputs". Call-chain checking verifies "data flow integrity". If the chain is broken or types don't match, tests won't even run.

### Q: Why delegate L0 tasks to Haiku?

L0 tasks are mechanical operations (file lookup, info query). Main model processing costs 5-15x more tokens for equivalent results. Delegating to Haiku saves cost.

### Q: What are change reports useful for?

1. **Newcomer understanding** — Quickly understand "why changed, what changed"
2. **Rollback reference** — Know what to remove if issues arise
3. **AI context** — AI understands historical change intent for future sessions
