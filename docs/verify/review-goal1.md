판정: 불합격 — 2026-09-05 (재작성)

> 본 보고서와 `docs/verify/review-content-quality.md` 는 같은 성공 기준(글 품질—발행 글 5개 HF 대조)의 중복 검증이다. `review-content-quality.md` 가 공식 판정 근거다. 본 보고서는 1차 검증으로 참고용이며 review-content-quality.md 의 판정이 우선한다.

## 선택 방법 (재현 가능)

- 선택 기준: `data/published.json` 발행 모델 중 `discovered_at` 내림차순, `likes` 내림차순 상위 5개
- 조회 시각: 2026-09-05 (KST 약 16:40)

| # | model_id | org | task | reason | likes | downloads |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B | Qwen | image-text-to-text | trending | 13,948 | 5,739,341 |
| 2 | MiniMaxAI/MiniMax-H3 | MiniMaxAI | image-text-to-video | trending | 4,905 | 5,118,457 |
| 3 | Qwen/Qwen3.8-Flash-Next | Qwen | image-text-to-text | trending, major-org | 4,871 | 351,374 |
| 4 | Lightricks/LTX-2.5 | Lightricks | image-to-video | trending | 2,784 | 1,399,511 |
| 5 | zai-org/GLM-5.3-Flash | zai-org | image-text-to-text | trending, major-org | 2,046 | 654,957 |

## 1. 수치 대조 (글 frontmatter vs HF API)

| # | model_id | 필드 | 글 | HF API | 일치 |
| --- | --- | --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B | likes | 13,948 | 13,994 | 스냅샷 차이(+46, 정상) |
| 1 |  | downloads | 5,739,341 | 6,024,467 | 스냅샷 차이(+285K, 정상) |
| 1 |  | license | apache-2.0 | apache-2.0 | OK |
| 1 |  | params | 27.8B | 27.8B | OK |
| 1 |  | task | image-text-to-text | image-text-to-text | OK |
| 1 |  | createdAt | 2026-08-05 | 2026-08-05 | OK |
| 2 | MiniMaxAI/MiniMax-H3 | likes | 4,905 | 4,919 | 스냅샷 차이(+14, 정상) |
| 2 |  | downloads | 5,118,457 | 5,057,414 | 스냅샷 차이(-61K, 통계 보정) |
| 2 |  | license | other | other | OK |
| 2 |  | params | 33.1B | 33.1B | OK |
| 2 |  | task | image-text-to-video | image-text-to-video | OK |
| 2 |  | createdAt | 2026-07-28 | 2026-07-28 | OK |
| 3 | Qwen/Qwen3.8-Flash-Next | likes | 4,871 | 4,896 | 스냅샷 차이(+25, 정상) |
| 3 |  | downloads | 351,374 | 401,327 | 스냅샷 차이(+50K, 정상) |
| 3 |  | license | other | other | OK |
| 3 |  | params | 180B | 180B | OK |
| 3 |  | task | image-text-to-text | image-text-to-text | OK |
| 3 |  | createdAt | 2026-08-24 | 2026-08-24 | OK |
| 4 | Lightricks/LTX-2.5 | likes | 2,784 | 2,833 | 스냅샷 차이(+49, 정상) |
| 4 |  | downloads | 1,399,511 | 1,484,329 | 스냅샷 차이(+85K, 정상) |
| 4 |  | license | other | other | OK |
| 4 |  | params | (정보 없음) | (없음) | OK |
| 4 |  | task | image-to-video | image-to-video | OK |
| 4 |  | createdAt | 2026-07-23 | 2026-07-23 | OK |
| 5 | zai-org/GLM-5.3-Flash | likes | 2,046 | 2,065 | 스냅샷 차이(+19, 정상) |
| 5 |  | downloads | 654,957 | 727,610 | 스냅샷 차이(+73K, 정상) |
| 5 |  | license | mit | mit | OK |
| 5 |  | params | 321.3B | 321.3B | OK |
| 5 |  | task | image-text-to-text | image-text-to-text | OK |
| 5 |  | createdAt | 2026-08-25 | 2026-08-25 | OK |

수치 차이는 전부 수집 시점(2026-09-05) 이후 증가로, 글에 "(수집 시점 2026-09-05)" 표기되어 있어 모순 아님.

## 2. "왜 주목받는가" — 원문 인용 및 수치 비교 판정

### #1 Qwen/Qwen3.8-27B

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 13,948개, 다운로드 5,739,341회(수집 시점 2026-09-05). 같은 기관(Qwen)의 다른 발행 모델 Qwen/Qwen-Drive-1.0-4B 와 함께 살펴보세요."

| 항목 | 판정 |
| --- | --- |
| 선정 이유 | OK |
| 수치(좋아요/다운로드) | OK |
| 같은 기관·같은 태스크 이전 모델 대비 수치 변화 | **미충족** — 수치 비교 없음 |
| 비교 대상 같은 태스크 | OK (Qwen-Drive-1.0-4B: image-text-to-text) |

### #2 MiniMaxAI/MiniMax-H3

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 4,905개, 다운로드 5,118,457회(수집 시점 2026-09-05). 같은 기관의 이전 모델과의 비교는 발행 이력이 부족해 제공하지 않습니다."

| 항목 | 판정 |
| --- | --- |
| 선정 이유 | OK |
| 수치 | OK |
| 같은 기관·같은 태스크 이전 모델 대비 수치 변화 | OK — "비교 대상 없음" 명시 |
| 비교 대상 같은 태스크 | 해당 없음 |

