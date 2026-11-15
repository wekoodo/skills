"""Synthetic regression suite: python -B -m unittest discover -s <skill>/scripts."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import audit_routed_context as audit

class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write('AGENTS.md', '# Synthetic project\n')
        self.write('CONTEXT.md', '# Task routing\n')
    def write(self, name, text):
        p = self.root/name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
    def messages(self, **kwargs):
        return '\n'.join(f'{f.level}: {f.message}' for f in audit.audit(self.root, **kwargs))
    def test_table_and_bullet_required_inputs(self):
        self.write('cycles/CONTEXT.md', '## Inputs\n| Layer | Path | Use |\n|---|---|---|\n| Reference | `rules.md` | Required |\n- Reference: `other.md`\n')
        text=self.messages()
        self.assertIn('Missing required input: rules.md',text)
        self.assertIn('Missing required input: other.md',text)
    def test_real_contract_title_and_nested_input_groups(self):
        self.write('cycles/CONTEXT.md', '# Synthetic specialist\n\n## Identity\nTopic selected.\n\n## Inputs\n\n### Always load\n- `required.md`\n\n### Load as needed\n- `optional.md`\n\n## Process\nUse the inputs.\n## Outputs\n[future](future.md)\n')
        text = self.messages()
        self.assertIn('Missing required input: required.md', text)
        self.assertNotIn('warn: Missing optional input', text)
        self.assertNotIn('Missing route: future.md', text)

    def test_input_annotations_are_not_dependencies(self):
        self.write('cycles/real.md', '# Rules\n')
        self.write('cycles/CONTEXT.md', '# Contract\n## Inputs\n- Reference: `real.md` (do not load `unrelated/`)\n- The scoped owner has `state.md` and routed sections.\n')
        text = self.messages()
        self.assertNotIn('Missing required input', text)
        self.assertIn('Additional input prose paths', text)
        self.assertIn('base/requiredness needs manual review', text)

    def test_containing_file_base_not_root_fallback(self):
        self.write('rules.md','# Root\n')
        self.write('cycles/CONTEXT.md','## Inputs\n- Reference: `rules.md`\n')
        self.assertIn('Missing required input: rules.md',self.messages())
    def test_future_optional_and_execution(self):
        self.write('cycles/CONTEXT.md','## Inputs\n- Working: `run.md`\n- Future working: `later.md`\n- Optional reference: `optional.md`\n')
        self.assertNotIn('warn: Missing',self.messages())
        text=self.messages(execution=True)
        self.assertIn('warn: Missing working input: run.md',text)
        self.assertNotIn('warn: Missing future',text)
        self.assertNotIn('warn: Missing optional',text)
    def test_routing_table_code_and_bare_paths(self):
        self.write('CONTEXT.md', '# Router\n## Task routing\n| Task | Go to |\n|---|---|\n| Rules | `missing.md` |\n| Other | other.md |\n| Scoped | the owner listed by the contract |\n')
        text=self.messages()
        self.assertIn('Missing route: missing.md',text)
        self.assertIn('Missing route: other.md',text)
        self.assertIn('Routing cell is prose',text)

    def test_layer_map_prose_is_not_an_executable_route(self):
        self.write('CONTEXT.md', '# Router\n| Layer | Location |\n|---|---|\n| Control | None yet; add `stages/` only if needed |\n| Rules | `_config/`, each package has `references/` |\n')
        text=self.messages()
        self.assertNotIn('Missing route',text)
        self.assertIn('Routing cell is prose',text)

    def test_unsupported_input_table_reported(self):
        self.write('cycles/CONTEXT.md', '# Contract\n## Inputs\n| Resource | Read |\n|---|---|\n| Rule | prose only |\n')
        self.assertIn('Input table has no recognized', self.messages())

    def test_anchors_url_encoding_duplicate_and_explicit(self):
        self.write('rules.md','# Hello, world!\n## Repeated\n## Repeated\n<a id="custom"></a>\n')
        self.write('CONTEXT.md','[a](rules.md#hello-world)\n[b](rules.md#repeated-1)\n[c](rules.md#custom)\n[d](rules.md#absent)\n[e](rules.md#hello%2Dworld)\n')
        text=self.messages()
        self.assertEqual(text.count('Missing section anchor'),1)
        self.assertIn('rules.md#absent',text)
    def test_shim(self):
        self.write('CLAUDE.md','@missing.md\n')
        self.assertIn('Missing shim target: missing.md',self.messages())
    def test_fences_not_live_headings_or_routes(self):
        self.write('CONTEXT.md','````markdown\n## Inputs\n- Reference: `missing.md`\n```\n[bad](absent.md)\n````\n')
        self.assertNotIn('Missing',self.messages())
    def test_history_only_when_requested_and_informational(self):
        self.write('handoffs/old.md','[old](gone.md)\n')
        self.assertNotIn('gone.md',self.messages())
        text=self.messages(histories=['handoffs'])
        self.assertIn('info: Missing route: gone.md',text)
        self.assertNotIn('warn: Missing route: gone.md',text)
    def test_numbering_alone_is_not_a_library(self):
        self.write('records/01-item/notes.md','# Record\n')
        self.assertNotIn('Reference library found',self.messages())
        self.write('roles/01-specialist/CONTEXT.md','# Topic-selected specialist\n')
        self.assertIn('Reference library found',self.messages())
    def test_custom_overlay_locations(self):
        (self.root/'CONTEXT.md').unlink()
        self.write('cycles/README.md','# Task routing\n')
        self.write('policy/rules.md','# Rules\n')
        text=self.messages(routers=['cycles/README.md'],reference_areas=['policy'],control_paths=['cycles'])
        self.assertIn('Layer 1 router found: cycles/README.md',text)
        self.assertIn('Layer 3 reference area found: policy',text)
        self.assertIn('Foreign control surface found: cycles',text)
    def test_shared_and_equivalent_gates(self):
        self.write('_shared/rules.md','# Rules\n')
        for gate in ['Check','Verify','Review Gate']:
            self.write('stages/01_work/CONTEXT.md',f'## Inputs\n- Reference: `../../_shared/rules.md`\n## Process\nWork.\n## Outputs\nAlternate path, future.\n## {gate}\nA reviewer checks claims; stop on failure.\n')
            text=self.messages()
            self.assertNotIn('Stage has no Check',text)
            self.assertNotIn('Empty ',text)
            self.assertIn('Layer 3 reference area found: _shared',text)
    def test_empty_gate_and_stale_pass_not_approval(self):
        self.write('stages/01_work/CONTEXT.md','## Inputs\n## Process\n## Outputs\n## Check\n')
        self.write('stages/01_work/output/check.md','pass\n')
        text=self.messages()
        self.assertIn('Empty Check',text)
        self.assertIn('does not prove review passed',text)
        self.assertNotIn('review gate found',text)
    def test_external_and_unsupported_are_visible(self):
        self.write('CONTEXT.md','[external](../outside.md)\n[x]({run}/file.md)\n[[Wiki]]\n')
        text=self.messages()
        self.assertIn('External route not inspected',text)
        self.assertIn('Unresolved route',text)
        self.assertIn('wiki/reference-style',text)
    def test_context_only_idempotent_no_writes_and_cli_exit(self):
        self.write('CONTEXT.md','[missing](no.md)\n')
        def snapshot(): return {str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        before=snapshot()
        script=Path(audit.__file__)
        outputs=[]
        for flags, expected in [([],0),([],0),(['--strict'],1)]:
            r=subprocess.run([sys.executable,'-B',str(script),str(self.root),'--json',*flags],capture_output=True,text=True)
            self.assertEqual(r.returncode,expected,r.stderr)
            outputs.append(json.loads(r.stdout))
        self.assertEqual(outputs[0],outputs[1])
        self.assertEqual(before,snapshot())
    def test_installed_cli_without_B_creates_no_cache(self):
        import shutil
        scripts = self.root/'.agents/skills/icm/scripts'
        scripts.mkdir(parents=True)
        for name in ('audit_routed_context.py', 'audit_paths.py'):
            shutil.copyfile(Path(audit.__file__).parent/name, scripts/name)
        before = set(self.root.rglob('*'))
        result = subprocess.run([sys.executable, str(scripts/'audit_routed_context.py'), str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, set(self.root.rglob('*')))

    def test_external_symlink_not_followed(self):
        with tempfile.TemporaryDirectory() as other:
            outside=Path(other)
            (outside/'CONTEXT.md').write_text('[bad](missing.md)')
            try: (self.root/'linked').symlink_to(outside,target_is_directory=True)
            except OSError: self.skipTest('Symlink creation unavailable')
            self.write('CONTEXT.md','[outside](linked/CONTEXT.md)\n')
            self.assertIn('External route not inspected',self.messages())
            self.assertNotIn('Missing route: missing.md',self.messages())

if __name__ == '__main__': unittest.main()
