판정: 합격

# 공개 사이트 실동작 검증 (Playwright, 공개 URL)

- 일시: 2026-09-05
- 대상: `https://jhl-labs.github.io/ai-model-news/` (로컬 빌드가 아닌 GitHub Pages 배포본, origin/main 89fc250 기준 배포)
- 도구: Playwright(Node, Chromium headless). Playwright MCP 서버가 세션에서 연결되지 않아 동일한 Playwright 라이브러리를 스크립트로 직접 구동했다. 뷰포트 1280×900 / 360×900
- 규칙: 코드 수정 없음. 결함은 기록만 한다

## 1. docs/verify 검증 파일 (origin/main)

`git ls-tree origin/main docs/verify/` 와 `git show origin/main:docs/verify/<파일>` 로 확인했다.

| 파일 | origin/main | 판정 문구 |
| --- | --- | --- |
| browser-check.md | 있음 | 첫 줄 판정 없음. 결과 요약 표 12항목 전부 "통과", 결함 1건 수정 후 재검증 스크린샷 첨부 |
| ci-run.md | 있음 | `판정: 합격` |
| e2e.md | 있음 | `판정: 합격` |
| e2e-review.md | 있음 | `판정: 합격` |
| review-collector.md | 있음 | `판정: 합격` |
| review-docs.md | 있음 | 첫 줄 판정 없음. "## 9. 판정" 절에 "합격. 추가 수정 없이 운영 가능한 상태다." |
| review-ops.md | 있음 | `판정: 합격` |
| repo-settings.md | 있음 | 판정 문구 없음(설정 확인 기록 문서). 토픽 8개·Pages·Actions 확인, 민감 정보 없음 |

지적: browser-check.md, review-docs.md, repo-settings.md 는 첫 줄에 `판정:` 문구가 없다. 내용상 모두 합격 상태이나 판정을 grep 으로 뽑는 자동 점검을 위해 첫 줄 문구 통일을 권한다(코드·문서 수정은 이 검증 범위 밖이므로 기록만 한다).

## 2. 브라우저 실동작

두 뷰포트 결과가 동일한 항목은 한 줄로 적고, 뷰포트별 값이 다른 항목만 나눠 적었다.

| 항목 | 기대값 | 실제값 (1280 / 360) | 결과 |
| --- | --- | --- | --- |
| (a) 루트 카드 수 | 47 | 47 / 47 (모두 표시, `#stat-visible` 47) | 통과 |
| (a) 마지막 갱신 표시 | 날짜 표시 | `마지막 갱신 2026-09-05` | 통과 |
| (b) 태스크 필터 `text-generation` 클릭 | 카드 수 감소, 해시 갱신 | 16개, `aria-pressed="true"`, `#task=text-generation` | 통과 |
| (b) 기관 필터 `Qwen` 선택 | 카드 수 감소, 해시에 org 추가 | 2개, `#task=text-generation&org=Qwen` (기관 옵션 25개) | 통과 |
| (b) 검색어 `zzzz-no-match` 입력 | 0개 + 안내 문구, 해시에 q | 0개, `#no-match` 표시, `#task=text-generation&q=zzzz-no-match` | 통과 |
| (b) 초기화 클릭 | 47개, 해시·검색창 비움 | 47개, 해시 `""`, 검색창 `""` | 통과 |
| (c) 카드 클릭 → 상세 진입 | `models/<slug>/` 로 이동 | `models/Qwen__Qwen3.8-27B/` | 통과 |
| (c) 상세 모델 ID | 표시 | `Qwen/Qwen3.8-27B` | 통과 |
| (c) 상세 태스크 / 파라미터 / 라이선스 | 표시 | `image-text-to-text` / `27.8B` / `apache-2.0` | 통과 |
| (c) HF 링크 href | `https://huggingface.co/` 로 시작 | `https://huggingface.co/Qwen/Qwen3.8-27B` (`target=_blank rel=noopener`) | 통과 |
| (d) About 페이지 | 제목·절 표시 | `About — AI Model News`, h2: '유명 모델' 선정 기준 / 데이터 출처 / 동작 방식 / 구독과 기여 | 통과 |
| (e) 다크/라이트 토글 | 토글 후 새로고침 유지 | 초기 `data-theme` 없음(시스템) → 토글 후 `dark` → 새로고침 후 `dark` 유지, 상세 페이지 이동 후에도 `dark`, 재토글 `light` | 통과 |
| (f) 360px `scrollWidth` | ≤ 360 | 목록 360, 상세 360, About 360 | 통과 |
| (g) 콘솔 error·warning | 0 | 목록 0 / 상세 0 / About 0 (두 뷰포트 모두, `pageerror` 0) | 통과 |
| feed.xml | XML 파싱 성공, item 수 | HTTP 200, `DOMParser` parsererror 없음, item 47 | 통과 |

1280px 에서는 `scrollWidth` 1280 으로 뷰포트와 같아 가로 스크롤이 없다.

### 콘솔 집계

| 페이지 | 1280 error/warning | 360 error/warning |
| --- | --- | --- |
| 목록(필터 조작·테마 토글·새로고침 포함) | 0 / 0 | 0 / 0 |
| 상세 | 0 / 0 | 0 / 0 |
| About | 0 / 0 | 0 / 0 |

## 3. 스크린샷 (`docs/verify/live/`)

| 파일 | 내용 |
| --- | --- |
| `index-1280-light.png` | 목록, 1280px, 라이트(시스템 기본) |
| `index-360-dark.png` | 목록, 360px, 다크 토글 후 새로고침 상태. 필터 조작 직후라 필터 패널 하단(초기화 버튼)과 첫 카드가 보이도록 스크롤된 위치. 카드 1열, 가로 스크롤 없음 |
| `detail-360-light.png` | 상세(Qwen/Qwen3.8-27B), 360px, 라이트로 재토글한 상태 |

## 4. 판정

불합격 조건(콘솔 error 1건 이상, 가로 스크롤, 필터 미동작, HF 링크 오류) 중 해당하는 항목이 없다. **판정: 합격**.

지적 사항(수정하지 않음):
- docs/verify 파일 3개(browser-check.md, review-docs.md, repo-settings.md)의 첫 줄 판정 문구 부재. 위 1절 참고.

## 사용한 명령

```
git ls-tree origin/main docs/verify/
git show origin/main:docs/verify/<파일>.md | grep -m1 -oE "판정: ?(합격|불합격)"
node live.js   # Playwright chromium.launch → goto/click/selectOption/fill/reload/screenshot/evaluate
curl -s https://jhl-labs.github.io/ai-model-news/ | grep -o "마지막 갱신 <strong>[^<]*"
```
