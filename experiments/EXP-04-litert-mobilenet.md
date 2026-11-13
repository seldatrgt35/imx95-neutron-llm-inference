# EXP-04: LiteRT NPU dispatch smoke test

**Research period:** November 2026  
**Evidence type:** Captured terminal  
**Status:** Recorded observation; not a fresh board test

## Objective

Run quantized MobileNet example with NPU requested and verbose logging.

## Observed result

NPU accelerator registered, CPU accelerator also present; five runs averaged 116.480 ms.

## Primary source

../evidence/terminal/20261111-082645-litert-npu-mobilenet-validation.log

## Interpretation

This record documents the specific observation above; it does not infer successful Qwen3-4B Neutron acceleration. Inspect the source before extending the claim to another BSP, model size or execution provider.

## Remaining verification gate

Per-operation delegate attribution and Neutron counter activity.

## Reproducibility notes

Collect model checksums, BSP/DTB/firmware identifiers, compiler/ORT versions, exact command, stdout/stderr, exit code and timing methodology for the next run. Distinguish setup-phase placement from execution-phase profiling.
