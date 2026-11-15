"""Bounded, read-only path checks for ICM routers and contracts (stdlib only)."""
from __future__ import annotations
import os
import re
from pathlib import Path
from urllib.parse import unquote

SKIP = {'.git', '.agents', '.claude', '.codex', 'node_modules', 'vendor', 'tmp', '__pycache__', '_archive', '_templates', 'handoffs', 'meetings', 'output', 'outputs'}
LINK = re.compile(r'\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)')
HEADING = re.compile(r'^(#{1,6})\s+(.+?)\s*#*\s*$')
TICK = re.compile(r'`([^`]+)`')

def active_text(text):
    """Remove fenced examples, preserving line boundaries."""
    lines, fence = [], None
    for line in text.splitlines():
        mark = re.match(r'^\s*(`{3,}|~{3,})', line)
        if mark:
            token = mark[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            lines.append('')
        else:
            lines.append(line if fence is None else '')
    return '\n'.join(lines)

def inside(path, root):
    return path.resolve().is_relative_to(root)

def files_under(root):
    # os.walk does not follow symlinks; explicitly prune Windows junctions too.
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not d.startswith('.')
                         and not (Path(directory)/d).is_symlink()
                         and not getattr(Path(directory)/d, "is_junction", lambda: False)())
        for name in sorted(files):
            path = Path(directory)/name
            if name == 'CONTEXT.md' and inside(path, root):
                yield path

def slugs(text):
    counts, result = {}, set()
    for line in active_text(text).splitlines():
        m = HEADING.match(line)
        if not m:
            continue
        title = re.sub(r'<[^>]+>', '', m[2]).lower()
        slug = ''.join(c for c in title if c.isalnum() or c in '_- ' ).replace(' ', '-')
        n = counts.get(slug, 0)
        counts[slug] = n+1
        result.add(slug if n == 0 else f'{slug}-{n}')
    result.update(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)', text))
    return result

def pathish(value):
    return '/' in value or '\\' in value or bool(re.search(r'\.[a-zA-Z0-9]{1,8}(?:#.*)?$', value)) or value.startswith('#')

