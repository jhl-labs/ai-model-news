판정: 불합격 — 2026-09-05 (재작성)

> 본 보고서와 `docs/verify/review-goal1.md` 는 같은 성공 기준(글 품질—발행 글 5개 HF 대조)의 중복 검증이다. 본 보고서(`review-content-quality.md`)가 공식 판정 근거다. review-goal1.md 는 1차 검증으로 참고용이며 본 보고서의 판정이 우선한다.

## 선택 방법 (재현 가능)

- 선택 기준: `data/published.json` 의 발행 모델 중 `discovered_at` 내림차순, `likes` 내림차순 상위 5개
- 조회 시각: 2026-09-05 (KST 약 16:40)
- 모든 글의 discovered_at 이 2026-09-05 로 동일하여 likes 순으로 결정

| # | model_id | org | task | reason | likes | downloads |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B | Qwen | image-text-to-text | trending | 13,948 | 5,739,341 |
| 2 | MiniMaxAI/MiniMax-H3 | MiniMaxAI | image-text-to-video | trending | 4,905 | 5,118,457 |
| 3 | Qwen/Qwen3.8-Flash-Next | Qwen | image-text-to-text | trending, major-org | 4,871 | 351,374 |
| 4 | Lightricks/LTX-2.5 | Lightricks | image-to-video | trending | 2,784 | 1,399,511 |
| 5 | zai-org/GLM-5.3-Flash | zai-org | image-text-to-text | trending, major-org | 2,046 | 654,957 |

## 1. 수치 대조 (글 frontmatter vs HF API)

### #1 Qwen/Qwen3.8-27B

| 필드 | 글에 표시된 값 | HF API 실제 값 | 일치 |
| --- | --- | --- | --- |
| likes | 13,948 | 13,994 | 차이 +46 (수집 시점 이후 증가, 정상) |
| downloads | 5,739,341 | 6,024,467 | 차이 +285,126 (수집 시점 이후 증가, 정상) |
| license | apache-2.0 | cardData.license: apache-2.0 | OK |
| params | 27.8B | 27.8B | OK |
| createdAt | 2026-08-05 | 2026-08-05T08:22:59.000Z | OK |
| pipeline_tag | image-text-to-text | image-text-to-text | OK |

### #2 MiniMaxAI/MiniMax-H3

| 필드 | 글에 표시된 값 | HF API 실제 값 | 일치 |
| --- | --- | --- | --- |
| likes | 4,905 | 4,919 | 차이 +14 (정상 증분) |
| downloads | 5,118,457 | 5,057,414 | 차이 -61,043 (감소, 통계 보정 가능) |
| license | other | cardData.license: other | OK |
| params | 33.1B | 33.1B | OK |
| createdAt | 2026-07-28 | 2026-07-28T10:45:18.000Z | OK |
| pipeline_tag | image-text-to-video | image-text-to-video | OK |

### #3 Qwen/Qwen3.8-Flash-Next

| 필드 | 글에 표시된 값 | HF API 실제 값 | 일치 |
| --- | --- | --- | --- |
| likes | 4,871 | 4,896 | 차이 +25 (정상 증분) |
| downloads | 351,374 | 401,327 | 차이 +49,953 (정상 증분) |
| license | other | cardData.license: other | OK |
| params | 180B | 180B | OK |
| createdAt | 2026-08-24 | 2026-08-24T08:24:59.000Z | OK |
| pipeline_tag | image-text-to-text | image-text-to-text | OK |

### #4 Lightricks/LTX-2.5

| 필드 | 글에 표시된 값 | HF API 실제 값 | 일치 |
| --- | --- | --- | --- |
| likes | 2,784 | 2,833 | 차이 +49 (정상 증분) |
| downloads | 1,399,511 | 1,484,329 | 차이 +84,818 (정상 증분) |
| license | other | cardData.license: other | OK |
| params | (정보 없음) | (없음) | OK — safetensors.total 없음 |
| createdAt | 2026-07-23 | 2026-07-23T07:55:24.000Z | OK |
| pipeline_tag | image-to-video | image-to-video | OK |

### #5 zai-org/GLM-5.3-Flash

