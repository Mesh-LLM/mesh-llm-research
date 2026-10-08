# Pinned model converters

This project owns the complete Python checkpoint-to-GGUF converter and GGUF library formerly carried by Mesh's llama.cpp patch queue. It preserves the patched converter source for Inkling, DiffusionGemma and Laya, including converter registration, metadata, tensor mapping, tokenizer behavior and explicit unsupported-layout refusals. Mesh keeps the native runtime implementation and ABI; its prepared upstream checkout no longer carries these Python additions.

The source is extracted from ggml-org/llama.cpp upstream `8212c7802455255460ab8e18fc34754560031b34` with the former Mesh queue applied at `ff6779035febf91eed41cdd16757873e6a81d446`. `provenance/source-files.json` records every copied source file and digest. The original dependency metadata and README are preserved under `provenance/`; the scoped project uses the same dependency constraints, its local GGUF library, and a resolved `uv.lock`. MIT licensing and attribution remain in `LICENSE`, `AUTHORS`, `gguf-py/LICENSE` and `licenses/`.

Use this project from a pinned checkout of the external research repository; publication and the eventual repository revision are separate release steps. For a local checkout:

```sh
cd "$MESH_RESEARCH_ROOT/model-converters"
just prepare
just offline-tests
just converter-help
```

`prepare` installs locked dependencies into this project's private `.venv`; it does not download model checkpoints or invoke native builds. `offline-tests` runs the upstream GGUF metadata and malformed-file tests. Native-library quantization and tokenizer integration tests are retained but require their separately built native library and test model inputs; they are not covered by the offline recipe.

Convert an already acquired checkpoint with the preserved upstream interface:

```sh
uv run --locked --no-sync python convert_hf_to_gguf.py /absolute/checkpoint \
  --outtype f16 --outfile /absolute/output/model-F16.gguf
```

The same project contains `convert_lora_to_gguf.py`, `convert_llama_ggml_to_gguf.py` and the tokenizer-update utility. `conversion/`, `gguf-py/`, the original requirements, model templates/tokenizer fixtures and upstream tests are kept together, so imports and template lookup do not depend on a Mesh `.deps` directory. Optional converter dependencies remain subject to the upstream feature's own import errors; the default lock does not claim every optional architecture is installed or qualified.

Native Skippy conversion already implements parts of Inkling metadata, vocabulary and tensor transformation. This extraction does not claim native equivalence for the complete Python family converters, and it does not establish model output accuracy, serving compatibility or platform qualification. No checkpoint conversion is performed during extraction.
