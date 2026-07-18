#!/usr/bin/env python3
"""Tests for audit_routed_context.py.

Fixture trees are built in a temporary directory at runtime and deleted
afterwards -- no fixture repos ship inside the skill package. Run:

    python test_audit_routed_context.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import audit_routed_context as audit

failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}{f' -- {detail}' if detail else ''}")
        failures.append(name)


def audit_tree(tree: dict[str, str]) -> list[audit.Finding]:
    """Build the given {relpath: content} tree in a temp dir and audit it.

    A key ending in '/' creates an empty directory.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for relpath, content in tree.items():
            path = root / relpath
            if relpath.endswith("/"):
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
        return audit.audit(root)


def has(findings: list[audit.Finding], level: str, fragment: str) -> bool:
    return any(f.level == level and fragment in f.message for f in findings)


def mode_of(findings: list[audit.Finding]) -> str:
    return findings[0].message


def no_fails(findings: list[audit.Finding]) -> bool:
    return not any(f.level == "fail" for f in findings)


AGENTS = "# Project\n\nIdentity and constraints for agents.\n"

ROUTER = """# Context

Where to go for common tasks.

| Task | Go to |
| --- | --- |
| Add a feature | src/ then stages/01_research/CONTEXT.md |
| Audit context | scripts/audit.md |

Layer 3 references live in _config/.
"""

GLOSSARY = """# Domain Language

## Language

**Invoice**: A bill sent to a customer for payment.

**Ledger**: The append-only record of transactions.

**Quote**: A price offer that has not been accepted yet.

_Avoid_: "bill" -- say invoice.
"""

HYBRID = GLOSSARY + "\n" + """## Where to go

| Task | Go to |
| --- | --- |
| Billing work | src/billing/ |
| Audit context | docs/agents/audit.md |
"""

GLOSSARY_INDEX = """# Context Map

Bounded contexts in this workspace:

- [Billing](billing/CONTEXT.md)
- [Shipping](shipping/CONTEXT.md)

## Relationships

Billing is upstream of Shipping.
"""

BULLET_ROUTER = """# Context

- **Deploy**: read docs/deploy.md
- **Add a skill**: read skills/README.md
- **Audit**: run the audit script
"""

AGENTS_WITH_ROUTING = AGENTS + """
## Task routing

| Task | Go to |
| --- | --- |
| Build | src/ |
| Docs | docs/ |
"""

STAGE_CONTRACT = """# 01 Research

## Inputs

| Layer | Path | Use |
| --- | --- | --- |
| Layer 4 working | ../../input/source.md | Source material |
| Layer 3 reference | ../../_config/voice.md | Constraints |

## Process

1. Read only the listed inputs.

## Outputs

- Write research.md to output/.

## Verify

- Claims trace to sources.
"""


def test_classifier() -> None:
    print("classify_context_file")
    check("router text -> router", audit.classify_context_file(ROUTER) == "router", audit.classify_context_file(ROUTER))
    check("glossary text -> glossary", audit.classify_context_file(GLOSSARY) == "glossary", audit.classify_context_file(GLOSSARY))
    check("hybrid text -> hybrid", audit.classify_context_file(HYBRID) == "hybrid", audit.classify_context_file(HYBRID))
    check("multi-glossary map -> glossary-index", audit.classify_context_file(GLOSSARY_INDEX) == "glossary-index", audit.classify_context_file(GLOSSARY_INDEX))
    check("empty-ish text -> unknown", audit.classify_context_file("# Notes\n\nHello.\n") == "unknown")
    check("bullet-style router NOT demoted to glossary", audit.classify_context_file(BULLET_ROUTER) == "unknown", audit.classify_context_file(BULLET_ROUTER))


def test_bullet_router_back_compat() -> None:
    print("back-compat: bullet-style router still counts as Layer 1")
    findings = audit_tree({
        "AGENTS.md": AGENTS,
        "CONTEXT.md": BULLET_ROUTER,
    })
    check("counted as Layer 1", has(findings, "ok", "Layer 1 router found: CONTEXT.md"))
    check("not demoted", not has(findings, "info", "treated as Layer 3 domain language"))
    check("no hybrid warn", not has(findings, "warn", "mixes glossary and routing"))


def test_icm_native() -> None:
    print("pure ICM pipeline")
    findings = audit_tree({
        "AGENTS.md": AGENTS,
        "CONTEXT.md": ROUTER,
        "_config/voice.md": "Voice rules.\n",
        "stages/01_research/CONTEXT.md": STAGE_CONTRACT,
        "stages/01_research/output/": "",
    })
    check("mode icm-native", "icm-native" in mode_of(findings), mode_of(findings))
    check("router counted as Layer 1", has(findings, "ok", "Layer 1 router found: CONTEXT.md (router-shaped)"))
    check("pipeline found", has(findings, "ok", "Stage pipeline found"))
    check("no fails", no_fails(findings))


