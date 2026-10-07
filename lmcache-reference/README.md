# Independent LMCache fixture reference

`generate_lmcache_compat.py` is the original scalar transcription of LMCache
revision `b5d109ea99a89b4d8a670ee4fc2e8cb76411ee5c`. It needs only stdlib Python.
It reproduces the arithmetic coder, CDF construction, and float16/float32
quantization independently of Mesh's Rust codec.

Running it writes the two `.bin` files beside the generator. The extraction's
offline tests instead run a temporary copy and compare both outputs byte for
byte against the preserved reference files. They do not overwrite Mesh data or
regenerate references from the codec under test.

Mesh's native `matches_lmcache_bins16_fixture` and
`matches_lmcache_bins32_fixture` tests continue to consume their checked copies
under `skippy/crates/skippy-cache/src/cachegen/fixtures/`.
