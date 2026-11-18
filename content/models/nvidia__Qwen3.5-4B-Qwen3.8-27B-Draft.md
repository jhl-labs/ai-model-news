---
model_id: "nvidia/Qwen3.5-4B-Qwen3.8-27B-Draft"
title: "Qwen3.5 4B Qwen3.8 27B Draft"
org: "nvidia"
task: "text-generation"
license: "other"
params: "4.2B"
likes: 59
downloads: 290
discovered_at: "2026-11-18"
created_at: "2026-11-11"
hf_url: "https://huggingface.co/nvidia/Qwen3.5-4B-Qwen3.8-27B-Draft"
tags: ["Model Optimizer", "safetensors", "qwen3_5_text", "nvidia", "ModelOpt", "Qwen3.5", "Qwen3.8", "Draft", "text-generation", "conversational", "base_model:Qwen/Qwen3.5-4B", "base_model:finetune:Qwen/Qwen3.5-4B", "license:other", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 59개, 다운로드 290회(수집 시점 2026-11-18). 이전 모델 nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-NVFP4(파라미터 4B, 다운로드 3,973) 대비 이번 모델은 파라미터 5.0% 증가, 다운로드 92.7% 감소, 라이선스 동일(other).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-generation` |
| 파라미터 | 4.2B |
| 라이선스 | other |
| 최초 등록일 | 2026-11-11 |
| 좋아요 | 59 |
| 다운로드 | 290 |

## 요약

The NVIDIA Qwen3.5-4B-Qwen3.8-27B-Draft model is an external draft model for Qwen’s [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) – a complete language model rather than a draft head, sharing the target's tokenizer and vocabulary. It proposes blocks of candidate tokens which Qwen3.8-27B verifies by rejection sampling, reducing decode latency without changing the target's output distribution.

Trained with NVIDIA Model Optimizer in external speculative decoding mode.

This model is ready for commercial or non-commercial use.

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [Cosmos3 Nano](../nvidia__Cosmos3-Nano/)
- [DeepSeek V4 Flash 0731 NVFP4](../nvidia__DeepSeek-V4-Flash-0731-NVFP4/)
- [DeepSeek V4.1 Flash 1017 NVFP4](../nvidia__DeepSeek-V4.1-Flash-1017-NVFP4/)
- [Kolibri 1](../Aleph-Alpha__Kolibri-1/)
- [Hemmingway 1](../Altworld__Hemmingway-1/)
- [claude fable 5 1](../Anthropic__claude-fable-5-1/)
