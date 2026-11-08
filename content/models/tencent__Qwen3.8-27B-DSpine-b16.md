---
model_id: "tencent/Qwen3.8-27B-DSpine-b16"
title: "Qwen3.8 27B DSpine b16"
org: "tencent"
task: "text-generation"
license: "apache-2.0"
params: "2B"
likes: 84
downloads: 652
discovered_at: "2026-11-08"
created_at: "2026-11-07"
hf_url: "https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16"
tags: ["safetensors", "qwen3", "dspine", "speculative-decoding", "draft-model", "sglang", "text-generation", "arxiv:2609.36173", "arxiv:2607.05147", "base_model:Qwen/Qwen3.8-27B", "base_model:finetune:Qwen/Qwen3.8-27B", "license:apache-2.0", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 84개, 다운로드 652회(수집 시점 2026-11-08). 이전 모델 tencent/Hy-Memory-30B-A3B-GGUF(파라미터 정보 없음, 다운로드 10,479) 대비 이번 모델은 파라미터 비교 정보 없음, 다운로드 93.8% 감소, 라이선스 동일(apache-2.0).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-generation` |
| 파라미터 | 2B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-11-07 |
| 좋아요 | 84 |
| 다운로드 | 652 |

## 요약

DSpine generates draft tokens in parallel. Each layer passes predicted predecessor features to adjacent positions, carrying causal dependencies through network depth.

This checkpoint is a five-layer draft model for [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), with block size 16 and an 8,192-token sliding window.

- **Runtime:** SGLang 0.5.22, BF16, FlashAttention 3, concurrency 8. - **Draft blocks:** DSpine 16; official [DFlash2](https://huggingface.co/z-lab/Qwen3.8-27B-DFlash2) 8. - **DSpine inference:** dynamic verification referencing [DSpark](https://github.com/deepseek-ai/Deep…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [AuK](../tencent__AuK/)
- [AuK Flash](../tencent__AuK-Flash/)
- [ContextPilot 14B](../tencent__ContextPilot-14B/)
- [Kolibri 1](../Aleph-Alpha__Kolibri-1/)
- [Hemmingway 1](../Altworld__Hemmingway-1/)
- [claude fable 5 1](../Anthropic__claude-fable-5-1/)
