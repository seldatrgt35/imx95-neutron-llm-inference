# Evidence retention and traceability

The `terminal/` directory contains sanitized copies of *user-provided, previously captured* terminal output, not newly run hardware tests. Original filenames and SHA-256 hashes are recorded in `manifest.json`.

Exact original bytes may contain malformed Minicom control sequences or externally authored source code. The public copies normalize control bytes, render non-ASCII as escaped sequences, and exclude certain third-party source/licensing material. Such transformations are documented per file in the manifest. Terminal captures can also include copied commands that were not successfully executed; command appearance alone is not evidence of execution.

Evidence hierarchy:

1. **Direct observation**: preserved output with a command/result pair in a cited terminal capture.
2. **Conversation record**: numbers reported in a session but no raw trace in the available file archive.
3. **Derived analysis**: scripts and calculations based on those observations.
4. **Research/reference**: vendor documentation; never confused with a result obtained on this board.
5. **Proposed**: new diagnostic helpers or next experiments, unexecuted on the target.

Hardware state was not captured afresh for this repository. No model weights, firmware images, vendor source bundles, private keys, access tokens, or binary BSP distributions are included.
