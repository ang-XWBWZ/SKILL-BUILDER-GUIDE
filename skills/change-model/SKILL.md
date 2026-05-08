---
name: change-model
description: >-
  Change Model skill template. Transforms code changes into structured change reports
  (WHY/WHAT/HOW/VALIDATION four-layer architecture), with call-chain checking, archival storage,
  and automatic Git analysis. Triggered when generating change reports, DiffLogs, Release Notes,
  or archiving change records.
model_tier: L1
skill_tier: functional
composes:
  - atomic: example-dev
  - atomic: example-code-map
composed_by:
  - planning: delegation
  - meta: skill-builder-guide
context_budget:
  l1_metadata: 125
  l2_body: 5000
  l3_references: 12000
version: 1.2.0
status: active
review_by: 2026-07-28
trust_level: internal
requires_network: false
requires_file_write: true
compatibility: requires git, python3
allowed_tools: Bash Read Write Edit Grep Glob
evolution:
  usage_count: 0
  last_corrections: []
  stale_markers: []
---

# Change Model — Change Model Skill Template

> **Positioning**: Functional tier skill — provides a structured change-report methodology (WHY/WHAT/HOW/VALIDATION), guiding the full workflow from requirements analysis through archival storage.
>
> **Composition**: This skill orchestrates [code-map](../example-code-map/SKILL.md) (L0 file location) and [dev](../example-dev/SKILL.md) (L1 spec lookup). It is orchestrated by [delegation](../delegation/SKILL.md) (planning tier).
>
> **Deep References**: See [references/archive-design.md](references/archive-design.md) for the archival system design; [references/archive-workflow.md](references/archive-workflow.md) for the archival workflow; [references/git-analysis.md](references/git-analysis.md) for automatic Git analysis.

## Trigger Conditions

- Generate change report / DiffLog / Release Notes
- Analyze changes from Git history / generate report from commits
- Archive change records / change archive / historical change query
- User asks "how to write a change report" / "how to archive changes"
- Create project-specific change-report skills
- Need call-chain checking methodology

## Related Skills

- [Skill Builder Guide](../skill-builder-guide/SKILL.md) — meta tier skill creation
- [Dev Specs](../example-dev/SKILL.md) — atomic tier tech stack info
- [Code Map](../example-code-map/SKILL.md) — atomic tier file location [L0]
- Reference implementation scripts in `scripts/` directory

---

## 1. Skill Overview

### 1.1 What Is Change Model

Change Model transforms raw code diffs into a four-layer structured document:

```
┌─────────────────────────────────────┐
│  Layer 1: WHY — Change Context & Requirements   │
│  ├─ 1. Change Background                        │
│  └─ 2. Requirements Analysis                    │
├─────────────────────────────────────┤
│  Layer 2: WHAT — Impact & Risk                 │
│  ├─ 3. Impact Analysis                          │
│  └─ 4. Risk Assessment                          │
├─────────────────────────────────────┤
│  Layer 3: HOW — Design & Implementation        │
│  ├─ 5. Design Approach                          │
│  └─ 6. Implementation Mapping                   │
├─────────────────────────────────────┤
│  Layer 4: VALIDATION — Verification & Delivery  │
│  ├─ 7. Call-Chain Check (pre-test)              │
│  ├─ 8. Test Verification                        │
│  └─ 9. Delivery & Rollback                      │
└─────────────────────────────────────┘
```

### 1.2 Problems Solved

| Problem | Change Model Solution |
|------|-------------------|
| Diff fragmentation | Organize by causal chain, not by file listing |
| Lack of behavioral abstraction | Make "condition → result" decision logic explicit |
| Hard for newcomers to understand | Four-layer structure: background → requirements → design → verification |
| AI cannot infer intent | Structured, machine-readable section design |
| Changes cannot be traced | Archival system: date-based archiving + INDEX.md index |
| Missing historical reports | Git analysis: auto-generate report skeleton from commit history |

