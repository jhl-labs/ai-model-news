---
model_id: "kandinskylab/Kandinsky-ImageSR-2.0"
title: "Kandinsky ImageSR 2.0"
org: "kandinskylab"
task: "image-to-image"
license: "mit"
params: "4.5B"
likes: 116
downloads: 4
discovered_at: "2026-11-26"
created_at: "2026-11-24"
hf_url: "https://huggingface.co/kandinskylab/Kandinsky-ImageSR-2.0"
tags: ["diffusers", "safetensors", "super-resolution", "image-super-resolution", "kandinsky", "image-to-image", "license:mit", "diffusers:KandinskyImageSRPipeline", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 116개, 다운로드 4회(수집 시점 2026-11-26). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-to-image` |
| 파라미터 | 4.5B |
| 라이선스 | mit |
| 최초 등록일 | 2026-11-24 |
| 좋아요 | 116 |
| 다운로드 | 4 |

## 요약

Kandinsky Image Super-Resolution 2.0 as a Diffusers bundle. A single set of transformer weights serves both `x2` and `x4`. The release uses pre-baked zero-text conditioning: the text tower and all 50 cross-attention layers are replaced by small per-timestep Safetensors tables.

This repository contains all components needed for inference with `from_pretrained`.

The pipeline uses the Kandinsky 5 transformer included in Diffusers 0.41 or newer.

## 라이선스

mit — 상업 이용 가능

## 관련 모델

- [BFS Best Face Swap](../Alissonerdx__BFS-Best-Face-Swap/)
- [flux 3 image klein](../black-forest-labs__flux-3-image-klein/)
- [flux 3 image klein base](../black-forest-labs__flux-3-image-klein-base/)
