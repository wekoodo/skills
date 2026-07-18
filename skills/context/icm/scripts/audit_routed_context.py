#!/usr/bin/env python3
"""Audit a folder-based routed context (ICM) layout.

Recognizes two valid Layer-2/3 shapes, not just one:

* Stage pipeline  -- a ``stages/`` directory of numbered, sequential stage
  contracts (Inputs/Process/Outputs). This is ICM as described in the paper.
* Reference library -- any directory of numbered ``NN-name/`` members each
  carrying a ``CONTEXT.md`` (e.g. ``advisors/``). A library is Layer-3
  reference material that a stage *selects from* by topic; it is NOT a broken
  pipeline. A project may have a pipeline, a library, both, or neither.

Coexistence-aware: ICM certifies layer *properties*, not filenames. Root
``CONTEXT.md``/``CONTEXT-MAP.md`` are classified by content shape -- a
router (task tables, path pointers) counts as Layer 1; a domain *glossary*
(``## Language``, ``**Term**:`` definitions) owned by another skill pack is
Layer 3 language, and Layer 1 may instead live at an alternate location
(``docs/agents/routing.md``, a ``## Task routing`` section in ``AGENTS.md``,
or root ``TASK-MAP.md``). Foreign plan/spec trees (e.g.
``docs/superpowers/plans/``) are an accepted control surface; their presence
without ``stages/`` is coexistence, not a defect. The detected mode is
reported as the first finding: icm-native, coexist-glossary,
coexist-process, or coexist-mixed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ENTRYPOINTS = [
    "AGENTS.md",
    "CLAUDE.md",
    ".github/copilot-instructions.md",
    ".cursor/rules",
]
ROUTERS = ["CONTEXT.md", "CONTEXT-MAP.md"]
ALT_ROUTERS = ["docs/agents/routing.md", "docs/agents/task-map.md", "TASK-MAP.md"]
STABLE_DIRS = ["_config", "shared", "references", "docs/agents", "docs/adr"]
WORKING_DIRS = [
    "output",
    "outputs",
    "input",
    "inputs",
    "handoffs",
    "artifacts",
    "meetings",
    "docs/superpowers/plans",
    "docs/superpowers/specs",
]
# Foreign control surfaces: multi-step execution owned by another skill pack.
CONTROL_SURFACES = ["docs/superpowers/plans", "docs/superpowers/specs"]
SKIP_DIRS = {".git", ".agents", ".claude", ".codex", "node_modules", "tmp", "__pycache__"}

STAGE_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
NUMBERED_RE = re.compile(r"^\d{2}[-_][a-z0-9][a-z0-9_-]*$")
TERM_DEF_RE = re.compile(r"^\s*(?:[-*]\s+)?\*\*[^*\n]+\*\*\s*[:—–-]", re.MULTILINE)
AVOID_RE = re.compile(r"^\s*[_*]+Avoid[_*]+\s*[:]?", re.MULTILINE | re.IGNORECASE)
LAYER_REF_RE = re.compile(r"\bLayer\s*[0-4]\b", re.IGNORECASE)
ROUTER_PHRASE_RE = re.compile(
    r"task[ -]rout|context[ -]rout|where (?:do i|to) go|go to|start here|which stage", re.IGNORECASE
)
GLOSSARY_LINK_RE = re.compile(r"\]\([^)\s]*CONTEXT\.md\)")
ROUTING_SECTION_RE = re.compile(r"^##\s+(?:task|context) routing\s*$", re.MULTILINE | re.IGNORECASE)


@dataclass
class Finding:
    level: str
    message: str
    path: str | None = None


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def existing(root: Path, candidates: list[str]) -> list[Path]:
    return [root / candidate for candidate in candidates if (root / candidate).exists()]


def add(findings: list[Finding], level: str, message: str, path: Path | None = None, root: Path | None = None) -> None:
    findings.append(Finding(level=level, message=message, path=rel(path, root) if path and root else None))


def heading_names(text: str) -> set[str]:
    return {match.group(1).strip().lower() for match in STAGE_HEADING_RE.finditer(text)}


def has_heading(headings: set[str], name: str) -> bool:
    return any(heading == name.lower() or heading.startswith(name.lower() + " ") for heading in headings)


def classify_context_file(text: str) -> str:
    """Classify a CONTEXT.md / CONTEXT-MAP.md by content shape.

    Content is the primary signal (pack conventions drift; what the file *is*
    does not): router | glossary | glossary-index | hybrid | unknown.
    Thresholds are deliberately simple -- tune only if false positives appear.
    """
    headings = heading_names(text)

    # Demotion is deliberately conservative: bold-term definition lines alone
    # also appear in bullet-style routers, so they never demote by themselves.
    # A glossary needs a "## Language" heading, or Avoid-markers plus term
    # density; anything weaker stays "unknown" and keeps counting as Layer 1.
    glossary = 0
    if has_heading(headings, "Language"):
        glossary += 2
    if AVOID_RE.search(text):
        glossary += 1
    if len(TERM_DEF_RE.findall(text)) >= 3:
        glossary += 1

    router = 0
    table_path_rows = [
        line
        for line in text.splitlines()
        if line.lstrip().startswith("|") and not set(line) <= set("|-: \t") and (".md" in line or "/" in line)
    ]
    if len(table_path_rows) >= 2:
        router += 2
    if LAYER_REF_RE.search(text):
        router += 1
    if ROUTER_PHRASE_RE.search(text):
        router += 1

    # Multi-glossary index (bounded contexts): links to several per-context
    # glossaries plus relationship/context framing, without routing tables.
    glossary_links = len(GLOSSARY_LINK_RE.findall(text))
    if (
        glossary_links >= 2
        and router < 2
        and (
            has_heading(headings, "Relationships")
            or has_heading(headings, "Contexts")
            or re.search(r"bounded context", text, re.IGNORECASE)
        )
    ):
        return "glossary-index"

    if glossary >= 2 and router >= 2:
        return "hybrid"
    if glossary >= 2:
        return "glossary"
    if router >= 2:
        return "router"
    return "unknown"


def routing_section_in_entrypoint(root: Path) -> Path | None:
    """A ``## Task routing`` / ``## Context routing`` section in a Layer-0 file."""
    for name in ["AGENTS.md", "CLAUDE.md"]:
        candidate = root / name
        if candidate.is_file() and ROUTING_SECTION_RE.search(candidate.read_text(encoding="utf-8")):
            return candidate
    return None


