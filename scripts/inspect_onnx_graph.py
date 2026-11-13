#!/usr/bin/env python3
"""Inspect ONNX graph without loading its potentially multi-gigabyte external weights."""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path

def inspect(model_path: Path) -> dict:
    import onnx
    from onnx import external_data_helper
    model=onnx.load(str(model_path),load_external_data=False)
    counts=Counter(n.op_type for n in model.graph.node)
    referenced=set()
    for tensor in model.graph.initializer:
        for field in tensor.external_data:
            if field.key=='location':
                loc=Path(field.value)
                # Protect consumers from traversing arbitrary paths.
                if loc.is_absolute() or '..' in loc.parts:
                    referenced.add(f'UNSAFE_REFERENCE:{field.value}')
                else:
                    referenced.add(field.value)
    data_files=[]
    for r in sorted(referenced):
        safe=not r.startswith('UNSAFE_REFERENCE:')
        full=model_path.parent/r if safe else None
        data_files.append({'reference':r,'exists':full.exists() if full else False,
                           'size_bytes':full.stat().st_size if full and full.exists() else None})
    return {'model':str(model_path), 'onnx_ir_version':model.ir_version,
            'node_count':len(model.graph.node), 'graph_inputs':len(model.graph.input),
            'graph_outputs':len(model.graph.output),
            'opsets':{x.domain:x.version for x in model.opset_import},
            'operations':dict(counts.most_common()),
            'external_data_files':data_files,
            'note':'Metadata-only inspection. This does not validate runtime correctness.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('model',type=Path)
    args=ap.parse_args()
    if not args.model.is_file():raise SystemExit(f'No such model: {args.model}')
    print(json.dumps(inspect(args.model),indent=2))
if __name__=='__main__':main()
