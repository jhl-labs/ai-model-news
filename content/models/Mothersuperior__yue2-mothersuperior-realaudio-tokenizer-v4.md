---
model_id: "Mothersuperior/yue2-mothersuperior-realaudio-tokenizer-v4"
title: "yue2 mothersuperior realaudio tokenizer v4"
org: "Mothersuperior"
task: "other"
license: "cc-by-nc-4.0"
params: ""
likes: 144
downloads: 0
discovered_at: "2026-09-19"
created_at: "2026-09-13"
hf_url: "https://huggingface.co/Mothersuperior/yue2-mothersuperior-realaudio-tokenizer-v4"
tags: ["audio", "music", "yue2", "tokenizer", "lora", "base_model:m-a-p/MERT-v2-FullSong", "base_model:adapter:m-a-p/MERT-v2-FullSong", "license:cc-by-nc-4.0", "region:us"]
reason: "new, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 144개, 다운로드 0회(수집 시점 2026-09-19). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `other` |
| 파라미터 | 정보 없음 |
| 라이선스 | cc-by-nc-4.0 |
| 최초 등록일 | 2026-09-13 |
| 좋아요 | 144 |
| 다운로드 | 0 |

## 요약

Real-audio tooling for [YuE2-3B](https://huggingface.co/m-a-p/YuE2-3B): the **audio → semantic-token encoder** YuE2 doesn't ship, plus a **NAR-branch LoRA** so the decoder renders real-production latents. Together they let you tokenize your own recordings, LoRA-tune YuE2's AR on an artist, and generate new songs or covers.

Same weights as the `.pt` files, bit-exact in fp32 (the `.bf16` variants are half the size; head top-1 agreement with fp32 is 98.6%). The previously published scripts accept either extension via `scripts/ckpt_io.load_ckpt(path)`, which returns the same dict the `.pt` files…

## 라이선스

cc-by-nc-4.0 — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [Minimax H3 ComfyUI](../Alissonerdx__Minimax-H3-ComfyUI/)
- [YuE2](../Comfy-Org__YuE2/)
- [granite 4.2 3b GGUF](../ibm-granite__granite-4.2-3b-GGUF/)
