#!/usr/bin/env python3
"""Summarize successful execution events from an ONNX Runtime Chrome-trace JSON file.

This tool reports profile attribution, not independent hardware utilization.
"""
from __future__ import annotations
from collections import Counter
import argparse
import json
from pathlib import Path

def analyze_events(events: list[dict]) -> dict:
    events_by_provider=Counter()
    duration_us=Counter()
    sample_names: dict[str,list[str]]={}
    for event in events:
        if not isinstance(event,dict): continue
        args=event.get('args',{})
        if not isinstance(args,dict):continue
        provider=args.get('provider')
        if not provider:continue
        name=str(event.get('name',''))
        if not ('kernel_time' in name or event.get('cat')=='Node'):continue
        events_by_provider[str(provider)]+=1
        dur=event.get('dur',0)
        if isinstance(dur,(int,float)) and dur>=0:
            duration_us[str(provider)]+=dur
        sample_names.setdefault(str(provider),[])
        if len(sample_names[str(provider)])<15:
            sample_names[str(provider)].append(name)
    return {'provider_kernel_events':dict(events_by_provider),
            'provider_event_duration_us':dict(duration_us),
            'sample_events':sample_names,
            'note':'Per-node profile events require a session that completed inference. CPU/NPU timelines can overlap.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('profile',type=Path)
    args=ap.parse_args()
    data=json.loads(args.profile.read_text())
    if not isinstance(data,list):
        raise SystemExit('Expected a list of ONNX Runtime Chrome-trace events.')
    print(json.dumps(analyze_events(data),indent=2,sort_keys=True))
if __name__=='__main__':main()