def numbered_members(directory: Path) -> list[Path]:
    """Direct child folders named NN-slug / NN_slug."""
    if not directory.is_dir():
        return []
    return sorted(c for c in directory.iterdir() if c.is_dir() and NUMBERED_RE.match(c.name))


def find_libraries(root: Path) -> list[tuple[Path, list[Path]]]:
    """Directories (other than stages/) whose children are numbered members.

    This is how a roster of personas/specialists (advisors/) is expressed in
    ICM: a Layer-3 library, selected from per run, not a sequential stage list.
    """
    libraries: list[tuple[Path, list[Path]]] = []
    for child in sorted(p for p in root.iterdir() if p.is_dir()):
        if child.name in SKIP_DIRS or child.name == "stages":
            continue
        members = numbered_members(child)
        if members:
            libraries.append((child, members))
    return libraries


def has_recursive_routing(directory: Path) -> bool:
    """A CONTEXT.md nested below the top of a reference area (footnote-4 pattern)."""
    if not directory.is_dir():
        return False
    for context in directory.rglob("CONTEXT.md"):
        if context.parent != directory:
            return True
    return False


def audit_stage(findings: list[Finding], stage: Path, root: Path) -> None:
    context = stage / "CONTEXT.md"
    if not context.exists():
        add(findings, "fail", "Stage is missing CONTEXT.md.", stage, root)
        return

    text = context.read_text(encoding="utf-8")
    headings = heading_names(text)
    missing = [name for name in ["Inputs", "Process", "Outputs"] if not has_heading(headings, name)]
    if missing:
        add(findings, "fail", f"Stage contract is missing required heading(s): {', '.join(missing)}.", context, root)
    else:
        add(findings, "ok", "Stage contract has Inputs, Process, and Outputs.", context, root)

    if not re.search(r"Layer\s*3|reference", text, re.IGNORECASE):
        add(findings, "warn", "Inputs do not clearly mark Layer 3 reference material.", context, root)
    if not re.search(r"Layer\s*4|working", text, re.IGNORECASE):
        add(findings, "warn", "Inputs do not clearly mark Layer 4 working artifacts.", context, root)
    if not has_heading(headings, "Verify"):
        add(findings, "warn", "Stage has no Verify section. Add one for cross-stage alignment checks when useful.", context, root)

    output = stage / "output"
    if output.exists() and output.is_dir():
        add(findings, "ok", "Stage output/ review gate found.", output, root)
    else:
        add(findings, "warn", "Stage has no output/ directory for reviewable handoffs.", stage, root)


