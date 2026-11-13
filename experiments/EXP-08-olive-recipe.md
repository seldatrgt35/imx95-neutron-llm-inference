# EXP-08: eIQ Olive Qwen3 model optimization recipe

**Research period:** November 2026  
**Evidence type:** Captured terminal  
**Status:** Recorded observation; not a fresh board test

## Objective

Inspect Qwen3-1.7B SpinQuant and RTN quantization configuration.

## Observed result

Found settings for blockwise RTN, ModelBuilder, dataset/evaluation and external data; not a completed export.

## Primary source

../evidence/terminal/20261112-083614-eiq-olive-qwen-recipe-investigation.log

## Interpretation

This record documents the specific observation above; it does not infer successful Qwen3-4B Neutron acceleration. Inspect the source before extending the claim to another BSP, model size or execution provider.

## Remaining verification gate

Pinned Olive commit, run output, quantization accuracy and model bundle.

## Reproducibility notes

Collect model checksums, BSP/DTB/firmware identifiers, compiler/ORT versions, exact command, stdout/stderr, exit code and timing methodology for the next run. Distinguish setup-phase placement from execution-phase profiling.
