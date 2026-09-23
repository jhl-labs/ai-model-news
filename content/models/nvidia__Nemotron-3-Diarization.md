---
model_id: "nvidia/Nemotron-3-Diarization"
title: "Nemotron 3 Diarization"
org: "nvidia"
task: "voice-activity-detection"
license: "openmdw-1.1"
params: "99.2M"
likes: 98
downloads: 27
discovered_at: "2026-09-23"
created_at: "2026-09-01"
hf_url: "https://huggingface.co/nvidia/Nemotron-3-Diarization"
tags: ["nemo", "safetensors", "nemotron3_diarization", "audio-frame-classification", "speaker-diarization", "streaming-sortformer", "speaker-tagging", "transformers", "voice-activity-detection", "arxiv:2409.06656", "arxiv:2507.18446", "arxiv:2605.15442", "arxiv:2507.09226", "arxiv:2408.13106", "license:openmdw-1.1", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 98개, 다운로드 27회(수집 시점 2026-09-23). 이전 모델 nvidia/Nemotron-3-Diarization-preview(파라미터 정보 없음, 다운로드 110) 대비 이번 모델은 파라미터 비교 정보 없음, 다운로드 75.5% 감소, 라이선스 other→openmdw-1.1.

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `voice-activity-detection` |
| 파라미터 | 99.2M |
| 라이선스 | openmdw-1.1 |
| 최초 등록일 | 2026-09-01 |
| 좋아요 | 98 |
| 다운로드 | 27 |

## 요약

**[Nemotron 3 Diarization](https://huggingface.co/blog/nvidia/nemotron-diarization)** is an open-weight speaker diarization model designed to determine "who spoke when" in real-world audio. It supports both streaming and offline inference and handles up to eight speakers. Following Sortformer [\[1\]](#ref-1), the model resolves speaker permutation by ordering its output channels according to each speaker's first arrival in the input audio.

For streaming inference, the model adopts the Arrival-Order Speaker Cache (AOSC) and FIFO queue introduced in **Streaming Sortformer** [\[2\]](#ref-2). The…

## 라이선스

openmdw-1.1 — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [DeepSeek V4 Flash 0731 NVFP4](../nvidia__DeepSeek-V4-Flash-0731-NVFP4/)
- [DeepSeek V4.1 Flash NVFP4](../nvidia__DeepSeek-V4.1-Flash-NVFP4/)
- [GLM 5.3 Flash NVFP4](../nvidia__GLM-5.3-Flash-NVFP4/)
- [Nemotron 3 Diarization preview](../nvidia__Nemotron-3-Diarization-preview/)
