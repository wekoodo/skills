# Wekoodo Skills

This repository is the public skill pack for **Wekoodo**: installable agent skills published at [wekoodo/skills](https://github.com/wekoodo/skills) and indexed on [skills.sh](https://skills.sh/wekoodo/skills).

## Identity

- **Product:** reusable Agent Skills (`skills/<category>/<name>/SKILL.md`) for coding agents.
- **Audience:** Wekoodo projects and anyone installing via `npx skills add wekoodo/skills`.
- **Standards:** [Agent Skills specification](https://agentskills.io/specification); install/discovery via [skills CLI](https://github.com/vercel-labs/skills).
- **Authoring discipline:** Interpretable Context Methodology (ICM) for *this* repo’s own context — see [CONTEXT.md](./CONTEXT.md).

## Non-negotiables (skills.sh compatibility)

1. **Published skills live under `skills/<category>/<name>/`** with a root `SKILL.md` (categories today: `context`).
2. **`name` in frontmatter = skill folder name** (not the category); lowercase, hyphens; max 64 chars.
3. **Do not put a `SKILL.md` outside `skills/`** unless it is intentionally a skill the CLI should discover.
4. **Do not put non-skill work product inside `skills/`** (drafts, notes, handoffs belong elsewhere).
5. Prefer optional `scripts/`, `references/`, `assets/` *inside* each skill package, not repo-wide dumps of skill content.
6. Keep [skills.sh.json](./skills.sh.json) groupings aligned with skill names when adding public skills.
7. **Private skills do not live here.** Internal packs (e.g. dual-pricing) belong in the sibling private repo / `../private` workspace folder — never copy them into this public tree.

## Harness notes

- Canonical agent entrypoint for this workspace: **this file** (`AGENTS.md`).
- Tool-specific files (e.g. `CLAUDE.md`) are thin shims that point here.
- Install projections (`.agents/`, `.claude/`, etc.) are re-installable tooling, not source of truth for skill content.
