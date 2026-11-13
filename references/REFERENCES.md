# External references and licensing notes

Sources are external technical background. Citation of a workflow does not establish that the workflow was executed in this project. Retrieval/inspection cutoff: 13 November 2026.

1. [NXP eIQ GenAI Flow Demonstrator](https://github.com/nxp-appcodehub/dm-eiq-genai-flow-demonstrator) — board compatibility, conversational AI pipeline, memory/DTB requirements and vendor baseline.
2. [NXP eIQ GenAI Flow README](https://github.com/nxp-appcodehub/dm-eiq-genai-flow-demonstrator/blob/main/eiq_genai_flow/README.md) — details on `--use-neutron`, supported models and BSP support.
3. [NXP eIQ Olive](https://github.com/NXP/eiq-olive) — NXP-specific Olive passes and model recipes; original example scripts must be accessed under their source license.
4. [NXP Neutron conversion overview](https://eiq.nxp.com/learning-hub/convQuant/neutron.html) — quantized TFLite-to-Neutron workflow.
5. [NXP eIQ Neutron SDK](https://eiq.nxp.com/learning-hub/tools/neutronSdk/index.html) — SDK installation and conversion concepts.
6. [NXP UG10166 ONNX model test](https://docs.nxp.com/bundle/UG10166/page/topics/onnx_model_test.html) — ONNX Runtime support and testing context.
7. [ONNX Runtime Execution Providers](https://onnxruntime.ai/docs/execution-providers/) — execution provider model and registration.
8. [ONNX Runtime profiling documentation](https://onnxruntime.ai/docs/performance/tune-performance/profiling-tools.html) — profiling and kernel timing.
9. [ONNX external data](https://onnx.ai/onnx/repo-docs/ExternalData.html) — model external tensor representation.
10. [Microsoft Olive](https://microsoft.github.io/Olive/) — model optimization and passes.
11. [llama.cpp](https://github.com/ggml-org/llama.cpp) — alternate CPU/GPU runtime; build and model licensing separate.
12. [NXP community discussion on CPU/NPU result differences](https://community.nxp.com/t5/Generative-AI-LLMs/i-MX95-Neutron-NPU-CPU-discrepancy-on-one-answer-in-four-with/m-p/2410859) — external community observation on numerical differences, **not a result of this project**.

## Provenance and copyright

No vendor driver source, model weights, proprietary BSP distribution or compiled SDK is bundled. A small amount of user-origin code and user terminal text is preserved, with some third-party source excerpts removed from the public archive. Model licenses, NXP SDK redistribution terms and licenses for copied code must be reviewed separately before public distribution. This repository intentionally does not apply a license to external works or assert ownership over them. The repository owner should choose a suitable license for genuinely original materials.
