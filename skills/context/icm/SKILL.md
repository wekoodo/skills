---
name: icm
description: "Use when building, auditing, or maintaining a folder-based agent context architecture (Interpretable Context Methodology / ICM) — AGENTS.md/CLAUDE.md entrypoints, CONTEXT.md routing, numbered stage pipelines OR numbered reference libraries (rosters), references, working artifacts, and review gates. Use when a project wants portable, model/harness-agnostic, plain-markdown agent context instead of monolithic prompts, and whenever structure should be kept ICM-compliant as it grows. Certifies layer properties rather than filenames: when another installed skill pack owns an overlapping path (e.g. a domain-glossary CONTEXT.md or a process pack's plan tree), ICM defers to that structure and audits in coexistence mode."
license: MIT
metadata:
  author: wekoodo
  version: "1.1"
  based_on: "Jake Van Clief, David McDermott, Eduba (University of Edinburgh) — Interpretable Context Methodology, arXiv:2603.16021"
  paper: "https://arxiv.org/abs/2603.16021"
---

# Interpretable Context Methodology

Method from Jake Van Clief, David McDermott, and Eduba (University of Edinburgh). This skill packages operational guidance for agents; it does not claim authorship of ICM itself. See [Attribution](#attribution).

## Core Idea

Use folder structure as agent architecture. A project should tell agents where they are, where to go, what to do at one step, which stable references constrain behavior, and which working artifacts to transform. This is an *ongoing* discipline — build the structure once, then keep it compliant as the project grows.

Keep the system plain-text and harness-agnostic. Use scripts for deterministic mechanical work; use Markdown contracts for judgment, synthesis, routing, and review.

Read [icm-patterns.md](references/icm-patterns.md) for layer definitions, the two valid Layer-2/3 shapes, folder templates, fit criteria, token budgets, contract examples, and the validation checklist.

## Two valid shapes (read this before auditing)

ICM as published describes a **sequential stage pipeline**. But the same five layers support a second, equally valid shape, and confusing them is the most common audit error:

- **Stage pipeline** — a `stages/` directory of numbered, sequential contracts (`01_research/` → `02_draft/`). Layer 2 = stage contracts. Use for sequential, reviewable, repeatable workflows.
- **Reference library (roster)** — a directory of numbered `NN-name/` members each with a `CONTEXT.md` (e.g. `advisors/01-financial-planner/`). **A library is Layer 3 reference material, not a broken pipeline.** A controlling stage *selects from* it per run; the members are not executed in sequence.

A project may have a pipeline, a library, both, or neither. **A numbered folder is not automatically a stage.** If its members are personas/specialists/domains selected by topic rather than run in order, it is a Layer-3 library — do not flag the absence of `stages/`.

> Example: a live "board meeting" system is pure ICM. Layer 2 is the *meeting lifecycle* (intake → deliberation → minutes). Layer 3 is the *advisor roster library*, selected per topic. Layer 4 is the per-meeting artifacts. The conversational feel of deliberation is an execution-style choice, not an architectural violation.

## Coexistence and deferral

ICM certifies **properties** — the five layers, stable/working separation, a reviewable control surface — not filenames. Other installed skill packs may own the same paths under different contracts: a domain-modeling pack may own root `CONTEXT.md` as a term **glossary**; a process pack may own multi-step execution under its own tree (e.g. `docs/superpowers/plans/` and `specs/`). When another pack clearly owns a path's role, **defer**: map ICM layers onto the existing structure and add only what is missing. Never rewrite a path's role to fit ICM's preferred names.

Classify by **content shape first**, pack fingerprints second (conventions drift; content is what the file actually is). Installed-skill lists are a supporting clue for you during Explore, not something the audit script can see:

- **Router-shaped** `CONTEXT.md`/`CONTEXT-MAP.md` — task tables, layer/path pointers, "where do I go" → Layer 1.
- **Glossary-shaped** `CONTEXT.md` — `## Language`, `**Term**:` definitions, `_Avoid_:` notes, no routing → Layer 3 domain language. A multi-glossary `CONTEXT-MAP.md` (bounded-context index with links to per-context glossaries) → Layer 3 index.
- **Hybrid** (both in one file) — say so and propose a split; do not silently pick a side.
- **Foreign plan/spec tree in active use** → the project's control surface (Layer 4 working, or declared product under `docs/`).

State the detected mode before proposing changes: `icm-native`, `coexist-glossary`, `coexist-process`, or `coexist-mixed`.

Deferral rules:

1. **Never convert a glossary-shaped `CONTEXT.md` into a router (or the reverse) without explicit user approval.** These are the destructive failure modes coexistence exists to prevent.
2. When root `CONTEXT.md` is glossary-owned, put Layer-1 routing at — in order of preference — `docs/agents/routing.md`; a `## Task routing` section in `AGENTS.md`; root `TASK-MAP.md`. Do **not** use `CONTEXT-MAP.md` as the escape hatch: glossary packs use that name for multi-glossary indexes (same homonym trap).
3. Do not add `stages/` when another pack already owns multi-step execution — its plans, specs, or tickets are the control point. Build an ICM pipeline only when the user asks for one.
4. Treat foreign stable artifacts (glossaries, `docs/adr/`, `docs/agents/*`) as Layer 3. Never rename, delete, or "clean up" them to fit ICM.
5. Preserve existing `AGENTS.md`/`CLAUDE.md` content, including other packs' setup blocks; update the canonical file in place, never append duplicate routing blocks.
6. Ephemeral outputs some packs deliberately keep out of the workspace (e.g. handoffs to OS temp) stay out; do not force them into in-repo `handoffs/`.

Greenfield, or no foreign ownership detected: keep the paper-aligned layout (root `CONTEXT.md` router, optional `stages/`). See [icm-patterns.md](references/icm-patterns.md) § Coexistence Profiles for the mapping table; the audit script performs the same shape classification and reports the mode.

## Workflow

### 1. Explore existing context

- Read root `AGENTS.md`, `CLAUDE.md`, `README.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/agents/`, `handoffs/`, `_config/`, `.cursor/rules`, `.github/copilot-instructions.md`, and local scripts only as relevant.
- Classify any root `CONTEXT.md`/`CONTEXT-MAP.md` by content shape **before** treating it as a Layer 1 router, and check for foreign plan/spec trees — see [Coexistence and deferral](#coexistence-and-deferral). Detect foreign ownership before proposing any rename or restructure.
- Identify the canonical Layer-0 entrypoint. If a tool-specific file is only a shim (e.g. `CLAUDE.md` importing `AGENTS.md`), preserve the shim and edit the canonical file.
- Notice ignored/generated projection directories (`.claude/`, `.codex/`, `.agents/`). Do not duplicate canonical content into them — they are re-installable tooling, not workspace content.

### 2. Check fit and identify the shape

- Sequential, repeatable, human-reviewed-per-step work → **stage pipeline**.
- A roster of roles/specialists/domains selected by topic → **reference library**.
- Durable context but no workflow yet → Layers 0–1 (+3) only; add a pipeline or library later.
- Prefer conventional code for real-time multi-agent messaging, high concurrency, or automated mid-pipeline branching on model output.

### 3. Map the context layers

- **Layer 0** — root identity + harness routing (`AGENTS.md`, `CLAUDE.md`).
- **Layer 1** — workspace routing (`CONTEXT.md`/`CONTEXT-MAP.md`): which stage handles a task, what shared resources exist.
- **Layer 2** — the control point: stage contracts (`Inputs`/`Process`/`Outputs`, optional `Verify`), OR a controlling stage that selects Layer-3 library members per run. The Inputs table names exact files *and the relevant sections*.
- **Layer 3** — stable reference material (`_config/`, `references/`, `shared/`): conventions, domain frameworks, and **roster libraries**. Large reference collections may carry their own `CONTEXT.md` router (recursive Layer-1 routing).
- **Layer 4** — per-run working artifacts (`output/`, `meetings/`, `handoffs/`, generated `.md`/`.json`).

### 4. Design files and folders

- Make each stage (or library member) one job / one role with one clear contract.
- Number folders to encode order (pipeline) or stable identity (library). Treat numbers as stable IDs: never renumber survivors after a deletion; leave the gap and scrub cross-references.
- In every contract, list exact Layer-3 and Layer-4 inputs. Avoid whole-repo reads when a scoped list is possible.
- Keep instructions and intermediate artifacts in Markdown/JSON/YAML/plain text.
- Put deterministic mechanical work in local scripts; keep semantic decisions in Markdown contracts.
- Keep a stage's delivered context small (the paper's target: ~2–8k tokens; Layers 0–2 ≈ 1.3–1.6k). If a step needs far more, re-scope its Inputs.

### 5. Edit conservatively

- Preserve existing repo guidance and user terminology.
- Update the canonical router instead of appending duplicate routing blocks.
- Separate factory from product: stable rules/rosters → Layer 3; per-run outputs → Layer 4.
- Persist durable memory as files **inside** the workspace (Layer 3 for stable facts, Layer 4 for evolving state), not in harness-private user-level stores, so the project stays portable.
- Treat repeated output edits as diagnostic: if the same fix recurs, change the contract or reference source, not the output.

### 6. Validate

- Run `python <skill>/scripts/audit_routed_context.py <project-root>`. It recognizes pipelines, reference libraries, recursive routing, and Layer-4 areas; a complete library-only project audits clean. It classifies router- vs glossary-shaped context files and reports the coexistence mode — a foreign-owned but property-complete repo audits clean, an honest gap (e.g. glossary owns `CONTEXT.md` and no alternate router exists) is a warning.
- Manually check: each stage has reviewable output, a scoped input list, no irrelevant context loading, and no hidden dependency on one model or harness.
- If the project keeps project-specific ICM decisions in a committed reference file (e.g. `_config/shared/icm-conventions.md`), audit against it too.

## Deliverable shape

Prefer a small changed set:

- `AGENTS.md`/`CLAUDE.md` (Layer 0), `CONTEXT.md`/`CONTEXT-MAP.md` (Layer 1).
- `stages/NN_slug/CONTEXT.md` + `output/` for pipelines, OR `NN-name/CONTEXT.md` library members for rosters.
- `references/`, `_config/`, `shared/` for stable reference material; a committed conventions file for project-specific ICM decisions.
- Local scripts only when they replace repeated deterministic work.

## Attribution

Interpretable Context Methodology (ICM) was introduced by **Jake Van Clief**, **David McDermott**, and **Eduba** (University of Edinburgh, USA) in:

> Jake Van Clief, David McDermott, Eduba. *Interpretable Context Methodology.* arXiv:2603.16021.  
> https://arxiv.org/abs/2603.16021 · [PDF](https://arxiv.org/pdf/2603.16021)

This skill is a practical packaging of that methodology for coding agents (workflow, audit checklist, and scripts). Credit for the method belongs to the paper authors. Extensions here (e.g. treating numbered roster libraries as Layer 3) are operational guidance built on top of their work — not a rebrand of it.
