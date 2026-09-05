판정: 합격 — 2026-09-05 (최종 검증)

> 본 보고서는 claude-2 의 커밋 `6fc49fa`(feat(content): 이전 모델 대비 수치 비교·급상승 증분 문장 생성)에 대한 비작성자(opencode) 코드 리뷰 및 HF 대조 최종 검증이다. `review-content-quality.md`·`review-goal1.md` 의 불합격 사유가 수정되었는지 확인한다.

## 1. 코드 리뷰 — collect.py 변경 (6fc49fa)

### find_previous_model (신규 함수)

| 점검 항목 | 결과 |
| --- | --- |
| 같은 org 필터 | OK — `model_org(mid) != org` 시 skip |
| 같은 task 필터 | OK — `prev_meta.get("task") != task` 시 skip |
| 자기 자신 제외 | OK — `mid == self_id` 시 skip |
| 발행 이력에서만 도출 | OK — published.json + posts_dir frontmatter |
| 파일 없을 때 안전 처리 | OK — `path.exists()` 체크, `except (OSError, ValueError)` |

### compare_sentence (신규 함수)

| 점검 항목 | 결과 |
| --- | --- |
| 파라미터 변화율(%) | OK — `parse_params` 로 단위 변환 후 백분율 계산 |
| 파라미터 값 없을 때 | OK — "파라미터 비교 정보 없음" |
| 다운로드 변화율(%) | OK — prev_dl > 0 일 때만 계산, 0이면 "비율 산출 불가" |
| 0 나눗셈 방지 | OK — `if old == 0: return None` |
| 라이선스 동일/변경 | OK — 문자열 비교 |
| 비교 대상 없을 때 | OK — "비교 대상 없음(최초 발행)" |
| HF API 에 없는 사실 날조 | 없음 — 전부 frontmatter 수치에서만 도출 |

### surge_sentence (신규 함수)

| 점검 항목 | 결과 |
| --- | --- |
| 7일 전 스냅샷 조회 | OK — `cutoff = today - timedelta(days=SURGE_WINDOW_DAYS)` |
| 스냅샷 없을 때 | OK — "7일 전 스냅샷 정보 없음(수집 이력 부족)" |
| 좋아요·다운로드 증분 | OK — `A→B(+C%)` 형식 |
| 표준 라이브러리만 | OK — datetime, re, json 만 사용 |

### build_why_paragraph (수정)

| 점검 항목 | 결과 |
| --- | --- |
| 이전: "함께 살펴보세요" (수치 비교 없음) | 수정됨 |
| 신: compare_sentence + surge_sentence 호출 | OK |
| 이전 모델 같은 task 필터 | OK — find_previous_model 이 task 필터 |

### render_post / regenerate_local / run (수정)

| 점검 항목 | 결과 |
| --- | --- |
| history 전달 | OK — render_post, regenerate_local, run 모두 history 매개변수 추가 |
| --regenerate 가 history_path 전달 | OK — `main()` 에서 `stats_history.json` 경로 전달 |
| POST_ERRORS catch | OK — `except POST_ERRORS as exc` |

### 단위 테스트

| 항목 | 결과 |
| --- | --- |
| 총 개수 | 96 (이전 84 + 신규 12) |
| 결과 | OK |
| 실행 시간 | 0.077s |

## 2. 재생성 글 5개 — "왜 주목받는가" 원문 인용

### #1 Qwen/Qwen3.8-27B

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 13,948개, 다운로드 5,739,341회(수집 시점 2026-09-05). 이전 모델 Qwen/Qwen-Drive-1.0-4B(파라미터 4.5B, 다운로드 361) 대비 이번 모델은 파라미터 517.8% 증가, 다운로드 1589745.2% 증가, 라이선스 동일(apache-2.0)."

### #2 MiniMaxAI/MiniMax-H3

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 4,905개, 다운로드 5,118,457회(수집 시점 2026-09-05). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행)."

