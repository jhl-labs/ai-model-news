---
model_id: "nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2"
title: "Qwen3.8 27B Coder390 EfficientThink Opus5.5 GPT6Astra Grok4.7 DSV4Pro K3 SFT RLOO MTP DFlash2"
org: "nerkyor"
task: "image-text-to-text"
license: "apache-2.0"
params: ""
likes: 185
downloads: 42336
discovered_at: "2026-10-10"
created_at: "2026-10-04"
hf_url: "https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2"
tags: ["safetensors", "gguf", "qwen3.8", "efficient-thinking", "reasoning", "coding", "uncensored", "sft", "simpo", "rloo", "fp8", "bf16", "nvfp4", "modelopt", "quantization", "calibration", "static-quantization", "compressed-tensors", "gsq-rco", "gsq", "rco", "hessian", "imatrix", "block128", "mtp", "dflash2", "speculative-decoding", "multimodal", "sglang", "vllm"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 185개, 다운로드 42,336회(수집 시점 2026-10-10). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-text` |
| 파라미터 | 정보 없음 |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-10-04 |
| 좋아요 | 185 |
| 다운로드 | 42,336 |

## 요약

A model post-trained with several rounds of SFT and RLOO on top of [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2), which is itself the official [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) post-trained with SFT and SimPO. It is built to fix the original model's habit of failing to stop: it already has an answer, yet keeps re-deriving until it hits the 94K cap with no final answer. This repository provides five safetensors tiers, **BF16**, **static FP8 Block128**, **NVFP4…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [Agnes 3.0 Flash](../Agnes-AI__Agnes-3.0-Flash/)
- [clef](../Cloudflare__clef/)
- [clef flash](../Cloudflare__clef-flash/)
