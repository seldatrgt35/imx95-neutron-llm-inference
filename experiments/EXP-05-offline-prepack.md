# EXP-05: ONNX Neutron offline weight prepacking discovery

**Research period:** November 2026  
**Evidence type:** Captured inspection  
**Status:** Recorded observation; not a fresh board test

## Objective

Inspect installed Neutron ONNX converter and its driver packing interface.

## Observed result

Found script, MatMulNBits selection and libNeutronDriver dependency; no successful custom model conversion trace.

## Primary source

../evidence/terminal/20261111-064922-neutron-driver-weight-packing-investigation.log

## Interpretation

This record documents the specific observation above; it does not infer successful Qwen3-4B Neutron acceleration. Inspect the source before extending the claim to another BSP, model size or execution provider.

## Remaining verification gate

Successful converter exit with before/after model hashes and an NPU-executed kernel.

## Reproducibility notes

Collect model checksums, BSP/DTB/firmware identifiers, compiler/ORT versions, exact command, stdout/stderr, exit code and timing methodology for the next run. Distinguish setup-phase placement from execution-phase profiling.
