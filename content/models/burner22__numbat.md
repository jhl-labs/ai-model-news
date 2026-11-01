---
model_id: "burner22/numbat"
title: "numbat"
org: "burner22"
task: "other"
license: "unknown"
params: "6.8T"
likes: 180
downloads: 5846
discovered_at: "2026-11-01"
created_at: "2026-10-23"
hf_url: "https://huggingface.co/burner22/numbat"
tags: ["safetensors", "numbat", "custom_code", "8-bit", "modelopt", "region:us"]
reason: "new, updated, trending"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 180개, 다운로드 5,846회(수집 시점 2026-11-01). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `other` |
| 파라미터 | 6.8T |
| 라이선스 | unknown |
| 최초 등록일 | 2026-10-23 |
| 좋아요 | 180 |
| 다운로드 | 5,846 |

## 요약

~14T param, 114 layers, hybrid GDN/MLA, MoE (1,224 experts, top-48 + 1 shared), NVFP4. Internal codename `numbat`, Anthropic's next Mythos-class training run. `numbat` is the codename referenced in the Claude Code source leak (Mar 2026). This is a checkpoint from that training run, pulled mid-pretraining.

The 772 shards total ~7.72 TB of tensor data. Each shard is safetensors format, under 10.6 GB per file.

`configuration_numbat.py` and `modeling_numbat.py` are included: a complete reference implementation of the checkpoint. Its module tree has an exact slot for every tensor in every shard,…

## 라이선스

unknown — 라이선스 정보 없음 — 원문 확인 필요

## 관련 모델

- [Minimax H3 ComfyUI](../Alissonerdx__Minimax-H3-ComfyUI/)
- [Fibo 2.0](../Comfy-Org__Fibo-2.0/)
- [MOSS Image](../Comfy-Org__MOSS-Image/)
