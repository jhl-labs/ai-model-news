---
model_id: "deepseek-ai/DeepSeek-V4.1-Flash"
title: "DeepSeek V4.1 Flash"
org: "deepseek-ai"
task: "image-text-to-text"
license: "mit"
params: "763.2B"
likes: 1263
downloads: 6
discovered_at: "2026-09-10"
created_at: "2026-09-10"
hf_url: "https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash"
tags: ["transformers", "safetensors", "deepseek_v41", "text-generation", "image-text-to-text", "license:mit", "eval-results", "endpoints_compatible", "8-bit", "fp8", "region:us"]
reason: "new, updated, trending, surge, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 최근 7일 사이 좋아요·다운로드가 급증했습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 1,263개, 다운로드 6회(수집 시점 2026-09-10). 급상승 근거: 7일 전 스냅샷 정보 없음(수집 이력 부족). 이전 모델 deepseek-ai/DeepSeek-V4-Flash-Vision-Exp(파라미터 304.6B, 다운로드 133,024) 대비 이번 모델은 파라미터 150.6% 증가, 다운로드 100.0% 감소, 라이선스 동일(mit).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-text` |
| 파라미터 | 763.2B |
| 라이선스 | mit |
| 최초 등록일 | 2026-09-10 |
| 좋아요 | 1,263 |
| 다운로드 | 6 |

## 요약

We introduce **DeepSeek-V4.1-Flash**, a multimodal Mixture-of-Experts (MoE) model with 552B backbone parameters and support for contexts of up to one million tokens. The model natively processes images and text, and generates text autoregressively.

**Architecture.** DeepSeek-V4.1-Flash adopts a **Causal Encoder-Decoder (CED)** architecture: a 40-layer Transformer organized as a 20-layer causal encoder followed by a 20-layer decoder. With CED, the decoder's global KV cache is projected from the final encoder hidden states rather than derived from each decoder layer's own hidden states. This al…

## 라이선스

mit — 상업 이용 가능

## 관련 모델

- [DeepSeek V4 Flash Vision Exp](../deepseek-ai__DeepSeek-V4-Flash-Vision-Exp/)
- [DeepSeek V4 Pro 0813](../deepseek-ai__DeepSeek-V4-Pro-0813/)
- [North Micro Vision Instruct](../CohereLabs__North-Micro-Vision-Instruct/)
- [Qwen Drive 1.0 4B](../Qwen__Qwen-Drive-1.0-4B/)
- [Qwen3.8 27B](../Qwen__Qwen3.8-27B/)
