---
model_id: "AlexWortega/openjev"
title: "openjev"
org: "AlexWortega"
task: "text-classification"
license: "mit"
params: ""
likes: 193
downloads: 0
discovered_at: "2026-09-19"
created_at: "2026-09-16"
hf_url: "https://huggingface.co/AlexWortega/openjev"
tags: ["transformers", "safetensors", "nli", "cross-encoder", "qwen3.5", "reranker", "text-classification", "image-text-to-text", "en", "base_model:Qwen/Qwen3.5-4B", "base_model:finetune:Qwen/Qwen3.5-4B", "license:mit", "endpoints_compatible", "region:us"]
reason: "new, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 193개, 다운로드 0회(수집 시점 2026-09-19). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-classification` |
| 파라미터 | 정보 없음 |
| 라이선스 | mit |
| 최초 등록일 | 2026-09-16 |
| 좋아요 | 193 |
| 다운로드 | 0 |

## 요약

**openjev** is Qwen3.5 turned into a *jev* model: a single cross-encoder that reads a premise and a hypothesis and answers with entailment, contradiction or neutral. That one primitive is enough to rerank answers, grade them against a reference, guard content, and play games in real time: hand it the game state and a few statements about it, and the argmax entailment is the move. Nothing is trained per task.

The new 4B checkpoint (`qwen3.5-4b-nli-v2/`) reads images as well as text and was trained on a much larger and harder mixture. It is strictly zero-shot on everything shown here.

* Doom s…

## 라이선스

mit — 상업 이용 가능

## 관련 모델

- [laya](../convaiinnovations__laya/)
