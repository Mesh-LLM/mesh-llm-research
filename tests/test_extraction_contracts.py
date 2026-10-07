"""Offline extraction controls; no model calls, installs, or paid recording."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExtractionContracts(unittest.TestCase):
    def run_python(self, *arguments, cwd):
        return subprocess.run(
            [sys.executable, "-I", "-B", *map(str, arguments)],
            cwd=cwd, capture_output=True, text=True, timeout=30,
            env={"PATH": os.environ.get("PATH", "")},
        )

    def test_schema_import_has_no_capture_or_network_side_effect(self):
        with tempfile.TemporaryDirectory() as directory:
            script = (
                "import sys; sys.path.insert(0,sys.argv[1]); "
                "import probe_tools,record; assert len(probe_tools.TOOLS)>0"
            )
            result = self.run_python("-c", script, ROOT / "moa-openrouter", cwd=directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_fixture_requires_output_and_preserves_captured_worker_fields(self):
        generator = ROOT / "moa-openrouter/make_fixture.py"
        with tempfile.TemporaryDirectory() as directory:
            denied = self.run_python(generator, cwd=directory)
            self.assertNotEqual(denied.returncode, 0)
            self.assertIn("--output", denied.stderr)
            self.assertEqual(list(Path(directory).iterdir()), [])
            destination = Path(directory) / "explicit-output.json"
            result = self.run_python(generator, "--output", destination, cwd=directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            cases = json.loads(destination.read_text())["cases"]
            corpus = ROOT / "moa-openrouter"
            source = [json.loads(line) for name in ("agentic.jsonl", "corpus.jsonl")
                      for line in (corpus / name).read_text().splitlines() if line.strip()]
            self.assertEqual(len(cases), len(source))
            for case, captured in zip(cases, source):
                self.assertEqual(case["messages"], captured["messages"])
                self.assertEqual(len(case["workers"]), len(captured["workers"]))
                for worker, original in zip(case["workers"], captured["workers"]):
                    self.assertEqual(worker["content"], original.get("text"))
                    self.assertEqual(worker["tool_calls"], original.get("tool_calls"))
                    self.assertEqual(worker["finish_reason"], original.get("finish_reason"))
                    self.assertEqual(worker["elapsed_ms"], round((original["elapsed"] or 0) * 1000))

    def test_independent_lmcache_generator_matches_preserved_reference_bytes(self):
        reference = ROOT / "lmcache-reference"
        with tempfile.TemporaryDirectory() as directory:
            generator = Path(directory) / "generate_lmcache_compat.py"
            shutil.copyfile(reference / generator.name, generator)
            result = self.run_python(generator, cwd=directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            for bins in (16, 32):
                filename = f"lmcache_b5d109e_bins{bins}.bin"
                self.assertEqual((Path(directory) / filename).read_bytes(),
                                 (reference / filename).read_bytes())


if __name__ == "__main__":
    unittest.main()
