---
model_id: "autotrust/GEV-26B-Decide"
title: "GEV 26B Decide"
org: "autotrust"
task: "text-classification"
license: "apache-2.0"
params: "25.8B"
likes: 674
downloads: 854574
discovered_at: "2026-10-06"
created_at: "2026-10-02"
hf_url: "https://huggingface.co/autotrust/GEV-26B-Decide"
tags: ["transformers", "safetensors", "gemma4", "image-text-to-text", "system-one", "system-two", "adaptive-thinking", "typed-decisions", "decision-model", "calibrated-probabilities", "jev", "noul", "choice", "score", "lora", "mixture-of-experts", "multimodal", "vllm", "text-classification", "en", "base_model:google/gemma-4-26B-A4B-it", "base_model:adapter:google/gemma-4-26B-A4B-it", "license:apache-2.0", "model-index", "endpoints_compatible", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 674개, 다운로드 854,574회(수집 시점 2026-10-06). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-classification` |
| 파라미터 | 25.8B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-10-02 |
| 좋아요 | 674 |
| 다운로드 | 854,574 |

## 요약

How the score was computed (our scoring with the kit's `score --edition 0.2.1`, not a board entry):

* **Knowledge & Reasoning:** all ten benchmarks with adaptive thinking (per-benchmark table under [Adaptive thinking](#adaptive-thinking)). * **Other four areas:** System 1 only (thinking off), from the complete System 1 run of these weights (all 150,759 requests, 0 errors), results in [`autotrust/jev-decision-index-results`](https://huggingface.co/datasets/autotrust/jev-decision-index-results) (`runs/jev-gemma4-26b-a4b`, the weights' previous name). Thinking was tried on five of their benchmar…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [JEV 27B VL](../autotrust__JEV-27B-VL/)
- [openjev](../AlexWortega__openjev/)
- [Julia 1](../SupersonicLabs__Julia-1/)
- [Jev Omni](../akhilaaa3__Jev-Omni/)
