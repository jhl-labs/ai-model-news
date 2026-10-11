---
model_id: "speridlabs/iris-3b"
title: "iris 3b"
org: "speridlabs"
task: "text-to-image"
license: "apache-2.0"
params: "3B"
likes: 144
downloads: 393
discovered_at: "2026-10-11"
created_at: "2026-10-05"
hf_url: "https://huggingface.co/speridlabs/iris-3b"
tags: ["pytorch", "safetensors", "text-to-image", "diffusion", "pixel-space", "flow-matching", "general-vision-learner", "vision-foundation-model", "depth-estimation", "image-restoration", "super-resolution", "arxiv:2610.09450", "license:apache-2.0", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 144개, 다운로드 393회(수집 시점 2026-10-11). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-to-image` |
| 파라미터 | 3B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-10-05 |
| 좋아요 | 144 |
| 다운로드 | 393 |

## 요약

Generative priors are a promising foundation for downstream vision tasks. In this project we explore pixel-space generative models as an alternative to vision foundation models such as DINOv2.

Most image generators work in a compressed "latent" space and rely on a separate decoder to turn that into an image. Iris-3B skips that step: the network itself outputs every pixel, so nothing is lost to a lossy, texture-biased latent. You type a prompt, and you get a 1024-pixel image.

Iris-3B is not only an image generator. The same pixel-space prior, fine-tuned with no architectural change, is a gene…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [Qwen Image 2.1](../Qwen__Qwen-Image-2.1/)
- [Qwen Image 2.1 PE T2I](../Qwen__Qwen-Image-2.1-PE-T2I/)
- [Qwen Image 2.1 Turbo](../Qwen__Qwen-Image-2.1-Turbo/)
