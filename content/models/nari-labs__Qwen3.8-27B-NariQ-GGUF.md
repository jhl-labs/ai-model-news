---
model_id: "nari-labs/Qwen3.8-27B-NariQ-GGUF"
title: "Qwen3.8 27B NariQ GGUF"
org: "nari-labs"
task: "image-text-to-text"
license: "apache-2.0"
params: ""
likes: 37
downloads: 2243
discovered_at: "2026-11-23"
created_at: "2026-11-20"
hf_url: "https://huggingface.co/nari-labs/Qwen3.8-27B-NariQ-GGUF"
tags: ["gguf", "nariq", "qwen", "quantized", "coding-agent", "llama.cpp", "image-text-to-text", "arxiv:2611.26157", "arxiv:2406.11235", "base_model:Qwen/Qwen3.8-27B", "base_model:quantized:Qwen/Qwen3.8-27B", "license:apache-2.0", "endpoints_compatible", "region:us", "conversational"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 37개, 다운로드 2,243회(수집 시점 2026-11-23). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `image-text-to-text` |
| 파라미터 | 정보 없음 |
| 라이선스 | apache-2.0 |
| 최초 등록일 | 2026-11-20 |
| 좋아요 | 37 |
| 다운로드 | 2,243 |

## 요약

(Nov 20, 2026) We are releasing NariQ v1 GGUFs of Qwen3.8-27B at 3, 2.5 and 2 bits per weight. Run them on our **[llama.cpp fork](https://github.com/nari-labs/nari-llama.cpp) (required)**.

- **The 3-bit and 2.5-bit files match BF16 on long-horizon agent tasks**, math and image understanding. The 2-bit file scores lower. - **NariQ** is a **trellis-coded** post-training quantization (PTQ), calibrated on real coding-agent traces and stored in a layout that runs on a single GPU. - More details are in the [tech report](https://arxiv.org/abs/2611.26157).

One command on Linux with an NVIDIA GPU and…

## 라이선스

apache-2.0 — 상업 이용 가능

## 관련 모델

- [Agnes 3.0 Flash](../Agnes-AI__Agnes-3.0-Flash/)
- [mirage](../Cactus-Compute__mirage/)
- [clef](../Cloudflare__clef/)