def audit_paths(root, findings, *, routers=(), histories=(), execution=False):
    # Lazy import avoids a module cycle and preserves the public Finding format.
    from audit_routed_context import add, classify_context_file
    def emit(level, message, source):
        add(findings, level, message, source, root)
    sources = set(files_under(root))
    for name in ('AGENTS.md', 'CLAUDE.md', 'GEMINI.md', 'CONTEXT-MAP.md', 'TASK-MAP.md', 'docs/agents/routing.md', 'docs/agents/task-map.md', *routers):
        path = root/name
        if inside(path, root) and path.is_file():
            sources.add(path)
        elif name in routers:
            emit('warn', f'Declared router unavailable or outside root: {name}', root)
    history_sources = set()
    for name in histories:
        path = root/name
        if not inside(path, root):
            emit('info', f'History outside root not scanned: {name}', root)
        elif path.is_file():
            history_sources.add(path)
        elif path.is_dir():
            # Only explicitly requested history, never follow reparse points.
            for directory, dirs, files in os.walk(path, followlinks=False):
                dirs[:] = sorted(d for d in dirs if not (Path(directory)/d).is_symlink() and not getattr(Path(directory)/d, "is_junction", lambda: False)() and d not in SKIP - {'handoffs', 'meetings'})
                history_sources.update(Path(directory)/f for f in files if f.endswith('.md') and inside(Path(directory)/f, root))
        else:
            emit('info', f'History unavailable: {name}', root)
    sources -= history_sources
    checked = 0
    unresolved = 0
    def check(source, target, *, role='route', historical=False):
        nonlocal checked, unresolved
        target = target.strip().strip('<>')
        if re.match(r'^(?:https?|mailto|tel):', target, re.I):
            return
        level = 'info' if historical else 'warn'
        if any(c in target for c in '{}<>[]*?|') or target.startswith(('~', '/', '\\')) or re.match(r'^[\w+.-]+:', target):
            unresolved += 1
            emit('info', f'Unresolved {role} (dynamic/absolute/unsupported): {target}', source)
            return
        filepart, _, anchor = unquote(target).partition('#')
        path = (source.parent/filepart).resolve() if filepart else source.resolve()
        if not inside(path, root):
            unresolved += 1
            emit('info', f'External {role} not inspected: {target}', source)
            return
        checked += 1
        if not path.exists():
            if role in ('future input', 'optional input', 'working input') and (role != 'working input' or not execution):
                emit('info', f'Not produced/optional input; execution readiness untested: {target}', source)
            else:
                emit(level, f'Missing {role}: {target}', source)
        elif anchor:
            if path.is_file() and path.suffix.lower() == '.md':
                if anchor not in slugs(path.read_text(encoding='utf-8-sig', errors='replace')):
                    emit(level, f'Missing section anchor in {role}: {target}', source)
            else:
                unresolved += 1
                emit('info', f'Anchor format untested: {target}', source)
    for source in sorted(sources | history_sources):
        historical = source in history_sources
        text = active_text(source.read_text(encoding='utf-8-sig', errors='replace'))
        if source.name in ('CONTEXT.md', 'CONTEXT-MAP.md') and classify_context_file(text) in ('glossary', 'glossary-index'):
            continue
        section, depth, table_path, subgroup, route_column = '', 0, None, '', None
        for line in text.splitlines():
            heading = HEADING.match(line)
            if heading:
                if not section.startswith('inputs') or len(heading[1]) <= depth:
                    section, depth = heading[2].lower(), len(heading[1])
                    table_path, subgroup = None, ''
                else:
                    subgroup = heading[2].lower()
                route_column = None
                continue
            in_inputs = section.startswith('inputs')
            tokens = []
            if in_inputs and line.strip().startswith('|'):
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                header = next((i for i,c in enumerate(cells) if c.lower() in ('path', 'file', 'input')), None)
                if header is not None:
                    table_path = header
                elif table_path is not None and len(cells) > table_path and not re.fullmatch(r'[-: ]+', cells[table_path]):
                    cell = cells[table_path]
                    tokens = [m[1] for m in LINK.finditer(cell)] or TICK.findall(cell) or [cell]
            elif in_inputs and re.match(r'^\s*[-*+]\s', line):
                mentions = sorted([(m.start(), m[1]) for m in LINK.finditer(line)] + [(m.start(), m[1]) for m in TICK.finditer(line)])
                if mentions:
                    start, target = mentions[0]
                    prefix = re.sub(r'^\s*[-*+]\s*', '', line[:start]).strip()
                    if re.fullmatch(r'(?:(?:layer\s*[34]\s*)?(?:reference|working|required|optional|future)(?:\s*\([^)]*\))?)?\s*:?\s*', prefix, re.I):
                        tokens = [target]
                        if len(mentions) > 1:
                            unresolved += 1
                            emit('info', 'Additional input prose paths are not declarations; inspect scoped references manually.', source)
                    else:
                        unresolved += 1
                        emit('info', 'Input path embedded in prose; base/requiredness needs manual review.', source)
                else:
                    bare = re.sub(r'^\s*[-*+]\s*(?:(?:Reference|Working|Required|Optional|Future):\s*)?', '', line, flags=re.I).strip()
                    if re.fullmatch(r'[\w./#%-]+', bare) and pathish(bare):
                        tokens = [bare]
            if in_inputs and line.strip().startswith('|') and table_path is None and not re.fullmatch(r'[|\s:-]+', line):
                unresolved += 1
                emit('info', 'Input table has no recognized Path/File/Input column; inspect manually.', source)
            if in_inputs and re.match(r'^\s*[-*+]\s', line) and not any(pathish(t) for t in tokens):
                unresolved += 1
                emit('info', 'Input has no explicit supported path; inspect manually.', source)
            lower = subgroup + ' ' + line.lower()
            role = 'required input'
            if 'optional' in lower or 'as needed' in lower:
                role = 'optional input'
            elif re.search(r'future|not.yet.produced|produced later|per.run', lower):
                role = 'future input'
            elif re.search(r'layer\s*4|working', lower):
                role = 'working input'
            targets = set(t for t in tokens if pathish(t))
            for target in sorted(targets):
                check(source, target, role=role, historical=historical)
            if section.startswith('outputs'):
                continue
            # Routing tables can use backticks or bare paths, not only Markdown links.
            if not in_inputs and line.strip().startswith('|'):
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                header = next((i for i, c in enumerate(cells) if c.lower() in ('go to', 'target', 'route', 'location')), None)
                if header is not None:
                    route_column = header
                elif route_column is not None and len(cells) > route_column:
                    cell = cells[route_column]
                    if not LINK.search(cell) and not re.fullmatch(r'[-: ]+', cell):
                        code_path = re.fullmatch(r'`([^`]+)`', cell)
                        paths = [code_path[1]] if code_path else ([cell] if re.fullmatch(r'[\w./#%-]+', cell) else [])
                        for target in paths:
                            if pathish(target):
                                check(source, target, historical=historical)
                        if not paths:
                            unresolved += 1
                            emit('info', 'Routing cell is prose; inspect targets manually.', source)
            elif line.strip():
                route_column = None
            for match in LINK.finditer(line):
                if match[1] not in targets:
                    check(source, match[1], historical=historical)
            imp = re.match(r'^\s*@([^\s]+\.md)\s*$', line)
            if imp:
                check(source, imp[1], role='shim target', historical=historical)
            if '[[' in line or re.search(r'\[[^\]]+\]\[[^\]]*\]', line):
                unresolved += 1
                emit('info', 'Unresolved wiki/reference-style link; inspect manually.', source)
    emit('info', f'Coverage: {len(sources)} active routing/entry contracts, {len(history_sources)} explicit history files; {checked} local targets checked, {unresolved} unresolved. Generic Markdown, private records, ignored/projection/runtime trees and fenced examples are not recursively scanned. Exclusions: {", ".join(sorted(SKIP))}. Review completion, freshness and semantic correctness require a walk test.', root)
