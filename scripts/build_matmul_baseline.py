#!/usr/bin/env python3
"""Generate a tiny FP32 MatMul test model. It may run on CPU despite NPU EP presence."""
import argparse
from pathlib import Path
import numpy as np

def main():
    import onnx
    from onnx import helper, TensorProto, numpy_helper
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output',type=Path)
    ap.add_argument('--width',type=int,default=256)
    args=ap.parse_args()
    if not 1<=args.width<=2048:raise SystemExit('width out of permitted test range')
    rng=np.random.default_rng(123)
    w=rng.standard_normal((args.width,args.width)).astype(np.float32)
    nodes=[helper.make_node('MatMul',['X','W'],['Y'],name='MatMul_0')]
    graph=helper.make_graph(nodes,'fp32_matmul_cpu_fallback_control',
              [helper.make_tensor_value_info('X',TensorProto.FLOAT,[1,args.width])],
              [helper.make_tensor_value_info('Y',TensorProto.FLOAT,[1,args.width])],
              [numpy_helper.from_array(w,name='W')])
    model=helper.make_model(graph,opset_imports=[helper.make_opsetid('',17)])
    model.ir_version=min(model.ir_version,9)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    onnx.save(model,str(args.output))
    print(f'Wrote {args.output}; FP32 control is NOT an NPU-ready model')
if __name__=='__main__':main()
