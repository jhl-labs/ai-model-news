# AI Model News

[![publish](https://github.com/jhl-labs/ai-model-news/actions/workflows/publish.yml/badge.svg)](https://github.com/jhl-labs/ai-model-news/actions/workflows/publish.yml)
[![CI](https://github.com/jhl-labs/ai-model-news/actions/workflows/ci.yml/badge.svg)](https://github.com/jhl-labs/ai-model-news/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Hugging Face 에 등장하는 **주목받는 AI 모델 소식만** 골라 자동으로 수집·발행하는 기술 블로그입니다.
사람 손을 거치지 않고 GitHub Actions 스케줄이 매일 Hugging Face 공개 API 를 조회해 새 글을 만들고,
정적 사이트를 다시 빌드해 GitHub Pages 에 배포합니다.

- 사이트: <https://jhl-labs.github.io/ai-model-news/>
- RSS: <https://jhl-labs.github.io/ai-model-news/feed.xml>

## 무엇을 발행하나

각 글은 모델 카드 요약(태스크, 파라미터 수, 라이선스, 좋아요·다운로드, 원문 링크, 설명 요약)과 선정 이유를 담습니다.
다음 기준 중 하나 이상을 만족하는 모델만 발행합니다. 값은 모두 `scripts/collect.py` 상단의 상수입니다.

| 기준 | `reason` 태그 | 조건 |
| --- | --- | --- |
| 트렌딩 상위 | `trending` | `/api/models?sort=trendingScore` 상위 30위 이내 |
| 최근 7일 급상승 | `surge` | 7일 전 스냅샷 대비 좋아요 +200 이상, 또는 다운로드 2배 이상(절대치 10,000 이상). 비교할 이력이 없는 첫 실행에서는 생성 7일 이내이면서 좋아요 100 또는 다운로드 10,000 이상 |
| 주요 기관 신작 | `major-org` | meta-llama, google, mistralai, Qwen, deepseek-ai, openai, microsoft, nvidia, stabilityai, black-forest-labs 등 주요 기관이 30일 이내 공개했고 좋아요 20 이상 |

제외: 주요 기관이 아닌 곳의 GGUF 재업로드, `pipeline_tag` 와 태그가 모두 없는 모델. 이미 발행한 모델은 다시 발행하지 않습니다.

## 동작 방식

```
schedule (매일 21:00 UTC, 06:00 KST)
  └─ scripts/collect.py ── Hugging Face 공개 API (인증 없음)
       ├─ content/models/<org>__<name>.md   (모델별 글, 프런트매터 + 마크다운)
       ├─ data/published.json               (발행 이력, 중복 방지)
       └─ data/stats_history.json           (14일치 좋아요·다운로드 스냅샷, 급상승 판정용)
  └─ git commit & push (github-actions[bot]; GITHUB_TOKEN 커밋은 다른 워크플로를 재트리거하지 않음)
  └─ scripts/build.py ── dist/ (index, models/*/, about/, feed.xml, sitemap.xml, robots.txt, 404.html)
  └─ actions/deploy-pages
```

- 의존성은 Python 표준 라이브러리뿐입니다. 토큰이나 시크릿은 필요 없습니다.
- `main` 에 push 되면 수집 없이 빌드·배포만 다시 수행합니다.
- 사이트는 다크/라이트 테마, 반응형 카드 그리드, 태스크·기관·검색 필터(URL 해시로 공유 가능), 모델 상세 페이지, RSS 를 제공합니다.

## 로컬에서 실행하기

Python 3.10 이상이면 충분합니다.

```bash
# 테스트
python3 -m unittest discover -s tests -t . -v

# 수집 (드라이 런: 선정 결과만 출력, 파일은 쓰지 않음. 네트워크 필요)
python3 scripts/collect.py --dry-run

# 수집 (실제 발행, 최대 5개)
python3 scripts/collect.py --max-new 5

# 빌드 후 미리보기
python3 scripts/build.py --content-dir content/models --out dist
python3 -m http.server -d dist 8000
```

`--site-url` 을 주면 다른 경로에서도 절대 URL(canonical, RSS, sitemap)이 맞게 생성됩니다.

## 저장소 구조

```
scripts/
  collect.py      수집기 (선정 기준, 모델 카드 요약 추출, 글 생성)
  build.py        정적 사이트 생성기 (마크다운 부분집합 변환기 내장)
  frontmatter.py  프런트매터 직렬화/파싱, slug 규칙
templates/        base, index, card, detail, about, 404
static/           style.css, app.js (외부 의존성 없음)
content/models/   자동 생성 글 (손으로 편집하지 않음)
data/             발행 이력과 통계 스냅샷
tests/            단위 테스트 (네트워크 없이 fixture 로 실행)
docs/verify/      검증 스크린샷·설정 기록
.github/workflows publish.yml (수집·빌드·배포), ci.yml (PR 검증)
```

## 기여

[CONTRIBUTING.md](CONTRIBUTING.md) 를 참고하세요. 선정 기준을 바꾸는 PR 은 `scripts/collect.py` 의 상수와 이 README 의 표를 함께 수정해야 합니다.

## 라이선스

코드는 [MIT](LICENSE) 입니다. 각 모델의 설명 요약은 해당 모델 카드에서 발췌한 것이며 저작권과 라이선스는 원 저작자에게 있습니다.
