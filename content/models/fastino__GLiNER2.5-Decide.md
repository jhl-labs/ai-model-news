---
model_id: "fastino/GLiNER2.5-Decide"
title: "GLiNER2.5 Decide"
org: "fastino"
task: "token-classification"
license: "apache-2.0"
params: "486.4M"
likes: 207
downloads: 19757
discovered_at: "2026-09-27"
created_at: "2026-09-23"
hf_url: "https://huggingface.co/fastino/GLiNER2.5-Decide"
tags: ["gliner2", "safetensors", "extractor", "Text classification", "Intent classification", "Sentiment Analysis", "Topic classification", "Named Entity Recognition", "token-classification", "en", "arxiv:2507.18546", "base_model:fastino/gliner2-large-v1", "base_model:finetune:fastino/gliner2-large-v1", "license:apache-2.0", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 207개, 다운로드 19,757회(수집 시점 2026-09-27). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `token-classification` |
| 파라미터 | 486.4M |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-09-23 |
| 좋아요 | 207 |
| 다운로드 | 19,757 |

## 요약

**The 340M English classification model in the GLiNER2.5 family.** Pass any label set at call time: intent, routing, sentiment, priority, policy, and multi-label tags, in a single forward pass. No prompt template. No generated tokens. Load it with `AutoExtractor` and ship it locally.

A single call can score several heads at once. Single-label tasks return one string. Multi-label tasks return every label above the threshold.

Exact-match accuracy on [`fastino/fast-decisions`](https://huggingface.co/datasets/fastino/fast-decisions): 17 domains, 300 held-out examples each, with the same text and…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

아직 관련 모델이 발행되지 않았습니다.
