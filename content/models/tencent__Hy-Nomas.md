---
model_id: "tencent/Hy-Nomas"
title: "Hy Nomas"
org: "tencent"
task: "text-to-video"
license: "apache-2.0"
params: ""
likes: 31
downloads: 0
discovered_at: "2026-10-23"
created_at: "2026-10-21"
hf_url: "https://huggingface.co/tencent/Hy-Nomas"
tags: ["diffusers", "safetensors", "hy-nomas", "world-model", "video-generation", "interactive-video-generation", "camera-control", "autoregressive", "diffusion-transformer", "pytorch", "text-to-video", "license:apache-2.0", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 31개, 다운로드 0회(수집 시점 2026-10-23). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-to-video` |
| 파라미터 | 정보 없음 |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-10-21 |
| 좋아요 | 31 |
| 다운로드 | 0 |

## 요약

**Hy-Nomas** is a video world generation model that supports free-form, multi-turn interaction through text instructions and camera control. It generates a world one video segment at a time, allowing users to introduce objects, change styles and scenes, describe actions, or control the camera as generation continues.

The model combines a segment-autoregressive diffusion transformer (DiT), a Qwen text encoder, camera-conditioning modules, and a PixelUMM video decoder. A persistent key/value (KV) cache carries context between segments. The distilled inference configuration uses **8 denoising st…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [AuK](../tencent__AuK/)
- [AuK Flash](../tencent__AuK-Flash/)
- [ContextPilot 14B](../tencent__ContextPilot-14B/)
- [FastVideo FastH3 4 step Preview v1 VSA DataFree](../FastVideo__FastVideo-FastH3-4-step-Preview-v1-VSA-DataFree/)
- [vdn minimax h3](../OpenVDN__vdn-minimax-h3/)
