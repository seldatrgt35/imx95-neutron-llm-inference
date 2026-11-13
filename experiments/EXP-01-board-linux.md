# EXP-01: Board and serial Linux access

**Research period:** November 2026  
**Evidence type:** Captured terminal  
**Status:** Recorded observation; not a fresh board test

## Objective

Read device-tree model, system resource reports and boot transcript.

## Observed result

Linux shell and NXP board identification observed; Weston service failed.

## Primary source

../evidence/terminal/20261110-081607-boot-weston-console.log

## Interpretation

This record documents the specific observation above; it does not infer successful Qwen3-4B Neutron acceleration. Inspect the source before extending the claim to another BSP, model size or execution provider.

## Remaining verification gate

A fresh boot log with exact image hash and clean service status.

## Reproducibility notes

Collect model checksums, BSP/DTB/firmware identifiers, compiler/ORT versions, exact command, stdout/stderr, exit code and timing methodology for the next run. Distinguish setup-phase placement from execution-phase profiling.
