# AI Model News

[![publish](https://github.com/jhl-labs/ai-model-news/actions/workflows/publish.yml/badge.svg)](https://github.com/jhl-labs/ai-model-news/actions/workflows/publish.yml)
[![CI](https://github.com/jhl-labs/ai-model-news/actions/workflows/ci.yml/badge.svg)](https://github.com/jhl-labs/ai-model-news/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Hugging Face 에 등장하는 **주목받는 AI 모델 소식만** 골라 자동으로 수집·발행하는 기술 블로그입니다.
사람 손을 거치지 않고 GitHub Actions 스케줄이 매일 Hugging Face 공개 API 를 조회해 새 글을 만들고,
정적 사이트를 다시 빌드해 GitHub Pages 에 배포합니다.

- 사이트: <https://jhl-labs.github.io/ai-model-news/>
- RSS: <https://jhl-labs.github.io/ai-model-news/feed.xml>
- 변경 이력: [CHANGELOG.md](CHANGELOG.md)

## 무엇을 발행하나

각 글은 다음 다섯 섹션으로 구성된 본문을 담습니다. 모든 정보는 Hugging Face 공개 API 필드와 published.json 발행 이력에서만 도출하며, API에 없는 정보(성능 벤치마크 등)는 추정하지 않습니다.

- **왜 주목받는가** — 선정 이유(reason) 문장과 좋아요·다운로드 수치. `surge` 글에는 7일 전 스냅샷(`data/stats_history.json`) 대비 "좋아요 A→B(+C%), 다운로드 D→E(+F%)" 증분을, 스냅샷이 없으면 "스냅샷 정보 없음"을 적습니다. 같은 기관·같은 태스크로 가장 최근 발행된 이전 모델 1개를 찾아 파라미터·다운로드 변화율과 라이선스 동일/변경을 문장으로 생성하고, 없으면 "비교 대상 없음(최초 발행)"으로 명시합니다. 수치는 HF API·저장 스냅샷·기존 글 frontmatter 에서만 가져오며 없으면 "정보 없음"입니다.
- **핵심 스펙** — 태스크, 파라미터, 라이선스, 최초 등록일, 좋아요, 다운로드를 6행 표로 정리.
- **요약** — 모델 카드(README)에서 발췌한 1~3 문단(이미지·배지·HTML 제거, 600자 초과 시 말줄임).
- **라이선스** — 라이선스 식별자와 상업 이용 가능 여부를 한 줄로 표시. `apache-2.0`·`mit`·`llama3.1`·`qwen` 등 상업 허용 집합에 속하면 "상업 이용 가능", 아니면 "상업 이용 제한 또는 확인 필요", 정보가 없으면 "라이선스 정보 없음 — 원문 확인 필요".
- **관련 모델** — 같은 기관(org)과 같은 태스크(task)의 다른 발행 모델로 각각 최대 3개, 자기 자신과 중복은 제외한 상대 경로 링크 목록. 발행 이력이 없으면 "아직 관련 모델이 발행되지 않았습니다."

다음 기준 중 하나 이상을 만족하는 모델만 발행합니다. 값은 모두 `scripts/collect.py` 상단의 상수입니다.

모든 경로의 공통 조건(신규성 게이트): **최근 60일 내 최초 공개(`createdAt`) 또는 14일 내 의미 있는 갱신(`lastModified`)**. 이 조건을 만족하지 못하면 트렌딩·급상승·주요 기관 여부와 상관없이 발행하지 않습니다. 고전 모델(gpt2, bert-base-uncased 등)은 신규성이 없어 제외됩니다.

| 기준 | `reason` 태그 | 조건 |
| --- | --- | --- |
| 신규 모델 | `new` | `createdAt` 이 now 기준 60일 이내 |
| 최근 갱신 | `updated` | `lastModified` 가 14일 이내 |
| 트렌딩 상위 | `trending` | `/api/models?sort=trendingScore` 상위 30위 이내 |
| 최근 7일 급상승 | `surge` | 7일 전 스냅샷 대비 좋아요 +200 이상, 또는 다운로드 2배 이상(절대치 10,000 이상). 비교할 이력이 없는 첫 실행에서는 생성 7일 이내이면서 좋아요 100 또는 다운로드 10,000 이상 |
| 주요 기관 신작 | `major-org` | meta-llama, google, mistralai, Qwen, deepseek-ai, openai, microsoft, nvidia, stabilityai, black-forest-labs 등 주요 기관이 30일 이내 공개했고 좋아요 20 이상 |

선정된 모델의 `reason` 에는 신규성 태그(`new` 또는 `updated`)가 항상 포함되며, 추가로 `trending`·`surge`·`major-org` 중 만족하는 항목이 붙습니다.

제외: 주요 기관이 아닌 곳의 GGUF 재업로드, `pipeline_tag` 와 태그가 모두 없는 모델, `createdAt`/`lastModified` 모두 없는 모델. 이미 발행한 모델은 다시 발행하지 않습니다.

### 첫 화면 구성

- **오늘의 하이라이트** — 최근 3일 이내 발행 모델 중 좋아요 상위 3개를 상단에 카드로 노출.
- **이번 주 급상승** — 최근 7일 이내 좋아요/다운로드 급증 모델을 별도 섹션에 정렬.
- **전체 목록** — 전체 발행 글을 태스크·기관·검색 필터(URL 해시로 공유 가능)로 탐색 가능한 카드 그리드.
- **배지** — 카드에 신규(`new`)·갱신(`updated`)·급상승(`surge`) 배지와 "며칠 전" 상대 시각을 표시.
- 360px 모바일까지 반응형이며, 다크/라이트 테마를 유지합니다.

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
- Hugging Face API 가 429·5xx 를 돌려주거나 일시적 네트워크 오류가 나면 최대 4회 지수 backoff(1·2·4·8초, `Retry-After` 헤더 우선, 상한 30초)로 재시도하고, 404 등 다른 4xx 는 즉시 실패로 처리합니다.
- `main` 에 push 되면 수집 없이 빌드·배포만 다시 수행합니다.
- 매 실행마다 `GITHUB_STEP_SUMMARY` 에 수집/신규/제외 건수와 0건 시의 안내문을 자동으로 기록해 워크플로 로그에서 한눈에 확인할 수 있습니다.
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

# 기존 글 본문만 새 구조로 재작성(네트워크 없음)
python3 scripts/collect.py --regenerate
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
