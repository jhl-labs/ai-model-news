---
model_id: "nvidia/NV-Reason-CT"
title: "NV Reason CT"
org: "nvidia"
task: "image-text-to-text"
license: "openmdw-1.1"
params: "5.3B"
likes: 21
downloads: 558
discovered_at: "2026-09-28"
created_at: "2026-09-08"
hf_url: "https://huggingface.co/nvidia/NV-Reason-CT"
tags: ["transformers", "safetensors", "qwen3_5", "image-text-to-text", "medical-imaging", "ct", "3d-vlm", "vision-language", "nv-reason-ct", "nvidia", "conversational", "custom_code", "en", "dataset:ibrahimhamamci/CT-RATE", "dataset:BodyMaps/CancerVerse", "arxiv:2609.27511", "base_model:Qwen/Qwen3.5-4B", "base_model:finetune:Qwen/Qwen3.5-4B", "license:openmdw-1.1", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 21개, 다운로드 558회(수집 시점 2026-09-28). 이전 모델 nvidia/DeepSeek-V4.1-Flash-NVFP4(파라미터 763.2B, 다운로드 132) 대비 이번 모델은 파라미터 99.3% 감소, 다운로드 322.7% 증가, 라이선스 mit→openmdw-1.1.

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-text` |
| 파라미터 | 5.3B |
| 라이선스 | openmdw-1.1 |
| 최초 등록일 | 2026-09-08 |
| 좋아요 | 21 |
| 다운로드 | 558 |

## 요약

NV-Reason-CT is a 3D vision-language model (VLM) for CT image analysis. It combines a native 3D vision encoder (3D ViT) with a language model and is designed for radiology report generation, general question answering, and multi-step reasoning across chest and abdominal CT volumes.

Computed tomography encodes clinically important anatomy across hundreds of slices, yet most vision–language systems either operate on 2D images or compress volumetric features before language decoding. The 3D vision encoder converts a 384×384×384-mm input volume into a 24×24×24 grid of 13,824 visual tokens. All to…

## 라이선스

openmdw-1.1 — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [DeepSeek V4 Flash 0731 NVFP4](../nvidia__DeepSeek-V4-Flash-0731-NVFP4/)
- [DeepSeek V4.1 Flash NVFP4](../nvidia__DeepSeek-V4.1-Flash-NVFP4/)
- [GLM 5.3 Flash NVFP4](../nvidia__GLM-5.3-Flash-NVFP4/)
- [Agnes 3.0 Flash](../Agnes-AI__Agnes-3.0-Flash/)
- [North Micro Vision Instruct](../CohereLabs__North-Micro-Vision-Instruct/)
- [Qwen Drive 1.0 4B](../Qwen__Qwen-Drive-1.0-4B/)
