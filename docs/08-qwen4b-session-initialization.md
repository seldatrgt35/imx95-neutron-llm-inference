# Qwen3-4B Neutron session initialization and memory failure

## Core evidence

A verbose session log, recorded during the Nov 11 investigation and pasted on Nov 12, identifies the model as:

```text
/root/Qwen3-4B-ONNX-INT4/model.onnx
```

The same preserved log includes:

```text
Alloc CMA userspace memory 2048 MB
Alloc 512MB for slot 0
Alloc 512MB for slot 1
Alloc 512MB for slot 2
Alloc 512MB for slot 3
Node(s) placed on [NeutronExecutionProvider]. Number of nodes: 253
```

The node details include low-bit attention projections and feedforward projections from many transformer layers; the operation type is `MatMulNBits`.

The log also records graph transformations and CPU assignments for numerous other operators, consistent with a heterogeneous execution plan. The preserved long trace ends after ONNX Runtime starts saving initialized tensors; it is not itself proof that a session completed and executed successfully.

## Associated but separate report

During the same Qwen experimentation a Neutron session initialization failure `std::bad_alloc` was reported, while a CPU session was reported to load in **33.91 seconds**. These are conversation-reported observations without a complete, matching saved traceback and memory snapshot in the recovered file set. We do not merge them into the verbose log as if one source contained all outcomes.

## What 253 assigned nodes means

`VerifyEachNodeIsAssignedToAnEp` is invoked during session setup. It reports graph placement decisions. The placement count confirms that the ONNX Runtime Neutron EP recognized a substantial set of quantized matrix operations. It does not prove:

- NPU memory allocation completed;
- kernel compilation or prepacking succeeded;
- a forward pass executed;
- resulting logits matched a CPU baseline;
- actual NPU compute time was measured.

## Hypotheses that still require experiment

| Hypothesis | Why plausible | Missing measurement |
|---|---|---|
| CMA allocation / fragmentation | Dedicated buffer slots and multi-GB model assets | CMA snapshots before and after failed allocation |
| Weight preparation memory | ONNX external data and low-bit packing can require transient copies | Peak RSS and allocator traces during prepack |
| Runtime/driver mismatch | Versions changed during setup | Exact build ID, driver ABI and BSP provenance |
| Unsupported model composition | Neutron supports selected operators only | Operator-level session init diagnostics |
| Memory footprint of full Qwen3-4B | 36 transformer layers and growing KV cache | Static/dynamic tensor accounting by subgraph |

None of these hypotheses should be written as the definitive root cause until measured.

## Stronger reproduction

Use a fresh controlled boot. Collect `uname`, `free`, `CmaTotal/CmaFree`, driver messages and environment hashes. Turn on ORT verbose logs and profiling, monitor memory while the model loads, capture exit status and all outputs, then repeat with Neutron disabled using precisely the same model bits and input.

Tools: `scripts/collect_board_information.sh`, `scripts/analyze_neutron_ort_log.py`, `scripts/analyze_ort_profile.py`.
