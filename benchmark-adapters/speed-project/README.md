# Explicit SPEED SDK preparation inputs

The upstream script and requirements are copied byte-for-byte from llama.cpp
ff6779035febf91eed41cdd16757873e6a81d446. The dependency graph was resolved with
existing uv 0.12.23 and existing CPython 3.12.15; no interpreter was acquired and
no packages were installed by that operation. `uv.lock` binds 40 packages and
wheel/source hashes. A native explicit preparation owner must perform locked
sync into a private environment, admit its complete installed closure, and run
`../speed-prepare-dataset.py` to acquire the pinned qualitative Parquet artifact.

The external authentication bridge then uses the actual datasets Parquet reader
with that exact local file; its finite override refuses other repo/config/split
requests. Runtime uses the admitted environment interpreter directly, with
HF_HUB_OFFLINE/HF_DATASETS_OFFLINE and private dataset caches; no uv resolver or
installer is allowed at runtime. Only the benchmark HTTP endpoint remains live.

Dataset nvidia/SPEED-Bench revision
454f88454792dfa3ccfd7ef15fff248efde44cd1 has qualitative/test-00000-of-00001.parquet
size364138 and SHA-256
4f76bc45bdffb38712a5c26d7a7c9a9a791484b392a7b64a6ffb9abe48e02e26.
Official metadata is retained under ../../provenance/speed-source.

Native preparation/runtime wiring is source-complete but native validation is
pending. An explicit isolated local sync and pinned data acquisition passed, and
three actual SDK data controls passed with no endpoint or model requests. See
../../provenance/benchmark-adapters-current.json for those narrow receipts; no
benchmark or model qualification is claimed.
