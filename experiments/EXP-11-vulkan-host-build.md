# EXP-11: Vulkan llama.cpp host cross-compile

**Research period:** November 2026  
**Evidence type:** Captured terminal  
**Status:** Recorded observation; not a fresh board test

## Objective

Prepare SPIR-V/shaderc and configure llama.cpp for AArch64 sysroot.

## Observed result

CMake configuration completed and generated build files; target inferencing not proven.

## Primary source

../evidence/terminal/20261110-124019-host-vulkan-cross-compilation.log

## Interpretation

This record documents the specific observation above; it does not infer successful Qwen3-4B Neutron acceleration. Inspect the source before extending the claim to another BSP, model size or execution provider.

## Remaining verification gate

Successful compilation, deployed executable and Vulkan model-generation benchmark.

## Reproducibility notes

Collect model checksums, BSP/DTB/firmware identifiers, compiler/ORT versions, exact command, stdout/stderr, exit code and timing methodology for the next run. Distinguish setup-phase placement from execution-phase profiling.
