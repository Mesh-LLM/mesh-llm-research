# MeshLLM research references

This local repository owns optional research scripts extracted from MeshLLM.
`provenance/extraction-manifest.json` records each original path and byte hash
at Mesh source `b66a426539eab5ed249ff832d7e984e80efd8c6d`.
It is not a Mesh build, required CI, native reader, or SDK client project.

- `moa-openrouter/`: seven recording, analysis, and trace-fixture scripts with
  their original captures and results. Recording makes paid OpenRouter calls;
  none were run during extraction.
- `scenarios/` and `agent-harness/`: complete agent task inputs and their four
  historical shell runners. The Python task subjects retain their intentional
  defects. Running the harness needs explicitly selected existing models,
  endpoints, and agent tools.
- `hook-experiments/`: historical hook/injection and virtual-LLM experiments.
  They do not describe the current Mesh serving lane. The injection experiment
  requires an explicit absolute `MESH_RESEARCH_LLAMA_SERVER`; it never discovers
  an unrelated checkout-relative executable.
- `latency-benchmarking/`: historical upstream `llama-server`/`rpc-server`
  delay experiments and companions. These are not a supported Mesh release
  runtime. They contain broad process-stop commands inherited from the
  experiment; review them before use on a shared host. No servers were started.
- `granite-reference/`: the independent GGUF/SafeTensors tensor evaluator with
  its original Python3.12 project and genuine resolver lock.
- `lmcache-reference/`: independent scalar reference generator at LMCache
  `b5d109ea99a89b4d8a670ee4fc2e8cb76411ee5c`, plus copies of the two frozen
  reference binaries. Mesh retains the checked binary data consumed by Rust.
- `quantizer-reference/`: supplied upstream converter/quantizer comparison,
  with its declared numpy/GGUF dependencies. No dependency lock, environment
  installation, conversion, or real-model quantization was fabricated.

The root project declares existing CPython3.11 through3.14 and no packages for
stdlib research. Use the separately declared Granite/quantizer projects for
third-party imports. Source extraction does not prove installed SDK or model
compatibility.

From this repository, run the bounded offline controls using an existing
CPython3.12:

```bash
just offline-checks
```

For MoA conversion, choose an output explicitly:

```bash
python3.12 moa-openrouter/make_fixture.py --output /absolute/path/real_traces.json
```

The default input directory is beside the generator; `--input-dir` selects a
separate capture set. This command never infers or rewrites a Mesh fixture path.
Importing `probe_tools` or `record` no longer opens `fanout.jsonl`.

Historical latency companions require explicit roots:

```bash
export MESH_LLM_SOURCE_ROOT=/absolute/path/to/mesh-llm
export MESH_RESEARCH_RPC_ROOT=/absolute/path/to/historical-rpc-experiment
```

The RPC root contains the operator's existing `llama.cpp` and, for back-to-back
comparison, `llama.cpp-rpc-b2b` trees. Native observation helpers use the
explicit Mesh source Just interface; the external repo does not copy their
Rust implementation. These declarations do not authorize downloads or runs.

Original source documents and boundary records under `provenance/` are retained
as historical extraction evidence, not active Mesh exception grants.
