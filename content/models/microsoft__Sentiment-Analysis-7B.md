---
model_id: "microsoft/Sentiment-Analysis-7B"
title: "Sentiment Analysis 7B"
org: "microsoft"
task: "text-generation"
license: "mit"
params: "7.2B"
likes: 21
downloads: 289
discovered_at: "2026-10-23"
created_at: "2026-10-17"
hf_url: "https://huggingface.co/microsoft/Sentiment-Analysis-7B"
tags: ["transformers", "safetensors", "mistral", "text-generation", "sentiment-analysis", "text-classification", "reinforcement-learning", "conversational", "en", "base_model:mistralai/Mistral-7B-Instruct-v0.2", "base_model:finetune:mistralai/Mistral-7B-Instruct-v0.2", "license:mit", "text-generation-inference", "endpoints_compatible", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 21개, 다운로드 289회(수집 시점 2026-10-23). 이전 모델 microsoft/UserRepGen-4B(파라미터 4.5B, 다운로드 1,134) 대비 이번 모델은 파라미터 60.0% 증가, 다운로드 74.5% 감소, 라이선스 동일(mit).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-generation` |
| 파라미터 | 7.2B |
| 라이선스 | mit |
| 최초 등록일 | 2026-10-17 |
| 좋아요 | 21 |
| 다운로드 | 289 |

## 요약

**Sentiment-Analysis-7B** is a 7B-parameter autoregressive language model fine-tuned for sentiment classification of user messages directed at a service, product, or agent (the "Target"). It is built on top of [*mistralai/Mistral-7B-Instruct-v0.2*](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) and was fine-tuned with reinforcement learning, using an LLM as a judge, on a small internal training set of ~300 examples. No pre-defined labels were used for training.

Given a user message, the model generates a response in the following format: the **first token is the sentiment label**…

## 라이선스

mit — 상업 이용 가능

## 관련 모델

- [AesCode 32B](../microsoft__AesCode-32B/)
- [AesCode 8B](../microsoft__AesCode-8B/)
- [FrogNano 4B 2609](../microsoft__FrogNano-4B-2609/)
- [Kolibri 1](../Aleph-Alpha__Kolibri-1/)
- [Hemmingway 1](../Altworld__Hemmingway-1/)
- [claude fable 5 1](../Anthropic__claude-fable-5-1/)
