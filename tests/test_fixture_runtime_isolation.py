"""Exercise the actual existing copy helper under a synthetic source-root."""
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import tests.test_cli as cli


class FixtureRuntimeIsolationTests(unittest.TestCase):
    def test_actual_helper_excludes_only_source_root_runtime(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            files={'bin/vibe':'synthetic CLI','ordinary.txt':'keep','.vibe/core/contract.txt':'keep','.vibe/local/private-canary':'PRIVATE-CANARY','.git/private':'exclude','__pycache__/cache.py':'exclude','cached.pyc':'exclude','.vibe/manifest.json':'exclude','fixtures/local/retained.txt':'keep','nested/project/.vibe/local/retained.txt':'keep'}
            for relative,body in files.items():
                path=root/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)
            destination=root/'.vibe/local/tmp/copied'
            with mock.patch.object(cli,'ROOT',root):result=cli.copy_source(destination)
            self.assertEqual(result,destination/'bin/vibe');self.assertEqual(result.read_text(),'synthetic CLI')
            for relative in ('ordinary.txt','.vibe/core/contract.txt','fixtures/local/retained.txt','nested/project/.vibe/local/retained.txt'):
                self.assertEqual((destination/relative).read_text(),'keep')
            for relative in ('.vibe/local','.git','__pycache__','cached.pyc','.vibe/manifest.json'):
                self.assertFalse((destination/relative).exists(),relative)
            self.assertFalse(any('PRIVATE-CANARY' in path.read_text() for path in destination.rglob('*') if path.is_file()))