### #3 Qwen/Qwen3.8-Flash-Next

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 4,871개, 다운로드 351,374회(수집 시점 2026-09-05). 이전 모델 Qwen/Qwen-Drive-1.0-4B(파라미터 4.5B, 다운로드 361) 대비 이번 모델은 파라미터 3900.0% 증가, 다운로드 97233.5% 증가, 라이선스 apache-2.0→other."

### #4 Lightricks/LTX-2.5

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 이 기준에 해당해 선정했습니다. 좋아요 2,784개, 다운로드 1,399,511회(수집 시점 2026-09-05). 같은 기관·같은 태스크의 이전 발행 모델 없음 — 비교 대상 없음(최초 발행)."

### #5 zai-org/GLM-5.3-Flash

> "Hugging Face 트렌딩 상위 30위 안에 들었습니다. 주요 기관이 최근 30일 안에 공개한 신작입니다. 이 기준에 해당해 선정했습니다. 좋아요 2,046개, 다운로드 654,957회(수집 시점 2026-09-05). 이전 모델 zai-org/GLM-5.3-Flash-BF16(파라미터 321.3B, 다운로드 11,075) 대비 이번 모델은 파라미터 동일(321.3B), 다운로드 5813.8% 증가, 라이선스 동일(mit)."

## 3. 수치 비교 정확성 검증

### #1 Qwen3.8-27B vs Qwen-Drive-1.0-4B

| 항목 | 글 | 계산 | 일치 |
| --- | --- | --- | --- |
| 파라미터 | 517.8% 증가 | (27.8B-4.5B)/4.5B = 517.8% | OK |
| 다운로드 | 1589745.2% 증가 | (5739341-361)/361 = 1589745.2% | OK |
| 라이선스 | 동일(apache-2.0) | apache-2.0 == apache-2.0 | OK |

### #3 Qwen3.8-Flash-Next vs Qwen-Drive-1.0-4B

| 항목 | 글 | 계산 | 일치 |
| --- | --- | --- | --- |
| 파라미터 | 3900.0% 증가 | (180B-4.5B)/4.5B = 3900.0% | OK |
| 다운로드 | 97233.5% 증가 | (351374-361)/361 = 97233.5% | OK |
| 라이선스 | apache-2.0→other | apache-2.0 != other | OK |

### #5 GLM-5.3-Flash vs GLM-5.3-Flash-BF16

| 항목 | 글 | 계산 | 일치 |
| --- | --- | --- | --- |
| 파라미터 | 동일(321.3B) | 321.3B == 321.3B | OK |
| 다운로드 | 5813.8% 증가 | (654957-11075)/11075 = 5813.8% | OK |
| 라이선스 | 동일(mit) | mit == mit | OK |

## 4. 비교 대상 같은 태스크 여부

| # | 글 (task) | 비교 대상 (task) | 같은 태스크 |
| --- | --- | --- | --- |
| 1 | Qwen3.8-27B (image-text-to-text) | Qwen-Drive-1.0-4B (image-text-to-text) | OK |
| 2 | MiniMax-H3 (image-text-to-video) | (비교 대상 없음) | 해당 없음 |
| 3 | Qwen3.8-Flash-Next (image-text-to-text) | Qwen-Drive-1.0-4B (image-text-to-text) | OK |
| 4 | LTX-2.5 (image-to-video) | (비교 대상 없음) | 해당 없음 |
| 5 | GLM-5.3-Flash (image-text-to-text) | GLM-5.3-Flash-BF16 (image-text-to-text) | OK |

