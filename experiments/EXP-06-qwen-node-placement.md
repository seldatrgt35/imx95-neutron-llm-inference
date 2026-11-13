# EXP-06: Qwen3-4B Neutron node placement

**Research period:** November 2026  
**Evidence type:** Captured verbose log  
**Status:** Recorded observation; not a fresh board test

## Objective

Load ONNX INT4 Qwen graph with verbose ONNX Runtime Neutron EP.

## Observed result

253 MatMulNBits nodes assigned to Neutron during session setup; trace did not prove completed inference.

## Primary source

../evidence/terminal/20261112-113926-qwen-ort-verbose-253-neutron-nodes.log

## Interpretation

This record documents the specific observation above; it does not infer successful Qwen3-4B Neutron acceleration. Inspect the source before extending the claim to another BSP, model size or execution provider.

## Remaining verification gate

Session `Initialize` success, run success, per-op Neutron profile and numerical match.

## Reproducibility notes

Collect model checksums, BSP/DTB/firmware identifiers, compiler/ORT versions, exact command, stdout/stderr, exit code and timing methodology for the next run. Distinguish setup-phase placement from execution-phase profiling.
