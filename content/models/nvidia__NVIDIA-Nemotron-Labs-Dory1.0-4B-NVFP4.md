---
model_id: "nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-NVFP4"
title: "NVIDIA Nemotron Labs Dory1.0 4B NVFP4"
org: "nvidia"
task: "text-generation"
license: "other"
params: "4B"
likes: 23
downloads: 3973
discovered_at: "2026-11-05"
created_at: "2026-10-16"
hf_url: "https://huggingface.co/nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-NVFP4"
tags: ["transformers", "safetensors", "dory", "text-generation", "nvidia", "pytorch", "nemotron-labs", "conversational", "en", "dataset:nvidia/nemotron-post-training-v3", "dataset:nvidia/nemotron-pre-training-datasets", "license:other", "endpoints_compatible", "8-bit", "modelopt", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 23개, 다운로드 3,973회(수집 시점 2026-11-05). 이전 모델 nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-BF16(파라미터 8B, 다운로드 1,453) 대비 이번 모델은 파라미터 50.0% 감소, 다운로드 173.4% 증가, 라이선스 동일(other).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-generation` |
| 파라미터 | 4B |
| 라이선스 | other |
| 최초 등록일 | 2026-10-16 |
| 좋아요 | 23 |
| 다운로드 | 3,973 |

## 요약

**NVIDIA-Nemotron-Labs-Dory1.0-4B-NVFP4** is a looped (latent-recurrent) large language model (LLM) trained by NVIDIA. The model employs a normalized-GPT architecture with interleaved hybrid sliding window attention (SWA) and full attention layers. By repeatedly applying a shared block of layers, Dory1.0-4B can spend more compute per token allowing it to scale intelligence. This model is ready for commercial or non-commercial use.

* **Elastic Inference Compute:** A single checkpoint serves different inference compute budgets. By changing how many times the shared block of layers is applied, y…

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [DeepSeek V4 Flash 0731 NVFP4](../nvidia__DeepSeek-V4-Flash-0731-NVFP4/)
- [DeepSeek V4.1 Flash 1017 NVFP4](../nvidia__DeepSeek-V4.1-Flash-1017-NVFP4/)
- [DeepSeek V4.1 Flash NVFP4](../nvidia__DeepSeek-V4.1-Flash-NVFP4/)
- [Kolibri 1](../Aleph-Alpha__Kolibri-1/)
- [Hemmingway 1](../Altworld__Hemmingway-1/)
- [claude fable 5 1](../Anthropic__claude-fable-5-1/)
