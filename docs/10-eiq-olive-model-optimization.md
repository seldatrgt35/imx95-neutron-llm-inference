# NXP eIQ Olive, SpinQuant and Qwen recipe exploration

## Actual inspected recipe

The captured host-side command inspected a Qwen3-1.7B configuration file in `~/qwen3-neutron/eiq-olive`:

```text
examples/Qwen3/Qwen3-1.7B/qwen3-1.7B_Spinquant_ONNX_RTN_4bit.json
```

Key properties visible in that recipe:

| Property | Observed value |
|---|---|
| Model ID | `Qwen/Qwen3-1.7B` |
| Host/target accelerator | CPUExecutionProvider |
| Rotation | `SpinQuant`, Hadamard rotation, activation bits 8 |
| ONNX conversion | `ModelBuilder`, fp32 |
| Low-bit pass | `OnnxBlockWiseRtnQuantization` |
| Block size | 32 |
| Accuracy level | 4 |
| Quantization graph format | `QOperator` |
| Exclusions | language-model head MatMul and token embedding Gather |
| Output | External ONNX tensor data enabled |

The recipe also had a dynamic quantization pass and a WikiText-2 perplexity evaluator configured. The upstream `user_script.py` was inspected but is not redistributed here; refer to NXP/eiq-olive and its source license.

## Interpretation

eIQ Olive can compose model optimization passes. A config file is a declarative pipeline; the presence of passes does not prove that all stages ran successfully. Quantization results can change model quality, especially when numerical behavior differs between CPU and accelerator arithmetic.

## Separate paths

- **Qwen3-1.7B eIQ Olive recipe:** prospective host-side optimization and quantized ONNX generation.
- **Qwen3-4B already available ONNX INT4 graph:** board-side loading and Neutron EP exploration.
- **Neutron TFLite compiler:** separate model pathway, not automatically invoked by an ONNX graph.

## Verification plan

Record exact Git commit and `olive` version; model and tokenizer identifiers; command, config, installed dependencies, input/output hashes and directory sizes; perplexity/accuracy before and after conversion. Then run the target converter appropriate to the specific model format and BSP.
