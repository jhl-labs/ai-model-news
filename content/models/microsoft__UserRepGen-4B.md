---
model_id: "microsoft/UserRepGen-4B"
title: "UserRepGen 4B"
org: "microsoft"
task: "text-generation"
license: "mit"
params: "4.5B"
likes: 20
downloads: 1134
discovered_at: "2026-10-20"
created_at: "2026-10-14"
hf_url: "https://huggingface.co/microsoft/UserRepGen-4B"
tags: ["transformers", "safetensors", "qwen3_5", "image-text-to-text", "user-representation", "user-simulation", "simulation", "multi-turn", "text-generation", "conversational", "en", "base_model:Qwen/Qwen3.5-4B", "base_model:finetune:Qwen/Qwen3.5-4B", "license:mit", "endpoints_compatible", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 20개, 다운로드 1,134회(수집 시점 2026-10-20). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-generation` |
| 파라미터 | 4.5B |
| 라이선스 | mit |
| 최초 등록일 | 2026-10-14 |
| 좋아요 | 20 |
| 다운로드 | 1,134 |

## 요약

UserRepGen-4B is a fine-tuned Qwen3.5-4B language model that generates a structured, natural-language user representation from a multi-turn user-assistant conversation. Each representation contains a **task description** and a **behavior description** for a user, and is intended to condition a separate LLM-based user simulator.

Unlike [UserLM-8b](https://huggingface.co/microsoft/UserLM-8b) and [UserLM-2.0](https://huggingface.co/microsoft/UserLM-2.0), which generate user utterances, **UserRepGen-4B generates representations, not simulated user turns**. It does not itself execute the user's ta…

## 라이선스

mit — 상업 이용 가능

## 관련 모델

- [AesCode 32B](../microsoft__AesCode-32B/)
- [AesCode 8B](../microsoft__AesCode-8B/)
- [FrogNano 4B 2609](../microsoft__FrogNano-4B-2609/)
- [Kolibri 1](../Aleph-Alpha__Kolibri-1/)
- [Hemmingway 1](../Altworld__Hemmingway-1/)
- [claude fable 5 1](../Anthropic__claude-fable-5-1/)