def test_glossary_only() -> None:
    print("glossary owns CONTEXT.md, no alternate router")
    findings = audit_tree({
        "AGENTS.md": AGENTS,
        "CONTEXT.md": GLOSSARY,
        "docs/agents/domain.md": "Read the glossary before naming things.\n",
        "docs/adr/0001-record.md": "# ADR 1\n\nDecision.\n",
    })
    check("mode coexist-glossary", "coexist-glossary" in mode_of(findings), mode_of(findings))
    check("glossary NOT counted as Layer 1", not has(findings, "ok", "Layer 1 router found"))
    check("glossary demotion reported", has(findings, "info", "treated as Layer 3 domain language"))
    check("honest Layer-1 warn with escape hatch", has(findings, "warn", "glossary-owned"))
    check("glossary counted toward Layer 3", has(findings, "ok", "Layer 3 reference area found") and any("(glossary)" in f.message for f in findings))
    check("docs/adr counted as stable", any("docs/adr" in f.message for f in findings if f.level == "ok"))
    check("no fails (foreign is not failure)", no_fails(findings))


def test_glossary_with_alt_router() -> None:
    print("glossary + docs/agents/routing.md")
    findings = audit_tree({
        "AGENTS.md": AGENTS,
        "CONTEXT.md": GLOSSARY,
        "docs/agents/routing.md": ROUTER,
    })
    check("alternate counted as Layer 1", has(findings, "ok", "Layer 1 router found: docs/agents/routing.md"))
    check("no Layer-1 warn", not has(findings, "warn", "No Layer 1 router found"))
    check("mode still coexist-glossary", "coexist-glossary" in mode_of(findings), mode_of(findings))


def test_glossary_with_agents_section() -> None:
    print("glossary + '## Task routing' section in AGENTS.md")
    findings = audit_tree({
        "AGENTS.md": AGENTS_WITH_ROUTING,
        "CONTEXT.md": GLOSSARY,
    })
    check("section counted as Layer 1", has(findings, "ok", "routing section in AGENTS.md"))
    check("no Layer-1 warn", not has(findings, "warn", "No Layer 1 router found"))


def test_superpowers_tree() -> None:
    print("process pack tree, no stages/")
    findings = audit_tree({
        "AGENTS.md": AGENTS,
        "docs/superpowers/plans/2026-07-17-plan.md": "# Plan\n\n- [ ] Task 1\n",
        "docs/superpowers/specs/feature.md": "# Spec\n",
    })
    check("mode coexist-process", "coexist-process" in mode_of(findings), mode_of(findings))
    check("control surface accepted", has(findings, "ok", "Foreign control surface found"))
    check("no pressure to add stages/", not has(findings, "info", "Add a stages/ pipeline"))
    check("plan tree counted as Layer 4", has(findings, "ok", "Layer 4 working area found"))
    check("no fails", no_fails(findings))


def test_hybrid_file() -> None:
    print("hybrid CONTEXT.md")
    findings = audit_tree({
        "AGENTS.md": AGENTS,
        "CONTEXT.md": HYBRID,
    })
    check("hybrid counted as Layer 1", has(findings, "ok", "Layer 1 router found: CONTEXT.md (hybrid)"))
    check("split proposed, no silent side-pick", has(findings, "warn", "mixes glossary and routing"))


def test_glossary_index_map() -> None:
    print("multi-glossary CONTEXT-MAP.md")
    findings = audit_tree({
        "AGENTS.md": AGENTS,
        "CONTEXT-MAP.md": GLOSSARY_INDEX,
    })
    check("index NOT counted as Layer 1", not has(findings, "ok", "Layer 1 router found"))
    check("index demotion reported", has(findings, "info", "treated as a Layer 3 index"))


def test_exit_semantics() -> None:
    print("exit semantics")
    findings = audit_tree({"README.md": "# Nothing agent-shaped here\n"})
    check("missing Layer 0 is still a fail", has(findings, "fail", "No Layer 0 entrypoint"))


def main() -> int:
    for test in [
        test_classifier,
        test_bullet_router_back_compat,
        test_icm_native,
        test_glossary_only,
        test_glossary_with_alt_router,
        test_glossary_with_agents_section,
        test_superpowers_tree,
        test_hybrid_file,
        test_glossary_index_map,
        test_exit_semantics,
    ]:
        test()
    print(f"\n{len(failures)} failure(s)" if failures else "\nAll tests passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
