"""Explicit optional preparation of the pinned upstream SPEED qualitative data."""
import hashlib
import pathlib
import sys
from huggingface_hub import hf_hub_download

ROOT = pathlib.Path(sys.argv[1])
if not ROOT.is_absolute():
    raise ValueError("SPEED dataset cache must be absolute")
path = pathlib.Path(hf_hub_download(
    repo_id="nvidia/SPEED-Bench", repo_type="dataset",
    revision="454f88454792dfa3ccfd7ef15fff248efde44cd1",
    filename="qualitative/test-00000-of-00001.parquet", cache_dir=str(ROOT),
))
if path.stat().st_size != 364138:
    raise ValueError("SPEED dataset size mismatch")
if hashlib.sha256(path.read_bytes()).hexdigest() != "4f76bc45bdffb38712a5c26d7a7c9a9a791484b392a7b64a6ffb9abe48e02e26":
    raise ValueError("SPEED dataset digest mismatch")
print(str(path))
