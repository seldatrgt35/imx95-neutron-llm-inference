#!/usr/bin/env python3
"""Read-only provider/runtime inspection; does not download or replace packages."""
from __future__ import annotations
from pathlib import Path
import json
import platform
import sys

def main():
    info={'python':sys.version.split()[0], 'architecture':platform.machine(),
          'board_model':None,'onnxruntime_version':None,'available_providers':[],
          'neutron_device':Path('/dev/neutron0').exists()}
    path=Path('/proc/device-tree/model')
    if path.exists():info['board_model']=path.read_bytes().split(b'\x00')[0].decode(errors='replace')
    try:
        import onnxruntime as ort
        info['onnxruntime_version']=ort.__version__
        info['available_providers']=ort.get_available_providers()
    except ImportError as err:
        info['onnxruntime_error']=str(err)
    print(json.dumps(info,indent=2))
if __name__=='__main__':main()
