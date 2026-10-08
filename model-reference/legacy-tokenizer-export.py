import json
import pathlib
import shutil
import sys

config = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
root = pathlib.Path(sys.argv[2])
export_root = pathlib.Path(sys.argv[3])
wanted = {key.strip() for key in sys.argv[4].split(",") if key.strip()}

def directory_sha256(path: pathlib.Path) -> str:
    import hashlib
    digest = hashlib.sha256()
    files = sorted(candidate for candidate in path.rglob("*") if candidate.is_file())
    if not files:
        raise RuntimeError(f"directory contains no files: {path}")
    for candidate in files:
        relative = candidate.relative_to(path).as_posix().encode()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        inner = hashlib.sha256()
        with candidate.open("rb") as handle:
            for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
                inner.update(chunk)
        digest.update(bytes.fromhex(inner.hexdigest()))
    return digest.hexdigest()

failures = []
for model in config["models"]:
    key = model["key"]
    if key not in wanted:
        continue
    pin = model["vllm_hf_config"]
    export = export_root / key
    if key == "granite-h1-hybrid":
        # Pinned tokenizer directory is the full HF snapshot minus README.md.
        from huggingface_hub import snapshot_download
        snapshot = pathlib.Path(snapshot_download(
            repo_id=pin["repo"],
            revision=pin["revision"],
        ))
        export.mkdir(parents=True, exist_ok=True)
        for candidate in sorted(p for p in snapshot.rglob("*") if p.is_file()):
            if candidate.name == "README.md":
                continue
            shutil.copy2(candidate, export / candidate.name)
    else:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(pin["repo"], revision=pin["revision"])
        tokenizer.save_pretrained(export, legacy_format=False)
        # The pin contains exactly these three files for non-granite keys.
        allowed = {"tokenizer.json", "tokenizer_config.json", "chat_template.jinja"}
        for stray in export.iterdir():
            if stray.name not in allowed:
                stray.unlink()
    actual = directory_sha256(export)
    expected = model["tokenizer_sha256"]
    if actual != expected:
        failures.append((key, expected, actual))
        print(f"    MISMATCH {key}: expected={expected} actual={actual}", file=sys.stderr)
        continue
    target = root / "tokenizers" / key
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(export, target)
    print(f"    ok: {key} (directory sha256 verified)")
if failures:
    sys.exit(1)
