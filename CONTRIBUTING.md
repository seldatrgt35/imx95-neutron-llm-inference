# Contribution guidance

This is an engineering research archive, not a supported SDK distribution.

- Add evidence IDs and source paths to every new experimental claim.
- Do not mark a workload as NPU-accelerated solely because an Execution Provider enumerates.
- Supply ONNX Runtime profiling traces and/or Neutron performance-counter evidence for actual offload claims.
- Distinguish reproduction scripts from scripts recovered verbatim from captured sessions.
- Never commit proprietary SDK packages, NXP binary files, downloaded model weights, credentials, or copyrighted vendor tutorial dumps.
- For benchmark changes, preserve model hash, operator assignment, input size, batch, sampling mode, CPU load, memory configuration, and software versions.
- Keep code comments and documentation in professional English.
