---
model_id: "autotrust/Qwen3.8-Flash-Next-E384-FP4-V2"
title: "Qwen3.8 Flash Next E384 FP4 V2"
org: "autotrust"
task: "image-text-to-text"
license: "other"
params: "155.1B"
likes: 2373
downloads: 46017
discovered_at: "2026-11-09"
created_at: "2026-10-26"
hf_url: "https://huggingface.co/autotrust/Qwen3.8-Flash-Next-E384-FP4-V2"
tags: ["vllm", "safetensors", "qwen4_exp", "qwen3.8", "moe", "nvfp4", "modelopt", "mtp", "rl", "grpo", "image-text-to-text", "conversational", "en", "zh", "base_model:autotrust/Qwen3.8-Flash-Next-E384-FP4-Local", "base_model:merge:autotrust/Qwen3.8-Flash-Next-E384-FP4-Local", "license:other", "8-bit", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 2,373개, 다운로드 46,017회(수집 시점 2026-11-09). 이전 모델 autotrust/GLM5.3-Flash-E224-DGX-Spark(파라미터 127.6B, 다운로드 5,422) 대비 이번 모델은 파라미터 21.6% 증가, 다운로드 748.7% 증가, 라이선스 mit→other.

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-text` |
| 파라미터 | 155.1B |
| 라이선스 | other |
| 최초 등록일 | 2026-10-26 |
| 좋아요 | 2,373 |
| 다운로드 | 46,017 |

## 요약

A compact build of [nvidia/Qwen3.8-Flash-Next-FP4-Local](https://huggingface.co/nvidia/Qwen3.8-Flash-Next-FP4-Local) found by **Neural Architecture Search (NAS)** over the routed-expert configuration: it keeps **384 of the 512 routed experts** in every decoder MoE layer and in the MTP layer.

Unchanged from the original: - top-10 routing and the shared experts; - attention, the n-gram PLE table, the vision tower and the tokenizer.

This is an unofficial derivative, not produced or endorsed by Alibaba or NVIDIA.

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [GEV 26B Decide](../autotrust__GEV-26B-Decide/)
- [GEV 26B Decide NVFP4](../autotrust__GEV-26B-Decide-NVFP4/)
- [GLM5.3 Flash E224 DGX Spark](../autotrust__GLM5.3-Flash-E224-DGX-Spark/)
- [Agnes 3.0 Flash](../Agnes-AI__Agnes-3.0-Flash/)
- [clef](../Cloudflare__clef/)
- [clef flash](../Cloudflare__clef-flash/)
