# 첫 화면 재구성 Playwright 검증 (공개 URL)

- 일시: 2026-09-05 (UTC 07:36–07:38)
- 대상: `https://jhl-labs.github.io/ai-model-news/` (배포된 공개 사이트, 로컬 아님)
- 배포 기준: publish run 33952986891 (success, headSha `f676b9a`)
- 검증자 고지: 이 검증자는 첫 화면 프론트엔드 코드(커밋 `018315f` feat(ui): 하이라이트·급상승 섹션 + 배지 + 상대 시각)를 구현하지 않았다. 이 세션은 종단 검증(e2e-review)과 본 보고서만 작성했다.
- 이전 판(불합격, 도구 없음)을 대체한다. 이번 세션에는 Playwright MCP 도구가 실제 연결돼 `browser_navigate`·`browser_resize`·`browser_click`·`browser_evaluate`·`browser_take_screenshot`·`browser_console_messages` 만으로 검증했고 curl 등 대체 수단은 쓰지 않았다.

## 스크린샷 (`docs/verify/playwright/`)

| 파일 | 조건 |
| --- | --- |
| `firstview-1280-light.png` | 1280×900, 라이트, 첫 화면 뷰포트 |
| `firstview-1280-light-full.png` | 1280, 라이트, 전체 페이지(하단 전체 목록 포함) |
| `firstview-1280-dark.png` | 1280×900, 다크 토글 클릭 후 |
| `firstview-360-dark.png` | 360×800 리사이즈 후 |

## 확인 항목

### 1. 1280px 라이트: 섹션 구성

초기 로드 시 `data-theme` 없음, `color-scheme: light`, body 배경 `rgb(247, 248, 250)` (라이트 확인).

| 섹션(class) | 제목 | 카드 수 |
| --- | --- | --- |
| hero | 최신 모델 — "41 모델 · 마지막 갱신 2026-09-05 · 41개 표시" | 0 |
| highlights | 오늘의 하이라이트 | 3 |
| surge | 이번 주 급상승 | 5 |
| filters | 태스크 칩 12개 + 초기화 | 0 |
| cards(#cards) | 전체 목록 | 41 |

하이라이트 3개: Qwen3.8 27B, MiniMax H3, Qwen3.8 Flash Next (모두 발견일 2026-09-05, 24~72시간 내 신규).
급상승 5개: DeepSeek V4 Flash Vision Exp, GLM 5.3 Flash Uncensored FP8, vdn minimax h3, K2 Horizon MoVA 36B A4B, minimax h3 fused turbo int8 convrot.
하단 전체 목록 41개 존재(전체 페이지 스크린샷 참조). 결과: **렌더링됨**.

### 2. 배지·상대 시각

`browser_evaluate` 로 DOM 을 읽은 결과.

| 항목 | 실측 |
| --- | --- |
| 상태 배지 클래스 | `badge badge-new`(신규), `badge badge-surge`(급상승) |
| 하이라이트 카드 배지 | 각 카드 `신규` + 기관(`badge-org`) + 태스크(`badge-task`) |
| 급상승 카드 배지 | 각 카드 `급상승` + `신규` + 기관 + 태스크 |
| 전체 목록 중 상태 배지 보유 카드 | 41/41 |
| `갱신` 배지 | 0건 표시 — 현재 발행 글 전부가 오늘 최초 발견이라 갱신 대상이 없음(데이터 상태이며 결함 아님) |
| 상대 시각 | 모든 카드 `<time datetime="2026-09-05">오늘</time>` |

상대 시각은 `<time>` 요소에 절대 날짜(datetime)와 상대 표기("오늘")가 함께 있음을 확인했다. 발행 글이 모두 당일 발견분이어서 "N일 전" 표기는 이번 데이터로는 관찰할 수 없었다(스크린샷의 "♥ 13.9k ⬇ 5.7M 오늘" 참조).

### 3. 다크 모드 토글

`#theme-toggle`(aria-label "다크 테마로 전환") 을 실제 클릭.

| 항목 | 클릭 전 | 클릭 후 |
| --- | --- | --- |
| `html[data-theme]` | 없음 | `dark` |
| `color-scheme` | light | dark |
| body 배경 | rgb(247, 248, 250) | rgb(15, 18, 24) |
| body 글자색 | — | rgb(232, 236, 242) |
| 토글 aria-label | 다크 테마로 전환 | 라이트 테마로 전환 |
| localStorage `theme` | — | `dark` |

전/후 스크린샷: `firstview-1280-light.png` ↔ `firstview-1280-dark.png`. 결과: **전환됨**.

### 4. 360px 레이아웃

| 항목 | 실측 |
| --- | --- |
| innerWidth / scrollWidth / clientWidth | 360 / 360 / 360 |
| 가로 스크롤(overflow) | 없음 |
| 뷰포트 우측(361px) 을 넘는 요소 | 0개 |
| 하이라이트·전체 목록 grid 열 | 1열(328px) |

헤더 내비가 두 줄로 접히고 카드가 1열로 쌓이며 잘림·겹침 없음(`firstview-360-dark.png`). 결과: **깨지지 않음**.

### 5. 콘솔 오류

`browser_console_messages(level=debug, all=true)` 결과, 첫 화면 로드·토글·리사이즈 전 구간:

```
Total messages: 0 (Errors: 0, Warnings: 0)
```

콘솔 오류 **0건**. (참고: 6항 확인을 위해 의도적으로 열어 본 고전 모델 상세 URL 에서만 `Failed to load resource: 404` 1건이 발생했으며 첫 화면과 무관하다.)

### 6. 고전 모델 처리

| 항목 | 실측 |
| --- | --- |
| 첫 화면 본문에 gpt2 / bert-base-uncased / all-MiniLM 문자열 | 없음 |
| 하이라이트·급상승·전체 목록 내 해당 카드 | 0개 |
| '에버그린' 섹션 | 없음(분리 대신 제외 방식) |
| `/models/openai-community__gpt2/` | HTTP 404 (제목 "페이지를 찾을 수 없습니다") |
| 모델 수 변화 | 이전 47 → 현재 41 (고전 모델 6건 제외) |

Goal 은 "에버그린 별도 섹션으로 분리되거나 제외" 를 허용하므로 제외 방식은 기준에 부합한다.

## 종합

| # | 항목 | 결과 |
| --- | --- | --- |
| 1 | 하이라이트·급상승·전체 목록 렌더링 | 합격 |
| 2 | 신규/급상승 배지·상대 시각 | 합격(갱신 배지는 대상 데이터 없음) |
| 3 | 다크 토글 전환 | 합격 |
| 4 | 360px 레이아웃 | 합격 |
| 5 | 콘솔 오류 0건 | 합격 |
| 6 | 고전 모델 제외 | 합격 |

판정: 합격
