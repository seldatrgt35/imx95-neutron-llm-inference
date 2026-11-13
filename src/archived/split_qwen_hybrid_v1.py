#!/usr/bin/env python3
"""Split Qwen3-4B ONNX into prefix (Neutron candidate) and suffix (CPU).
Does not load external weights into RAM or alter the original files.
"""
import argparse
import copy
import os
import re
from collections import Counter
from pathlib import Path
import onnx
from onnx import TensorProto, helper, shape_inference

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--model', default='/root/Qwen3-4B-ONNX-INT4/model.onnx')
PARSER.add_argument('--out', default='/root/Qwen3-4B-HYBRID')
PARSER.add_argument('--layers', type=int, default=4)
args = PARSER.parse_args()
assert 1 <= args.layers < 36
source = Path(args.model).resolve()
out = Path(args.out).resolve()
out.mkdir(parents=True, exist_ok=True)
print('Reading ONNX graph (not weights):', source, flush=True)
model = onnx.load(str(source), load_external_data=False)
graph = model.graph
all_inputs = {v.name: v for v in graph.input}
all_outputs = {v.name: v for v in graph.output}
init = {t.name: t for t in graph.initializer}
producers = {name: n for n in graph.node for name in n.output if name}

# Layer N's first fused skip-layernorm consumes two values produced by layer N-1.
node = next((n for n in graph.node if n.name == f'/model/layers.{args.layers}/input_layernorm/SkipLayerNorm'), None)
if node is None:
    raise SystemExit('Could not find layer boundary SkipLayerNorm; model layout differs.')
boundary = [node.input[0], node.input[1]]
if any(v not in producers for v in boundary):
    raise SystemExit('Boundary input not produced by graph: ' + str(boundary))
print('Boundary tensors:', boundary)

# Obtain type/shape metadata without reading 3.9GB weights.
value_info = {v.name: v for v in list(graph.input) + list(graph.output) + list(graph.value_info)}
missing = [name for name in boundary if name not in value_info]
if missing:
    print('Missing intermediate tensor metadata; attempting shape inference...', flush=True)
    try:
        inferred = shape_inference.infer_shapes(model, strict_mode=False, data_prop=False)
        value_info.update({v.name: v for v in list(inferred.graph.value_info) + list(inferred.graph.input) + list(inferred.graph.output)})
    except Exception as exc:
        print('Shape inference unavailable:', exc)

# The two residual inputs have the same shape/dtype. If inference cannot
# determine them, use FLOAT16 and [batch, sequence, hidden] as a conservative
# hypothesis; fail rather than write a model with an unverified type.
missing = [name for name in boundary if name not in value_info or not value_info[name].HasField('type')]
if missing:
    print('ERROR: Could not infer type/shape for boundary tensors:', missing)
    print('Please run: python3 - <<\'PY\'\nimport onnx\nm=onnx.load(\''+str(source)+'\',load_external_data=False)\nfor x in m.graph.value_info:\n if \"layers.'+str(args.layers-1)+'\" in x.name: print(x.name, x.type)\nPY')
    raise SystemExit(2)

# Backward dependency walk: includes nodes, initializers and original graph inputs.
def collect(targets, blocked=frozenset()):
    used_nodes = set()
    used_inputs = set()
    used_initializers = set()
    stack = list(targets)
    seen = set()
    while stack:
        t = stack.pop()
        if not t or t in seen:
            continue
        seen.add(t)
        if t in blocked:
            used_inputs.add(t)
        elif t in init:
            used_initializers.add(t)
        elif t in producers:
            n = producers[t]
            used_nodes.add(id(n))
            stack.extend(x for x in n.input if x)
        elif t in all_inputs:
            used_inputs.add(t)
        else:
            raise RuntimeError(f'Unknown dependency: {t}')
    return used_nodes, used_inputs, used_initializers

# Prefix: boundary + KV cache for 0..N-1.
prefix_targets = boundary + [f'present.{i}.{kv}' for i in range(args.layers) for kv in ('key','value')]
p_nodes, p_inputs, p_init = collect(prefix_targets)
# Suffix: logits + KV cache for N..35; treat boundary as external inputs.
suffix_targets = ['logits'] + [f'present.{i}.{kv}' for i in range(args.layers,36) for kv in ('key','value')]
s_nodes, s_inputs, s_init = collect(suffix_targets, blocked=frozenset(boundary))

# Detect accidental shared computational nodes (shared constants are okay).
intersection = p_nodes & s_nodes
if intersection:
    print('WARNING: shared computation nodes between halves:', len(intersection))

# Add boundary input definitions to suffix.
def get_vi(name):
    if name in value_info:
        return copy.deepcopy(value_info[name])
    raise KeyError('Missing ValueInfo: ' + name)

def build(tag, selected_nodes, inputs, initializers, targets):
    nodes = [copy.deepcopy(n) for n in graph.node if id(n) in selected_nodes]
    original_input_order = [v.name for v in graph.input if v.name in inputs]
    boundary_extra = [b for b in boundary if b in inputs and b not in original_input_order]
    graph_inputs = [get_vi(n) for n in original_input_order + boundary_extra]
    graph_outputs = [get_vi(n) for n in targets]
    # Carry existing ValueInfo only for values produced inside this graph.
    produced = {x for n in nodes for x in n.output if x}
    extra_info = [copy.deepcopy(v) for v in graph.value_info if v.name in produced and v.name not in targets]
    g = helper.make_graph(nodes, f'Qwen3-4B-{tag}', graph_inputs, graph_outputs,
                          initializer=[copy.deepcopy(t) for t in graph.initializer if t.name in initializers],
                          value_info=extra_info)
    m = helper.make_model(g)
    m.ir_version = model.ir_version
    del m.opset_import[:]
    m.opset_import.extend(copy.deepcopy(model.opset_import))
    m.producer_name = model.producer_name
    m.producer_version = model.producer_version
    m.domain = model.domain
    m.model_version = model.model_version
    m.doc_string = model.doc_string
    m.metadata_props.extend(copy.deepcopy(model.metadata_props))
    # External tensor offsets/lengths remain unchanged, so both graphs may
    # reference the same original external-data file by symlink.
    external_locations = {e.value for t in g.initializer for e in t.external_data if e.key == 'location'}
    for location in external_locations:
        if os.path.isabs(location) or '..' in Path(location).parts:
            raise RuntimeError('Unsafe external-data location: ' + location)
        source_data = source.parent / location
        target_data = out / location
        if not source_data.exists():
            raise FileNotFoundError(source_data)
        target_data.parent.mkdir(parents=True, exist_ok=True)
        if not target_data.exists():
            target_data.symlink_to(source_data)
    path = out / f'{tag}.onnx'
    onnx.save_model(m, str(path), save_as_external_data=False)
    # Checker can operate without reading weights for model protobuf < 2GB.
    onnx.checker.check_model(str(path))
    print(f'{tag}: {len(nodes)} nodes; {Counter(n.op_type for n in nodes)["MatMulNBits"]} MatMulNBits; '
          f'{len(graph_inputs)} inputs; {len(graph_outputs)} outputs -> {path}', flush=True)
    return path

prefix_path = build('qwen_npu_prefix', p_nodes, p_inputs, p_init, prefix_targets)
suffix_path = build('qwen_cpu_suffix', s_nodes, s_inputs, s_init, suffix_targets)
print('\nDone. Original model untouched. The prefix uses Neutron+CPU fallback; suffix uses CPU only.')
print('NOTE: Split model correctness and Neutron session creation still require validation.')
