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
## 추가 점검 (2026-09-05, 스캐폴딩 리뷰)

- LICENSE: GitHub 이 `MIT` 로 자동 인식함 (`license.spdx_id == "MIT"`)
- .gitignore: `dist/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.venv/`, `*.log`, `tmp/` 제외. 추적 중인 빌드 산출물·캐시 없음 확인
- 저장소 옵션: Wiki 비활성화(문서는 README·docs/ 로 일원화), PR 병합 후 브랜치 자동 삭제 활성화
- 브랜치 보호: `main` 에 보호 규칙을 두지 않음. publish 워크플로가 `GITHUB_TOKEN` 으로 `main` 에 직접 커밋하므로,
  보호 규칙을 추가하려면 Actions 예외(bypass) 설정이 함께 필요함
- Actions: 활성, 워크플로 `publish`(스케줄·push·수동)와 `CI`(PR) 등록 확인
- 소스 코드·문서에 로컬 사용자명, 호스트명, 절대 경로 없음 (`grep` 확인)
