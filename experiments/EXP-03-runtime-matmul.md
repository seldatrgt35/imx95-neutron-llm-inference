# EXP-03: Plain ONNX MatMul runtime provider probe

**Research period:** November 2026  
**Evidence type:** Captured terminal  
**Status:** Recorded observation; not a fresh board test

## Objective

Run a synthetic MatMul model with Neutron then CPU and profile execution.

## Observed result

Output shape `(1,256)`; `MatMul_0_kernel_time -> CPUExecutionProvider`.

## Primary source

../evidence/terminal/20261110-140415-onnxruntime-matmul-cpu-fallback.log

## Interpretation

This record documents the specific observation above; it does not infer successful Qwen3-4B Neutron acceleration. Inspect the source before extending the claim to another BSP, model size or execution provider.

## Remaining verification gate

A properly supported low-bit MatMulNBits example with NPU kernel events.

## Reproducibility notes

Collect model checksums, BSP/DTB/firmware identifiers, compiler/ORT versions, exact command, stdout/stderr, exit code and timing methodology for the next run. Distinguish setup-phase placement from execution-phase profiling.
