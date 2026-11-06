---
model_id: "tencent/WeVisCut"
title: "WeVisCut"
org: "tencent"
task: "any-to-any"
license: "other"
params: "9.4B"
likes: 26
downloads: 16139
discovered_at: "2026-11-06"
created_at: "2026-09-09"
hf_url: "https://huggingface.co/tencent/WeVisCut"
tags: ["transformers", "safetensors", "qwen3_5", "image-text-to-text", "video-editing", "agent", "tool-use", "long-horizon", "reinforcement-learning", "qwen3.5", "any-to-any", "arxiv:2610.38352", "base_model:Qwen/Qwen3.5-9B", "base_model:finetune:Qwen/Qwen3.5-9B", "license:other", "endpoints_compatible", "region:us"]
reason: "new, updated, surge"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 최근 7일 사이 좋아요·다운로드가 급증했습니다. 이 기준에 해당해 선정했습니다. 좋아요 26개, 다운로드 16,139회(수집 시점 2026-11-06). 급상승 근거(7일 전 2026-10-30 스냅샷 대비): 좋아요 11→26(+136.4%), 다운로드 4→16,139(+403375.0%). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `any-to-any` |
| 파라미터 | 9.4B |
| 라이선스 | other |
| 최초 등록일 | 2026-09-09 |
| 좋아요 | 26 |
| 다운로드 | 16,139 |

## 요약

**WeVisCut** is a 9B tool-using agent that turns knowledge articles or narration scripts into multi-minute edited videos. At each step, it reads the current editing state and selects one of 12 tools for planning, narration, asset retrieval, composition, inspection, or repair. It is not a standalone text-to-video model; use it with the [WeVisCut runtime](https://github.com/Tencent/WeVisCut), which executes the model's tool calls.

Requirements: Python 3.11 or later and an NVIDIA GPU with about 24 GB of memory for bf16 inference. Install a PyTorch build compatible with your CUDA version before t…

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [AuK](../tencent__AuK/)
- [AuK Flash](../tencent__AuK-Flash/)
- [ContextPilot 14B](../tencent__ContextPilot-14B/)
- [LFM3 Audio 2B](../LiquidAI__LFM3-Audio-2B/)
- [LFM3 Omni 2B](../LiquidAI__LFM3-Omni-2B/)
