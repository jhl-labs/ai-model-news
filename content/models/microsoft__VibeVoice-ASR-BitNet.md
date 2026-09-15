---
model_id: "microsoft/VibeVoice-ASR-BitNet"
title: "VibeVoice ASR BitNet"
org: "microsoft"
task: "automatic-speech-recognition"
license: "mit"
params: "322.6M"
likes: 198
downloads: 28179
discovered_at: "2026-09-15"
created_at: "2026-07-24"
hf_url: "https://huggingface.co/microsoft/VibeVoice-ASR-BitNet"
tags: ["ggml", "safetensors", "gguf", "vibevoice", "ASR", "quantization", "cpu-inference", "bitnet", "multilingual", "automatic-speech-recognition", "en", "zh", "fr", "it", "ko", "pt", "vi", "arxiv:2607.21075", "license:mit", "endpoints_compatible", "region:us", "conversational"]
reason: "new, surge"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 7일 사이 좋아요·다운로드가 급증했습니다. 이 기준에 해당해 선정했습니다. 좋아요 198개, 다운로드 28,179회(수집 시점 2026-09-15). 급상승 근거(7일 전 2026-09-08 스냅샷 대비): 좋아요 195→198(+1.5%), 다운로드 13,329→28,179(+111.4%). 이전 모델 microsoft/VibeVoice-ASR-Streaming-7B(파라미터 8.7B, 다운로드 573) 대비 이번 모델은 파라미터 96.3% 감소, 다운로드 4817.8% 증가, 라이선스 동일(mit).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `automatic-speech-recognition` |
| 파라미터 | 322.6M |
| 라이선스 | mit |
| 최초 등록일 | 2026-07-24 |
| 좋아요 | 198 |
| 다운로드 | 28,179 |

## 요약

**VibeVoice-ASR-BitNet** is a compressed variant of [VibeVoice-ASR](https://huggingface.co/microsoft/VibeVoice-ASR) optimized for **real-time inference on edge CPUs** — no GPU required. Through heterogeneous quantization, the model is compressed from 4.62 GB to **1.58 GB** while achieving **1.6–2.3× faster** inference than Whisper.cpp with real-time capability (RTF < 1) on as few as 3 CPU threads.

➡️ **Code:** [microsoft/VibeASR.cpp](https://github.com/microsoft/VibeASR.cpp) ➡️ **Report:** [VibeVoice-ASR-BitNet Technical Report](https://arxiv.org/abs/2607.21075) ➡️ **Base Model:** [microsoft/…

## 라이선스

mit — 상업 이용 가능

## 관련 모델

- [VibeVoice ASR Streaming 1.5B](../microsoft__VibeVoice-ASR-Streaming-1.5B/)
- [VibeVoice ASR Streaming 7B](../microsoft__VibeVoice-ASR-Streaming-7B/)
