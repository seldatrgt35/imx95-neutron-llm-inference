# Research scope, provenance and confidence

## Purpose

This project reconstructs a development investigation from historical terminal pastes, recovered Python scripts, and conversational observations. No fresh model download, NPU performance run, or on-target compilation has been performed to generate this archive.

## Evidence classes

| Class | Criteria | Example |
|---|---|---|
| E1: captured output | Command and response appear in the preserved terminal file | `MatMul_0_kernel_time -> CPUExecutionProvider` |
| E2: reported outcome | Directly reported in a prior technical session but underlying full log unavailable | `std::bad_alloc` and 33.91 s CPU session load |
| E3: computed/derived | Analysis generated from E1/E2 data with its script | Count nodes assigned to Neutron from ORT verbose log |
| E4: documentation | Official upstream requirement or technical description | NXP extended-CMA and matching-BSP requirement |
| E5: proposed | Reproduction script or next planned experiment, not yet executed | `scripts/inspect_onnx_graph.py` on an accessible model |

Do not promote E2/E4/E5 into E1 claims. In particular, a documented conversion command does not mean that command was successfully executed in this project.

## Source inventory and integrity

There are 13 indexed dated terminal/research pastes; 11 are included as sanitized terminal captures. A vendor-licensing page and broad verbatim README excerpts were deliberately excluded from public redistribution. Other proprietary source sections were redacted rather than copied. Source SHA-256 hashes and transformation notes appear in `evidence/manifest.json`.

Two uploaded Python graph-splitting revisions are preserved byte-for-byte in `src/archived/`; they should be treated as historical source, not production code. A third script, the elementary Neutron probe, was transcribed from a `cat >` heredoc in the captured November 10 terminal session.

### Specific evidence map

- **Nov 10 board boot:** `evidence/terminal/20261110-081607-boot-weston-console.log`
- **Nov 10 Vulkan host configuration:** `evidence/terminal/20261110-124019-host-vulkan-cross-compilation.log`
- **Nov 10 CPU fallback:** `evidence/terminal/20261110-140415-onnxruntime-matmul-cpu-fallback.log`
- **Nov 11 driver and prepack exploration:** `evidence/terminal/20261111-064922-neutron-driver-weight-packing-investigation.log`
- **Nov 11 LiteRT example:** `evidence/terminal/20261111-082645-litert-npu-mobilenet-validation.log`
- **Nov 11 verbose Qwen assignment, saved on Nov 12:** `evidence/terminal/20261112-113926-qwen-ort-verbose-253-neutron-nodes.log`
- **Nov 12 Olive recipe:** `evidence/terminal/20261112-083614-eiq-olive-qwen-recipe-investigation.log`
- **Nov 12 hybrid failures:** `evidence/terminal/20261112-122647-hybrid-graph-partitioning-errors.log`

The filename date is the capture/paste timestamp; commands inside a paste can show an earlier runtime timestamp.

## Environmental variability

Observed environments included ONNX Runtime 1.22.0 and 1.24.3, at least two CMA configurations, and Python 3.13/3.14 references. These are not a single reproducible image. Comparison tables must pair every benchmark with the actual software, BSP, DTB and allocator state from that run.

## Honest completion criteria

- Hardware NPU recognized: **achieved**.
- ONNX Runtime EP enumerated: **achieved**.
- Standard FP32 MatMul on NPU: **not achieved** in recorded unit test.
- `MatMulNBits` node assignment to Neutron: **observed**.
- Qwen3-4B full NPU session successful: **not established**.
- Accurate CPU/NPU timing attribution: **not established**.
- Hybrid graph split validated and end-to-end decoded: **not established**.
