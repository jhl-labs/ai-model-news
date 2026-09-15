---
model_id: "Alissonerdx/Minimax-H3-ComfyUI"
title: "Minimax H3 ComfyUI"
org: "Alissonerdx"
task: "other"
license: "apache-2.0"
params: ""
likes: 179
downloads: 14533
discovered_at: "2026-09-15"
created_at: "2026-09-06"
hf_url: "https://huggingface.co/Alissonerdx/Minimax-H3-ComfyUI"
tags: ["minimax-h3", "lora", "video", "comfyui", "base_model:MiniMaxAI/MiniMax-H3", "base_model:adapter:MiniMaxAI/MiniMax-H3", "license:apache-2.0", "region:us"]
reason: "new, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 179개, 다운로드 14,533회(수집 시점 2026-09-15). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `other` |
| 파라미터 | 정보 없음 |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-09-06 |
| 좋아요 | 179 |
| 다운로드 | 14,533 |

## 요약

LoRAs for [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3), built to run in ComfyUI with the [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3) weights. Trained and tested mainly against the `ref2va` base model; `fl2va` should also work as a base but is less tested.

Rank-64 LoRA for MiniMax H3 `ref2va` that sharpens a source video while keeping it photorealistic. It conditions on the source through guide latents rather than through the model's native reference-video node.

This LoRA conditions on your source video as a latent guide, not as a text description of it.

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [granite 4.2 3b GGUF](../ibm-granite__granite-4.2-3b-GGUF/)
