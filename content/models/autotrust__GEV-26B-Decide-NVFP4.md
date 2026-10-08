---
model_id: "autotrust/GEV-26B-Decide-NVFP4"
title: "GEV 26B Decide NVFP4"
org: "autotrust"
task: "text-classification"
license: "apache-2.0"
params: "14.4B"
likes: 164
downloads: 19655
discovered_at: "2026-10-08"
created_at: "2026-10-05"
hf_url: "https://huggingface.co/autotrust/GEV-26B-Decide-NVFP4"
tags: ["transformers", "safetensors", "gemma4", "image-text-to-text", "system-one", "system-two", "adaptive-thinking", "typed-decisions", "decision-model", "calibrated-probabilities", "jev", "noul", "choice", "score", "lora", "mixture-of-experts", "multimodal", "vllm", "nvfp4", "modelopt", "fp4", "text-classification", "en", "base_model:autotrust/GEV-26B-Decide", "base_model:quantized:autotrust/GEV-26B-Decide", "license:apache-2.0", "model-index", "endpoints_compatible", "8-bit", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 164개, 다운로드 19,655회(수집 시점 2026-10-08). 이전 모델 autotrust/GEV-26B-Decide(파라미터 25.8B, 다운로드 854,574) 대비 이번 모델은 파라미터 44.2% 감소, 다운로드 97.7% 감소, 라이선스 동일(apache-2.0).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-classification` |
| 파라미터 | 14.4B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-10-05 |
| 좋아요 | 164 |
| 다운로드 | 19,655 |

## 요약

This repository is **autotrust/GEV-26B-Decide with its 3,840 routed expert MLPs (30 layers × 128 experts) quantized to NVFP4**. Everything else is the bf16 model unchanged: attention, the dense MLP of every layer, the routers, the vision tower, the lm_head, the System 1 adapter, the decision head and the temperatures. The rest of this card is the card of GEV-26B-Decide; its benchmark tables are the bf16 results, and the NVFP4 comparison is below.

GPQA Diamond and HLE are the Decision Index items; the bf16 row is the model's `transformers` engine, the NVFP4 row is vLLM with this checkpoint. Th…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [GEV 26B Decide](../autotrust__GEV-26B-Decide/)
- [JEV 27B VL](../autotrust__JEV-27B-VL/)
- [GLM5.3 Flash E224 DGX Spark](../autotrust__GLM5.3-Flash-E224-DGX-Spark/)
- [openjev](../AlexWortega__openjev/)
- [Julia 1](../SupersonicLabs__Julia-1/)
- [Jev Omni](../akhilaaa3__Jev-Omni/)
