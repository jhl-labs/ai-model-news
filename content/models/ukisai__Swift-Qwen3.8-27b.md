---
model_id: "ukisai/Swift-Qwen3.8-27b"
title: "Swift Qwen3.8 27b"
org: "ukisai"
task: "image-text-to-text"
license: "other"
params: "27.8B"
likes: 251
downloads: 1355
discovered_at: "2026-09-15"
created_at: "2026-09-08"
hf_url: "https://huggingface.co/ukisai/Swift-Qwen3.8-27b"
tags: ["transformers", "safetensors", "qwen3_5", "image-text-to-text", "qwen3_8", "efficient-thinking", "reasoning", "token-efficient", "lora", "conversational", "base_model:Qwen/Qwen3.8-27B", "base_model:finetune:Qwen/Qwen3.8-27B", "license:other", "endpoints_compatible", "region:us"]
reason: "new, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 251개, 다운로드 1,355회(수집 시점 2026-09-15). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-text` |
| 파라미터 | 27.8B |
| 라이선스 | other |
| 최초 등록일 | 2026-09-08 |
| 좋아요 | 251 |
| 다운로드 | 1,355 |

## 요약

Swift-Qwen3.8-27B is UkisAI's reasoning-efficient derivative of Qwen3.8-27B, using **58.3% fewer thinking tokens** while maintaining near-identical performance (**&lt;1% loss**) and as a result getting a **x1.95 speed-up** on several tasks.

We built Swift by identifying reasoning-marker tokens that, in our analysis, trigger overthinking in Qwen’s reasoning rollouts. We then fine-tuned Qwen by penalizing usage of those tokens while it reasons.

Swift produces shorter reasoning traces. In our testing, we also observe fewer overthinking errors.

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [Agnes 3.0 Flash](../Agnes-AI__Agnes-3.0-Flash/)
- [North Micro Vision Instruct](../CohereLabs__North-Micro-Vision-Instruct/)
- [Qwen Drive 1.0 4B](../Qwen__Qwen-Drive-1.0-4B/)
