---
model_id: "tencent/Hy-Memory-30B-A3B"
title: "Hy Memory 30B A3B"
org: "tencent"
task: "text-generation"
license: "apache-2.0"
params: "30.1B"
likes: 113
downloads: 0
discovered_at: "2026-10-16"
created_at: "2026-10-15"
hf_url: "https://huggingface.co/tencent/Hy-Memory-30B-A3B"
tags: ["transformers", "safetensors", "hy_v3", "text-generation", "conversational", "en", "zh", "arxiv:2610.22196", "license:apache-2.0", "endpoints_compatible", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 113개, 다운로드 0회(수집 시점 2026-10-16). 이전 모델 tencent/ContextPilot-14B(파라미터 14.8B, 다운로드 804) 대비 이번 모델은 파라미터 103.4% 증가, 다운로드 100.0% 감소, 라이선스 other→apache-2.0.

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-generation` |
| 파라미터 | 30.1B |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-10-15 |
| 좋아요 | 113 |
| 다운로드 | 0 |

## 요약

**Hy-Memory-30B-A3B** is a compact long-term-memory writer model (~3B active parameters) developed by Tencent Hunyuan to execute the write path inside external memory frameworks. It directly replaces the general-purpose LLM inside **Mem0**, **MemOS**, and **Hy-Memory** (covering Chat, Working, and Coding scenarios), deciding what information to retain, how precisely to represent it, and how new evidence should update the persistent memory bank. The model is trained in two stages—Memory On-Policy Distillation (OPD) followed by Attributed Memory Reinforcement Learning—and transfers directly to u…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [AuK](../tencent__AuK/)
- [AuK Flash](../tencent__AuK-Flash/)
- [ContextPilot 14B](../tencent__ContextPilot-14B/)
- [Kolibri 1](../Aleph-Alpha__Kolibri-1/)
- [Hemmingway 1](../Altworld__Hemmingway-1/)
- [claude fable 5 1](../Anthropic__claude-fable-5-1/)
