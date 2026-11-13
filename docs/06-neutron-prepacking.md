# Neutron compiler and ONNX INT4 weight-prepacking investigation

This was a central technical question during the project: **Did we compile the custom Qwen model, or did the runtime require a different ONNX weight-packing step?** The preserved records support the investigation of those paths, but not a verified completed Qwen weight-packing operation.

## Two separate toolchains

### A. Neutron SDK/compiler for quantized TFLite models

The standard eIQ Neutron SDK pipeline expects a compatible quantized TFLite input and prepares model graph, memory layout and hardware-specific execution format. NXP eIQ Olive exposes a `NeutronConversion` pass for this route. It is used in several edge-model workflows, but it is **not interchangeable with the Qwen ONNX MatMulNBits preprocessing path**.

```text
Quantized TFLite --> NeutronConversion / SDK --> NPU-compatible TFLite --> delegate/runtime
```

### B. Offline ONNX MatMulNBits weight conversion

The board contained a Python utility at approximately:

```text
/usr/lib/python3.13/site-packages/onnxruntime/tools/convert_ort_models_to_neutron.py
```

Another board configuration exposed the utility under Python 3.14. Inspection of its command-line parser and implementation showed:

- Selection of `MatMulNBits` nodes for conversion.
- Offline packing of low-bit weights into a Neutron-specific layout.
- A dependency on `libNeutronDriver.so`, loaded through Python `ctypes`.
- An interface advertised as `-i/--input`, `-o/--output`, and `-j/--jobs`.
- A native driver packing interface referred to internally as the Neutron BMM prepack API.

The original user investigation also examined fixed-point/scaling helpers and contiguous weight buffers in this vendor tool. The vendor's Python source itself is not redistributed in this archive; inspect the locally installed package and its license.

**Example command to inspect availability (not a recorded successful Qwen conversion):**

```bash
python3 -m onnxruntime.tools.convert_ort_models_to_neutron --help
```

**Potential direct local invocation based on the observed parser, not executed by the archive generator:**

```bash
python3 /usr/lib/python3.14/site-packages/onnxruntime/tools/convert_ort_models_to_neutron.py \
  --input /path/to/quantized/model.onnx \
  --output /path/to/neutron-prepacked/model.onnx \
  --jobs 2
```

Path and CLI acceptance must be verified on the installed BSP tool. Before conversion, ensure the output path is distinct from input, the full external-data bundle exists and adequate disk/RAM/CMA budget is available. Do not overwrite source weights.

## What 'packing' means technically

INT4 quantization describes numerical precision. Packing describes physical arrangement of quantized values and per-block metadata. A device-specific packing routine may reorder tiles, align channels, combine nibbles into bytes, arrange scales/zero points and prepare accelerator-specific data structures. Exact format depends on the driver and SDK revision and is not reverse-engineered from our logs.

```text
ONNX MatMulNBits tensors
  |-- quantized nibble storage
  |-- per-block scales / optional zero points
  '--> driver prepack routine --> Neutron-specific packed buffers or model data
                                      |
                              NeutronExecutionProvider
```

## What evidence did we obtain?

1. The offline script existed on the image and matched `MatMulNBits` in the inspected implementation.
2. The script described offline packing in its command-line interface.
3. The expected Neutron driver library was installed.
4. A later Qwen ONNX session showed that ONNX Runtime tried to assign 253 low-bit MatMul nodes to Neutron.

**Missing proof:** a successful conversion invocation, complete converter stdout/stderr, model before/after hashes, valid prepacked output graph, or on-device execution profile that can be tied to that output. None is manufactured here.

## Compiler verification checklist

- [ ] Identify exact board/BSP/Neutron EP version and model export revision.
- [ ] Hash graph and external weight files before conversion.
- [ ] Run the installed offline converter with a small supported `MatMulNBits` example.
- [ ] Save converter stdout, stderr, exit code and output model files to an external drive.
- [ ] Confirm node types and attribute compatibility before session creation.
- [ ] Capture ONNX Runtime provider assignment and profiling after successful inference.
- [ ] Measure Neutron performance counters during execution.
- [ ] Compare output numerically with CPU baseline at fixed seed and tolerance.

## Why this matters

'Quantized model available', 'Neutron EP reported', and 'NPU ready' are three different milestones. Weight packing and execution depend on exact runtime and hardware compatibility. The project advanced as far as inspection and a failing large-model initialization, but the complete verified NPU port remains an engineering task.

Vendor sources: `references/REFERENCES.md`.
