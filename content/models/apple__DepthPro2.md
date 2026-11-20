---
model_id: "apple/DepthPro2"
title: "DepthPro2"
org: "apple"
task: "depth-estimation"
license: "other"
params: ""
likes: 112
downloads: 0
discovered_at: "2026-11-20"
created_at: "2026-11-03"
hf_url: "https://huggingface.co/apple/DepthPro2"
tags: ["depth-pro-2", "depth-estimation", "metric-depth", "monocular-depth", "video-depth", "arxiv:2611.26603", "license:other", "region:us"]
reason: "new, updated, trending, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. Hugging Face 트렌딩 상위 30위 안에 들었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 112개, 다운로드 0회(수집 시점 2026-11-20). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `depth-estimation` |
| 파라미터 | 정보 없음 |
| 라이선스 | other |
| 최초 등록일 | 2026-11-03 |
| 좋아요 | 112 |
| 다운로드 | 0 |

## 요약

Depth Pro 2 estimates metric depth for every pixel from an ordinary camera: a single photo, a whole video, or a live feed, at the input's full resolution. Its depth is sharp at object edges and steady from frame to frame.

Each size is its own repository with its weights. Larger sizes give sharper, steadier depth; smaller ones run faster.

All sizes share a focal length estimator, [apple/DepthPro2-focal](https://huggingface.co/apple/DepthPro2-focal) (23.5M parameters, 94 MB), which loads with each size and predicts the focal length when it is unknown.

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [FastFrames L](../apple__FastFrames-L/)
- [FastFrames S](../apple__FastFrames-S/)
- [LensVLM 9B](../apple__LensVLM-9B/)
