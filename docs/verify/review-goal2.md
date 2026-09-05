판정: 합격 — 2026-09-05

## 검증 방법

Playwright(headless Chromium)로 공개 URL https://jhl-labs.github.io/ai-model-news/ 을 실제 브라우저에서 열어 검증. 스크린샷 3장(1280px 라이트·1280px 다크·360px 라이트) 캡처.

## 1. 1280x720 — "오늘의 하이라이트" 섹션

| 항목 | 결과 |
| --- | --- |
| `section.highlights` 존재 | true |
| 하이라이트 카드 수 | 3 (최대 3개, 기준 충족) |
| 스크린샷 | `docs/verify/playwright-goal3/index-1280-light.png` |

하이라이트 카드 3개: Qwen3.8 27B (♥ 13.9k), MiniMax H3 (♥ 4.9k), Qwen3.8 Flash Next (♥ 4.9k)

## 2. "이번 주 급상승" 섹션

| 항목 | 결과 |
| --- | --- |
| `section.surge` 존재 | true |
| 급상승 카드 수 | 5 |

급상승 카드: DeepSeek V4 Flash Vision Exp, GLM 5.3 Flash Uncensored FP8, vdn-minimax-h3, K2 Horizon MoVA 36B, minimax-h3-fused-turbo

## 3. 배지 (badge-new / badge-surge / badge-updated)

| 배지 | 개수 |
| --- | --- |
| `badge-new` | 49 (하이라이트+급상승+전체 목록 중복 카드 포함) |
| `badge-surge` | 10 |
| `badge-updated` | 0 |

badge-updated 가 0개인 것은 현재 발행 글 41개 모두가 신규(createdAt 60일 내) 경로로 선정되어 updated 배지가 붙을 글이 없기 때문이며, 이는 정상 동작임.

## 4. 상대 시각

| 항목 | 결과 |
| --- | --- |
| `<time>` 요소 수 | 49 |
| 시각 텍스트 | "오늘" (전체 49개 동일) |

모든 글이 2026-09-05 수집되어 "오늘"로 표시됨.

## 5. 전체 목록

| 항목 | 결과 |
| --- | --- |
| `section.cards .card` 수 | 41 |
| 태스크 필터 chips | 12 (전체 포함) |
| 기관 필터 select | 존재 |
| 검색 input | 존재 |

## 6. 다크/라이트 테마

| 항목 | 결과 |
| --- | --- |
| `#theme-toggle` 버튼 존재 | true |
| 다크 모드 스크린샷 | `docs/verify/playwright-goal3/index-1280-dark.png` |
| 라이트 모드 스크린샷 | `docs/verify/playwright-goal3/index-1280-light.png` |

## 7. 360px 모바일

| 항목 | 결과 |
| --- | --- |
| 하이라이트 섹션 존재 (360px) | true |
| 하이라이트 카드 수 (360px) | 3 |
| 스크린샷 | `docs/verify/playwright-goal3/index-360-light.png` |

360px에서도 하이라이트 섹션이 정상 표시됨.

## 8. 콘솔 오류

| 항목 | 결과 |
| --- | --- |
| console error (1280px) | 0건 |
| console error (360px) | 0건 |
| pageerror | 0건 |

## 9. 고전 모델 부재

| 모델 | 사이트에 존재 |
| --- | --- |
| gpt2 | 없음 |
| bert-base-uncased | 없음 |
| all-MiniLM-L6-v2 | 없음 |
| clip-vit-base-patch32 | 없음 |
| distilbert-base-uncased | 없음 |
| mms-300m | 없음 |

## 판정

합격. 공개 URL 을 Playwright 로 실제 열어 검증한 결과:
- 1280x720 에서 "오늘의 하이라이트" 섹션(카드 3개)과 "이번 주 급상승" 섹션(카드 5개) 존재
- badge-new 49개, badge-surge 10개 표시
- "오늘" 상대 시각 표시
- 다크/라이트 토글 정상, 360px 모바일에서 하이라이트 섹션 정상
- 콘솔 오류 0건
- 고전 모델 6개 제거 확인