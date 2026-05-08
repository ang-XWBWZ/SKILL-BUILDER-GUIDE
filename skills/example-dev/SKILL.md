---
name: example-dev
description: >-
  Development Standards skill template. Guides creation of project-specific
  development standards skills. Triggers on questions about tech stack, API
  conventions, code standards, coding style, or layered architecture.
model_tier: L1
skill_tier: atomic
composes: []
composed_by:
  - functional: change-model
  - planning: delegation
  - meta: skill-builder-guide
context_budget:
  l1_metadata: 110
  l2_body: 3500
  l3_references: 8000
version: 1.1.0
status: active
review_by: 2026-07-28
trust_level: internal
requires_network: false
requires_file_write: false
compatibility: universal
allowed_tools: Read Grep Glob
evolution:
  usage_count: 0
  last_corrections: []
  stale_markers: []
---

# Development Standards Skill Template

> **Positioning**: Atomic tier skill — provides an **information lookup table** for tech stack, layered architecture, and naming conventions. Orchestrated by [change-model](../change-model/SKILL.md) (functional), [delegation](../delegation/SKILL.md) (planning), and [skill-builder-guide](../skill-builder-guide/SKILL.md) (meta).
>
> **Usage**: AI scans project code → extracts standard patterns per layer → follows this template structure → generates a project-specific development standards skill.
>
> **Further reference**: See [references/code-scanning-guide.md](references/code-scanning-guide.md) for detailed code scanning methods.

## Trigger Conditions

- Create a development standards skill / ask how to write tech stack or code standards
- Ask about coding style, naming conventions / layered code standard guidance
- Need standard pattern recognition methods / ask about dependency versions

## Related Skills

- [Code Map](../example-code-map/SKILL.md) — file location methodology [L0]
- [Change Model](../change-model/SKILL.md) — change report generation
- [Delegation](../example-delegation/SKILL.md) — model tier delegation rules

---

## 1. Tech Stack

> AI scans project dependency configuration files and extracts the actual tech stack in use.

| Category | Technology | Version | Description |
|----------|------------|---------|-------------|
| Language | {language} | {version} | Runtime environment |
| Framework | {framework} | {version} | Core framework |
| Database | {database} | {version} | Storage engine |
| Cache | {cache component} | {version} | Cache middleware |
| Message Queue | {MQ} | {version} | Async messaging |

---

## 2. Code Layering Standards

### 2.1 Layered Architecture (General Model)

```
┌─────────────────────────────────────────────────────────┐
│  Interface Layer (API / Entry Layer)                     │
│  ├─ Request parameter validation & format conversion     │
│  ├─ Unified response wrapper                             │
│  └─ Error handling & exception translation               │
├─────────────────────────────────────────────────────────┤
│  Business Layer (Business Logic Layer)                   │
│  ├─ Core business logic                                  │
│  ├─ Transaction / consistency management                 │
│  ├─ Data assembly & transformation                       │
│  └─ External service orchestration                       │
├─────────────────────────────────────────────────────────┤
│  Data Layer (Data Access Layer)                          │
│  ├─ Persistence operations                               │
│  ├─ Query construction                                   │
│  └─ Cache operations                                     │
├─────────────────────────────────────────────────────────┤
│  Integration Layer (optional, per project reality)       │
│  ├─ Remote service calls                                 │
│  ├─ Message queue processing                             │
│  ├─ Scheduled tasks                                      │
│  └─ Third-party SDK wrappers                             │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Layer Responsibility Boundaries

| Layer | Responsibility | Prohibited |
|-------|---------------|------------|
| **Interface Layer** | Parameter validation, format conversion, unified response | Business logic, direct database access |
| **Business Layer** | Business logic, consistency management, data assembly | Direct request/response handling, inline query strings |
| **Data Layer** | Persistence operations, query construction | Business logic decisions |
| **Integration Layer** | Cross-service calls, async message processing | Core business logic implementation |

### 2.3 Layer Identification Method

> AI scans project files and records the actual layering situation.

| Identification Item | Record Format |
|---------------------|---------------|
| Interface layer directory | `{directory name}` |
| Interface layer naming | `{naming pattern}` |
| Business layer directory | `{directory name}` |
| Business layer naming | `{naming pattern}` |
| Data layer directory | `{directory name}` |
| Data layer naming | `{naming pattern}` |
| Integration layer directory | `{directory name}` |

---

## 3. Standard Pattern Recognition

### 3.1 Interface Layer Standard Patterns

| Check Item | Scan Target | Record Format |
|------------|-------------|---------------|
| Route declaration | Routing configuration method | `{annotation / config file / function}` |
| Parameter validation | Validation approach | `{declarative / manual / middleware}` |
| Response wrapper | Unified response structure | `{class name or function name}` |
| Error handling | Error handling approach | `{global / local}` |

```
Interface layer file structure:
Declare route & HTTP method → dependency-inject business components → each handler method:
    ├─ Parameter validation
    ├─ Call business layer
    └─ Return unified response format
