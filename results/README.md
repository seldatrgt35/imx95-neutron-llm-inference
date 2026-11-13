# Measurement policy

`observations.csv` contains one row per reported observation. Do not aggregate unlike experiments. The interactive Qwen text-generation timings are an application report and do not certify CPU/NPU kernel attribution.

- The November 10 standalone MatMul generated a result on **CPUExecutionProvider** despite a Neutron provider appearing in the session providers list.
- The November 11 Qwen load reached **253 nodes assigned to NeutronExecutionProvider**, but session initialization was not established as successful in that attempt.
- A `std::bad_alloc` failure for the Qwen NPU session was reported separately during the investigation; do not infer it happened in the exact archived log unless the line appears there.
- The November 11 LiteRT MobileNet example registered the NPU accelerator, ran five inferences, and produced classifier output. It also initialized a CPU accelerator; the preserved transcript alone is not a per-op assignment proof.
- The chat benchmark's `NPU prefix time` and `CPU suffix time` labels must not be reinterpreted as a hardware profiler report.

No CPU-vs-NPU speedup factor is claimed, because no matched, verified pair was recorded.
