---
model_id: "tencent/Qwen3-8B-DSpine-b16"
title: "Qwen3 8B DSpine b16"
org: "tencent"
task: "other"
license: "apache-2.0"
params: "1.2B"
likes: 21
downloads: 151
discovered_at: "2026-10-17"
created_at: "2026-10-16"
hf_url: "https://huggingface.co/tencent/Qwen3-8B-DSpine-b16"
tags: ["safetensors", "qwen3", "custom_code", "arxiv:2609.36173", "license:apache-2.0", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 21개, 다운로드 151회(수집 시점 2026-10-17). 이전 모델 tencent/WeVisDoc-2B(파라미터 2.4B, 다운로드 1,141) 대비 이번 모델은 파라미터 50.0% 감소, 다운로드 86.8% 감소, 라이선스 동일(apache-2.0).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `other` |
| 파라미터 | 1.2B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-10-16 |
| 좋아요 | 21 |
| 다운로드 | 151 |

## 요약

DSpine is a parallel drafter for speculative decoding. At every draft layer, each position receives the predicted feature of its predecessor, so the causal chain unfolds over network depth while all positions are still drafted in parallel.

- **[2026-10]** Inference code released. - **[2026-09]** Paper released on [arXiv](https://arxiv.org/abs/2609.36173).

Acceptance length on Qwen3-8B. DSpine, DSpark and DFlash2 are all retrained on [Open-PerfectBlend](https://huggingface.co/datasets/mlabonne/open-perfectblend) with the same configuration.

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [AuK](../tencent__AuK/)
- [AuK Flash](../tencent__AuK-Flash/)
- [ContextPilot 14B](../tencent__ContextPilot-14B/)
- [Minimax H3 ComfyUI](../Alissonerdx__Minimax-H3-ComfyUI/)
- [Qwen Image 2.1](../Comfy-Org__Qwen-Image-2.1/)
- [YuE2](../Comfy-Org__YuE2/)
