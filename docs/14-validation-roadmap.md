# Verification roadmap

## Immediate next experiment: a minimal quantized ONNX kernel

**Objective:** show one successfully executed and profiled `MatMulNBits` on Neutron, not simply an initialized provider.

1. Capture exact FRDM model and revision, BSP, kernel, DTB hash, driver and ORT version.
2. Preserve the BSP ONNX Runtime package; use a clean compatible environment.
3. Build/select a minimal supported low-bit ONNX model and external-data bundle.
4. Run the local offline Neutron weight prepacker and retain before/after hashes.
5. Create the session with Neutron then CPU fallback; save verbose logs and a profile.
6. Run deterministic data and compare CPU/NPU outputs within a justified tolerance.
7. Record NPU performance-counter behavior while the kernel executes.
8. Repeat with multiple input shapes to expose supported/unavailable cases.

**Pass:** same model, NPU kernel event, reproducible output and hardware activity. **Fail:** mere provider listing or node assignment with no successful execution.

## Medium-term experiment: constrained Qwen subgraph

Extract a small attention/MLP segment with explicit input/output types and no ambiguous external-data links. Validate numerically on CPU before attempting NPU. Track allocations, NPU workspace and fallbacks. Expand layers only when the previous stage passes.

## Full 4B hybrid proof

- Run original CPU graph and hybrid graph on identical inputs; compare logits.
- Confirm boundary tensors and full KV-cache semantics across many generation steps.
- Track total resident memory, CMA and session initialization time.
- Profile each stage, including host/device copy and synchronization cost.
- Provide a matched CPU baseline using the exact same tokenizer, batch/sequence, decoding policy and timing definition.

## Reporting quality gate

Before using the claim 'Qwen3-4B accelerated by Neutron', require successful on-device generation with a matching trace proving a non-zero set of Qwen `MatMulNBits` kernel events executed under Neutron EP, correlated with NPU hardware counters and documented numerical agreement. Report the accelerated node count, CPU fallbacks, memory footprint, total latency and uncertainty.
