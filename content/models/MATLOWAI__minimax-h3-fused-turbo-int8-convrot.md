---
model_id: "MATLOWAI/minimax-h3-fused-turbo-int8-convrot"
title: "minimax h3 fused turbo int8 convrot"
org: "MATLOWAI"
task: "image-text-to-video"
license: "other"
params: ""
likes: 84
downloads: 19517
discovered_at: "2026-09-05"
created_at: "2026-08-29"
hf_url: "https://huggingface.co/MATLOWAI/minimax-h3-fused-turbo-int8-convrot"
tags: ["diffusion-single-file", "minimax-h3", "comfyui", "int8", "convrot", "turbo", "merge", "synchronized-audio-video", "image-text-to-video", "base_model:Comfy-Org/MiniMax-H3", "base_model:merge:Comfy-Org/MiniMax-H3", "base_model:MiniMaxAI/MiniMax-H3", "base_model:merge:MiniMaxAI/MiniMax-H3", "base_model:diffusers-modular/MiniMax-H3-Pruned-Ref-Delta-Fused-r1024", "base_model:merge:diffusers-modular/MiniMax-H3-Pruned-Ref-Delta-Fused-r1024", "base_model:xmarre/MiniMax-H3-Pruned-Ref-Delta-Fused-r1024-ComfyUI", "base_model:merge:xmarre/MiniMax-H3-Pruned-Ref-Delta-Fused-r1024-ComfyUI", "license:other", "region:us"]
reason: "surge"
---

## 왜 주목받는가

최근 7일 사이 좋아요·다운로드가 급증했습니다. 이 기준에 해당해 선정했습니다. 좋아요 84개, 다운로드 19,517회(수집 시점 2026-09-05). 급상승 근거: 7일 전 스냅샷 정보 없음(수집 이력 부족). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-video` |
| 파라미터 | 정보 없음 |
| 라이선스 | other |
| 최초 등록일 | 2026-08-29 |
| 좋아요 | 84 |
| 다운로드 | 19,517 |

## 요약

One 21 GB ComfyUI diffusion-model file that does MiniMax-H3 text/image-to-video **and** reference-to-video in **4 steps**, with a distilled turbo and a motion-smoothing style LoRA already folded into the weights.

- **Base:** the pruned `fl2va` transformer with a rank-1024 SVD of the (`ref2va` - `fl2va`) weight delta fused in, so a single partition serves both first/last-frame and reference conditioning (`xmarre/MiniMax-H3-Pruned-Ref-Delta-Fused-r1024-ComfyUI`, ComfyUI conversion of `diffusers-modular/MiniMax-H3-Pruned-Ref-Delta-Fused-r1024`). - **Merged in:** lightx2v FL2VA Turbo **8-step v1.…

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [MiniMax H3](../MiniMaxAI__MiniMax-H3/)
