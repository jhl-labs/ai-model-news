---
model_id: "apple/DepthPro2-H"
title: "DepthPro2 H"
org: "apple"
task: "depth-estimation"
license: "other"
params: "872.1M"
likes: 24
downloads: 1216
discovered_at: "2026-11-23"
created_at: "2026-11-05"
hf_url: "https://huggingface.co/apple/DepthPro2-H"
tags: ["depth-pro-2", "safetensors", "depth-estimation", "metric-depth", "monocular-depth", "video-depth", "arxiv:2611.26603", "license:other", "region:us"]
reason: "new, updated, major-org"
---

## 왜 주목받는가

최근 60일 내 최초 공개된 신규 모델입니다. 최근 14일 내 의미 있는 갱신이 있었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 24개, 다운로드 1,216회(수집 시점 2026-11-23). 이전 모델 apple/DepthPro2-focal(파라미터 23.5M, 다운로드 370) 대비 이번 모델은 파라미터 3611.1% 증가, 다운로드 228.6% 증가, 라이선스 동일(other).

## 핵심 스펙

| 항목 | 값 |
| --- | --- |
| 태스크 | `depth-estimation` |
| 파라미터 | 872.1M |
| 라이선스 | other |
| 최초 등록일 | 2026-11-05 |
| 좋아요 | 24 |
| 다운로드 | 1,216 |

## 요약

- **GPU:** NVIDIA B200, in bfloat16 and PyTorch eager mode (no compilation) - **Input:** a 32-frame video clip, processed in one call at its native resolution - **Resolutions:** VGA is 640 × 480; 720p, 1080p and 4K are 16:9 - **Throughput:** frames per second, averaged over the clip - **Memory:** the peak GPU memory PyTorch reserves - **Included:** the [focal length estimator](https://huggingface.co/apple/DepthPro2-focal), a separate 23.5M-parameter model that loads with the depth model

Videos, the other sizes and the command line are on the [Depth Pro 2 page](https://huggingface.co/apple/Dep…

## 라이선스

other — 상업 이용 제한 또는 확인 필요

## 관련 모델

- [DepthPro2](../apple__DepthPro2/)
- [DepthPro2 focal](../apple__DepthPro2-focal/)
- [FastFrames L](../apple__FastFrames-L/)
