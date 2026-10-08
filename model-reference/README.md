# Historical tokenizer export reference

`legacy-tokenizer-export.py` preserves the actual Hugging Face/Transformers export block from the former Mesh competitive-input materializer. It takes four positional arguments: benchmark configuration JSON, model root, export root, and comma-separated model keys. It may download pinned Hugging Face inputs.

This is an independent historical reference. The former materializer required Transformers v5 without a complete locked environment; extraction does not turn that into a qualified dependency pin. Its exact package environment and real model results remain unqualified.

Mesh acquisition, selection, hashing and cleanup now belong to native `automation replay-matrix competitive-inputs-prefetch`. Its Rust tokenizer export has its own checked contract and digest. Do not substitute this reference's bytes or digest for native qualification.

The separate Python3.12 project now resolves a locked Transformers5/Hugging Face
SDK candidate from the declared original major-version intent. This is not a
reconstruction of the former unlocked environment. Use explicit `uv sync --locked
--no-python-downloads --project model-reference --python /existing/python3.12`
only when preparing this optional reference. No model export, environment install
or historical equivalence was performed while creating the lock.