```

### 3.2 Business Layer Standard Patterns

| Check Item | Scan Target | Record Format |
|------------|-------------|---------------|
| Interface definition | Whether abstract interface exists | `{yes / no}` |
| Consistency management | Transaction declaration method | `{annotation / manual / framework-managed}` |
| Parameter transformation | Model conversion approach | `{method}` |
| External calls | Cross-service call method | `{SDK / RPC / message}` |

```
Business layer file structure:
Declare business component → each business method:
    ├─ Transform parameters to internal model
    ├─ Business logic processing
    ├─ Consistency boundary declaration
    ├─ Call data layer / integration layer
    └─ Return result model
```

### 3.3 Data Layer Standard Patterns

| Check Item | Scan Target | Record Format |
|------------|-------------|---------------|
| ORM method | Persistence approach | `{ORM framework / raw queries / query builder}` |
| Query organization | Query storage method | `{annotation / separate file / inline}` |
| Pagination method | Pagination strategy | `{plugin / manual / framework built-in}` |

```
Data layer file structure:
Declare data access component → each data method:
    ├─ Build query conditions
    ├─ Parameterized query (injection prevention)
    ├─ Execute persistence operation
    └─ Return data model
```

### 3.4 Integration Layer Standard Patterns

| Check Item | Scan Target | Record Format |
|------------|-------------|---------------|
| Remote calls | Inter-service call method | `{method}` |
| Fault tolerance | Degradation / circuit-breaking strategy | `{yes / no}` |
| Timeout config | Timeout duration | `{default / custom}` |
| Message component | Message queue usage | `{producer / consumer / both}` |

---

## 4. Naming Conventions

### 4.1 File Naming

> AI extracts actual naming patterns from the project.

| Type | Naming Pattern | Example |
|------|---------------|---------|
| Interface layer files | `{pattern}` | `{example}` |
| Business layer files | `{pattern}` | `{example}` |
| Data layer files | `{pattern}` | `{example}` |
| Data model files | `{pattern}` | `{example}` |

### 4.2 Method Naming

| Operation Type | Naming Pattern | Example |
|---------------|---------------|---------|
| Single query | `{prefix}` + `{condition}` | `{example}` |
| List query | `{prefix}` + `{condition}` | `{example}` |
| Paginated query | `{prefix}` + `{condition}` | `{example}` |
| Create | `{prefix}` + `{target}` | `{example}` |
| Update | `{prefix}` + `{target}` | `{example}` |
| Delete | `{prefix}` + `{target}` | `{example}` |

### 4.3 Variable Naming

| Type | Naming Rule |
|------|-------------|
| Constants | ALL_CAPS_UNDERSCORE / PascalCase |
| Member variables | camelCase / underscore-prefixed |
| Local variables | Semantically clear |
| Boolean variables | is / has / can prefix |

---

## 5. Compatibility Pattern Recognition

### 5.1 What to Record

> When scanning code, AI identifies patterns that differ from mainstream conventions but are preserved for historical reasons.

| Scenario | Example | Record Notes |
|----------|---------|--------------|
| Legacy format | Old API response format differs from new API | Preserve, annotate applicable scope |
| Special optimization | High-performance handling for specific scenarios | Preserve, record the reason |
| Business exception | Unique transaction handling in a certain module | Preserve, annotate applicable conditions |

See [references/code-scanning-guide.md](references/code-scanning-guide.md).

---

## 6. Coding Style Formation Process

```
① Project analysis → ② Code scanning (dispatch Haiku — L0) → ③ Style extraction
    → ④ Document generation → ⑤ User confirmation
```

**AI execution steps**:
1. Analyze project type and tech stack
2. Dispatch Haiku to scan code samples per layer (L0 task)
3. Extract standard patterns and compatibility patterns
4. Populate project-specific content following this template structure
5. Generate a project-specific development standards SKILL.md
6. User confirms or provides document adjustments

### 6.1 User Document Integration

If the user provides coding standard documents, **follow the user's documents**:

```
1. Read the coding standard documents provided by the user
2. Compare differences against scan results
3. Follow user documents as the authority, supplement with scan-discovered realities
4. Record discrepancies for user confirmation
```

See [references/code-scanning-guide.md](references/code-scanning-guide.md).

---

## 7. Model Tier

**L1 — Sonnet / atomic tier**: Contains reasoning work such as standard interpretation, code analysis, and style extraction. Scan subtasks are dispatched to L0 — Haiku.
