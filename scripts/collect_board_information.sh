#!/bin/sh
# Read-only collection; does not edit device tree, bootloader or software packages.
set -u
printf '%s\n' '=== TIMESTAMP (UTC) ==='
date -u '+%Y-%m-%dT%H:%M:%SZ' || true
printf '%s\n' '=== SYSTEM ==='
cat /proc/device-tree/model 2>/dev/null; printf '\n'
uname -a
uname -m
printf '%s\n' '=== COMMAND LINE ==='
cat /proc/cmdline 2>/dev/null || true
printf '%s\n' '=== MEMORY ==='
free -h 2>/dev/null || true
grep -E '^(CmaTotal|CmaFree|MemTotal|MemAvailable|SwapTotal):' /proc/meminfo 2>/dev/null || true
printf '%s\n' '=== DEVICE ==='
ls -l /dev/neutron0 2>/dev/null || true
printf '%s\n' '=== NEUTRON KERNEL MESSAGES ==='
dmesg 2>/dev/null | grep -Ei 'neutron|npu|remoteproc' | tail -35 || true
printf '%s\n' '=== NPU LIBRARIES ==='
ldconfig -p 2>/dev/null | grep -Ei 'Neutron|LiteRt|onnxruntime' || true
printf '%s\n' '=== PYTHON ==='
python3 --version 2>&1 || true
printf '%s\n' '=== ONNX RUNTIME PROVIDERS ==='
python3 -c 'import onnxruntime as o;print(o.__version__);print(o.get_available_providers())' 2>&1 || true
