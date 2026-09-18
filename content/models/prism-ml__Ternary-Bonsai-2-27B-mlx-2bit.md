---
model_id: "prism-ml/Ternary-Bonsai-2-27B-mlx-2bit"
title: "Ternary Bonsai 2 27B mlx 2bit"
org: "prism-ml"
task: "text-generation"
license: "apache-2.0"
params: "27.4B"
likes: 166
downloads: 5056
discovered_at: "2026-09-18"
created_at: "2026-09-16"
hf_url: "https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit"
tags: ["mlx", "safetensors", "prism_hadamard_qwen35", "ternary", "2-bit", "cuda", "metal", "on-device", "hybrid-attention", "prismml", "bonsai", "text-generation", "conversational", "base_model:Qwen/Qwen3.8-27B", "base_model:finetune:Qwen/Qwen3.8-27B", "license:apache-2.0", "region:us"]
reason: "new, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 166개, 다운로드 5,056회(수집 시점 2026-09-18). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-generation` |
| 파라미터 | 27.4B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-09-16 |
| 좋아요 | 166 |
| 다운로드 | 5,056 |

## 요약

Full 27B-class reasoning in ternary transformer weights — on everyday laptops

**8.60 GB** on disk, language model + vision tower | **98.2%** of FP16 intelligence retained | **\~47 tok/s** on an Apple M5 Max laptop

- **8.60 GB** on disk: a 7.67 GB language model (down from \~54 GB FP16) plus the 0.92 GB vision tower. MLX's container stores a scale and a bias per group, so the language model costs 2.25 bits/weight where the same ternary weights take 1.75 in the GGUF PTQ1_0 packing - **98.2% of FP16 intelligence retained**: 84.78 average across 14 thinking-mode benchmarks — far above the conven…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [Edge0 35B A3B preview](../Edge0__Edge0-35B-A3B-preview/)
- [K2 Horizon MoVA 36B A4B](../IFM__K2-Horizon-MoVA-36B-A4B/)
- [Qwen3.8 27B OBLITERATED](../OBLITERATUS__Qwen3.8-27B-OBLITERATED/)
