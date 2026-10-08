"""Optional actual locked SPEED SDK data controls; no endpoint/model calls."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATASET = os.environ.get("MESH_SPEED_TEST_DATASET")


@unittest.skipUnless(DATASET, "requires explicit pinned SPEED SDK preparation")
class SpeedSdkContracts(unittest.TestCase):
    def call(self, data, directory, *arguments):
        return subprocess.run(
            [sys.executable, "-I", "-B", str(ROOT / "benchmark-adapters/speed-bench-auth.py"),
             str(ROOT / "benchmark-adapters/speed-project/upstream-speed-bench.py"),
             "--url", "http://127.0.0.1:1/v1", *arguments],
            timeout=30, capture_output=True, text=True,
            env={"PATH": "/usr/bin:/bin", "SKIPPY_BENCH_BASE_URL": "http://127.0.0.1:1/v1",
                 "SKIPPY_BENCH_API_KEY": "fixture-token", "SKIPPY_BENCH_SPEED_DATASET": str(data),
                 "SKIPPY_BENCH_SPEED_DATASET_CACHE": str(Path(directory) / "datasets"),
                 "HF_HUB_OFFLINE": "1", "HF_DATASETS_OFFLINE": "1",
                 "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def test_actual_parquet_reader_zero_selection_has_no_endpoint_request(self):
        data = Path(DATASET).resolve()
        self.assertEqual(data.stat().st_size, 364138)
        self.assertEqual(hashlib.sha256(data.read_bytes()).hexdigest(),
                         "4f76bc45bdffb38712a5c26d7a7c9a9a791484b392a7b64a6ffb9abe48e02e26")
        with tempfile.TemporaryDirectory() as directory:
            result = self.call(data, directory, "--bench", "qualitative", "--limit", "0")
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("no samples selected", result.stderr)
            self.assertNotIn("Connection", result.stderr)
            self.assertTrue((Path(directory) / "datasets").is_dir())

    def test_same_size_data_mutation_refuses_before_dataset_cache_or_http(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory) / "corrupted.parquet"
            raw = bytearray(Path(DATASET).read_bytes())
            raw[-1] ^= 1
            data.write_bytes(raw)
            result = self.call(data, directory, "--limit", "0")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("SPEED dataset digest mismatch", result.stderr)
            self.assertFalse((Path(directory) / "datasets").exists())

    def test_other_upstream_config_is_refused_without_acquisition(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.call(Path(DATASET).resolve(), directory,
                               "--bench", "throughput_1k", "--limit", "0")
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("unexpected SPEED dataset request", result.stderr)
            self.assertFalse((Path(directory) / "datasets").exists())


if __name__ == "__main__":
    unittest.main()
