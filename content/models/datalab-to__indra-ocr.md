---
model_id: "datalab-to/indra-ocr"
title: "indra ocr"
org: "datalab-to"
task: "image-to-text"
license: "openrail"
params: "1.2M"
likes: 165
downloads: 1053
discovered_at: "2026-10-17"
created_at: "2026-10-10"
hf_url: "https://huggingface.co/datalab-to/indra-ocr"
tags: ["onnx", "safetensors", "indra-ocr", "ocr", "cpu", "pdf", "markdown", "layout", "document-parsing", "image-to-text", "en", "fr", "de", "es", "it", "pt", "nl", "pl", "ru", "uk", "el", "hi", "bn", "zh", "license:openrail", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 165개, 다운로드 1,053회(수집 시점 2026-10-17). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-to-text` |
| 파라미터 | 1.2M |
| 라이선스 | openrail |
| 최초 등록일 | 2026-10-10 |
| 좋아요 | 165 |
| 다운로드 | 1,053 |

## 요약

Indra OCR is a 1M-parameter OCR model that reads up to 49 pages per second on CPU. It turns PDFs and images into markdown, plain text, or JSON with boxes, and it has these features:

- Throughput - 49 pages/s, 11-17x faster than Tesseract and PaddleOCR on the same machine and pages ([table](#throughput)) - Latency - ~230 ms per page on 4 x86 vCPUs, 12-24x faster than Tesseract and PaddleOCR - Accuracy - scores 41.3 on [OmniParseBench](https://github.com/datalab-to/omni_parse_bench) text, ahead of PaddleOCR's PP-OCR text models (35.8) and Tesseract (19.3). Its headline score (62.1) beats Paddle…

## 라이선스

openrail — 상업 이용 가능

## 관련 모델

- [PixelUMM](../nvidia__PixelUMM/)
