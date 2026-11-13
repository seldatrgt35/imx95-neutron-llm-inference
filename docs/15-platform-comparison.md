# Model and platform decision matrix

| Target / model | Intended role | Research status | Technical consideration |
|---|---|---|---|
| FRDM-i.MX95 / Danube-500M | Vendor reference baseline | Documentation explored | Curated path via eIQ GenAI Flow |
| FRDM-i.MX95 / Qwen3-1.7B | Intermediate custom-quantization candidate | eIQ Olive recipe inspected | Recipe must be executed and validated separately |
| FRDM-i.MX95 / Qwen3-4B | Main investigation target | ONNX INT4 session placement, CPU generation, partition work | Large transient working set and unsupported operator risk |
| FRDM-i.MX95 / LiteRT MobileNet | Accelerator smoke test | Example ran with NPU dispatch registered | Not an LLM benchmark; mixed CPU/NPU setup |
| FRDM-i.MX95 / llama.cpp Vulkan | GPU fallback | Host build configuration observed | No target inference proof |
| SolidRun i.MX8MP / local LLM | Alternative board comparison | Early feasibility discussion | Vulkan/CPU limitations, no validated NPU LLM result |
| Ara240 DNPU | External accelerator option | Documentation discussed | Requires compatible external hardware; not part of FRDM built-in Neutron |

Selection should be based on measured end-to-end throughput, response quality, startup latency, model and KV memory, power and reproducibility, not parameter count alone.