| 필드 | 글에 표시된 값 | HF API 실제 값 | 일치 |
| --- | --- | --- | --- |
| likes | 2,046 | 2,065 | 차이 +19 (정상 증분) |
| downloads | 654,957 | 727,610 | 차이 +72,653 (정상 증분) |
| license | mit | cardData.license: mit | OK |
| params | 321.3B | 321.3B | OK |
| createdAt | 2026-08-25 | 2026-08-25T06:43:14.000Z | OK |
| pipeline_tag | image-text-to-text | image-text-to-text | OK |

수치 차이는 모두 수집 시점(2026-09-05) 이후 HF API 값 증가로, 글에 "(수집 시점 2026-09-05)" 표기되어 있어 모순 아님.

## 2. "왜 주목받는가" 문단 — 원문 인용 및 수치 비교 판정

### #1 Qwen/Qwen3.8-27B

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 13,948개, 다운로드 5,739,341회(수집 시점 2026-09-05). 같은 기관(Qwen)의 다른 발행 모델 Qwen/Qwen-Drive-1.0-4B 와 함께 살펴보세요."

| 항목 | 판정 |
| --- | --- |
| 선정 이유 문장 | OK ("Hugging Face 트렌딩 상위 30위 안에 들었습니다") |
| 좋아요/다운로드 수치 | OK ("좋아요 13,948개, 다운로드 5,739,341회") |
| 같은 기관·같은 태스크 이전 모델 대비 변화 (수치) | **미충족** — "Qwen-Drive-1.0-4B 와 함께 살펴보세요"로 언급만 하고 파라미터·다운로드·라이선스 중 어떤 수치 비교도 없음 |
| 비교 대상 같은 태스크 여부 | OK (Qwen-Drive-1.0-4B: image-text-to-text = 동일) |

### #2 MiniMaxAI/MiniMax-H3

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 4,905개, 다운로드 5,118,457회(수집 시점 2026-09-05). 같은 기관의 이전 모델과의 비교는 발행 이력이 부족해 제공하지 않습니다."

| 항목 | 판정 |
| --- | --- |
| 선정 이유 문장 | OK |
| 좋아요/다운로드 수치 | OK |
| 같은 기관·같은 태스크 이전 모델 대비 변화 (수치) | OK — "비교 대상 없음"으로 명시 (MiniMaxAI 기관 발행 이력 1개뿐) |
| 비교 대상 같은 태스크 여부 | 해당 없음 (비교 대상 없음) |

### #3 Qwen/Qwen3.8-Flash-Next

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 4,871개, 다운로드 351,374회(수집 시점 2026-09-05). 같은 기관(Qwen)의 다른 발행 모델 Qwen/Qwen-Drive-1.0-4B 와 함께 살펴보세요."

| 항목 | 판정 |
| --- | --- |
| 선정 이유 문장 | OK |
| 좋아요/다운로드 수치 | OK |
| 같은 기관·같은 태스크 이전 모델 대비 변화 (수치) | **미충족** — "Qwen-Drive-1.0-4B 와 함께 살펴보세요"로 언급만 하고 수치 비교 없음 |
| 비교 대상 같은 태스크 여부 | OK (Qwen-Drive-1.0-4B: image-text-to-text = 동일) |

### #4 Lightricks/LTX-2.5

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 2,784개, 다운로드 1,399,511회(수집 시점 2026-09-05). 같은 기관의 이전 모델과의 비교는 발행 이력이 부족해 제공하지 않습니다."

| 항목 | 판정 |
| --- | --- |
| 선정 이유 문장 | OK |
| 좋아요/다운로드 수치 | OK |
| 같은 기관·같은 태스크 이전 모델 대비 변화 (수치) | OK — "비교 대상 없음"으로 명시 (Lightricks 기관 발행 이력 1개뿐) |
| 비교 대상 같은 태스크 여부 | 해당 없음 (비교 대상 없음) |

### #5 zai-org/GLM-5.3-Flash

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 2,046개, 다운로드 654,957회(수집 시점 2026-09-05). 같은 기관(zai-org)의 다른 발행 모델 zai-org/GLM-5.3 와 함께 살펴보세요."

