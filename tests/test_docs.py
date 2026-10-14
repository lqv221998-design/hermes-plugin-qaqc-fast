"""Portable documentation integrity: bundled references and sample request schemas."""
import json
import re
import unittest
from pathlib import Path
from typing import Any, cast
from test_expansion import plugin

ROOT=Path(__file__).resolve().parents[1]


class Documentation(unittest.TestCase):
    def test_every_json_request_example_uses_actual_public_schema(self):
        props=cast(Any,plugin).properties(cast(Any,plugin).MODULES)
        doc=(ROOT/'skills/tasks/references/examples.md').read_text(encoding='utf-8')
        examples=[json.loads(x) for x in re.findall(r'```json\s*(.*?)\s*```',doc,re.S)]
        self.assertGreaterEqual(len(examples),10)
        for example in examples:
            with self.subTest(example=example):
                self.assertEqual(set(example)-set(props),set())
                self.assertIn(example['action'],props['action']['enum'])
                for key,value in example.items():
                    schema=props[key]
                    if 'enum' in schema:self.assertIn(value,schema['enum'])
                    if schema.get('type')=='integer':self.assertIs(type(value),int)
                    if schema.get('type')=='string':
                        self.assertIsInstance(value,str)
                        self.assertLessEqual(len(value),schema.get('maxLength',100000))
                        if 'pattern' in schema:self.assertRegex(value,schema['pattern'])
    def test_all_relative_markdown_links_in_portable_docs_exist(self):
        for doc in ROOT.rglob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
                if link.startswith(('https://','http://','#')):continue
                relative=link.split('#',1)[0]
                if relative:
                    with self.subTest(doc=doc.name,link=link):self.assertTrue((doc.parent/relative).exists())
    def test_three_skills_and_top_guides_use_current_release(self):
        for path in ('skills/setup/SKILL.md','skills/operations/SKILL.md','skills/tasks/SKILL.md','README.md','START-HERE-HERMES.md','SETUP.md'):
            with self.subTest(path=path):self.assertIn('0.2.0-rc.3',(ROOT/path).read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
