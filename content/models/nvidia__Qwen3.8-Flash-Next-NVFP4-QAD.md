---
model_id: "nvidia/Qwen3.8-Flash-Next-NVFP4-QAD"
title: "Qwen3.8 Flash Next NVFP4 QAD"
org: "nvidia"
task: "image-text-to-text"
license: "other"
params: "180B"
likes: 33
downloads: 0
discovered_at: "2026-11-17"
created_at: "2026-11-17"
hf_url: "https://huggingface.co/nvidia/Qwen3.8-Flash-Next-NVFP4-QAD"
tags: ["modelopt", "safetensors", "qwen4_exp", "nvidia", "ModelOpt", "Qwen3.8", "quantized", "nvfp4", "mxfp8", "qad", "image-text-to-text", "conversational", "base_model:Qwen/Qwen3.8-Flash-Next", "base_model:quantized:Qwen/Qwen3.8-Flash-Next", "license:other", "8-bit", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 33개, 다운로드 0회(수집 시점 2026-11-17). 이전 모델 nvidia/Kimi-K3.1-Pro-NVFP4(파라미터 1.4T, 다운로드 906) 대비 이번 모델은 파라미터 87.1% 감소, 다운로드 100.0% 감소, 라이선스 동일(other).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-text` |
| 파라미터 | 180B |
| 라이선스 | other |
| 최초 등록일 | 2026-11-17 |
| 좋아요 | 33 |
| 다운로드 | 0 |

## 요약

This is an experimental mixed-precision QAD checkpoint of [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next), exported after 100 optimizer updates using NVIDIA Model Optimizer and NeMo AutoModel with FSDP2. It contains the full multimodal model, including the frozen vision encoder, PLE n-gram embedding, and MTP module. Weight files occupy approximately 129.7 GB (120.8 GiB).

**This checkpoint uses a more aggressive quantization recipe than [Qwen3.8-Flash-Next-NVFP4](https://huggingface.co/nvidia/Qwen3.8-Flash-Next-NVFP4).** In addition to routed experts, it quantizes shared e…

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [Cosmos3 Nano](../nvidia__Cosmos3-Nano/)
- [DeepSeek V4 Flash 0731 NVFP4](../nvidia__DeepSeek-V4-Flash-0731-NVFP4/)
- [DeepSeek V4.1 Flash 1017 NVFP4](../nvidia__DeepSeek-V4.1-Flash-1017-NVFP4/)
- [Agnes 3.0 Flash](../Agnes-AI__Agnes-3.0-Flash/)
- [mirage](../Cactus-Compute__mirage/)
- [clef](../Cloudflare__clef/)
