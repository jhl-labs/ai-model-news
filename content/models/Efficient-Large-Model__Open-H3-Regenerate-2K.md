---
model_id: "Efficient-Large-Model/Open-H3-Regenerate-2K"
title: "Open H3 Regenerate 2K"
org: "Efficient-Large-Model"
task: "video-to-video"
license: "other"
params: ""
likes: 153
downloads: 0
discovered_at: "2026-11-01"
created_at: "2026-10-26"
hf_url: "https://huggingface.co/Efficient-Large-Model/Open-H3-Regenerate-2K"
tags: ["diffusers", "safetensors", "minimax-h3", "lora", "video-refinement", "sol-engine", "video-to-video", "base_model:MiniMaxAI/MiniMax-H3", "base_model:adapter:MiniMaxAI/MiniMax-H3", "license:other", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 153개, 다운로드 0회(수집 시점 2026-11-01). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `video-to-video` |
| 파라미터 | 정보 없음 |
| 라이선스 | other |
| 최초 등록일 | 2026-10-26 |
| 좋아요 | 153 |
| 다운로드 | 0 |

## 요약

An open replacement for the closed H3-Regenerate-2K API: a three-step MiniMax-H3 refinement pass that regenerates a 768P H3 draft (1344×768, 121 frames) at **2560×1440**.

[Project page](https://nvlabs.github.io/Sana/Open-H3-Regenerate-2K/) · [Code](https://github.com/NVlabs/Sana/tree/sol-engine/models/Open-H3-Regenerate-2K)

One 5 s clip, 768P latent → 2560×1440 video: latent upscale + 3-step refine + VAE decode, warm, median of 3 runs:

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [Viggle Animate](../Viggle__Viggle-Animate/)
- [MiniMax H3 Character Swap LoRA](../akatz-ai__MiniMax-H3-Character-Swap-LoRA/)
