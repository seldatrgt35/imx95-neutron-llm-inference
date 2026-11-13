# Scripts and status

All scripts in this folder were **newly written during repository reconstruction** for evidence analysis and reproducibility. They are not claimed to have run successfully on the FRDM board.

| Script | Purpose | Dependencies |
|---|---|---|
| `analyze_neutron_ort_log.py` | Parse *static* Neutron/CPU node placement | Standard library |
| `analyze_ort_profile.py` | Parse actual ORT kernel event attribution | Standard library |
| `summarize_observations.py` | Show captured metrics and provenance | Standard library |
| `verify_evidence_manifest.py` | Check all sanitized evidence checksums | Standard library |
| `collect_board_information.sh` | Read-only device inventory | POSIX shell |
| `check_onnxruntime_environment.py` | Available providers and ORT version | optional target ONNX Runtime |
| `inspect_onnx_graph.py` | ONNX metadata without loading external data | ONNX |
| `build_matmul_baseline.py` | Deterministic FP32 control model | ONNX, NumPy |
| `run_matmul_probe.py` | Profile provider execution on an ONNX model | ONNX Runtime, NumPy |

Do not `pip install` generic ONNX Runtime over NXP's BSP runtime on the target device. Model conversion and prepacking are version-dependent and have not been automated in this archive.
