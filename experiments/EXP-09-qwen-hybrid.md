# EXP-09: Four-layer NPU/CPU ONNX partition hypothesis

**Research period:** November 2026  
**Evidence type:** Captured terminal + recovered source  
**Status:** Recorded observation; not a fresh board test

## Objective

Develop two scripts separating first four layers and CPU suffix with KV cache.

## Observed result

Boundary identified; ONNX custom-op schema and hard-link security validation failures observed.

## Primary source

../evidence/terminal/20261112-122647-hybrid-graph-partitioning-errors.log

## Interpretation

This record documents the specific observation above; it does not infer successful Qwen3-4B Neutron acceleration. Inspect the source before extending the claim to another BSP, model size or execution provider.

## Remaining verification gate

Validated source/model halves and matching logits over multiple decode steps.

## Reproducibility notes

Collect model checksums, BSP/DTB/firmware identifiers, compiler/ORT versions, exact command, stdout/stderr, exit code and timing methodology for the next run. Distinguish setup-phase placement from execution-phase profiling.