### #3 Qwen/Qwen3.8-Flash-Next

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 4,871개, 다운로드 351,374회(수집 시점 2026-09-05). 같은 기관(Qwen)의 다른 발행 모델 Qwen/Qwen-Drive-1.0-4B 와 함께 살펴보세요."

| 항목 | 판정 |
| --- | --- |
| 선정 이유 | OK |
| 수치 | OK |
| 같은 기관·같은 태스크 이전 모델 대비 수치 변화 | **미충족** — 수치 비교 없음 |
| 비교 대상 같은 태스크 | OK (Qwen-Drive-1.0-4B: image-text-to-text) |

### #4 Lightricks/LTX-2.5

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 2,784개, 다운로드 1,399,511회(수집 시점 2026-09-05). 같은 기관의 이전 모델과의 비교는 발행 이력이 부족해 제공하지 않습니다."

| 항목 | 판정 |
| --- | --- |
| 선정 이유 | OK |
| 수치 | OK |
| 같은 기관·같은 태스크 이전 모델 대비 수치 변화 | OK — "비교 대상 없음" 명시 |
| 비교 대상 같은 태스크 | 해당 없음 |

### #5 zai-org/GLM-5.3-Flash

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 2,046개, 다운로드 654,957회(수집 시점 2026-09-05). 같은 기관(zai-org)의 다른 발행 모델 zai-org/GLM-5.3 와 함께 살펴보세요."

| 항목 | 판정 |
| --- | --- |
| 선정 이유 | OK |
| 수치 | OK |
| 같은 기관·같은 태스크 이전 모델 대비 수치 변화 | **미충족** — 수치 비교 없음 |
| 비교 대상 같은 태스크 | **불일치** — GLM-5.3: text-generation ≠ GLM-5.3-Flash: image-text-to-text |

## 3. 급상승(surge) 배지 — 7일 전 스냅샷 대조

5개 글 중 surge 배지 없음 (전부 trending 또는 trending+major-org). `data/stats_history.json` 에 2026-09-05 스냅샷만 존재. 7일 전 대조표는 해당 없음.

## 4. 신규성 게이트 통과 근거

기준일 2026-09-05. 게이트: createdAt 60일 내(신규) 또는 lastModified 14일 내(갱신).

| # | model_id | createdAt | age(일) | lastModified | age(일) | 판정 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B | 2026-08-05 | 31 | 2026-08-14 | 22 | 신규(60일 내) |
| 2 | MiniMaxAI/MiniMax-H3 | 2026-07-28 | 39 | 2026-08-13 | 23 | 신규(60일 내) |
| 3 | Qwen/Qwen3.8-Flash-Next | 2026-08-24 | 12 | 2026-08-27 | 9 | 신규(60일 내) |
| 4 | Lightricks/LTX-2.5 | 2026-07-23 | 44 | 2026-09-01 | 4 | 신규(60일 내) |
| 5 | zai-org/GLM-5.3-Flash | 2026-08-25 | 11 | 2026-09-04 | 1 | 신규(60일 내) |

5개 모두 신규성 게이트 통과.

## 5. 관련 모델 섹션 — 같은 태스크 여부

| # | model_id (task) | 다른 태스크 모델 포함 | 판정 |
| --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B (image-text-to-text) | Qwen3.8-2.4T-A95B, Qwen3.8-2.4T-A95B-FP8 (text-generation) | **불일치** |
| 2 | MiniMaxAI/MiniMax-H3 (image-text-to-video) | 없음 | OK |
| 3 | Qwen/Qwen3.8-Flash-Next (image-text-to-text) | Qwen3.8-2.4T-A95B, Qwen3.8-2.4T-A95B-FP8 (text-generation) | **불일치** |
| 4 | Lightricks/LTX-2.5 (image-to-video) | (관련 모델 없음) | OK |
| 5 | zai-org/GLM-5.3-Flash (image-text-to-text) | zai-org/GLM-5.3, zai-org/GLM-5.3-BF16 (text-generation) | **불일치** |

## 6. 핵심 스펙 표·라이선스 문구·HF 웹 응답

| # | 핵심 스펙 6행 | 라이선스 문구 | 상세 페이지 | HF 웹 |
| --- | --- | --- | --- | --- |
| 1 | OK | "apache-2.0 — 상업 이용 가능" OK | 200 | 200 |
| 2 | OK | "other — 상업 이용 제한 또는 확인 필요" OK | 200 | 200 |
| 3 | OK | "other — 상업 이용 제한 또는 확인 필요" OK | 200 | 200 |
| 4 | OK (파라미터="정보 없음") | "other — 상업 이용 제한 또는 확인 필요" OK | 200 | 200 |
| 5 | OK | "mit — 상업 이용 가능" OK | 200 | 200 |

## 7. 불일치 및 미충족 요약

| 심각도 | 위치 | 내용 |
| --- | --- | --- |
| 상 | #1, #3, #5 "왜 주목받는가" | 같은 기관·같은 태스크 이전 모델 대비 수치 비교(파라미터·다운로드·라이선스 중 최소 1개) 누락 |
| 상 | #5 "왜 주목받는가" | 비교 대상 zai-org/GLM-5.3 이 다른 태스크(text-generation) |
| 중 | #1, #3, #5 관련 모델 섹션 | 다른 태스크(text-generation) 모델이 관련 모델에 포함됨 |

판정: 불합격 — 사유: "왜 주목받는가" 문단에 같은 기관·같은 태스크 이전 모델 대비 수치 비교가 3개 글(#1, #3, #5)에서 누락됐고, #5 의 비교 대상 모델(zai-org/GLM-5.3)이 다른 태스크(text-generation)이며, #1·#3·#5 의 관련 모델 섹션에도 다른 태스크 모델이 포함되어 있다.