### 1.3 Distinction from Changelog Skills

| Dimension | Change Model (change-model) | Changelog (diffs) |
|------|------------------------|-------------------|
| **Perspective** | Forward-looking: designed before changes occur | Retrospective: recorded after changes occur |
| **Granularity** | One report per requirement/task | One entry per commit/PR |
| **Content** | WHY→WHAT→HOW→VALIDATION complete causal chain | What changed, why it changed |
| **Timing** | Complete design before coding, complete verification before testing | Auto/manual recording after commit |
| **Purpose** | Guide development, risk control | History tracking, retrospective audit |

---

## 2. Layer 1: WHY — Change Context & Requirements

### 2.1 Change Background

```markdown
| Element | Description |
|------|------|
| **Requirement Source** | {requester/ticket number} |
| **Trigger Reason** | {why this change is needed} |
| **Desired Goal** | {what effect the change should achieve} |
```

**Fill-in Guidelines**: Source must be specific and traceable / Reason must clarify "what the problem is" / Goal must be verifiable.

### 2.2 Requirements Analysis

```
Input: {input params}

Judgment conditions:
- {condition 1} → {result 1}
- {condition 2} → {result 2}

Output: {output params}
```

**Fill-in Guidelines**: Use "condition → result" format / Cover all business branches / Specify inputs and outputs explicitly.

---

## 3. Layer 2: WHAT — Impact & Risk

### 3.1 Impact Analysis

```markdown
| Dimension | Impact Description | Impact Level |
|------|----------|:--------:|
| **Upstream Callers** | {description} | None/Low/Med/High |
| **Downstream Dependencies** | {description} | None/Low/Med/High |
| **Database** | {tables involved} | — |
```

### 3.2 Risk Assessment

```markdown
| Risk Item | Level | Description | Mitigation |
|--------|:----:|------|----------|
| {risk name} | L0/L1/L2/L3 | {description} | {mitigation} |
```

**Risk Level Definitions**:

| Level | Definition | Example |
|:----:|------|------|
| L0 | No external impact | Internal refactor, log optimization |
| L1 | Internal API change | New optional parameter, internal interface adjustment |
| L2 | External contract change | Interface signature change, response format change |
| L3 | Data/state migration | Database migration, config change |

---

## 4. Layer 3: HOW — Design & Implementation

### 4.1 Call Chain

```
{Caller}
  │ {Request method} {endpoint path}
  ▼
Interface Layer ({entry component})
  │ {business layer method}
  ▼
Business Layer ({business component})
  │ {business logic description}
  ▼
Data Layer ({data component})
  │ {query/persistence description}
  ▼
Database
```

### 4.2 Implementation Mapping

```markdown
#### Changed File List

| # | Operation | File Path | Change Description |
|:----:|:----:|----------|----------|
| 1 | ⭐/✏️ | `{path}` | {description} |
```

---

## 5. Call-Chain Checking Methodology

### 5.1 Core Objectives

| Objective | Description |
|------|------|
| Chain completeness | No breaks from entry point to endpoint |
| Type matching | Data types correctly passed at each link |
| Final call | SQL/API/message etc. final operation is correct |

### 5.2 Checking Procedure

```
Step 1: Identify the entry point
  ├─ API endpoint / page event / scheduled task / message consumption
  └─ Record input parameter types and validation rules

Step 2: Trace intermediate links
  ├─ Interface layer → Business layer → Data layer
  ├─ Record method signatures and return types at each link
  └─ Check whether types match

Step 3: Verify the final call
  ├─ SQL statement / external API / message queue / cache write
  └─ Check whether parameters are passed correctly

Step 4: Error handling check
  ├─ Are exceptions caught?
  └─ Are errors returned correctly?
```

### 5.3 Checklist

