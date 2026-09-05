판정: 합격 — 2026-09-05

## 대조 대상

발행 글 5개(무작위 선택, 서로 다른 모델):

| # | model_id | org | task | reason |
| --- | --- | --- | --- | --- |
| 1 | zai-org/GLM-5.3-Flash-BF16 | zai-org | image-text-to-text | major-org |
| 2 | tencent/EVIE-Preview-4.5B | tencent | visual-document-retrieval | major-org |
| 3 | FastVideo/FastVideo-FastH3-4-step-Preview-v1-VSA-DataFree | FastVideo | text-to-video | trending |
| 4 | ibm-granite/granite-4.2-3b | ibm-granite | text-generation | major-org |
| 5 | tencent/UI-Mate-9B | tencent | image-text-to-text | major-org |

## 1. 수치 대조 (좋아요 / 다운로드 / 라이선스 / 파라미터 / createdAt)

각 글의 frontmatter 및 핵심 스펙 표 값 vs `curl -s https://huggingface.co/api/models/<model_id>` 실제 응답.

### #1 zai-org/GLM-5.3-Flash-BF16

| 필드 | 글에 표시된 값 | HF API 실제 값 | 일치 |
| --- | --- | --- | --- |
| likes | 58 | 58 | OK |
| downloads | 11,075 | 11,075 | OK |
| license | mit | cardData.license: mit | OK |
| params | 321.3B | 321.3B | OK |
| createdAt | 2026-08-25 | 2026-08-25T06:45:05.000Z | OK |
| pipeline_tag | image-text-to-text | image-text-to-text | OK |
| lastModified | (글에 표시 없음) | 2026-09-04T06:45:54.000Z | 해당 없음 |

### #2 tencent/EVIE-Preview-4.5B

| 필드 | 글에 표시된 값 | HF API 실제 값 | 일치 |
| --- | --- | --- | --- |
| likes | 95 | 95 | OK |
| downloads | 2,225 | 2,225 | OK |
| license | apache-2.0 | cardData.license: apache-2.0 | OK |
| params | 4.5B | 4.5B | OK |
| createdAt | 2026-08-17 | 2026-08-17T11:53:54.000Z | OK |
| pipeline_tag | visual-document-retrieval | visual-document-retrieval | OK |

### #3 FastVideo/FastVideo-FastH3-4-step-Preview-v1-VSA-DataFree

| 필드 | 글에 표시된 값 | HF API 실제 값 | 일치 |
| --- | --- | --- | --- |
| likes | 270 | 277 | 차이 +7 (수집 시점 이후 증가, 정상) |
| downloads | 0 | 0 | OK |
| license | other | cardData.license: other | OK |
| params | 35B | 35B | OK |
| createdAt | 2026-08-27 | 2026-08-27T00:28:06.000Z | OK |
| pipeline_tag | text-to-video | text-to-video | OK |

likes 차이 +7: 글에 "수집 시점 2026-09-05"로 표기된 스냅샷 값(270)이며, HF API 조회 시점(2026-09-05 이후)에 277로 증가한 것. 글의 스냅샷 표기와 모순 아님.

### #4 ibm-granite/granite-4.2-3b

| 필드 | 글에 표시된 값 | HF API 실제 값 | 일치 |
| --- | --- | --- | --- |
| likes | 76 | 76 | OK |
| downloads | 16,721 | 16,721 | OK |
| license | apache-2.0 | cardData.license: apache-2.0 | OK |
| params | 3.7B | 3.7B | OK |
| createdAt | 2026-08-07 | 2026-08-07T16:26:43.000Z | OK |
| pipeline_tag | text-generation | text-generation | OK |

### #5 tencent/UI-Mate-9B

| 필드 | 글에 표시된 값 | HF API 실제 값 | 일치 |
| --- | --- | --- | --- |
| likes | 21 | 21 | OK |
| downloads | 832 | 832 | OK |
| license | apache-2.0 | cardData.license: apache-2.0 | OK |
| params | 9.4B | 9.4B | OK |
| createdAt | 2026-08-14 | 2026-08-14T04:55:32.000Z | OK |
| pipeline_tag | image-text-to-text | image-text-to-text | OK |

## 2. 라이선스 상업 이용 가능 여부 문구

| # | model_id | license | 글에 표시된 문구 | 정확 |
| --- | --- | --- | --- | --- |
| 1 | zai-org/GLM-5.3-Flash-BF16 | mit | "mit — 상업 이용 가능" | OK |
| 2 | tencent/EVIE-Preview-4.5B | apache-2.0 | "apache-2.0 — 상업 이용 가능" | OK |
| 3 | FastVideo/... | other | "other — 상업 이용 제한 또는 확인 필요" | OK |
| 4 | ibm-granite/granite-4.2-3b | apache-2.0 | "apache-2.0 — 상업 이용 가능" | OK |
| 5 | tencent/UI-Mate-9B | apache-2.0 | "apache-2.0 — 상업 이용 가능" | OK |

## 3. "왜 주목받는가" 문단 검증

선정 이유 + 좋아요/다운로드 수치 + 같은 기관/태스크 이전 모델 비교 포함 여부:

