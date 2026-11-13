# Failure analysis and causal boundaries

## 1. Neutron device exists but standard MatMul runs on CPU

**Evidence:** `/dev/neutron0`, Neutron EP listed, profiling still labels MatMul CPU. **Explanation:** provider registration is not operator support. This test did not use the device-specific supported graph representation. **Next experiment:** construct a minimal compatible quantized MatMulNBits model and run offline prepacking with an appropriate runtime.

## 2. Neutron buffer allocation failure

**Evidence:** `NEUTRON_IOCTL_BUFFER_CREATE failed!: Cannot allocate memory` in the small test; separate reported `std::bad_alloc` when attempting the large model. **Possible causes:** CMA budget, allocation alignment, fragmentation or ABI/runtime behavior. **Do not conflate:** the small test's IOCTL error is not automatically the cause of the separate Qwen `std::bad_alloc`.

## 3. ONNX graph checker rejects custom operator

**Evidence:** `ValidationError: No Op registered for SimplifiedLayerNormalization ...` during prefix checking. **Reason to investigate:** operator domain/opset and checker/runtime schema differences. **Next action:** inspect node domains and opset imports, preserve operator schemas or use an appropriate checker configured for custom ops.

## 4. ONNX checker rejects linked external weights

**Evidence:** `Data of TensorProto ... has multiple hard links, indicating a potential hardlink attack`. **Reason:** ONNX checker enforces safety while reading external tensors. **Next action:** use authorized copies, correct external data references, and separate metadata-only graph inspection from validation of external tensor payloads. Never bypass checks as a correctness claim.

## 5. Shared computations across a split

**Evidence:** `Shared computation nodes: 11`. **Risk:** computational overlap may be intentional (common inputs/constants) or may expose an invalid partition. **Next action:** inspect exact dependency sets, avoid double-processing side effects and compare full and hybrid CPU logits.

## 6. LiteRT recognizes NPU but also initializes CPU delegate

**Evidence:** `NpuAccelerator` registered; XNNPACK CPU delegate also created. **Risk:** accelerators can coexist and partition execution. **Next action:** capture operator placement or instrument NPU counters during a controlled run.

## 7. Vulkan configuration success does not equal inference success

**Evidence:** CMake generated `build-imx95` files. **Missing:** executable compiled, deployed and tested with a compatible Vulkan device driver. **Next action:** verify compiled binary, target loader features and actual model decode.

## 8. Toolchain mismatch risk

**Evidence:** ONNX Runtime 1.22.0 / 1.24.3 and Python 3.13 / 3.14 appeared at different stages. **Risk:** silently mixing BSP modules and pip wheels. **Next action:** capture a pinned software bill of materials and validate each environment separately.

## Priority and status

Do not turn unexplained failures into one global 'NPU cannot run LLMs' conclusion. The investigation exposes multiple independent software/hardware compatibility issues that require smaller controlled tests.
