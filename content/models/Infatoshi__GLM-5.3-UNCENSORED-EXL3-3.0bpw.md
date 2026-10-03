---
model_id: "Infatoshi/GLM-5.3-UNCENSORED-EXL3-3.0bpw"
title: "GLM 5.3 UNCENSORED EXL3 3.0bpw"
org: "Infatoshi"
task: "text-generation"
license: "mit"
params: "146.3B"
likes: 177
downloads: 520
discovered_at: "2026-10-03"
created_at: "2026-10-01"
hf_url: "https://huggingface.co/Infatoshi/GLM-5.3-UNCENSORED-EXL3-3.0bpw"
tags: ["exllamav3", "safetensors", "glm_moe_dsa", "exl3", "glm", "moe", "uncensored", "text-generation", "conversational", "base_model:dealignai/GLM-5.3-UNCENSORED-FP8", "base_model:quantized:dealignai/GLM-5.3-UNCENSORED-FP8", "license:mit", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 177개, 다운로드 520회(수집 시점 2026-10-03). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-generation` |
| 파라미터 | 146.3B |
| 라이선스 | mit |
| 최초 등록일 | 2026-10-01 |
| 좋아요 | 177 |
| 다운로드 | 520 |

## 요약

EXL3 quantization of [dealignai/GLM-5.3-UNCENSORED-FP8](https://huggingface.co/dealignai/GLM-5.3-UNCENSORED-FP8), itself a weight-edited (no fine-tune) variant of [zai-org/GLM-5.3](https://huggingface.co/zai-org/GLM-5.3). The edit is documented in `CRACK_SURGERY.json` (copied unchanged from the source repo). This repo is not affiliated with dealignai or Z.ai.

- Architecture: `GlmMoeDsaForCausalLM`, 753B total parameters, 256 routed experts (8 active) + 1 shared, MLA attention with DSA sparse indexer, 78 layers + 1 MTP layer - Average bitrate: 3.04 bpw (`-b 3.0 --hq`; attention and shared expe…

## 라이선스

mit — 상업 이용 가능

## 관련 모델

- [Hemmingway 1](../Altworld__Hemmingway-1/)
- [claude fable 5 1](../Anthropic__claude-fable-5-1/)
- [claude mythos 5 1](../Anthropic__claude-mythos-5-1/)
