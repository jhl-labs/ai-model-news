---
model_id: "tencent/Hy-Memory-30B-A3B-GGUF"
title: "Hy Memory 30B A3B GGUF"
org: "tencent"
task: "text-generation"
license: "apache-2.0"
params: ""
likes: 20
downloads: 10479
discovered_at: "2026-10-22"
created_at: "2026-10-19"
hf_url: "https://huggingface.co/tencent/Hy-Memory-30B-A3B-GGUF"
tags: ["transformers", "gguf", "llama.cpp", "text-generation", "en", "zh", "arxiv:2610.22196", "base_model:tencent/Hy-Memory-30B-A3B", "base_model:quantized:tencent/Hy-Memory-30B-A3B", "license:apache-2.0", "endpoints_compatible", "region:us", "imatrix", "conversational"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 20개, 다운로드 10,479회(수집 시점 2026-10-22). 이전 모델 tencent/Hy-Memory-30B-A3B(파라미터 30.1B, 다운로드 0) 대비 이번 모델은 파라미터 비교 정보 없음, 다운로드 0→10,479(비율 산출 불가), 라이선스 동일(apache-2.0).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-generation` |
| 파라미터 | 정보 없음 |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-10-19 |
| 좋아요 | 20 |
| 다운로드 | 10,479 |

## 요약

This repository provides GGUF quantizations of [Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) for efficient local inference with [llama.cpp](https://github.com/ggml-org/llama.cpp).

The releases use **Tencent Hunyuan's Hy-Memory quantization recipe**: imatrix calibration plus MoE-aware mixed precision. Routed experts, which dominate parameter count, can be compressed aggressively, while shared experts, attention, and input/output layers keep higher precision. On the same fixed Mem0 LoCoMo setup, even the **~8 GB** expert-mixed build stays within about **1.5 points** of t…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [AuK](../tencent__AuK/)
- [AuK Flash](../tencent__AuK-Flash/)
- [ContextPilot 14B](../tencent__ContextPilot-14B/)
- [Kolibri 1](../Aleph-Alpha__Kolibri-1/)
- [Hemmingway 1](../Altworld__Hemmingway-1/)
- [claude fable 5 1](../Anthropic__claude-fable-5-1/)
