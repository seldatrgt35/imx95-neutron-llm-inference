# Experimental four-layer hybrid ONNX partition

## Goal

Partition Qwen3-4B into a short prefix (candidate Neutron + CPU fallback) and a CPU-only suffix to reduce the accelerator memory burden. This is an experimental analysis approach and should not be represented as an operational split inference pipeline.

## Design assumptions

The recovered Python scripts assume 36 layers and a split boundary at layer 4. A `SkipLayerNorm` node at the start of layer 4 consumes two tensors output by layer 3. This boundary is **not necessarily a single hidden-state tensor**. The program collects dependencies for the boundary, logits and KV-cache outputs.

```text
input_ids, position data, past KV
      |
      v
    layers 0-3 ---> boundary tensor A + boundary tensor B
      |                                      |
      '---> present KV 0..3                v
                                       layers 4..35
                                           |
                                  logits + present KV 4..35
```

## Recovered source versions

- `src/archived/split_qwen_hybrid_v1.py`: first preserved uploaded version using symbolic links for external data.
- `src/archived/split_qwen_hybrid_v2.py`: later preserved uploaded version using hard links with more defensive handling; its success is **not** verified.

These files are included unchanged to preserve the real investigation history. Do not treat them as robust general-purpose ONNX splitters.

## Recorded commands and results

The captured session shows `python3 -m py_compile /root/split_qwen_hybrid.py` succeeding. Subsequent execution reported:

```text
Boundary: ['/model/layers.3/post_attention_layernorm/output_3',
 '/model/layers.3/mlp/down_proj/MatMul/output_0']
Shared computation nodes: 11
Checking: qwen_npu_prefix.onnx
```

It then failed with an ONNX validation error involving an unregistered `SimplifiedLayerNormalization` operator in opset context 21. Another captured error rejected checking external tensor data via a file with multiple hard links. These are distinct problems:

1. **Operator schema**: ONNX's generic checker may not understand a custom operator or incorrect domain registration even when ONNX Runtime can run it.
2. **External data**: ONNX external tensor references are relative to a model directory. Linking them must preserve offsets, byte lengths and the expected security model.
3. **Graph overlap**: shared computation nodes across halves require deliberate duplication or a common subgraph/interface, otherwise the split can be wrong.
4. **Decoder state**: KV-cache contracts and tensor names must be reconciled for every token step.

## Planned correctness validation

A valid implementation should load both models, check all input/output types, run one-step forward passes on identical input, combine the prefix and suffix, compare logits with the original full CPU session within a specified numerical tolerance, and then test multi-token KV-cache updates.

The current versions do not provide that proof. Deleting a checker call or bypassing an external-data safeguard is not a correctness fix.
