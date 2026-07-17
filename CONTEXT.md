# Context map

Where to go for common work in this repo. Keep loads scoped — prefer the files named here over whole-repo reads.

## Task routing

| Task | Go to | Notes |
| --- | --- | --- |
| Install / use skills as a consumer | [README.md](./README.md) | Public install commands and skill blurbs |
| Understand pack identity + hard constraints | [AGENTS.md](./AGENTS.md) | Layer 0 — skills.sh non-negotiables |
| Add or revise a **published** skill | `skills/<category>/<name>/` | Must end as valid Agent Skill; see [_config/skill-conventions.md](./_config/skill-conventions.md) |
| Skill writing rules (stable) | [_config/skill-conventions.md](./_config/skill-conventions.md) | Layer 3 — naming, frontmatter, attribution, discovery |
| ICM method details (when designing context elsewhere or auditing this repo) | [skills/context/icm/](./skills/context/icm/) | Published skill; also our authoring discipline |
| Dual pricing / other private skills | `../private/` (sibling pack) | Not published here; separate git remote |
| Public pack groupings (skills.sh) | [skills.sh.json](./skills.sh.json) | UI groups by skill name; keep in sync with categories |
| In-progress notes / session handoffs | [handoffs/](./handoffs/) | Layer 4 — not published, not installable |
| Draft material before it becomes a skill | [handoffs/](./handoffs/) or WIP with `metadata.internal: true` | Graduate into `skills/` only when ready |

## Layer map (this repo)

| Layer | Role here | Location |
| --- | --- | --- |
| 0 | Identity + harness routing | `AGENTS.md`, `CLAUDE.md` |
| 1 | Task routing | This file (`CONTEXT.md`) |
| 2 | Control point | None yet — add `stages/` only if authoring becomes a multi-step pipeline |
| 3 | Stable constraints | `_config/`, each skill’s own `references/` |
| 4 | Working artifacts | `handoffs/`; published skills under `skills/` are the **released product**, not session scratch |

## Compatibility rule (ICM ∩ skills.sh)

ICM owns **how we author and maintain** this pack. skills.sh owns **how published skills are discovered and installed**.

- ICM folders (`_config/`, `handoffs/`, future `stages/`) must **not** contain installable `SKILL.md` packages.
- The installable catalog is **only** `skills/<category>/<name>/SKILL.md` (or flat `skills/<name>/`) plus that skill’s bundled files.
- Categories (`context`, …) organize the monorepo; install still uses skill **name** (`icm`).
- When in doubt: consumer install path wins for layout under `skills/`; ICM patterns apply around it, not over it.

## Multi-repo workspace

This pack is often opened next to a private pack via the parent [wekoodo-ai-skills.code-workspace](../wekoodo-ai-skills.code-workspace). Public and private remotes stay independent; only this directory pushes to `wekoodo/skills`.

## Shape note

This is **Layers 0–1 + 3 (+4 handoffs)** — a minimal ICM project context layout. A numbered stage pipeline is optional later (e.g. draft → review → publish) if that workflow stabilizes.
