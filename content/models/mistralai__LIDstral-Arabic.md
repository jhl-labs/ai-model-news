---
model_id: "mistralai/LIDstral-Arabic"
title: "LIDstral Arabic"
org: "mistralai"
task: "text-classification"
license: "apache-2.0"
params: ""
likes: 20
downloads: 80
discovered_at: "2026-10-14"
created_at: "2026-10-08"
hf_url: "https://huggingface.co/mistralai/LIDstral-Arabic"
tags: ["fasttext", "language-identification", "dialect-identification", "text-classification", "ar", "ary", "ayl", "aeb", "arq", "mey", "tzm", "zgh", "afb", "ars", "acx", "ayn", "arz", "apd", "acm", "ajp", "apc", "shu", "az", "tr", "kk", "ky", "uz", "fa", "ps", "ur"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 20개, 다운로드 80회(수집 시점 2026-10-14). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `text-classification` |
| 파라미터 | 정보 없음 |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-10-08 |
| 좋아요 | 20 |
| 다운로드 | 80 |

## 요약

LIDstral Arabic is a fast language and dialect classifier for text written in Arabic script. It identifies Modern Standard Arabic, all Arabic dialects, and non-Arabic languages that use the same script.

We include these non-Arabic languages in training to help the model distinguish languages that share a script and avoid classifying text as Arabic based on its script alone.

The model combines a fastText one-vs-all (OVA) classifier, an MLP stacker, and per-class isotonic calibration:

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [Voxtral Mini 4B Realtime Arabic](../mistralai__Voxtral-Mini-4B-Realtime-Arabic/)
- [openjev](../AlexWortega__openjev/)
- [Phocinae Largha 150M v1](../Phocinae__Phocinae-Largha-150M-v1/)
- [Julia 1](../SupersonicLabs__Julia-1/)
