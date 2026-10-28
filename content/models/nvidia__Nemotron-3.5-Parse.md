---
model_id: "nvidia/Nemotron-3.5-Parse"
title: "Nemotron 3.5 Parse"
org: "nvidia"
task: "image-text-to-text"
license: "openmdw-1.1"
params: "630.8M"
likes: 132
downloads: 10678
discovered_at: "2026-10-28"
created_at: "2026-09-03"
hf_url: "https://huggingface.co/nvidia/Nemotron-3.5-Parse"
tags: ["transformers", "safetensors", "nemotron_parse", "text-generation", "VLM", "OCR", "Parse", "image-text-to-text", "conversational", "custom_code", "license:openmdw-1.1", "eval-results", "endpoints_compatible", "region:us"]
reason: "new, updated, surge"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 최근 7일 사이 좋아요·다운로드가 급증했습니다. 이 기준에 해당해 선정했습니다. 좋아요 132개, 다운로드 10,678회(수집 시점 2026-10-28). 급상승 근거(7일 전 2026-10-21 스냅샷 대비): 좋아요 42→132(+214.3%), 다운로드 1,217→10,678(+777.4%). 이전 모델 nvidia/Flora-Captioner(파라미터 27.4B, 다운로드 521) 대비 이번 모델은 파라미터 97.7% 감소, 다운로드 1949.5% 증가, 라이선스 other→openmdw-1.1.

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-text` |
| 파라미터 | 630.8M |
| 라이선스 | openmdw-1.1 |
| 최초 등록일 | 2026-09-03 |
| 좋아요 | 132 |
| 다운로드 | 10,678 |

## 요약

Nemotron 3.5 Parse is a document image parser that produces structured, machine-readable text with semantic layout classes, bounding boxes, and reading order. It combines a C-RADIOv4-SO400M vision encoder with a 10-layer mBART decoder that consumes the visual sequence as a causal prefix. The release uses dynamic rectangular NaViT preprocessing, content-normalized coordinates, grouped-query self-attention (16 query heads and 8 key/value heads), a 72,505-token multilingual tokenizer, and chart-aware output through the `` token. It is intended for document understanding, information retrieval, da…

## 라이선스

openmdw-1.1 — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [DeepSeek V4 Flash 0731 NVFP4](../nvidia__DeepSeek-V4-Flash-0731-NVFP4/)
- [DeepSeek V4.1 Flash NVFP4](../nvidia__DeepSeek-V4.1-Flash-NVFP4/)
- [Flora Captioner](../nvidia__Flora-Captioner/)
- [Agnes 3.0 Flash](../Agnes-AI__Agnes-3.0-Flash/)
- [clef](../Cloudflare__clef/)
- [clef flash](../Cloudflare__clef-flash/)
