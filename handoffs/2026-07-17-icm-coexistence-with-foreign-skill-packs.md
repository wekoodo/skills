# Handoff: ICM coexistence with foreign skill packs

**Date:** 2026-07-17  
**Audience:** Original builder of the `icm` skill (`public/skills/context/icm/`)  
**Status:** Review complete; product direction decided; **no skill/audit changes implemented yet**  
**Workspace:** `wekoodo-ai-skills` → public pack `wekoodo/skills`

---

## Why this exists

Users sometimes install **ICM** alongside popular skill packs that encode similar ideas (durable docs, explicit process, less vibe chaos) but use **different contracts for the same filenames** — especially `CONTEXT.md`.

The product goal is:

> Ensure structure is still **ICM-certified** (layer properties, separation of concerns, reviewable control surface), but **defer to another skill-set’s structure and workflow** when that pack clearly owns the overall process — as long as the result still passes an (updated) ICM audit.

This handoff curates the comparative review, product decisions, and a recommended implementation approach so you can implement without re-deriving the research.

---

## Product decisions (locked)

| # | Question | Decision |
| --- | --- | --- |
| 1 | Deferral as product goal? | **Yes.** ICM certifies structure (properties). Foreign workflow skills may own filenames, process, and artifact locations. Do not force ICM’s preferred names when another pack already drives the workflow. |
| 2 | Layer-1 escape hatch when `CONTEXT.md` is claimed | **Implementer-recommended default** (see [Recommended design](#recommended-design-for-the-builder)): semantic detection + alternate Layer-1 locations; do **not** rename ICM’s preferred router away from `CONTEXT.md` for greenfield projects. |
| 3 | Audit sophistication | **Do what’s needed for the intended result:** docs-only is not enough. Audit must classify content and accept coexistence shapes so “passes ICM” is meaningful. |
| 4 | Superpowers-style specs/plans | **Allowed.** Treat their structure as valid Layer-4 (or explicitly documented product under `docs/`) without inventing `stages/` unless the user wants an ICM pipeline. |

---

## Packs reviewed

| Pack | URL / source | Role vs ICM |
| --- | --- | --- |
| **ICM (ours)** | `public/skills/context/icm/` — paper arXiv:2603.16021 | Folder-as-architecture: Layers 0–4, routers, stages/rosters, audit script |
| **mattpocock/skills** | https://www.skills.sh/mattpocock/skills · https://github.com/mattpocock/skills | Engineering practices: grill, domain language, TDD, tickets, implement |
| **obra/superpowers** | https://www.skills.sh/obra/superpowers · https://github.com/obra/superpowers | End-to-end process: brainstorm → plan → TDD → review → finish |

---

## Comparative map (what each owns)

| | **ICM** | **mattpocock/skills** | **obra/superpowers** |
| --- | --- | --- | --- |
| Primary job | Routed Markdown context architecture | Engineering discipline skills | Mandatory process skill chain |
| Root `CONTEXT.md` | **Layer 1 task router** (“where do I go?”) | **Ubiquitous-language glossary** only | Not a project contract |
| `CONTEXT-MAP.md` | Alternate **Layer 1** router name | Index of **multiple glossaries** (bounded contexts) | Unused as a contract |
| Multi-step work | Optional `stages/NN_*/CONTEXT.md` + `output/` | Specs/tickets via issue tracker | Skills + `docs/superpowers/specs/` + `docs/superpowers/plans/` |
| Handoffs | In-repo `handoffs/` (Layer 4) | `/handoff` → **OS temp**, not workspace | N/A (plans/specs in repo) |
| Layer 0 | Canonical `AGENTS.md` / shims | Setup writes `## Agent skills` → `docs/agents/*` | User instructions **override** skills |
| Auto-trigger intensity | On demand (build/audit/maintain) | Mix of user- and model-invoked | Very aggressive (`using-superpowers`) |

### Hard conflict (must solve)

**Same path, opposite contracts: `CONTEXT.md` / `CONTEXT-MAP.md`.**

Matt’s domain-modeling skill is explicit:

- `CONTEXT.md` is a **glossary and nothing else**
- No implementation details, not a router, not a scratch pad
- Format: `## Language`, `**Term**:`, `_Avoid_:` (see their `skills/engineering/domain-modeling/CONTEXT-FORMAT.md`)
- `/setup-matt-pocock-skills` scaffolds single-context root `CONTEXT.md` + `docs/adr/` (or multi-context via root `CONTEXT-MAP.md`)
- Consumer rules live in `docs/agents/domain.md`

ICM today:

- Root `CONTEXT.md` / `CONTEXT-MAP.md` = Layer 1 **workspace routing**
- Stage/library member `CONTEXT.md` = contracts (Inputs / Process / Outputs)
- Our pack’s own `public/CONTEXT.md` is a pure router (task table + layer map)

**Failure modes if we don’t defer:**

1. ICM audit/build on a Matt repo → “fix” glossary into a router → **destroys domain language**.
2. Matt domain-modeling / grill-with-docs on an ICM repo → rewrite router into glossary → **destroys task routing**.
3. Both installed + ambiguous “update context” → agent oscillates.

### Soft / medium conflicts

| Area | Issue |
| --- | --- |
| **Layer 0** | Matt setup and ICM both edit `AGENTS.md` / `CLAUDE.md`. Compatible if ICM preserves existing blocks and only adds/updates canonical identity without clobbering `## Agent skills`. |
| **Handoffs** | ICM prefers durable in-repo `handoffs/`; Matt deliberately avoids workspace pollution. Document both as valid Layer-4 *or* ephemeral compaction; don’t force Matt handoffs into the repo. |
| **`docs/agents/`** | Both use it (ICM Layer 3 refs; Matt issue-tracker/domain/triage config). Treat Matt files as Layer 3; don’t “clean up” or rename. |
| **Superpowers process** | No `CONTEXT.md` war. Risk is ICM inventing `stages/` when Superpowers already owns design→plan→execute under `docs/superpowers/`. Defer pipeline shape to Superpowers when that tree + skills are present. |
| **Audit false confidence** | `audit_routed_context.py` only checks **existence** of `CONTEXT.md` / `CONTEXT-MAP.md`. A Matt **glossary** currently reports **“Layer 1 router found”** — green but wrong. |

### Not real conflicts

- Superpowers vs ICM on root `CONTEXT.md` content (Superpowers doesn’t define it).
- TDD / code-review / debugging skills vs ICM (behavior vs layout).
- Shared philosophy (plain Markdown, reviewable work, harness-agnostic where possible).

---

## ICM “certified” = properties, not filenames

For coexistence, **passing ICM audit** should mean these **properties** hold, not that the repo uses ICM’s preferred names:

| Property | Intent | Foreign-friendly realization |
| --- | --- | --- |
| **Layer 0** | Identity + harness entry | Existing `AGENTS.md` / `CLAUDE.md` (incl. Matt’s Agent skills block) |
| **Layer 1** | “Where do I go?” for common tasks | Router at preferred names **when free**; else alternate path or section (see below) |
| **Layer 3** | Stable constraints | `_config/`, `references/`, **Matt glossary + ADRs**, Matt `docs/agents/*` |
| **Layer 4** | Per-run / working (or released product, if declared) | `handoffs/`, `output/`, Superpowers `docs/superpowers/{specs,plans}/` |
| **Control point** | Scoped multi-step work | ICM stages **or** Superpowers plan tasks **or** Matt tickets — don’t force one |
| **Reviewable artifacts** | Diffable, human-editable outputs | Any durable path the controlling process writes |
| **Separation** | Stable vs working not mixed | Glossary/ADRs not inside per-run folders; plans not mixed into identity files |

Greenfield ICM can still recommend the paper-aligned layout (`CONTEXT.md` as router, optional `stages/`, etc.). **Coexistence mode** only engages when foreign ownership is detected.

---

## Recommended design (for the builder)

### Strategy: A + B + C (not E)

| Track | What | Why |
| --- | --- | --- |
| **A. Coexistence / deferral in skill prose** | Strong rules in `SKILL.md` + `references/icm-patterns.md` | Agents only defer if wording is explicit and early (explore step) |
| **B. Alternate Layer-1 locations when `CONTEXT.md` is claimed** | Accept additional router paths | Real multi-pack repos need a home for routing without stealing the glossary |
| **C. Smarter audit** | Classify glossary vs router; accept alternates; report coexistence mode | Makes “ICM certified” true under deferral |
| **Not E** | Don’t globally rename ICM’s preferred router off `CONTEXT.md` | Preserves paper alignment for pure ICM projects |

### Detection (run first during Explore)

Treat as **foreign-owned** when any of these are true:

**Matt-shaped domain docs**

- Root (or mapped) `CONTEXT.md` matches glossary shape: `## Language`, bold terms, `_Avoid_`, little/no task-routing table
- `docs/agents/domain.md` present (Matt consumer rules)
- `docs/adr/` with ADR-style decisions and glossary skill conventions
- Installed skills: `domain-modeling`, `grill-with-docs`, `setup-matt-pocock-skills`

**Superpowers-shaped workflow**

- `docs/superpowers/specs/` and/or `docs/superpowers/plans/` in active use
- Installed skills: `using-superpowers`, `brainstorming`, `writing-plans`, `executing-plans` / `subagent-driven-development`

**General**

- `docs/agents/issue-tracker.md` + triage config → Matt engineering setup, not ICM failure

### Ownership rule

> If another installed skill pack owns a path’s **role**, ICM must not rewrite that role. Map ICM layers **onto** their structure and only add missing **properties**.

### Coexistence mapping (default)

| Foreign artifact | ICM layer | ICM must not |
| --- | --- | --- |
| Matt root `CONTEXT.md` (glossary) | **Layer 3** language | Convert to task router; add routing tables; strip terms |
| Matt `CONTEXT-MAP.md` (multi-glossary index) | Multi-context **Layer 3** index | Treat as ICM Layer-1 task router without reading intent |
| Matt `docs/adr/`, `docs/agents/*` | Layer 3 | Delete or rename “to fit ICM” |
| Superpowers specs/plans | Layer 4 working **or** declared product under `docs/` | Invent parallel `stages/` unless user asks for ICM pipelines |
| Matt `/handoff` (temp) | Ephemeral compaction (out of band) | Force in-repo `handoffs/` for that skill’s output |

### Layer-1 escape hatch (recommended default when root `CONTEXT.md` is glossary-owned)

Prefer, in order:

1. **`docs/agents/routing.md`** (or `docs/agents/task-map.md`) — sits next to Matt’s other agent config; Layer 3 area already expected by both ecosystems; clear name.
2. **A dedicated `## Task routing` (or `## Context routing`) section in `AGENTS.md`** — fine for small repos; keep it a table with scoped paths, not a second identity dump.
3. **`TASK-MAP.md` at repo root** — only if the user wants a highly visible root file and refuses nesting under `docs/agents/`.

**Do not** use `CONTEXT-MAP.md` as the ICM router escape hatch when Matt may use that name for multi-glossary maps — same homonym trap.

**Greenfield / ICM-only:** keep recommending root `CONTEXT.md` (or `CONTEXT-MAP.md` only as *ICM* alternate router when *not* in Matt multi-context mode). Detection should distinguish:

- Router-shaped `CONTEXT.md` / `CONTEXT-MAP.md` → Layer 1
- Glossary-shaped `CONTEXT.md` → Layer 3
- Matt multi-context `CONTEXT-MAP.md` → Layer 3 index (links to glossaries, “Relationships” between domains)

### Nested `CONTEXT.md` (stages / library members)

Unchanged for pure ICM. Under coexistence:

- Do not require stage-folder `CONTEXT.md` if Superpowers/Matt already provide the control surface (plan tasks, tickets).
- If the project *does* use ICM stages, keep stage contracts as today.

### Workflow skill text (what to add to `SKILL.md`)

Suggested early section, e.g. **“Coexistence and deferral”**:

1. Explore for foreign conventions **before** proposing folder renames.
2. State detected mode: `icm-native` | `coexist-matt` | `coexist-superpowers` | `coexist-mixed`.
3. Certify **properties**; only create missing pieces (entrypoint, some Layer-1 routing, Layer-3/4 separation).
4. Never convert a glossary-shaped `CONTEXT.md` into a router (or the reverse) without explicit user approval.
5. Do not add `stages/` solely for audit aesthetics when another pack owns multi-step execution.
6. Preserve existing `AGENTS.md` / `CLAUDE.md` content; update in place; no duplicate routing blocks.
7. Run audit in coexistence-aware mode; report mode in findings.

### Audit changes (`scripts/audit_routed_context.py`)

Minimum viable “certified under deferral”:

1. **Classify root `CONTEXT.md` / `CONTEXT-MAP.md` content**
   - Heuristics for glossary: `## Language`, `_Avoid_`, term-definition density, absence of task-routing tables / “go to” style maps
   - Heuristics for router: task tables, “Layer”, path pointers, “where to go”
2. **If glossary-owned:** do **not** count it as Layer 1; look for alternate Layer 1 (preferred list above + section in `AGENTS.md`)
3. **Layer 1:** `ok` if any accepted router exists; `warn` if none (same as today, but honest)
4. **Layer 3:** count glossary + `docs/adr/` + `docs/agents/` + existing stable dirs as success
5. **Layer 4 / control surface:** accept `docs/superpowers/plans`, `docs/superpowers/specs`, `handoffs/`, `output/`, etc.
6. **Pipeline:** if no `stages/` but Superpowers plan tree or equivalent control surface exists, emit `info`/`ok` coexistence note — **not** pressure to add `stages/`
7. **Report mode** in output: e.g. `[INFO] Coexistence mode: matt-glossary (CONTEXT.md treated as Layer 3 language)`
8. Optional: `--strict-native` for pure ICM shape (current stricter expectations) vs default coexistence-tolerant audit

Keep exit code semantics: `fail` only for true gaps (no Layer 0; broken stage contracts *when stages exist*; etc.), not for “foreign but certified.”

### Patterns doc (`references/icm-patterns.md`)

Add a short **“Coexistence profiles”** section with the mapping table and escape-hatch order. Keep the five-layer model primary; coexistence is operational guidance on top of the paper, same as roster libraries already are.

---

## Implementation sketch (when you start)

Suggested PR-sized slices:

1. **Docs-first in skill:** coexistence/deferral section in `SKILL.md` + patterns section (behavior change for agents even before script ships).
2. **Audit: classification + alternate Layer 1 + coexistence findings** (+ fixtures for glossary-shaped vs router-shaped samples).
3. **Optional:** version bump in skill frontmatter; one-line note in pack README under `icm` blurb (“compatible with domain-glossary and process packs when they own structure”).
4. **Do not** change this pack’s own `public/CONTEXT.md` role (it remains ICM-native router).

Out of scope unless requested:

- Negotiating changes upstream with Matt/Superpowers
- Renaming ICM’s greenfield convention off `CONTEXT.md`
- Building adapters that rewrite foreign packs into pure ICM trees

---

## Key source pointers (local)

| Path | Note |
| --- | --- |
| `public/skills/context/icm/SKILL.md` | Workflow, layers, deliverables |
| `public/skills/context/icm/references/icm-patterns.md` | Templates, checklist, two shapes |
| `public/skills/context/icm/scripts/audit_routed_context.py` | Existence-based Layer 1 today — main technical gap |
| `public/CONTEXT.md` | ICM-native router example for this pack |

### External (as of review, 2026-07-17)

| Resource | Relevance |
| --- | --- |
| https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md | Glossary ownership of `CONTEXT.md` |
| https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/CONTEXT-FORMAT.md | Glossary format + multi-context `CONTEXT-MAP.md` |
| https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md | Scaffolds domain layout + `docs/agents/` |
| https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/domain.md | Consumer rules: read glossary, don’t require it upfront |
| https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md | Handoffs to OS temp, not workspace |
| https://github.com/obra/superpowers/blob/main/skills/using-superpowers/SKILL.md | Aggressive skill priority; user instructions override skills |
| https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md | Plans under `docs/superpowers/plans/` |
| https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md | Specs under `docs/superpowers/specs/` |

---

## Suggested skills / approach for the implementer

- Read this handoff fully, then re-read `SKILL.md` + `icm-patterns.md` + `audit_routed_context.py` against the design above.
- Prefer **small, reviewable diffs**: prose deferral first or audit+fixtures in the same change set if you want certification to be testable immediately.
- Add **fixture trees** (tiny fake repos) for: pure ICM router; Matt glossary only; Matt + alternate routing file; Superpowers docs tree without `stages/`.
- Manually sanity-check: running the new audit on a Matt-shaped fixture must **not** claim Layer 1 from the glossary alone, and must **pass** once a thin `docs/agents/routing.md` (or AGENTS section) exists.
- Do **not** open drive-by refactors of unrelated pack files.

---

## Open points (builder may choose)

These are not product blockers; pick defaults if unspecified:

1. Exact glossary/router heuristics thresholds (start simple; tune if false positives appear).
2. Whether `--strict-native` is needed in v1 or only coexistence-tolerant default.
3. Whether skill `metadata.version` bumps to `1.1` vs `1.0.1`.
4. Whether to document coexistence on skills.sh / README in the same PR.

---

## One-line summary for the PR description later

> Teach ICM to **defer path ownership** to workflow skill packs (especially Matt’s glossary `CONTEXT.md` and Superpowers plan trees) while **certifying ICM layer properties** via smarter audit and alternate Layer-1 locations — so multi-skill repos stay compatible without forcing a single folder orthodoxy.

---

## Session provenance

- Review requested in-session; comparative analysis of ICM vs mattpocock/skills vs obra/superpowers.
- Product answers captured above (deferral yes; Layer-1 and audit = implementer best judgment; Superpowers structure allowed if certified).
- **No code or skill package edits were made** as part of the review; this handoff is the handoff artifact only.