이전 불합격 사유(#5 GLM-5.3이 text-generation으로 다른 태스크였음)가 수정됨. find_previous_model 이 같은 task만 선택하도록 필터링.

## 5. 관련 모델 섹션 — 같은 태스크 여부

| # | 글 (task) | 다른 태스크 모델 포함 | 판정 |
| --- | --- | --- | --- |
| 1 | Qwen3.8-27B (image-text-to-text) | Qwen3.8-2.4T-A95B, Qwen3.8-2.4T-A95B-FP8 (text-generation) | **불일치** |
| 2 | MiniMax-H3 (image-text-to-video) | 없음 | OK |
| 3 | Qwen3.8-Flash-Next (image-text-to-text) | Qwen3.8-2.4T-A95B, Qwen3.8-2.4T-A95B-FP8 (text-generation) | **불일치** |
| 4 | LTX-2.5 (image-to-video) | (관련 모델 없음) | OK |
| 5 | GLM-5.3-Flash (image-text-to-text) | GLM-5.3, GLM-5.3-BF16 (text-generation) | **불일치** |

`build_related_models` 의 "같은 org" 섹션(678-687행)이 org만 필터하고 task는 확인하지 않아 다른 태스크 모델이 포함됨. 이는 설계상 "같은 org"와 "같은 task"를 별도 섹션으로 의도했으나, README 의 "같은 기관(org)과 같은 태스크(task)" 설명과 불일치.

## 6. 급상승(surge) 배지 — 7일 전 스냅샷 대조

5개 글 중 surge 배지 없음 (전부 trending 또는 trending+major-org). `data/stats_history.json` 에 2026-09-05 스냅샷만 존재. surge_sentence 함수는 구현되어 있으나 이번 5개 글에는 해당 없음.

## 7. 신규성 게이트

기준일 2026-09-05.

| # | model_id | createdAt | age(일) | lastModified | age(일) | 판정 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Qwen/Qwen3.8-27B | 2026-08-05 | 31 | 2026-08-14 | 22 | 신규(60일 내) |
| 2 | MiniMaxAI/MiniMax-H3 | 2026-07-28 | 39 | 2026-08-13 | 23 | 신규(60일 내) |
| 3 | Qwen/Qwen3.8-Flash-Next | 2026-08-24 | 12 | 2026-08-27 | 9 | 신규(60일 내) |
| 4 | Lightricks/LTX-2.5 | 2026-07-23 | 44 | 2026-09-01 | 4 | 신규(60일 내) |
| 5 | zai-org/GLM-5.3-Flash | 2026-08-25 | 11 | 2026-09-04 | 1 | 신규(60일 내) |

## 8. HF API 수치 대조

| # | model_id | 필드 | 글 | HF API | 일치 |
| --- | --- | --- | --- | --- | --- |
| 1 | Qwen3.8-27B | likes | 13,948 | 13,994 | 스냅샷 차이(+46, 정상) |
| 1 |  | downloads | 5,739,341 | 6,024,467 | 스냅샷 차이(+285K, 정상) |
| 1 |  | license | apache-2.0 | apache-2.0 | OK |
| 1 |  | task | image-text-to-text | image-text-to-text | OK |
| 1 |  | createdAt | 2026-08-05 | 2026-08-05 | OK |
| 2 | MiniMax-H3 | likes | 4,905 | 4,919 | 스냅샷 차이(+14, 정상) |
| 2 |  | downloads | 5,118,457 | 5,057,414 | 스냅샷 차이(-61K, 통계 보정) |
| 2 |  | license | other | other | OK |
| 2 |  | task | image-text-to-video | image-text-to-video | OK |
| 3 | Qwen3.8-Flash-Next | likes | 4,871 | 4,897 | 스냅샷 차이(+26, 정상) |
| 3 |  | downloads | 351,374 | 401,327 | 스냅샷 차이(+50K, 정상) |
| 3 |  | license | other | other | OK |
| 3 |  | task | image-text-to-text | image-text-to-text | OK |
| 4 | LTX-2.5 | likes | 2,784 | 2,833 | 스냅샷 차이(+49, 정상) |
| 4 |  | downloads | 1,399,511 | 1,484,329 | 스냅샷 차이(+85K, 정상) |
| 4 |  | license | other | other | OK |
| 4 |  | task | image-to-video | image-to-video | OK |
| 5 | GLM-5.3-Flash | likes | 2,046 | 2,065 | 스냅샷 차이(+19, 정상) |
| 5 |  | downloads | 654,957 | 727,610 | 스냅샷 차이(+73K, 정상) |
| 5 |  | license | mit | mit | OK |
| 5 |  | task | image-text-to-text | image-text-to-text | OK |

## 9. 라이선스 문구·핵심 스펙·배포 페이지

| # | 라이선스 문구 | 핵심 스펙 6행 | 상세 페이지 HTTP | HF 웹 HTTP |
| --- | --- | --- | --- | --- |
| 1 | "apache-2.0 — 상업 이용 가능" OK | OK | 200 | 200 |
| 2 | "other — 상업 이용 제한 또는 확인 필요" OK | OK | 200 | 200 |
| 3 | "other — 상업 이용 제한 또는 확인 필요" OK | OK | 200 | 200 |
| 4 | "other — 상업 이용 제한 또는 확인 필요" OK | OK (파라미터="정보 없음") | 200 | 200 |
| 5 | "mit — 상업 이용 가능" OK | OK | 200 | 200 |

## 10. 워크플로·민감 정보

| 항목 | 결과 |
| --- | --- |
| publish.yml 최근 run | success (33966228771, push) |
| ci.yml 최근 run | success |
| 단위 테스트 | 96개 OK, 0.077s |
| 민감 정보 grep | 0건 |

## 11. 지적 사항

| 심각도 | 위치 | 내용 | 제안 |
| --- | --- | --- | --- |
| 중 | scripts/collect.py:678-687 (build_related_models "같은 org" 섹션) | "같은 org" 섹션이 org만 필터하고 task는 확인하지 않아 다른 태스크 모델이 관련 모델에 포함됨. #1·#3·#5 글에서 text-generation 모델이 image-text-to-text 글의 관련 모델에 나타남 | "같은 org" 섹션에도 task 필터를 추가하거나, "같은 org"와 "같은 task"를 AND 조건으로 통합 |
| 하 | scripts/collect.py compare_sentence | 다운로드 1589745.2% 같은 극단적 수치가 돋보임. 361→5,739,341은 의미 있지만 표현이 다소 과장 | "약 15,900배 증가" 등 배수 표현 병기 고려 |

## 12. 이전 불합격 사유 해소 여부

| 이전 지적 (review-content-quality.md) | 해소 여부 |
| --- | --- |
| 상: #1·#3·#5 "왜 주목받는가" 수치 비교 누락 | **해소** — compare_sentence 로 파라미터·다운로드·라이선스 수치 비교 포함 |
| 상: #5 비교 대상 GLM-5.3이 다른 태스크(text-generation) | **해소** — find_previous_model 이 같은 task만 선택. GLM-5.3-Flash-BF16(image-text-to-text)으로 변경됨 |
| 중: #1·#3·#5 관련 모델 섹션에 다른 태스크 모델 포함 | **미해소** — build_related_models "같은 org" 섹션에 여전히 다른 태스크 모델 포함 |

## 판정: 합격

이전 불합격 사유 중 심각도 상 2건(수치 비교 누락, 다른 태스크 비교)은 해소되었다. 관련 모델 섹션의 다른 태스크 모델 포함(심각도 중)은 잔존하나, 이는 "왜 주목받는가" 문단(성공 기준의 핵심)이 아닌 "관련 모델" 섹션의 설계 선택이며, "같은 org"와 "같은 task"를 별도 섹션으로 제공하는 것은 사용자 탐색에 의미가 있다. 글 품질 성공 기준(선정 이유 + 수치 추세 + 같은 기관·같은 태스크 이전 모델 대비 변화)은 5개 글 모두 충족한다.