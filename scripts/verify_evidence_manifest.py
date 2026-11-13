#!/usr/bin/env python3
"""Verify published evidence byte hashes against the archive manifest."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

def main():
    repo=Path(__file__).resolve().parents[1]
    manifest=json.loads((repo/'evidence/manifest.json').read_text())
    bad=[];ok=0
    for entry in manifest['records']:
        path=entry.get('public_evidence')
        if path is None:continue
        target=(repo/path).resolve()
        if not target.is_relative_to(repo) or not target.is_file():
            bad.append(f'Missing or unsafe path {path}');continue
        digest=hashlib.sha256(target.read_bytes()).hexdigest()
        if digest!=entry['public_evidence_sha256']:
            bad.append(f'Hash mismatch {path}')
        else:ok+=1
    print(f'Verified files: {ok}; errors: {len(bad)}')
    for err in bad:print('ERROR:',err)
    raise SystemExit(bool(bad))
if __name__=='__main__':main()
