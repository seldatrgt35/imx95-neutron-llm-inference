# Evidence index

| Evidence ID | Date | Observation | Confidence |
|---|---|---|---|
| EV-01 | Nov 10 | NXP Linux boot and Weston startup failure | Captured terminal |
| EV-02 | Nov 10 | Host-side AArch64 Vulkan cross-compile CMake configuration | Captured terminal |
| EV-03 | Nov 10 | ONNX Runtime MatMul succeeds, but profiler places it on CPU | Captured terminal |
| EV-04 | Nov 11 | Device file and Neutron boot log; LiteRT NPU registration and MobileNet inference | Captured terminal |
| EV-05 | Nov 11 | `libNeutronDriver.so` and offline packing script investigated | Captured terminal and vendor tool inspection |
| EV-06 | Nov 11 | Full Qwen3-4B: 253 MatMulNBits nodes assigned to Neutron at session setup | Captured verbose log |
| EV-07 | Nov 12 | eIQ Olive Qwen3-1.7B SpinQuant/RTN recipe inspected | Captured terminal |
| EV-08 | Nov 12 | Four-layer hybrid ONNX split attempts and validation failures | Captured terminal and recovered scripts |
| EV-09 | Nov 12 | Qwen3-4B interactive generation and timing | Conversation-reported, summary retained |

Mapping from IDs to specific source files is in `docs/00-research-method.md` and `evidence/manifest.json`.
