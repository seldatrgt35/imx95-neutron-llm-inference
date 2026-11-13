# Neutron software stack on i.MX95

## What was detected

The target software inventory reported the following shared libraries:

```text
/usr/lib/libneutron_delegate.so
/usr/lib/liblitert_neutron_delegate.so
/usr/lib/libNeutronDriver.so
/usr/lib/libLiteRtDispatch_NxpNeutron.so
/usr/lib/libLiteRt.so
```

The board also exposed `/bin/neutron_perf.sh` and ONNX Runtime build artifacts under `/usr/bin/onnxruntime-1.24.3/` in a later state. Presence is not proof of compatibility or performance.

## Distinct inference pathways

**LiteRT/TFLite**: An application loads a `.tflite` model; the LiteRT accelerator infrastructure can load the NXP dispatch library to route compatible model segments through the Neutron delegate. A Neutron compiler/conversion phase is used for TFLite-based deployment workflows.

**ONNX Runtime/Neutron EP**: An ONNX application registers `NeutronExecutionProvider` and `CPUExecutionProvider`. ONNX Runtime partitions the graph based on operator and implementation capabilities. The `MatMulNBits` path can use a separate offline conversion/weight-prepacking routine (`convert_ort_models_to_neutron.py`) and driver interface.

**CPU fallback**: Nodes unsupported by Neutron remain on CPU. The EP names returned by `session.get_providers()` indicate available providers configured for the session, not that a particular node ran on each of them.

## What LiteRT actually demonstrated

The captured `label_image_litert` example loaded a quantized MobileNet model and registered `NpuAccelerator`; the dispatch library reported NXP vendor information. It also registered `CpuAccelerator` and created a CPU XNNPACK delegate. The output contained five classification results and a measured average of 116.480 ms over five invocations.

This is successful LiteRT example execution with NPU integration visible. A rigorous claim of *which model operators* actually executed on Neutron still needs dispatch-level or hardware profiling.

## Why a Neutron debug monitor matters

A kernel debugfs counter file was inspected at `/sys/kernel/debug/neutron/perf_counters`; `/bin/neutron_perf.sh` reads these counters to estimate NPU utilization. When collecting such evidence:

1. Record the idle baseline.
2. Run a single controlled inference workload.
3. Record counter movement during the workload.
4. Correlate hardware activity with runtime per-op profiling.

Background tasks or other clients can modify counters, so hardware activity is necessary corroboration, not sufficient attribution by itself.
