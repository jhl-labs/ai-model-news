---
model_id: "moondream/parakeet-redux"
title: "parakeet redux"
org: "moondream"
task: "automatic-speech-recognition"
license: "cc-by-4.0"
params: "148.9M"
likes: 267
downloads: 14056
discovered_at: "2026-10-09"
created_at: "2026-09-18"
hf_url: "https://huggingface.co/moondream/parakeet-redux"
tags: ["safetensors", "parakeet_tdt", "ternary", "parakeet", "tdt", "speech-recognition", "cpu", "apple-silicon", "automatic-speech-recognition", "en", "de", "fr", "es", "it", "pt", "ru", "uk", "hr", "sl", "lv", "lt", "et", "fi", "sv", "da", "nl", "pl", "cs", "sk", "hu"]
reason: "new, surge"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 7일 사이 좋아요·다운로드가 급증했습니다. 이 기준에 해당해 선정했습니다. 좋아요 267개, 다운로드 14,056회(수집 시점 2026-10-09). 급상승 근거(7일 전 2026-09-28 스냅샷 대비): 좋아요 168→267(+58.9%), 다운로드 6,086→14,056(+131.0%). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `automatic-speech-recognition` |
| 파라미터 | 148.9M |
| 라이선스 | cc-by-4.0 |
| 최초 등록일 | 2026-09-18 |
| 좋아요 | 267 |
| 다운로드 | 14,056 |

## 요약

A 1.58-bit version of [parakeet-tdt-0.6b-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3). Same architecture, same tokenizer, but every encoder weight is -1, 0 or +1. It fits in 178 MB, runs at 113× real time on eight x86 CPU cores, 2.5× the fastest other Parakeet runtime we measured, and stays within 0.3 WER of the original on English while beating it on the 25-language FLEURS set and on long-form audio.

Its sibling [Parakeet Ultra](https://huggingface.co/moondream/parakeet-ultra) is the full-precision version of the same architecture, trained further, for GPUs: better than the origin…

## 라이선스

cc-by-4.0 — 상업 이용 가능

## 관련 모델

- [whistle](../Cactus-Compute__whistle/)
- [Audio8 ASR Infinite](../Edge0__Audio8-ASR-Infinite/)
- [Phonon 2](../FermionResearch__Phonon-2/)
