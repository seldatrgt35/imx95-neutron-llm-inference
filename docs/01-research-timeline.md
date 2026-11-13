# Engineering timeline and decision log

## Phase A: Hardware and fallback pathways (Nov 9–10, 2026)

The project initially evaluated CPU/GPU/NPU possibilities. A SolidRun i.MX8MP board was considered, and device capabilities such as Vulkan queue flags and missing shader integer features were investigated in conversation. This earlier SolidRun work has no complete original terminal transcript in the recovered file set; it is recorded as prior exploratory context only.

On the FRDM-i.MX95, serial access and Linux boot were observed. The Nov 10 boot capture includes the NXP Linux login prompt and a Weston service failure. The graphical desktop error was not proof that the inference stack could not work.

The host prepared an ARM64 cross-compilation environment, `SPIRV-Headers`, shaderc and `llama.cpp` with Vulkan enabled. CMake reported successful configuration, but a working Vulkan inference run was not captured.

**Decision:** pursue the built-in Neutron accelerator and use CPU as the correctness baseline.

## Phase B: Runtime and Neutron bring-up (Nov 10–11)

The board exposed `NeutronExecutionProvider`. A test session with a simple float MatMul and both Neutron/CPU EPs initialized and produced `(1,256)` output. Yet the profiler clearly showed the kernel on CPU. The runtime warned that only the Neutron-specific graph type would be assigned to NPU on that installation.

Subsequent investigation checked Neutron boot messages, driver libraries, `neutron_perf.sh`, LiteRT delegates and ONNX conversion tools. A LiteRT classification demonstration initialized the NPU dispatch and produced image labels; CPU was also in the execution path.

**Decision:** test explicitly supported ONNX low-bit MatMulNBits models rather than treating any MatMul as automatically NPU-compatible.

## Phase C: Large-model deployment and memory (Nov 11–12)

The larger Qwen3-4B ONNX INT4 artifact was placed on the board. Verbose ORT logging showed `MatMulNBits` nodes distributed to the Neutron EP (253 nodes). The same investigation reported an unsuccessful Neutron session with `std::bad_alloc`. A separate CPU session was reported to load in 33.91 seconds.

The latest Linux configuration had approximately 7.5 GiB RAM and approximately 4.94 GiB reserved CMA; a previous state had approximately 0.94 GiB CMA. These are important constraints but cannot by themselves explain or rule out every allocator failure.

**Decision:** inspect offline packing and investigate a partial graph/CPU suffix as a potential way to reduce NPU working set.

## Phase D: Model optimization and partitioning (Nov 12)

The NXP eIQ Olive Qwen3-1.7B SpinQuant/RTN recipe was inspected as a prospective host-side model optimization approach. Two Python split-script variants were developed for the 36-layer Qwen3-4B ONNX graph, with a split at four layers and special handling of KV-cache outputs and external tensor data.

Actual tests exposed incompatible custom ONNX operators for a general checker and external-data hard-link safety checks. The scripts warn about shared computations across halves and require further graph validation.

**Decision:** preserve failed attempts, avoid reporting a successful hybrid deployment, and design smaller, verifiable experiments.

## Phase E: End-user generation and documentation (Nov 12–13)

A text-generation interaction produced an application performance report including 128 generated tokens and 2.80 tokens/s. The output did not independently prove NPU kernel attribution. This repository makes that limitation explicit.

The research archive was reconstructed on Nov 13 from actual historical code and terminal captures, complemented by new offline diagnostics. New scripts have not been tested on the board in the archive creation process.
