"""Transcribed from a captured 10 Nov 2026 board session.

The recorded run was successful but profiling placed MatMul on CPU.
This is an archival specimen, not a proof of Neutron NPU execution.
Requires a separately constructed /root/matmul_test.onnx.
"""
import numpy as np
import onnxruntime as ort

options = ort.SessionOptions()
options.log_severity_level = 0
options.enable_profiling = True
session = ort.InferenceSession(
    "/root/matmul_test.onnx",
    sess_options=options,
    providers=["NeutronExecutionProvider", "CPUExecutionProvider"],
)
print("Session providers:", session.get_providers())
X = np.random.randn(1, 256).astype(np.float32)
result = session.run(None, {"X": X})
print("Inference successful!")
print("Output shape:", result[0].shape)
profile = session.end_profiling()
print("Profiling file:", profile)