| # | Check Item | What to Check | Verification Method |
|:-:|--------|----------|----------|
| 1 | Entry parameters | Parameter types, required-field validation | Inspect interface definition |
| 2 | Parameter passing | Are parameters passed correctly across layers? | Trace the method call chain |
| 3 | Type matching | Do input/output types match at each layer? | Compare type definitions |
| 4 | Null handling | Do optional fields have default values? | Inspect code logic |
| 5 | Final call | Are SQL/API/message parameters correct? | Inspect final implementation |
| 6 | Return handling | Is the return value assembled correctly? | Inspect return path |
| 7 | Exception handling | Are exceptions caught? | Inspect try-catch |
| 8 | Degradation logic | Is there a fallback on failure? | Inspect fallback |

### 5.4 When to Check

| Phase | Execute? | Notes |
|------|:--------:|------|
| After requirements analysis | ❌ | Not yet implemented |
| After coding | ✅ | **Must execute** |
| Before testing | ✅ | Ensure chain is correct before testing |
| Before launch | ✅ | Final verification |

### 5.5 Call-Chain Check Template

```markdown
### 7. Call-Chain Check

| Check Item | Status | Notes |
|--------|:----:|------|
| Entry validation | ✅/❌ | Parameter validation correct |
| Type check | ✅/❌ | Data types match |
| Final call | ✅/❌ | SQL/API call correct |

**Data Flow Verification**:
{Entry}
  → {Intermediate link 1}
  → {Intermediate link 2}
  → {Final call}
```

**Pass Condition**: All check items must be ✅.

---

## 6. Generating a Project-Specific Skill

### 6.1 Customization Items

| Customization | Description |
|--------|------|
| Section add/remove | Add or remove sections as needed for the project |
| Risk levels | Adjust L0-L3 definitions to fit the project |
| Template format | Markdown / JSON / YAML |
| Trigger words | Project-specific change-related vocabulary |

### 6.2 Merging User Documentation

If the user provides an existing change report template or spec document, **the user's document takes precedence**:

```
1. Read the change report template/spec provided by the user
2. Compare differences with this text template
3. Use the user's document as the baseline; supplement missing parts with this methodology
4. Record differences for user confirmation
```

| Difference Type | Handling |
|----------|----------|
| User template has unique sections | Keep user sections, mark as project customization |
| User template is missing a layer | Suggest adding it (e.g., missing VALIDATION) |
| User has different risk level definitions | Use user's definitions |
| User uses different terminology | Keep user's terminology |

---

## 7. Archival System

### 7.1 Main Flow

```
Coding complete → Call-chain check → Test verification → Generate final report → 📦 Archive
```

### 7.2 Directory Structure

```
docs/changes/
├── INDEX.md              # Master index (dual-dimension: by time / by type)
├── 2026-04-26/
│   ├── 20260426-01-add-filter-feature.md
│   └── 20260426-02-fix-login-timeout.md
└── 2026-04-27/
    └── 20260427-01-refactor-payment-module.md
```

### 7.3 Archive Validation Checklist

- [ ] Report includes complete four-layer structure (WHY / WHAT / HOW / VALIDATION)
- [ ] All call-chain check items are ✅
- [ ] Referenced file paths have been verified against actual code
- [ ] Rollback plan is explicit and executable
- [ ] No sensitive information

### 7.4 Reference Scripts

```bash
# Git history analysis → generate report skeleton
python skills/change-model/scripts/generate-git-report.py \
  --range "HEAD~3..HEAD" --title "Add filter feature" --type feature --archive

# Manual report archival
python skills/change-model/scripts/archive-report.py \
  path/to/report.md --title "Add filter feature" --type feature --scope api
```

**See** [references/archive-design.md](references/archive-design.md) **for archive system design**.
**See** [references/archive-workflow.md](references/archive-workflow.md) **for archive workflow**.
**See** [references/git-analysis.md](references/git-analysis.md) **for Git automatic analysis**.

---

## 8. Model Tier

**L1 — Sonnet / functional tier**: Requires understanding change semantics, organizing causal chains, and generating structured documents. File lookups are delegated to L0 — Haiku.
