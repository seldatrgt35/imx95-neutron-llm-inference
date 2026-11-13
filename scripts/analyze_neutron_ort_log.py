#!/usr/bin/env python3
"""Analyze ONNX Runtime verbose placement reports without requiring ONNX Runtime.

Static node assignment is not proof of successful kernel execution.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import re

COUNT = re.compile(r'Node\(s\) placed on \[([^\]]+)\]\. Number of nodes: (\d+)')
DETAIL = re.compile(r'\b(?:session_state\.cc|VerifyEachNodeIsAssignedToAnEp).*?\]\s+([A-Za-z0-9_]+)\s+\(')
# Some ORT versions print the provider header then indented node names on subsequent lines.
TYPE = re.compile(r'\]\s+([A-Za-z0-9_]+)\s+\(')

def analyze(raw: str) -> dict:
    providers = Counter()
    op_counts: dict[str, Counter] = {}
    current: str | None = None
    for line in raw.splitlines():
        m = COUNT.search(line)
        if m:
            current=m.group(1)
            providers[current] += int(m.group(2))
            op_counts.setdefault(current,Counter())
            continue
        # Do not count arbitrary graph-transformer messages or model errors.
        if current and 'session_state.cc' in line and 'VerifyEachNodeIsAssignedToAnEp' in line:
            d=TYPE.search(line)
            if d:
                op_counts[current][d.group(1)] += 1
        elif 'session_state.cc' not in line:
            current=None
    result={
        'session_setup_node_placements':dict(providers),
        'operator_details':{p:dict(c) for p,c in op_counts.items()},
        'status':'STATIC_ASSIGNMENT_ONLY',
        'note':'This report cannot prove model initialization or inference execution.'
    }
    return result

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('verbose_log',type=Path)
    ap.add_argument('--json',action='store_true',help='Machine-readable output (default is readable JSON too)')
    args=ap.parse_args()
    result=analyze(args.verbose_log.read_text(errors='replace'))
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
