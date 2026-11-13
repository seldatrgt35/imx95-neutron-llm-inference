# Qwen3 ONNX, quantization and operator inspection

## Model under test

The board-side model path seen in the investigation was:

```text
/root/Qwen3-4B-ONNX-INT4/model.onnx
```

An inspection showed the ONNX graph file was approximately 410 KiB, with external tensor data stored separately (about 3.9 GB according to the source script's comment and session context). In large ONNX models, a small `.onnx` graph file does not imply small total weights.

The archived graph splitter assumes **36 transformer layers** and found an ONNX boundary associated with the `SkipLayerNorm` at the start of layer 4. A reported graph inventory included 253 `MatMulNBits` and 36 `GroupQueryAttention` nodes. Exact counts depend on the specific export and graph transformations, so the model hash is required for cross-run comparisons.

## FP16 versus INT4

Quantization lowers the representation precision of certain tensors. For a 4-bit weight representation, the idealized storage is roughly one quarter of a 16-bit representation for the same count of values, before scales, zero points, metadata, padding and packing overhead. The ONNX graph operator `MatMulNBits` expresses low-bit matrix multiplication; it is not itself a guarantee of accelerator compatibility.

## Sequence of operations we investigated

```text
Hugging Face model / optimization recipe
         |
    ONNX export
         |
  Blockwise low-bit quantization
         |
  MatMulNBits nodes, scales and quantized weight data
         |
  Offline Neutron-specific weight prepacking (separate step)
         |
  ONNX Runtime model session with Neutron/CPU EPs
         |
  Per-op placement verification and hardware profiling
```

The existence and theoretical order of these steps must not be confused with their successful completion. Our captured research inspected eIQ Olive recipes and the prepack utility; it did not preserve a successful complete Qwen3-4B NPU deployment pipeline.

## Model inspection protocol

On the host or target with compatible `onnx`:

```bash
python3 scripts/inspect_onnx_graph.py /root/Qwen3-4B-ONNX-INT4/model.onnx
```

The helper loads external-data **metadata only**, enumerates node op types, counts quantized MatMuls, and reports referenced data-file names and their existence; it does not load the multi-GB weights into RAM.

## KV cache and splitting concern

The full decoder can expose `past_key_values` inputs, `present.*.key`/`present.*.value` outputs, position information, logits and attention state. A prefix/suffix boundary needs correct types, shapes, ordering and cache updates for every decoding step; simply cutting an ONNX graph does not automatically create a working autoregressive generator.