def audit(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []

    if not root.exists():
        add(findings, "fail", "Project root does not exist.", root, root)
        return findings

    # Layer 0 / 1 / 3
    entrypoints = existing(root, ENTRYPOINTS)
    if entrypoints:
        add(findings, "ok", f"Layer 0 entrypoint found: {', '.join(rel(p, root) for p in entrypoints)}.")
    else:
        add(findings, "fail", "No Layer 0 entrypoint found. Expected AGENTS.md, CLAUDE.md, or a tool-specific equivalent.")

    # Layer 1 -- classify preferred router names by content shape before
    # counting them. A glossary owned by another pack is Layer 3, not Layer 1.
    layer1: list[str] = []
    glossary_owned: list[Path] = []
    for candidate in existing(root, ROUTERS):
        kind = classify_context_file(candidate.read_text(encoding="utf-8"))
        name = rel(candidate, root)
        if kind == "glossary":
            glossary_owned.append(candidate)
            add(findings, "info", "Glossary-shaped context file: treated as Layer 3 domain language, not a Layer 1 router.", candidate, root)
        elif kind == "glossary-index":
            glossary_owned.append(candidate)
            add(findings, "info", "Multi-glossary index: treated as a Layer 3 index, not a Layer 1 router.", candidate, root)
        elif kind == "hybrid":
            layer1.append(f"{name} (hybrid)")
            add(findings, "warn", "Context file mixes glossary and routing content. Propose a split (e.g. routing to docs/agents/routing.md); never silently rewrite either role.", candidate, root)
        elif kind == "router":
            layer1.append(f"{name} (router-shaped)")
        else:
            layer1.append(name)

    if not layer1:
        layer1 = [rel(alt, root) for alt in existing(root, ALT_ROUTERS)]
        section_host = routing_section_in_entrypoint(root)
        if section_host:
            layer1.append(f"routing section in {rel(section_host, root)}")

    if layer1:
        add(findings, "ok", f"Layer 1 router found: {', '.join(layer1)}.")
    elif glossary_owned:
        add(findings, "warn", "No Layer 1 router found: preferred names are glossary-owned. Add docs/agents/routing.md, a '## Task routing' section in AGENTS.md, or TASK-MAP.md (not CONTEXT-MAP.md -- glossary packs use that name).")
    else:
        add(findings, "warn", "No Layer 1 router found. Add CONTEXT.md or CONTEXT-MAP.md when tasks need routed context.")

    stable_dirs = existing(root, STABLE_DIRS)
    stable_names = [rel(p, root) for p in stable_dirs] + [f"{rel(p, root)} (glossary)" for p in glossary_owned]
    if stable_names:
        add(findings, "ok", f"Layer 3 reference area found: {', '.join(stable_names)}.")
        for area in stable_dirs:
            if has_recursive_routing(area):
                add(findings, "ok", "Recursive Layer-3 routing found (a CONTEXT.md inside the reference area).", area, root)
    else:
        add(findings, "warn", "No obvious Layer 3 reference area found. Consider _config/, shared/, references/, or docs/agents/.")

    # Layer 2 shape A: a stages/ pipeline
    stages_root = root / "stages"
    has_pipeline = False
    if stages_root.exists():
        stage_dirs = sorted(p for p in stages_root.iterdir() if p.is_dir())
        numbered = [p for p in stage_dirs if NUMBERED_RE.match(p.name)]
        unnumbered = [p for p in stage_dirs if p not in numbered]
        if not numbered:
            add(findings, "fail", "stages/ exists but has no numbered stage folders like 01_research.", stages_root, root)
        else:
            has_pipeline = True
            add(findings, "ok", f"Stage pipeline found: {len(numbered)} numbered stage(s).", stages_root, root)
        for path in unnumbered:
            add(findings, "warn", "Stage folder is not numbered as NN_slug.", path, root)
        for stage in numbered:
            audit_stage(findings, stage, root)

    # Layer 2/3 shape B: numbered reference libraries (e.g. advisors/)
    libraries = find_libraries(root)
    for lib_dir, members in libraries:
        add(findings, "ok", f"Reference library found: {len(members)} numbered member(s) (Layer 3, selected per run).", lib_dir, root)
        if has_recursive_routing(lib_dir):
            add(findings, "ok", "Recursive Layer-3 routing found inside the library.", lib_dir, root)
        for member in members:
            if not (member / "CONTEXT.md").exists():
                add(findings, "warn", "Library member has no CONTEXT.md contract.", member, root)

    # Layer 4 working area
    working = [d for name in WORKING_DIRS for d in [root / name] if d.exists() and d.is_dir()]
    if working:
        add(findings, "ok", f"Layer 4 working area found: {', '.join(rel(d, root) for d in working)}.")

    # Foreign control surface: multi-step execution owned by another pack.
    control_surfaces = [d for name in CONTROL_SURFACES for d in [root / name] if d.is_dir() and any(d.iterdir())]

    # Overall shape note -- only when NEITHER pipeline nor library is present.
    if not has_pipeline and not libraries:
        if control_surfaces:
            add(
                findings,
                "ok",
                f"Foreign control surface found: {', '.join(rel(d, root) for d in control_surfaces)}. "
                "Coexistence: that tree is the control point -- do not add stages/ unless the user wants an ICM pipeline.",
            )
        else:
            add(
                findings,
                "info",
                "No stage pipeline or numbered reference library found. This is a valid "
                "context-only project (Layers 0-1[/3]). Add a stages/ pipeline for a sequential "
                "workflow, or a numbered library (e.g. advisors/) for a selected-per-run roster.",
            )

    # Coexistence mode -- reported first so readers know how to interpret the rest.
    if glossary_owned and control_surfaces:
        mode, detail = "coexist-mixed", "glossary pack owns preferred router names; foreign process tree owns multi-step execution"
    elif glossary_owned:
        mode, detail = "coexist-glossary", f"{', '.join(rel(p, root) for p in glossary_owned)} treated as Layer 3 language"
    elif control_surfaces:
        mode, detail = "coexist-process", f"{', '.join(rel(d, root) for d in control_surfaces)} is the control surface"
    else:
        mode, detail = "icm-native", "no foreign ownership detected"
    findings.insert(0, Finding(level="info", message=f"Coexistence mode: {mode} ({detail})."))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a routed Markdown context (ICM) architecture.")
    parser.add_argument("root", nargs="?", default=".", help="Project root to audit.")
    parser.add_argument("--json", action="store_true", help="Emit JSON findings.")
    args = parser.parse_args()

    findings = audit(Path(args.root))

    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2))
    else:
        for finding in findings:
            path = f" ({finding.path})" if finding.path else ""
            print(f"[{finding.level.upper()}] {finding.message}{path}")

    return 1 if any(finding.level == "fail" for finding in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