| 항목 | 판정 |
| --- | --- |
| 선정 이유 문장 | OK |
| 좋아요/다운로드 수치 | OK |
| 같은 기관·같은 태스크 이전 모델 대비 변화 (수치) | **미충족** — "GLM-5.3 와 함께 살펴보세요"로 언급만 하고 수치 비교 없음 |
| 비교 대상 같은 태스크 여부 | **불일치** — GLM-5.3-Flash task=image-text-to-text, GLM-5.3 task=text-generation (다름) |

## 3. 급상승(surge) 배지 — 7일 전 스냅샷 대조표

5개 글 중 surge 배지를 가진 글은 없음 (전부 trending 또는 trending+major-org).

| # | model_id | reason | surge 배지 | 7일 전 스냅샷 대조 필요 |
| --- | --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B | trending | 없음 | 해당 없음 |
| 2 | MiniMaxAI/MiniMax-H3 | trending | 없음 | 해당 없음 |
| 3 | Qwen/Qwen3.8-Flash-Next | trending, major-org | 없음 | 해당 없음 |
| 4 | Lightricks/LTX-2.5 | trending | 없음 | 해당 없음 |
| 5 | zai-org/GLM-5.3-Flash | trending, major-org | 없음 | 해당 없음 |

`data/stats_history.json` 에 2026-09-05 스냅샷만 존재 (7일 전 스냅샷 없음). 첫 실행이므로 급상승 판정이 불가능한 상태이나, surge 배지 글이 없으므로 일관성 문제 아님.

## 4. 신규성 게이트 통과 근거

기준일: 2026-09-05. 게이트: createdAt 60일 내(신규) 또는 lastModified 14일 내(갱신).

| # | model_id | createdAt | age(일) | lastModified | age(일) | 판정 | 근거 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B | 2026-08-05 | 31 | 2026-08-14 | 22 | 신규(new) | createdAt 60일 내 (31일) |
| 2 | MiniMaxAI/MiniMax-H3 | 2026-07-28 | 39 | 2026-08-13 | 23 | 신규(new) | createdAt 60일 내 (39일) |
| 3 | Qwen/Qwen3.8-Flash-Next | 2026-08-24 | 12 | 2026-08-27 | 9 | 신규(new) | createdAt 60일 내 (12일) |
| 4 | Lightricks/LTX-2.5 | 2026-07-23 | 44 | 2026-09-01 | 4 | 신규(new) | createdAt 60일 내 (44일) |
| 5 | zai-org/GLM-5.3-Flash | 2026-08-25 | 11 | 2026-09-04 | 1 | 신규(new) | createdAt 60일 내 (11일) |

5개 모두 신규성 게이트 통과.

## 5. 라이선스 상업 이용 가능 여부

| # | model_id | license | 글에 표시된 문구 | 정확 |
| --- | --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B | apache-2.0 | "apache-2.0 — 상업 이용 가능" | OK |
| 2 | MiniMaxAI/MiniMax-H3 | other | "other — 상업 이용 제한 또는 확인 필요" | OK |
| 3 | Qwen/Qwen3.8-Flash-Next | other | "other — 상업 이용 제한 또는 확인 필요" | OK |
| 4 | Lightricks/LTX-2.5 | other | "other — 상업 이용 제한 또는 확인 필요" | OK |
| 5 | zai-org/GLM-5.3-Flash | mit | "mit — 상업 이용 가능" | OK |

## 6. 핵심 스펙 표 존재

| # | model_id | 6행(태스크·파라미터·라이선스·최초 등록일·좋아요·다운로드) | 판정 |
| --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B | 모두 존재 | OK |
| 2 | MiniMaxAI/MiniMax-H3 | 모두 존재 | OK |
| 3 | Qwen/Qwen3.8-Flash-Next | 모두 존재 | OK |
| 4 | Lightricks/LTX-2.5 | 모두 존재 (파라미터="정보 없음") | OK |
| 5 | zai-org/GLM-5.3-Flash | 모두 존재 | OK |

## 7. 관련 모델 링크 — 같은 태스크 여부 검증

관련 모델 섹션에 표시된 모델이 같은 pipeline_tag 인지 확인:

| # | model_id (task) | 관련 모델 (task) | 같은 태스크 | 판정 |
| --- | --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B (image-text-to-text) | Qwen-Drive-1.0-4B (image-text-to-text) | OK | OK |
|  |  | Qwen3.8-2.4T-A95B (text-generation) | **다름** | **불일치** |
|  |  | Qwen3.8-2.4T-A95B-FP8 (text-generation) | **다름** | **불일치** |
|  |  | North-Micro-Vision-Instruct (image-text-to-text) | OK | OK |
|  |  | Qwen3.8-27B-FP8 (image-text-to-text) | OK | OK |
|  |  | Qwen3.8-Flash-Next (image-text-to-text) | OK | OK |
| 2 | MiniMaxAI/MiniMax-H3 (image-text-to-video) | MATLOWAI/minimax-h3-fused-turbo (image-text-to-video) | OK | OK |
| 3 | Qwen/Qwen3.8-Flash-Next (image-text-to-text) | Qwen-Drive-1.0-4B (image-text-to-text) | OK | OK |
|  |  | Qwen3.8-2.4T-A95B (text-generation) | **다름** | **불일치** |
|  |  | Qwen3.8-2.4T-A95B-FP8 (text-generation) | **다름** | **불일치** |
|  |  | North-Micro-Vision-Instruct (image-text-to-text) | OK | OK |
|  |  | Qwen3.8-27B (image-text-to-text) | OK | OK |
|  |  | Qwen3.8-27B-FP8 (image-text-to-text) | OK | OK |
| 4 | Lightricks/LTX-2.5 (image-to-video) | (관련 모델 없음) | — | OK |
| 5 | zai-org/GLM-5.3-Flash (image-text-to-text) | zai-org/GLM-5.3 (text-generation) | **다름** | **불일치** |
|  |  | zai-org/GLM-5.3-BF16 (text-generation) | **다름** | **불일치** |
|  |  | zai-org/GLM-5.3-Flash-BF16 (image-text-to-text) | OK | OK |
|  |  | North-Micro-Vision-Instruct (image-text-to-text) | OK | OK |
|  |  | Qwen-Drive-1.0-4B (image-text-to-text) | OK | OK |
|  |  | Qwen3.8-27B (image-text-to-text) | OK | OK |

## 8. 배포된 상세 페이지 및 HF 웹 페이지 응답

| # | model_id | 상세 페이지 HTTP | HF 웹 페이지 HTTP |
| --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B | 200 | 200 |
| 2 | MiniMaxAI/MiniMax-H3 | 200 | 200 |
| 3 | Qwen/Qwen3.8-Flash-Next | 200 | 200 |
| 4 | Lightricks/LTX-2.5 | 200 | 200 |
| 5 | zai-org/GLM-5.3-Flash | 200 | 200 |

## 9. 불일치 및 미충족 항목 요약

| 심각도 | 위치 | 내용 |
| --- | --- | --- |
| 상 | #1 Qwen/Qwen3.8-27B "왜 주목받는가" | 같은 기관·같은 태스크 이전 모델 대비 수치 비교(파라미터·다운로드·라이선스 중 최소 1개) 없음. "함께 살펴보세요"로 언급만 함 |
| 상 | #3 Qwen/Qwen3.8-Flash-Next "왜 주목받는가" | 동일. 수치 비교 없음 |
| 상 | #5 zai-org/GLM-5.3-Flash "왜 주목받는가" | 수치 비교 없음 + 비교 대상 zai-org/GLM-5.3 이 다른 태스크(text-generation) |
| 중 | #1, #3 관련 모델 섹션 | Qwen3.8-2.4T-A95B, Qwen3.8-2.4T-A95B-FP8 (text-generation)이 image-text-to-text 글의 관련 모델에 포함됨 (다른 태스크) |
| 중 | #5 관련 모델 섹션 | zai-org/GLM-5.3, zai-org/GLM-5.3-BF16 (text-generation)이 image-text-to-text 글의 관련 모델에 포함됨 (다른 태스크) |

## 판정: 불합격 — 사유: "왜 주목받는가" 문단에 같은 기관·같은 태스크 이전 모델 대비 수치 비교가 3개 글(#1, #3, #5)에서 누락됐고, #5 의 비교 대상 모델(zai-org/GLM-5.3)이 다른 태스크(text-generation)이며, #1·#3·#5 의 관련 모델 섹션에도 다른 태스크 모델이 포함되어 있다.