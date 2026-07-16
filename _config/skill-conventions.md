# Skill conventions (Wekoodo pack)

Stable rules for authoring skills in this repository. Scoped reference — load when adding or editing a skill under `skills/`.

## Catalog shape (required by skills.sh)

This pack uses a **one-level category** layout (CLI-supported):

```text
skills/
  <category>/              # payments | context | …
    <skill-name>/
      SKILL.md
      scripts/             # optional
      references/          # optional
      assets/              # optional
      agents/              # optional (e.g. openai.yaml for Codex UI)
```

### Categories

| Category | Use for |
| --- | --- |
| `payments` | Payment-method pricing, processors, checkout/compliance domain skills |
| `context` | Agent context architecture, ICM, routing/structure meta-skills |

Add a new category folder when a third bucket is clearly needed; also add it to `skills.sh.json` groupings and README.

### Rules

- Skill folder name = frontmatter `name` (install identifier).
- Category is **not** part of the install name.
- One skill per directory; do not nest a skill under another skill.
- Max depth under `skills/`: `skills/<category>/<skill-name>/` (do not go deeper for packages).
- Keep [skills.sh.json](../skills.sh.json) skill lists aligned with published skill names.

## Frontmatter

Required:

```yaml
---
name: skill-name
description: What it does and when to use it (include trigger keywords). Max 1024 chars.
---
```

Recommended for this pack:

```yaml
---
name: skill-name
description: "..."
license: MIT
metadata:
  author: wekoodo
  version: "1.0"
---
```

Optional:

- `metadata.internal: true` — hide from normal discovery until ready (`INSTALL_INTERNAL_SKILLS=1` to install).
- `metadata.based_on` / `metadata.paper` — when packaging a third-party method (see `icm`).

`name` rules: lowercase `a-z`, `0-9`, hyphens; no leading/trailing hyphen; no consecutive hyphens; max 64 characters.

## Body

- Instructions the agent follows when the skill is active.
- Prefer progressive disclosure: keep `SKILL.md` focused; put long reference material in `references/`.
- Relative links from the skill root only (one level deep preferred).
- Do not require a specific harness; stay model/harness-agnostic unless `compatibility` is set.

## Attribution

- If the skill operationalizes someone else’s method or paper, credit them in frontmatter metadata **and** a short Attribution section (or quiet line under the title). Do not imply Wekoodo invented the method.
- Wekoodo-original domain skills (e.g. `dual-pricing`) use `metadata.author: wekoodo` without a third-party Attribution block unless sources warrant it.

## What does not go under `skills/`

| Put here instead | Examples |
| --- | --- |
| `_config/` | Pack-wide conventions (this file) |
| `handoffs/` | Session notes, incomplete drafts, audit dumps |
| Future `stages/` | Multi-step authoring contracts (CONTEXT.md per stage) |
| Repo root | README, AGENTS.md, CONTEXT.md, LICENSE |

## Validation checklist (before commit)

- [ ] `skills/<category>/<name>/SKILL.md` exists; `name` matches skill folder
- [ ] Category is intentional (`payments`, `context`, or documented new bucket)
- [ ] Description states *what* and *when*
- [ ] No installable `SKILL.md` outside `skills/`
- [ ] Optional scripts are runnable or documented; paths relative to skill root
- [ ] Third-party methods credited
- [ ] README skill list updated if this is a new public skill
- [ ] `skills.sh.json` includes the skill under the right grouping
