# ONNX Runtime provider enumeration versus execution

## Baseline experiment from November 10

The user ran `test_neutron.py` using an ONNX model at `/root/matmul_test.onnx`, with this provider ordering:

```python
providers=["NeutronExecutionProvider", "CPUExecutionProvider"]
```

Observed output:

```text
Session providers: ['NeutronExecutionProvider', 'CPUExecutionProvider']
Inference successful!
Output shape: (1, 256)
MatMul_0_kernel_time -> CPUExecutionProvider
```

This is a useful negative control: the NPU EP was present but the elementary `MatMul` executed on CPU. The session also printed a warning that only `NeutronGraph` ops would be assigned to NPU, and `NEUTRON_IOCTL_BUFFER_CREATE` reported allocation failure. The exact ORT build and graph preparation explain why naive provider ordering was inadequate.

The original script is reconstructed in `src/archived/test_neutron_matmul_2026_11_10.py`; the source stdout/stderr is saved in `evidence/terminal/20261110-140415-onnxruntime-matmul-cpu-fallback.log`.

## How we proved fallback

ONNX Runtime profiling JSON provides events with an `args.provider` field. The investigation parsed the file and observed an explicit `CPUExecutionProvider` placement for the tested kernel.

For a saved profile, use:

```bash
python3 scripts/analyze_ort_profile.py onnxruntime_profile_YYYY-MM-DD_HH-MM-SS.json
```

A useful verification must distinguish:

1. **Provider installed**: `onnxruntime.get_available_providers()`.
2. **Providers chosen**: `session.get_providers()`.
3. **Graph node assignment**: ONNX Runtime verbose setup log.
4. **Actual execution**: profile events from an initialized and executed session.
5. **Hardware activity**: Neutron performance counters during the same workload.

Failing at any later stage means earlier stages alone do not certify acceleration.

## Why this test did not refute Qwen INT4 support

A plain FP32 `MatMul` graph may not be transformed to the accelerator-specific format supported by the installed Neutron EP. Qwen uses quantized `MatMulNBits` nodes and a different packing route. Therefore, the CPU fallback is an expected test outcome under some configurations; it is not direct evidence that Qwen INT4 cannot be delegated.
