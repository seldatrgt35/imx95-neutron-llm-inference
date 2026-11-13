# EXP-07: Large-model allocation boundary

**Research period:** November 2026  
**Evidence type:** Conversation report  
**Status:** Recorded observation; not a fresh board test

## Objective

Attempt Neutron session initialization on full 4B graph.

## Observed result

`std::bad_alloc` reported during investigation; matching complete failure trace not recovered.

## Primary source

../evidence/terminal/20261112-113926-qwen-ort-verbose-253-neutron-nodes.log

## Interpretation

This record documents the specific observation above; it does not infer successful Qwen3-4B Neutron acceleration. Inspect the source before extending the claim to another BSP, model size or execution provider.

## Remaining verification gate

Full exception stack, memory/CMA snapshots, model hash and allocator trace.

## Reproducibility notes

Collect model checksums, BSP/DTB/firmware identifiers, compiler/ORT versions, exact command, stdout/stderr, exit code and timing methodology for the next run. Distinguish setup-phase placement from execution-phase profiling.
