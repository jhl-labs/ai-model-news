---
model_id: "autotrust/JEV-27B-VL"
title: "JEV 27B VL"
org: "autotrust"
task: "image-text-to-text"
license: "apache-2.0"
params: "27.8B"
likes: 968
downloads: 1525286
discovered_at: "2026-10-06"
created_at: "2026-09-30"
hf_url: "https://huggingface.co/autotrust/JEV-27B-VL"
tags: ["transformers", "safetensors", "qwen3_5", "image-text-to-text", "jev", "system-one", "system-two", "typed-decisions", "calibrated-probabilities", "multimodal", "vision", "zero-shot", "recommendation", "lora", "vllm", "conversational", "en", "arxiv:2512.16899", "base_model:Qwen/Qwen3.8-27B", "base_model:adapter:Qwen/Qwen3.8-27B", "license:apache-2.0", "endpoints_compatible", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 968개, 다운로드 1,525,286회(수집 시점 2026-10-06). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-text` |
| 파라미터 | 27.8B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-09-30 |
| 좋아요 | 968 |
| 다운로드 | 1,525,286 |

## 요약

**autotrust/JEV-27B-VL** is [autotrust/JEV-27B](https://huggingface.co/autotrust/JEV-27B) with vision.

Every step below is **one System 1 decision**: a camera image or a screenshot in, a probability for every action out, in a single forward pass.

**Robot arm: pick and place from a camera image.** At every step System 1 looks at the top camera image and answers two questions: is the target left or right of the gripper, and above or below it? The arm moves accordingly and halves its step whenever an answer flips. It grasps the cube, carries it and drops it in the tray (MuJoCo simulation).

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [Agnes 3.0 Flash](../Agnes-AI__Agnes-3.0-Flash/)
- [clef](../Cloudflare__clef/)
- [clef flash](../Cloudflare__clef-flash/)
