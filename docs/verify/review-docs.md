# README·CONTRIBUTING 정합성 리뷰

검토 일시: 2026-09-05
검토 범위: README.md, CONTRIBUTING.md 가 코드·워크플로·템플릿·실제 동작과 일치하는지.

## 1. 검증 방법

- `python3 -m unittest discover -s tests -t .` 로 단위 테스트 실행
- `python3 scripts/build.py --content-dir content/models --out /tmp/verify-dist` 로 실제 빌드
- `xml.dom.minidom` 로 `feed.xml`, `sitemap.xml` 파싱 검증
- `scripts/collect.py` 상수 값을 README 표와 직접 대조
- 템플릿·static 자산이 README 의 기능 설명과 일치하는지 육안 점검
- `git ls-files`, `data/*.json` 로 운영 상태 확인

## 2. 단위 테스트·빌드

| 항목 | 결과 |
| --- | --- |
| 단위 테스트 | 48개 전부 통과 (0.043s) |
| 빌드 | 47개 모델 페이지 생성 성공 |
| RSS(feed.xml) | XML 파싱 OK |
| sitemap.xml | XML 파싱 OK |
| 산출물 | index.html, about/, models/*/index.html, feed.xml, sitemap.xml, robots.txt, 404.html, assets/ |

## 3. 선정 기준 표 ↔ collect.py 상수

README 의 선정 기준 표와 `scripts/collect.py` 상수가 모두 일치한다.

| README 표 | collect.py 상수 | 값 | 일치 |
| --- | --- | --- | --- |
| 트렌딩 상위 30위 | `TRENDING_TOP_N` | 30 | OK |
| 7일 전 스냅샷 | `SURGE_WINDOW_DAYS` | 7 | OK |
| 좋아요 +200 | `SURGE_LIKES_DELTA` | 200 | OK |
| 다운로드 2배 | `SURGE_DOWNLOAD_RATIO` | 2.0 | OK |
| 다운로드 절대치 10,000 | `SURGE_MIN_DOWNLOADS` | 10,000 | OK |
| 첫 실행 생성 7일 이내 | `FIRST_RUN_NEW_DAYS` | 7 | OK |
| 첫 실행 좋아요 100 | `FIRST_RUN_LIKES` | 100 | OK |
| 첫 실행 다운로드 10,000 | `FIRST_RUN_DOWNLOADS` | 10,000 | OK |
| 주요 기관 30일 이내 | `MAJOR_ORG_DAYS` | 30 | OK |
| 주요 기관 좋아요 20 | `MAJOR_ORG_MIN_LIKES` | 20 | OK |
| 14일치 스냅샷 | `HISTORY_KEEP_DAYS` | 14 | OK |

주요 기관 목록: README 가 예시로 `meta-llama, google, mistralai, Qwen, deepseek-ai, openai, microsoft, nvidia, stabilityai, black-forest-labs` 만 나열하고 `등` 으로 처리했고, 코드는 위 10개에 `apple, ibm-granite, allenai, CohereLabs, zai-org, moonshotai, xai-org, HuggingFaceTB, nari-labs, tencent` 를 추가한다. "등" 표현이 추가 기관을 포함하므로 모순이 아니다.

## 4. 워크플로 ↔ README

| README 설명 | publish.yml | 일치 |
| --- | --- | --- |
| 매일 21:00 UTC(06:00 KST) 스케줄 | `cron: "0 21 * * *"` | OK |
| `main` push 시 빌드·배포 | `push: branches: [main]` | OK |
| 수동 실행 | `workflow_dispatch` + `max_new` 입력 | OK |
| `github-actions[bot]` 커밋·push | `git config user.name "github-actions[bot]"` | OK |
| GITHUB_TOKEN 커밋은 재트리거 안 함 | 기본 동작(GitHub 정책) | OK |
| `scripts/collect.py` → `content/models/*.md`, `data/*.json` | `git add content/models data` | OK |
| `scripts/build.py` → `dist/` | `--out dist` | OK |
| `actions/deploy-pages` | `actions/deploy-pages@v4` | OK |
| 인증·시크릿 불필요 | HF API 익명 호출, 시크릿 0 | OK |

## 5. 기능 ↔ 템플릿·JS

| README 설명 | 구현 | 일치 |
| --- | --- | --- |
| 다크/라이트 테마 | `base.html` 인라인 스크립트(localStorage) + `app.js` 토글 + `prefers-color-scheme` | OK |
| 반응형 카드 그리드 | `templates/card.html`, `static/style.css` | OK |
| 태스크·기관·검색 필터 | `index.html` chips + org select + search input, `app.js` | OK |
| URL 해시로 필터 공유 | `app.js` readHash/writeHash + `history.replaceState` | OK |
| 모델 상세 페이지 | `templates/detail.html`, `build.py::render_detail` | OK |
| RSS | `templates/base.html` `<link rel="alternate">` + `feed.xml` | OK |
| sitemap·robots | `sitemap.xml`, `robots.txt` | OK |
| 404 | `templates/404.html`, 절대 URL 자산 | OK |

## 6. CONTRIBUTING ↔ 실제 환경

| CONTRIBUTING 항목 | 실제 | 일치 |
| --- | --- | --- |
| Python 3.10+ | `ci.yml` matrix `["3.10", "3.12"]`, publish 는 3.12 | OK |
| 외부 의존성 없음 | `scripts/*.py` 표준 라이브러리만 | OK |
| 테스트 명령 | `python3 -m unittest discover -s tests -t . -v` | OK (publish.yml, ci.yml 동일) |
| dry-run 명령 | `python3 scripts/collect.py --dry-run` | OK (`collect.py::main`) |
| 빌드 명령 | `python3 scripts/build.py --content-dir content/models --out dist` | OK |
| 미리보기 | `python3 -m http.server -d dist 8000` | OK (Python 3.10+ `-d` 지원) |
| main 직접 push 제한 | publish.yml 봇 커밋, ci.yml `branches-ignore: [main]` | OK |
| Conventional Commits | 최근 커밋 메시지 일관성 OK | OK |
| 선정 기준 변경 시 양쪽 수정 | README·collect.py 동시 반영 가이드 | OK |
| content/models 편집 금지 | 자동 생성물, published.json 중복 방지 | OK |
| 보안: 경로·토큰·호스트명 금지 | USER_AGENT 는 저장소 URL 만, 시스템 정보 노출 0 | OK |

## 7. 운영 상태

| 항목 | 값 |
| --- | --- |
| 발행 이력(`data/published.json`) | 47개 모델 |
| 통계 스냅샷(`data/stats_history.json`) | 553개 모델, 2026-09-05 스냅샷 |
| `content/models/` 글 | 47개 |
| `dist/` 추적 여부 | .gitignore 로 제외, 0개 추적 |
| 최근 자동 커밋 | `4b74fb6 content: 2026-09-05 수집 (새 모델 0개)` |

## 8. 발견된 정합성 문제

없음. README 의 모든 설명이 코드·워크플로·템플릿·실제 산출물과 일치한다.

## 9. 판정

합격. 추가 수정 없이 운영 가능한 상태다.