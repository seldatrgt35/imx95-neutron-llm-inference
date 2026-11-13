#!/usr/bin/env python3
"""Probe an existing ONNX MatMul model and profile actual ONNX Runtime provider events.

This script is newly authored; not part of the recovered on-board session.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import onnxruntime as ort

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('model',type=Path)
    ap.add_argument('--width',type=int,default=256)
    ap.add_argument('--cpu-only',action='store_true')
    args=ap.parse_args()
    opts=ort.SessionOptions()
    opts.enable_profiling=True
    opts.log_severity_level=2
    if not args.model.exists():raise SystemExit(f'Model not found: {args.model}')
    providers=['CPUExecutionProvider'] if args.cpu_only else ['NeutronExecutionProvider','CPUExecutionProvider']
    print('Requested providers:',providers)
    print('Runtime providers:',ort.get_available_providers())
    session=ort.InferenceSession(str(args.model),sess_options=opts,providers=providers)
    print('Registered for session:',session.get_providers())
    inputs=session.get_inputs()
    if len(inputs)!=1:raise SystemExit('Expected test model with one X input')
    x=np.random.default_rng(0).standard_normal((1,args.width)).astype(np.float32)
    outputs=session.run(None,{inputs[0].name:x})
    profile=session.end_profiling()
    print('Output shape:',outputs[0].shape)
    print('Profile:',profile)
    print('Use analyze_ort_profile.py to determine *actual* recorded provider events.')
if __name__=='__main__':main()
