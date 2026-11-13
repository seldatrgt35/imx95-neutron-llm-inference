# NXP eIQ GenAI Flow demonstrator

## Why we investigated it

Before adapting a larger custom model, the NXP GenAI Flow demonstrator provides a reference runtime for conversational AI on i.MX platforms. Its pipeline can combine speech, retrieval, an LLM and speech synthesis; the research focused on model loading and Neutron acceleration rather than building a new speech application.

## Observed repository exploration

The investigation included searching the demonstrator for relevant configuration and runtime references:

```bash
grep -RniE 'danube|neutron|download.*model|huggingface' eiq_genai_flow/README.md eiq_genai_flow/ 2>/dev/null
```

The documented baseline uses the Danube 500M quantized model with a Neutron option:

```bash
eiq_genai_flow --use-neutron -m danube-500M-q8
```

This is a **vendor-documented command**, not proof that the user successfully deployed that exact model with that exact command. NXP notes software version and CMA requirements, and that some components are shipped as compiled Python wheels or encrypted models. Users cannot assume the demo internally supports arbitrary Qwen ONNX files by simply changing one model name.

## Why we considered custom Qwen

The research objective was not merely to run the default Danube demonstration but to estimate the upper practical model size and speed for Qwen on the FRDM hardware. That requires model conversion, memory accounting and compatibility tests outside the curated demonstrator model list.

## Reproduction boundary

A fresh reproduction must pin the exact public repository revision, BSP release, Python and ONNX Runtime versions. It must also record the model artifact hash, model license and exact invocation. This archive has the research notes but does not redistribute NXP demo binaries or encrypted models.

Source: NXP demonstrator repository (see `references/REFERENCES.md`).
