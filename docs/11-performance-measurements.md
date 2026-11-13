# Performance measurement notes

## Text generation sample

A single application output from the project reported:

| Metric | Measurement |
|---|---:|
| Prompt tokens | 21 |
| Generated tokens | 128 |
| Time to first token | 1.976 s |
| Prefill inference | 1.968 s |
| Total generation | 47.310 s |
| Stage labelled NPU prefix | 19.504 s |
| Stage labelled CPU suffix | 26.632 s |
| Decode speed | 2.80 tokens/s |

These numbers are quoted from a conversational test output. There is no claim that all measures use precisely the same clock interval or that stage names describe actual hardware kernel placement. For example `19.504 + 26.632` does not exactly equal 47.310; instrumentation overhead and rounding or semantics are not fully documented.

## Comparative observations

| Test | Result | Attribution |
|---|---|---|
| Simple FP32 MatMul | Successfully ran with shape `(1,256)` | Explicitly **CPUExecutionProvider** |
| LiteRT quantized MobileNet | 116.480 ms mean over 5 runs | NPU delegate initialized, mixed accelerator stack; per-op attribution unverified |
| Qwen3-4B ONNX session setup | 253 MatMulNBits assigned to Neutron EP | **Static assignment only** |
| Qwen3-4B CPU session | Reported initialization in 33.91 s | Separate conversation observation |
| Qwen3-4B chat | 2.80 tokens/s in one recorded sample | Application timing; device attribution unverified |

None of these values is a fair apples-to-apples speedup denominator for the others.

## Correct benchmark protocol

Use the same model artifacts, input tokens, generation settings, and prompt lengths across EP variants. Record: operating temperature, device governor, CPU and NPU clocks, runtime versions, CMA, RSS, data transfer overhead, cold/warm state, first-token latency, per-token latency, output correctness, tokenization time, sampling policy, and session setup time. Run multiple repetitions and report median, distribution and confidence intervals.

Avoid presenting the first working text response as a production throughput guarantee.

## Structured data

`results/observations.csv` is a machine-readable table with one row for each observed metric and a provenance field. Newly authored summary script: `scripts/summarize_observations.py`.
