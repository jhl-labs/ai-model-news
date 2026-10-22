---
model_id: "nvidia/RFD4-Proteina"
title: "RFD4 Proteina"
org: "nvidia"
task: "other"
license: "bsd-3-clause"
params: "435.6M"
likes: 20
downloads: 919
discovered_at: "2026-10-22"
created_at: "2026-10-06"
hf_url: "https://huggingface.co/nvidia/RFD4-Proteina"
tags: ["rfd4-proteina", "safetensors", "rfd4_proteina", "biology", "protein-design", "biomolecular-design", "structure-generation", "flow-matching", "annotated-cif", "en", "dataset:nvidia/RFD4-Proteina", "license:bsd-3-clause", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 20개, 다운로드 919회(수집 시점 2026-10-22). 이전 모델 nvidia/NV-Generate-CT(파라미터 정보 없음, 다운로드 11,643) 대비 이번 모델은 파라미터 비교 정보 없음, 다운로드 92.1% 감소, 라이선스 other→bsd-3-clause.

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `other` |
| 파라미터 | 435.6M |
| 라이선스 | bsd-3-clause |
| 최초 등록일 | 2026-10-06 |
| 좋아요 | 20 |
| 다운로드 | 919 |

## 요약

RFD4-Proteína is a flow-matching model for biomolecular design. It generates protein sequences and all-atom structures together, conditioned on the molecular context you want to preserve: a binding target, an enzyme motif, a ligand, or selected structural features.

This repository is the **canonical native bundle**. `config.json` and `model.safetensors` at the root are the *native* weights, loaded by `Proteina.from_pretrained`.

It is one model throughout — nothing is retrained. The Diffusers weights are the same tensors re-prefixed and split across `transformer/` and `vae/`. Diffusers needs…

## 라이선스

bsd-3-clause — 상업 이용 가능

## 관련 모델

- [DeepSeek V4 Flash 0731 NVFP4](../nvidia__DeepSeek-V4-Flash-0731-NVFP4/)
- [DeepSeek V4.1 Flash NVFP4](../nvidia__DeepSeek-V4.1-Flash-NVFP4/)
- [GLM 5.3 Flash FP4 Local](../nvidia__GLM-5.3-Flash-FP4-Local/)
- [Minimax H3 ComfyUI](../Alissonerdx__Minimax-H3-ComfyUI/)
- [MOSS Image](../Comfy-Org__MOSS-Image/)
- [Qwen Image 2.1](../Comfy-Org__Qwen-Image-2.1/)
