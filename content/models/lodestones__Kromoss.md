---
model_id: "lodestones/Kromoss"
title: "Kromoss"
org: "lodestones"
task: "text-to-image"
license: "apache-2.0"
params: "5.1B"
likes: 164
downloads: 5365
discovered_at: "2026-10-20"
created_at: "2026-10-19"
hf_url: "https://huggingface.co/lodestones/Kromoss"
tags: ["diffusers", "safetensors", "moss-image", "text-to-image", "en", "base_model:OpenMOSS-Team/MOSS-Image-Base", "base_model:finetune:OpenMOSS-Team/MOSS-Image-Base", "license:apache-2.0", "diffusers:MOSSImagePipeline", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 164개, 다운로드 5,365회(수집 시점 2026-10-20). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-to-image` |
| 파라미터 | 5.1B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-10-19 |
| 좋아요 | 164 |
| 다운로드 | 5,365 |

## 요약

Kromoss is a full fine-tune of [MOSS-Image-Base](https://huggingface.co/OpenMOSS-Team/MOSS-Image-Base) at 1024 px. It uses the same architecture, inference pipeline, text encoder (Qwen3.5-9B) and VAE (FLUX.2 small decoder) as [MOSS-Image-SFT](https://huggingface.co/OpenMOSS-Team/MOSS-Image-SFT), and this repo has the same layout, so it is a drop-in replacement.

The repo also ships two 8-step turbo LoRAs distilled from MOSS-Image-Base: **8 steps, CFG 1**, no negative branch. - `8-steps-dmd2-lora.safetensors` (recommended): the DMD LoRA below, further trained with DMD2's GAN stage against real…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [MOSS Image SFT 8 steps dmd](../lodestones__MOSS-Image-SFT-8-steps-dmd/)
- [MOSS Image Base](../OpenMOSS-Team__MOSS-Image-Base/)
- [MOSS Image SFT](../OpenMOSS-Team__MOSS-Image-SFT/)
- [Qwen Image 2.1](../Qwen__Qwen-Image-2.1/)
