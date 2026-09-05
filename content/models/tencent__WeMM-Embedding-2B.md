---
model_id: "tencent/WeMM-Embedding-2B"
title: "WeMM Embedding 2B"
org: "tencent"
task: "feature-extraction"
license: "other"
params: "2.7B"
likes: 83
downloads: 10278
discovered_at: "2026-09-05"
created_at: "2026-08-25"
hf_url: "https://huggingface.co/tencent/WeMM-Embedding-2B"
tags: ["transformers", "safetensors", "qwen3_5", "image-text-to-text", "sentence-transformers", "multimodal-embedding", "text-embedding", "image-embedding", "video-embedding", "mrl", "feature-extraction", "custom_code", "zh", "en", "arxiv:2608.24053", "base_model:Qwen/Qwen3.5-2B", "base_model:finetune:Qwen/Qwen3.5-2B", "license:other", "endpoints_compatible", "region:us"]
reason: "major-org"
---

## 왜 주목받는가

주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 83개, 다운로드 10,278회(수집 시점 2026-09-05). 같은 기관(tencent)의 다른 발행 모델 tencent/EVIE-Preview-4.5B 와 함께 살펴보세요.

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `feature-extraction` |
| 파라미터 | 2.7B |
| 라이선스 | other |
| 최초 등록일 | 2026-08-25 |
| 좋아요 | 83 |
| 다운로드 | 10,278 |

## 요약

WeMM-Embedding-2B is a universal multimodal embedding model built on Qwen3.5. It accepts text, images, videos, visual documents, and interleaved multimodal inputs, and returns a 2,048-dimensional L2-normalized embedding. Audio input is not supported.

Use any subset of the content items to encode text, image, or video independently.

Each input is a string, a URL or path, a `PIL.Image`, or a dict combining `image`, `video`, and `text` keys. Chat messages such as `{"role": "user", "content": [{"type": "image", "image": ...}, {"type": "text", "text": ...}]}` are also accepted, which is the way t…

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [EVIE Preview 4.5B](../tencent__EVIE-Preview-4.5B/)
- [Hy4 preview](../tencent__Hy4-preview/)
- [Hy4 preview FP8](../tencent__Hy4-preview-FP8/)
- [WeMM Embedding 4B](../tencent__WeMM-Embedding-4B/)
- [WeMM Embedding 9B](../tencent__WeMM-Embedding-9B/)
