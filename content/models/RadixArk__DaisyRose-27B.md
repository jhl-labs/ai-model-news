---
model_id: "RadixArk/DaisyRose-27B"
title: "DaisyRose 27B"
org: "RadixArk"
task: "image-text-to-text"
license: "apache-2.0"
params: "27.8B"
likes: 261
downloads: 918
discovered_at: "2026-11-20"
created_at: "2026-11-18"
hf_url: "https://huggingface.co/RadixArk/DaisyRose-27B"
tags: ["transformers", "safetensors", "qwen3_5", "image-text-to-text", "daisyrose", "qwen3.8", "reinforcement-learning", "conversational", "base_model:Qwen/Qwen3.8-27B", "base_model:finetune:Qwen/Qwen3.8-27B", "license:apache-2.0", "endpoints_compatible", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 261개, 다운로드 918회(수집 시점 2026-11-20). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-text` |
| 파라미터 | 27.8B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-11-18 |
| 좋아요 | 261 |
| 다운로드 | 918 |

## 요약

This repository holds the **BF16** weights of DaisyRose-27B.

DaisyRose-27B is RadixArk's first model: a multimodal reasoning model built on Qwen3.8-27B with reinforcement learning only, without any supervised fine-tuning or distillation. It was trained on about 1,200 curated long-horizon agent tasks, with sessions of up to 1M tokens, for 18 days on 144 H200 GPUs. Terminal Bench 4.1 pass@1 rises from 5.6 to 12.0, and the model also improves on most of the other coding, reasoning and instruction-following benchmarks below.

DaisyRose-27B keeps the base model's architecture, tokenizer and chat t…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [Agnes 3.0 Flash](../Agnes-AI__Agnes-3.0-Flash/)
- [mirage](../Cactus-Compute__mirage/)
- [clef](../Cloudflare__clef/)
