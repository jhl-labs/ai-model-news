# 저장소 설정 확인 (Repository Settings Verification)

확인 날짜: 2026-09-05

## 저장소 기본 정보

```json
{
  "name": "ai-model-news",
  "description": "Hugging Face 에서 주목받는 AI 모델 소식을 매일 자동 수집·발행하는 기술 블로그",
  "homepageUrl": "https://jhl-labs.github.io/ai-model-news/",
  "defaultBranchRef": { "name": "main" }
}
```

## 토픽 (8개)

- ai-models
- github-pages
- huggingface
- machine-learning
- python
- rss
- static-site
- tech-blog

## GitHub Pages

```json
{
  "url": "https://api.github.com/repos/jhl-labs/ai-model-news/pages",
  "html_url": "https://jhl-labs.github.io/ai-model-news/",
  "build_type": "workflow",
  "source": { "branch": "main", "path": "/" },
  "public": true,
  "https_enforced": true
}
```

- build_type: `workflow` (GitHub Actions 배포 방식) — 확인 완료
- HTTPS 강제 적용됨