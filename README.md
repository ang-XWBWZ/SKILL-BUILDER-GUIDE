# Skill Builder Guide

> **Agent-Native Skill Architecture v2.0** — From human-readable docs to agent-executable architecture

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What Is This?

**Skill Builder Guide** is a system of guides, templates, and tools for building AI Agent Skills. Redesigned as an **agent-executable architecture** based on five key 2026 principles (Progressive Disclosure / SkillX / MCE / SSL / Context-as-Budget).

### Three Core Concepts

| # | Concept | One-Liner |
|:--:|------|--------|
| 1 | **Dual-Axis Model** | Every skill is defined on both the execution axis (L0-L3, who executes) and composition axis (meta/planning/functional/atomic, what layer) |
| 2 | **Four-Layer Progressive Disclosure** | L1 metadata always loaded → L2 instruction body loaded on trigger → L3 references loaded on demand → L4 scripts execute with zero tokens in context |
| 3 | **Three-State Evolution** | Runtime signal collection (~10t per task) → Offline Haiku scan analysis → User manually triggers skill rebirth |

---

## Architecture Overview

```
CLAUDE.md (~500t)              ← Router, not an encyclopedia
  │
  ├─ delegation [planning, L1] ← Orchestration hub
  │   └─ composes: change-model + example-dev + example-code-map
  │
  ├─ skill-builder-guide [meta, L1] ← Meta-skill: creates other skills
  │   └─ composes: delegation + change-model + all atomic
  │
  ├─ change-model [functional, L1] ← Change reports WHY/WHAT/HOW/VALIDATION
  │   └─ composes: example-dev + example-code-map
  │
  ├─ example-dev [atomic, L1]     ← Tech stack / standards
  ├─ example-code-map [atomic, L0] ← File location (must delegate to Haiku)
  └─ example-delegation [atomic, L1] ← Delegation template

Each skill:
  SKILL.md          ← L2: Core instruction body (≤5000 tokens)
  agents/openai.yaml ← L1: Trigger metadata
  references/        ← L3: Deep reference (loaded on demand)
  scripts/           ← L4: Executable scripts (zero tokens in context)
```

---

## Quick Start

> 5-minute intro: [docs/quick-start.md](docs/quick-start.md)

### Create Project-Specific Skills

```
In Claude Code:
"Create a skill system for my {project name} project"
```

skill-builder-guide (meta) executes the five-phase pipeline automatically: analyze project → scan code (L0 Haiku) → generate skills → validate → confirm.

### Run Skill Health Checks

```bash
python scripts/check-skill-health.py skills/     # Tier 2 offline scan
python scripts/validate-skills.py skills/        # V1+V2 format+structure validation
```

---

## Project Structure

```
SKILL-BUILDER-GUIDE/
├── CLAUDE.md                       ← Minimal routing table (~500 tokens)
├── README.md                       ← This file
├── SKILL-BUILDER-GUIDE.md          ← Core guide (human reference, 14 chapters)
│
├── docs/
│   ├── quick-start.md              ← 5-minute intro
│   └── changes/                    ← Change report archive
│
├── skills/                         ← Skill system (6 skills)
│   ├── delegation/                 ← [planning] Delegation hub
│   ├── skill-builder-guide/        ← [meta] Skill creation pipeline
│   ├── change-model/               ← [functional] Change reports
│   ├── example-dev/                ← [atomic, L1] Dev standards template
│   ├── example-code-map/           ← [atomic, L0] Code map template
│   ├── example-delegation/         ← [atomic, L1] Delegation rules template
│   └── README.md                   ← Skill index + composition graph
│
├── templates/                      ← Reusable templates
│   ├── skill-template.md
│   ├── change-model-template.md
│   └── openai-template.yaml
│
├── scripts/                        ← Tool scripts
│   ├── validate-skills.py          ← V1+V2 format+structure validation
│   ├── check-skill-health.py       ← Tier 2 health scan
│   └── package-skill.py            ← Skill packaging
│
└── workflows/
    └── validate.yml                ← CI: auto validation
```

---

## Skill Dual-Axis Quick Reference

| Skill | Execution | Composition | Purpose |
|------|:------:|:------:|------|
| delegation | L1 | planning | Task decomposition, model routing, sub-agent orchestration |
| skill-builder-guide | L1 | meta | Five-phase skill creation pipeline |
| change-model | L1 | functional | WHY/WHAT/HOW/VALIDATION change reports |
| example-dev | L1 | atomic | Tech stack standards, layered architecture, naming conventions |
| example-code-map | **L0** | atomic | File location, directory structure (**delegate to Haiku**) |
| example-delegation | L1 | atomic | Delegation rules template, dispatch format |

---

## Roadmap

- [x] Dual-axis model (model_tier × skill_tier)
- [x] Four-layer progressive disclosure (L1→L2→L3→L4)
- [x] CLAUDE.md minimalism (3000t → 500t)
- [x] skill-builder-guide meta-skill pipeline (five phases)
- [x] Three-state skill evolution (Tier 1 signal collection → Tier 2 offline scan → Tier 3 rebirth pipeline)
- [x] V1+V2 skill validation + health checks
- [ ] V3 semantic validation (code-level fact checking, coming soon)
- [ ] Skill auto-generation CLI tool
- [ ] Multi-agent framework support

---

## Contribute

```bash
# Validate all skills
python scripts/validate-skills.py skills/

# Health check
python scripts/check-skill-health.py skills/

# Package for distribution
python scripts/package-skill.py skills/skill-builder-guide
```

---

## License

MIT
