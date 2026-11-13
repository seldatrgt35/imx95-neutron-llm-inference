# FRDM-i.MX95 board, BSP, boot configuration and CMA

## Board-level observations

Commands used across the investigation included:

```bash
cat /proc/device-tree/model
uname -r
python3 --version
uname -m
free -h
cat /proc/cmdline
grep -E '^(CmaTotal|CmaFree):' /proc/meminfo
ls -l /dev/neutron0
dmesg | grep -Ei 'neutron|npu|remoteproc|firmware'
```

One captured system identification returned `NXP FRDM-IMX95`. A later observed kernel was `6.18.37-2.1.0-g6e694eda40aa`; a later Python version was 3.14.5. The user reported Linux-visible 7.5 GiB of RAM, with no swap.

In the preserved Nov 11 driver trace:

```text
remoteproc remoteproc0: neutron-rproc is available
neutron 4ab00004.imx95-neutron: created neutron device, name=neutron0
crw-rw---- 1 root video 509, 0 ... /dev/neutron0
```

These prove device registration but are not an inference result.

## CMA progression

Contiguous Memory Allocator (CMA) supports hardware memory clients requiring contiguous physical regions. It is distinct from ordinary free system RAM.

| Snapshot | `CmaTotal` | Approx. GiB | Context |
|---|---:|---:|---|
| Earlier boot | 983040 kB | 0.94 GiB | NPU present, restricted reserve |
| Later boot | 5177344 kB | 4.94 GiB | Extended reserve, `CmaFree` 4706348 kB |

A prior boot command line contained `cma=3200M@4G-8G`; another later command line lacked the `cma=` override while the device tree supplied CMA. These were investigated as alternatives and were not simultaneously active.

The runtime trace from the large Qwen investigation includes the following allocation setup:

```text
Alloc CMA userspace memory 2048 MB
Alloc 512MB for slot 0
Alloc 512MB for slot 1
Alloc 512MB for slot 2
Alloc 512MB for slot 3
```

**Interpretation:** a 4.94 GiB CMA reservation does not guarantee that all allocations of a multi-gigabyte ONNX model, weights and runtime workspace can complete. Fragmentation, pool exhaustion, incompatible buffers, address-space pressure, duplicate external tensor loads and other causes remain hypotheses until a complete allocation trace is captured.

## BSP constraints

NXP's GenAI Flow documentation requires a compatible i.MX95 B0 BSP, Neutron-enabled device tree and sufficiently large CMA region for its accelerated LLM demonstrator. The BSP-integrated ONNX Runtime version matters: replacing it with an arbitrary PyPI wheel may remove or break Neutron EP support.

**Read-only diagnosis before changing firmware or U-Boot:**

```bash
cat /proc/device-tree/model
ls /boot/*neutron* 2>/dev/null
cat /proc/cmdline
find /sys/firmware/devicetree/base -maxdepth 2 -iname '*neutron*' 2>/dev/null
```

Do not copy EVK `fdtfile` examples directly onto the FRDM board without matching the board-specific DTB and a tested recovery procedure.

## Power, debugging and boot quality

The boot transcript includes a failed Weston startup, while serial shell access succeeded. Graphical service health and Neutron runtime availability are independent. Serial console was observed using Minicom over a `ttyACM0` interface at 115200 baud, 8N1; exact host port naming depends on enumeration.

## Evidence and limitations

Source: `evidence/terminal/20261110-081607-boot-weston-console.log`, `evidence/terminal/20261111-082645-litert-npu-mobilenet-validation.log`, and previous conversation-reported CMA and kernel snapshots. See `evidence/manifest.json` for original paste hashes.