| # | model_id | 선정 이유 문장 | 수치 (좋아요/다운로드) | 같은 기관 모델 비교 | 수집 시점 표기 |
| --- | --- | --- | --- | --- | --- |
| 1 | zai-org/GLM-5.3-Flash-BF16 | "주요 기관이 최근 30일 안에 공개한 신작" | "좋아요 58개, 다운로드 11,075회" | "같은 기관(zai-org)의 다른 발행 모델 zai-org/GLM-5.3 와 함께 살펴보세요" | "(수집 시점 2026-09-05)" |
| 2 | tencent/EVIE-Preview-4.5B | "주요 기관이 최근 30일 안에 공개한 신작" | "좋아요 95개, 다운로드 2,225회" | "같은 기관(tencent)의 다른 발행 모델 tencent/Hy4-preview 와 함께 살펴보세요" | "(수집 시점 2026-09-05)" |
| 3 | FastVideo/... | "Hugging Face 트렌딩 상위 30위 안에 들었습니다" | "좋아요 270개, 다운로드 0회" | "같은 기관의 이전 모델과의 비교는 발행 이력이 부족해 제공하지 않습니다" | "(수집 시점 2026-09-05)" |
| 4 | ibm-granite/granite-4.2-3b | "주요 기관이 최근 30일 안에 공개한 신작" | "좋아요 76개, 다운로드 16,721회" | "같은 기관(ibm-granite)의 다른 발행 모델 ibm-granite/granite-4.2-30b 와 함께 살펴보세요" | "(수집 시점 2026-09-05)" |
| 5 | tencent/UI-Mate-9B | "주요 기관이 최근 30일 안에 공개한 신작" | "좋아요 21개, 다운로드 832회" | "같은 기관(tencent)의 다른 발행 모델 tencent/EVIE-Preview-4.5B 와 함께 살펴보세요" | "(수집 시점 2026-09-05)" |

5개 모두 선정 이유 + 수치 추세 + 같은 기관 모델 비교(또는 비교 불가 명시)를 포함.

## 4. 핵심 스펙 표 존재

| # | model_id | 핵심 스펙 표 (6행) | 확인 |
| --- | --- | --- | --- |
| 1 | zai-org/GLM-5.3-Flash-BF16 | 태스크·파라미터·라이선스·최초 등록일·좋아요·다운로드 | OK |
| 2 | tencent/EVIE-Preview-4.5B | 동일 6행 | OK |
| 3 | FastVideo/... | 동일 6행 | OK |
| 4 | ibm-granite/granite-4.2-3b | 동일 6행 | OK |
| 5 | tencent/UI-Mate-9B | 동일 6행 | OK |

## 5. 관련 모델 링크 (클릭 가능한 실제 URL)

배포된 상세 페이지에서 관련 모델 링크 추출 및 200 응답 확인:

| # | model_id | 관련 모델 링크 수 | 링크 예시 | 200 응답 |
| --- | --- | --- | --- | --- |
| 1 | zai-org/GLM-5.3-Flash-BF16 | 6 | ../zai-org__GLM-5.3/, ../zai-org__GLM-5.3-BF16/, ../zai-org__GLM-5.3-Flash/ | 샘플 200 OK |
| 2 | tencent/EVIE-Preview-4.5B | 3 | ../tencent__Hy4-preview/, ../tencent__Hy4-preview-FP8/, ../tencent__UI-Mate-27B/ | 샘플 200 OK |
| 3 | FastVideo/... | 1 | ../OpenVDN__vdn-minimax-h3/ | 200 OK |
| 4 | ibm-granite/granite-4.2-3b | 5 | ../ibm-granite__granite-4.2-30b/, ../ibm-granite__granite-4.2-8b/ | 샘플 200 OK |
| 5 | tencent/UI-Mate-9B | 6 | ../tencent__EVIE-Preview-4.5B/, ../tencent__Hy4-preview/ | 샘플 200 OK |

관련 모델 링크는 같은 기관(org) + 같은 태스크(task)의 다른 발행 모델을 상대 경로로 표시하며, 클릭 시 실제 상세 페이지로 200 응답.

## 6. HF 웹 페이지 응답

| # | model_id | https://huggingface.co/<model_id> HTTP |
| --- | --- | --- |
| 1 | zai-org/GLM-5.3-Flash-BF16 | 200 |
| 2 | tencent/EVIE-Preview-4.5B | 200 |
| 3 | FastVideo/FastVideo-FastH3-4-step-Preview-v1-VSA-DataFree | 200 |
| 4 | ibm-granite/granite-4.2-3b | 200 |
| 5 | tencent/UI-Mate-9B | 200 |

## 7. 불일치 항목

| # | model_id | 필드 | 글에 쓴 값 | 실제 API 값 | 비고 |
| --- | --- | --- | --- | --- | --- |
| 3 | FastVideo/... | likes | 270 | 277 | 수집 시점(2026-09-05) 스냅샷 이후 증가. 글에 "(수집 시점 2026-09-05)" 표기되어 있어 모순 아님 |

불일치로 간주할 수 있는 유일한 항목은 FastVideo 모델의 likes(270 vs 277)이나, 이는 수집 시점 이후의 자연스러운 증가이며 글에 "수집 시점 2026-09-05"로 명시되어 있어 정합성 문제가 아님.

## 8. 사실 출처 검증

모든 정보(model_id, task, license, params, likes, downloads, createdAt, hf_url)가 HF API 필드에서만 도출됨. 추정·날조 정보 없음. "왜 주목받는가"의 같은 기관 모델 비교는 published.json 발행 이력에서 도출.

판정: 합격