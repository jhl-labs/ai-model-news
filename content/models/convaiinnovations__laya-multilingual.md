---
model_id: "convaiinnovations/laya-multilingual"
title: "laya multilingual"
org: "convaiinnovations"
task: "text-classification"
license: "apache-2.0"
params: "321.9M"
likes: 218
downloads: 0
discovered_at: "2026-09-23"
created_at: "2026-09-19"
hf_url: "https://huggingface.co/convaiinnovations/laya-multilingual"
tags: ["transformers", "safetensors", "laya", "multilingual", "mmbert", "system-one", "calibrated-decisions", "rlcd", "classification", "routing", "guardrails", "moderation", "commercial-use", "text-classification", "en", "de", "fr", "es", "pt", "it", "nl", "sv", "da", "nb", "ru", "pl", "tr", "ar", "he", "fa"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 218개, 다운로드 0회(수집 시점 2026-09-23). 이전 모델 convaiinnovations/laya(파라미터 421.3M, 다운로드 0) 대비 이번 모델은 파라미터 23.6% 감소, 다운로드 0→0(비율 산출 불가), 라이선스 동일(apache-2.0).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-classification` |
| 파라미터 | 321.9M |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-09-19 |
| 좋아요 | 218 |
| 다운로드 | 0 |

## 요약

Non-autoregressive **System 1 decision model** covering 100+ languages. Give it a **state** (text, email, ticket, or JSON) and **typed questions**; it returns typed answers with probabilities in a single forward pass. No text generation, so nothing to parse and nothing to hallucinate.

Part of the [Laya family](https://huggingface.co/convaiinnovations/laya) — **use this checkpoint for anything that is not English.**

Since laya 0.3.11 the default `Router()` keeps both `english` and this checkpoint resident, so a mixed workload no longer swaps checkpoints on every language change. For a server,…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [laya](../convaiinnovations__laya/)
- [openjev](../AlexWortega__openjev/)
