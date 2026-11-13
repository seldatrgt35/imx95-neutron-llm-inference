# Vulkan and llama.cpp fallback investigation

## Why the GPU route was explored

On-board LLM inference can use CPUs, dedicated NPUs or GPUs when the hardware drivers and compute features support the runtime. GPU experiments were considered as an alternative to, not evidence for, Neutron offload. On the i.MX95 the Mali-G310 GPU and Vulkan tooling were investigated.

A separate SolidRun i.MX8MP investigation included `vulkaninfo` checks, queue flag inspection and absent integer/16-bit storage features; archived source text for that board was not recovered in this file set. Those observations belong to historical context and should not be attributed to the FRDM-i.MX95.

## Captured host compilation session

The Nov 10 log from an Ubuntu host shows steps involving `shaderc`, `SPIRV-Headers`, an AArch64 sysroot and CMake for `llama.cpp`.

```bash
cmake -S . -B build-imx95 \
  -DCMAKE_TOOLCHAIN_FILE=/home/dev/edge-ai/imx95-toolchain.cmake \
  -DCMAKE_BUILD_TYPE=Release
```

The session reported:

```text
-- CMAKE_SYSTEM_PROCESSOR: aarch64
-- Including Vulkan backend
-- Configuring done
-- Generating done
-- Build files have been written to: /home/dev/edge-ai/llama.cpp/build-imx95
```

These messages establish successful CMake **configuration**, not compilation success, target deployment, compatible GPU kernels or actual model inference. The host pathname is preserved only as an original environment reference; new users must replace it.

## Outstanding validation

Check target Vulkan loader, ICD, extensions, shader compiler, float16 and shader integer capability, then build and run a small model with measured per-token latency. Shader feature availability may rule out some kernels even if Vulkan itself is present.

Source: `evidence/terminal/20261110-124019-host-vulkan-cross-compilation.log`.
