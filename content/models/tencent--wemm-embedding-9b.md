---
model_id: "tencent/WeMM-Embedding-9B"
title: "WeMM Embedding 9B"
org: "tencent"
task: "feature-extraction"
license: "other"
params: "9.4B"
likes: 114
downloads: 3360
discovered_at: "2026-09-05"
created_at: "2026-08-25"
hf_url: "https://huggingface.co/tencent/WeMM-Embedding-9B"
tags: ["transformers", "safetensors", "qwen3_5", "image-text-to-text", "sentence-transformers", "multimodal-embedding", "text-embedding", "image-embedding", "video-embedding", "mrl", "feature-extraction", "custom_code", "zh", "en", "arxiv:2608.24053", "base_model:Qwen/Qwen3.5-9B", "base_model:finetune:Qwen/Qwen3.5-9B", "license:other", "endpoints_compatible", "region:us"]
reason: "major-org"
---

## 요약

WeMM-Embedding-9B is a universal multimodal embedding model built on Qwen3.5. It accepts text, images, videos, visual documents, and interleaved multimodal inputs, and returns a 4,096-dimensional L2-normalized embedding. Audio input is not supported.

Use any subset of the content items to encode text, image, or video independently.

Each input is a string, a URL or path, a `PIL.Image`, or a dict combining `image`, `video`, and `text` keys. Chat messages such as `{"role": "user", "content": [{"type": "image", "image": ...}, {"type": "text", "text": ...}]}` are also accepted, which is the way t…

## 모델 정보

- 태스크: `feature-extraction`
- 파라미터: 9.4B
- 라이선스: other
- 좋아요 114 · 다운로드 3,360 (2026-09-05 수집 시점)
- 원문: [Hugging Face 모델 페이지](https://huggingface.co/tencent/WeMM-Embedding-9B)

## 선정 이유

주요 기관이 최근 30일 안에 공개한 신작이라 선정했습니다.
