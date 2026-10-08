# Independent upstream quantizer comparison

The extracted `compare-reference-quantization.py` preserves actual upstream
GGUFReader/numpy conversion and quantizer comparisons. It compares tensor
names/shapes/types/data, and requires selected split quantization outputs to be
byte identical. Optional matching-failure handling and deterministic all-ones
importance matrices retain their original semantics.

Use the declared Python3.12 project explicitly. Its uv.lock is a genuine
49-package resolver graph, including the optional conversion dependencies;
resolution installed nothing and did not run a model comparison. The optional `upstream-conversion` group declares the existing
converter imports. The converter, checkpoint, native tools, and their exact
source identities are supplied by the operator.

```bash
uv sync --locked --no-python-downloads --project quantizer-reference --python python3.12
quantizer-reference/.venv/bin/python -I quantizer-reference/compare-reference-quantization.py --help
```

No installation or model comparison was run during extraction. Consult the
script's actual argument parser for conversion/quantization inputs. Native
Mesh quantizer code and policy remain in Mesh, not in this research project.
