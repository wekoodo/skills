# Wekoodo Skills

Agent skills maintained by [Wekoodo](https://github.com/wekoodo) for coding agents (Claude Code, Cursor, Codex, Copilot, and others).

Skills follow the [Agent Skills](https://agentskills.io/) format and install via [skills.sh](https://skills.sh).

[![skills.sh](https://skills.sh/b/wekoodo/skills)](https://skills.sh/wekoodo/skills)

## Install

```bash
# All skills in this pack
npx skills add wekoodo/skills

# List skills without installing
npx skills add wekoodo/skills --list

# One skill
npx skills add wekoodo/skills --skill icm

# Shorthand
npx skills add wekoodo/skills@icm
```

Global install (available in every project):

```bash
npx skills add wekoodo/skills -g
```

Update later:

```bash
npx skills update
```

## Available skills

### Context

#### `icm` — Interpretable Context Methodology

Build, audit, and maintain folder-based agent context (ICM): entrypoints, routing, stage pipelines or reference libraries, and reviewable artifacts.

**Use when:** designing or auditing agent context architecture; keeping a project portable and harness-agnostic; growing structure without monolithic prompts.

Method introduced by Jake Van Clief, David McDermott, and Eduba (University of Edinburgh): [arXiv:2603.16021](https://arxiv.org/abs/2603.16021). This skill packages operational guidance; credit for the methodology belongs to the paper authors.

## Skill layout (skills.sh contract)

Published skills live under `skills/<category>/<skill-name>/` and are self-contained:

```text
skills/
  <category>/              # e.g. context — pack organization only
    <skill-name>/
      SKILL.md             # required — name + description + instructions
      scripts/             # optional
      references/          # optional
      assets/              # optional
```

Install name is the **skill** folder / frontmatter `name` (e.g. `icm`), not the category. Categories group the monorepo and the skills.sh pack page (`skills.sh.json`); they do not change install commands.

## Repo maintenance (ICM)

This repository is itself maintained with a light [Interpretable Context Methodology](https://arxiv.org/abs/2603.16021) layout so agents can add and revise skills consistently. That structure wraps authoring workflow; it does **not** replace the `skills/` catalog shape above.

See [AGENTS.md](./AGENTS.md) and [CONTEXT.md](./CONTEXT.md).

Local multi-repo workspace (public + private packs side by side): parent of this folder — open `wekoodo-ai-skills.code-workspace` one level up.

## License

MIT — see [LICENSE](./LICENSE).
