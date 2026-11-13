# EXP-02: Memory reservation and allocator investigation

**Research period:** November 2026  
**Evidence type:** Conversation report  
**Status:** Recorded observation; not a fresh board test

## Objective

Compare CMA size after changing image/DTB/cmdline and record `/proc/meminfo`.

## Observed result

Two snapshots: about 0.94 GiB and 4.94 GiB CMA; size alone did not establish LLM success.

## Primary source

../evidence/terminal/20261112-113926-qwen-ort-verbose-253-neutron-nodes.log

## Interpretation

This record documents the specific observation above; it does not infer successful Qwen3-4B Neutron acceleration. Inspect the source before extending the claim to another BSP, model size or execution provider.

## Remaining verification gate

Consistent boot/DTB provenance plus allocations/RSS during Neutron session init.

## Reproducibility notes

Collect model checksums, BSP/DTB/firmware identifiers, compiler/ORT versions, exact command, stdout/stderr, exit code and timing methodology for the next run. Distinguish setup-phase placement from execution-phase profiling.
