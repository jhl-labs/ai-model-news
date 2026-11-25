---
model_id: "tencent/OmniEVIE-4B"
title: "OmniEVIE 4B"
org: "tencent"
task: "feature-extraction"
license: "apache-2.0"
params: "4.5B"
likes: 20
downloads: 399
discovered_at: "2026-11-25"
created_at: "2026-11-24"
hf_url: "https://huggingface.co/tencent/OmniEVIE-4B"
tags: ["sentence-transformers", "safetensors", "qwen3_5", "omnievie", "evie", "multimodal", "retrieval", "late-interaction", "multi-vector", "colbert", "matryoshka", "video-retrieval", "visual-document-retrieval", "image-retrieval", "text-retrieval", "token-compression", "feature-extraction", "dataset:TIGER-Lab/MMEB-V2", "dataset:vidore/vidore_benchmark_v3", "arxiv:2611.32203", "base_model:Qwen/Qwen3.5-4B", "base_model:finetune:Qwen/Qwen3.5-4B", "license:apache-2.0", "endpoints_compatible", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 20개, 다운로드 399회(수집 시점 2026-11-25). 이전 모델 tencent/WeMM-Embedding-9B(파라미터 9.4B, 다운로드 3,360) 대비 이번 모델은 파라미터 52.1% 감소, 다운로드 88.1% 감소, 라이선스 other→apache-2.0.

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `feature-extraction` |
| 파라미터 | 4.5B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-11-24 |
| 좋아요 | 20 |
| 다운로드 | 399 |

## 요약

**OmniEVIE-4B** is a 4.5B-parameter unified multi-modal, multi-vector retrieval model by **Tencent IMA Product Center** and **Tencent Youtu Lab**, ranking **#1 on the [MMEB-Leaderboard](https://huggingface.co/spaces/TIGER-Lab/MMEB-Leaderboard) (excluding audio)**—with `OmniEVIE-4B (Full)` at **60.68** and `OmniEVIE-4B (Compressed)` at **60.06** across 190 tasks (also **#1** in both Text `52.97` and Agent `54.14`). Built on Qwen3.5 with bidirectional full-attention layers, Prefix-MRL projection, spatio-temporal Ward clustering (**ST-HAC**), and a learned query saliency gate (`query_gate.safeten…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [AuK](../tencent__AuK/)
- [AuK Flash](../tencent__AuK-Flash/)
- [ContextPilot 14B](../tencent__ContextPilot-14B/)
- [embeddinggemma 2](../google__embeddinggemma-2/)
- [WeMM Embedding 2B](../tencent__WeMM-Embedding-2B/)
- [WeMM Embedding 4B](../tencent__WeMM-Embedding-4B/)
