판정: 합격 — 2026-09-05

## 대조 대상

발행 글 5개(무작위 선택, 다양한 기관·태스크 포함):

| # | model_id | org | task | reason |
| --- | --- | --- | --- | --- |
| 1 | tencent/EVIE-Preview-4.5B | tencent | visual-document-retrieval | major-org |
| 2 | Qwen/Qwen3.8-Flash-Next | Qwen | image-text-to-text | trending, major-org |
| 3 | MATLOWAI/minimax-h3-fused-turbo-int8-convrot | MATLOWAI | image-text-to-video | surge |
| 4 | IFM/K2-Horizon-MoVA-36B-A4B | IFM | text-generation | trending, surge |
| 5 | tencent/UI-Mate-9B | tencent | image-text-to-text | major-org |

## 1. frontmatter ↔ HF API 대조

각 글의 frontmatter(model_id, task, license, params, likes, downloads, created_at, hf_url)를 `curl -s https://huggingface.co/api/models/<model_id>` 응답과 대조.

### model_id

| # | 글 | HF API id | 일치 |
| --- | --- | --- | --- |
| 1 | tencent/EVIE-Preview-4.5B | tencent/EVIE-Preview-4.5B | OK |
| 2 | Qwen/Qwen3.8-Flash-Next | Qwen/Qwen3.8-Flash-Next | OK |
| 3 | MATLOWAI/minimax-h3-fused-turbo-int8-convrot | MATLOWAI/minimax-h3-fused-turbo-int8-convrot | OK |
| 4 | IFM/K2-Horizon-MoVA-36B-A4B | IFM/K2-Horizon-MoVA-36B-A4B | OK |
| 5 | tencent/UI-Mate-9B | tencent/UI-Mate-9B | OK |

### task (pipeline_tag)

| # | 글 | HF API pipeline_tag | 일치 |
| --- | --- | --- | --- |
| 1 | visual-document-retrieval | visual-document-retrieval | OK |
| 2 | image-text-to-text | image-text-to-text | OK |
| 3 | image-text-to-video | image-text-to-video | OK |
| 4 | text-generation | text-generation | OK |
| 5 | image-text-to-text | image-text-to-text | OK |

### license (cardData.license)

| # | 글 | HF API cardData.license | 일치 |
| --- | --- | --- | --- |
| 1 | apache-2.0 | apache-2.0 | OK |
| 2 | other | other | OK |
| 3 | other | other | OK |
| 4 | apache-2.0 | apache-2.0 | OK |
| 5 | apache-2.0 | apache-2.0 | OK |

### params (safetensors.total)

| # | 글 | HF API (humanized) | 일치 |
| --- | --- | --- | --- |
| 1 | 4.5B | 4.5B | OK |
| 2 | 180B | 180B | OK |
| 3 | (빈) | (빈) | OK — safetensors.total 없음 |
| 4 | 37.4B | 37.4B | OK |
| 5 | 9.4B | 9.4B | OK |

### likes / downloads (수집 시점 스냅샷)

| # | 글 likes | HF API likes | 글 downloads | HF API downloads | 비고 |
| --- | --- | --- | --- | --- | --- |
| 1 | 95 | 95 | 2,225 | 2,225 | 일치 |
| 2 | 4,871 | 4,883 | 351,374 | 351,374 | likes +12 (수집 후 증가, 정상) |
| 3 | 84 | 89 | 19,517 | 19,517 | likes +5 (수집 후 증가, 정상) |
| 4 | 149 | 160 | 433 | 433 | likes +11 (수집 후 증가, 정상) |
| 5 | 21 | 21 | 832 | 832 | 일치 |

좋아요 차이는 수집 시점(2026-09-05) 이후 HF API 값이 증가한 것으로, 글의 "수집 시점 2026-09-05" 표기와 모순 아님.

### created_at

| # | 글 | HF API createdAt | 일치 |
| --- | --- | --- | --- |
| 1 | 2026-08-17 | 2026-08-17T11:53:54.000Z | OK |
| 2 | 2026-08-24 | 2026-08-24T08:24:59.000Z | OK |
| 3 | 2026-08-29 | 2026-08-29T22:04:12.000Z | OK |
| 4 | 2026-09-01 | 2026-09-01T23:01:25.000Z | OK |
| 5 | 2026-08-14 | 2026-08-14T04:55:32.000Z | OK |

### hf_url

| # | 글 hf_url | HF 웹 페이지 HTTP | 일치 |
| --- | --- | --- | --- |
| 1 | https://huggingface.co/tencent/EVIE-Preview-4.5B | 200 | OK |
| 2 | https://huggingface.co/Qwen/Qwen3.8-Flash-Next | 200 | OK |
| 3 | https://huggingface.co/MATLOWAI/minimax-h3-fused-turbo-int8-convrot | 200 | OK |
| 4 | https://huggingface.co/IFM/K2-Horizon-MoVA-36B-A4B | 200 | OK |
| 5 | https://huggingface.co/tencent/UI-Mate-9B | 200 | OK |

## 2. 신규성 게이트 검증 (createdAt 60일 내)

기준일: 2026-09-05

| # | model_id | createdAt | age(일) | 60일 내 | 판정 |
| --- | --- | --- | --- | --- | --- |
| 1 | tencent/EVIE-Preview-4.5B | 2026-08-17 | 19 | True | OK |
| 2 | Qwen/Qwen3.8-Flash-Next | 2026-08-24 | 12 | True | OK |
| 3 | MATLOWAI/minimax-h3-fused-turbo-int8-convrot | 2026-08-29 | 7 | True | OK |
| 4 | IFM/K2-Horizon-MoVA-36B-A4B | 2026-09-01 | 4 | True | OK |
| 5 | tencent/UI-Mate-9B | 2026-08-14 | 22 | True | OK |

5개 모두 신규성 게이트 통과.

## 3. 글 품질 — 5개 섹션 존재

| # | model_id | 왜 주목받는가 | 핵심 스펙 | 요약 | 라이선스 | 관련 모델 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | tencent/EVIE-Preview-4.5B | OK | OK | OK | OK | OK |
| 2 | Qwen/Qwen3.8-Flash-Next | OK | OK | OK | OK | OK |
| 3 | MATLOWAI/minimax-h3-fused-turbo-int8-convrot | OK | OK | OK | OK | OK |
| 4 | IFM/K2-Horizon-MoVA-36B-A4B | OK | OK | OK | OK | OK |
| 5 | tencent/UI-Mate-9B | OK | OK | OK | OK | OK |

## 4. "왜 주목받는가" 내용 검증

선정 이유 + 좋아요/다운로드 수치 + 같은 기관 모델 비교 포함 여부:

| # | model_id | 선정 이유 문장 | 좋아요/다운로드 수치 | 같은 기관 비교 | 추정 표기 |
| --- | --- | --- | --- | --- | --- |
| 1 | tencent/EVIE-Preview-4.5B | "주요 기관이 최근 30일 안에 공개한 신작" | "좋아요 95개, 다운로드 2,225회(수집 시점 2026-09-05)" | "같은 기관(tencent)의 다른 발행 모델 tencent/Hy4-preview 와 함께 살펴보세요" | 해당 없음 |
| 2 | Qwen/Qwen3.8-Flash-Next | (trending+major-org) | 수치 포함 | 같은 기관 모델 링크 | 해당 없음 |
| 3 | MATLOWAI/minimax-h3-fused-turbo-int8-convrot | (surge) | 수치 포함 | 비교 제공 불가 명시 | 해당 없음 |
| 4 | IFM/K2-Horizon-MoVA-36B-A4B | "Hugging Face 트렌딩 상위 30위... 최근 7일 사이 좋아요·다운로드가 급증" | "좋아요 149개, 다운로드 433회(수집 시점 2026-09-05)" | "같은 기관의 이전 모델과의 비교는 발행 이력이 부족해 제공하지 않습니다" | 해당 없음 |
| 5 | tencent/UI-Mate-9B | (major-org) | 수치 포함 | 같은 기관 모델 링크 | 해당 없음 |

## 5. 라이선스 상업 이용 가능 여부

| # | model_id | license | 표시 문구 | 일치 |
| --- | --- | --- | --- | --- |
| 1 | tencent/EVIE-Preview-4.5B | apache-2.0 | "상업 이용 가능" | OK |
| 2 | Qwen/Qwen3.8-Flash-Next | other | "other — 상업 이용 제한 또는 확인 필요" | OK |
| 3 | MATLOWAI/minimax-h3-fused-turbo-int8-convrot | other | "other — 상업 이용 제한 또는 확인 필요" | OK |
| 4 | IFM/K2-Horizon-MoVA-36B-A4B | apache-2.0 | "상업 이용 가능" | OK |
| 5 | tencent/UI-Mate-9B | apache-2.0 | "상업 이용 가능" | OK |

## 6. 배포된 상세 페이지 확인

| # | slug | HTTP | HF 링크 일치 |
| --- | --- | --- | --- |
| 1 | tencent__EVIE-Preview-4.5B | 200 | OK |
| 2 | Qwen__Qwen3.8-Flash-Next | 200 | OK |
| 3 | MATLOWAI__minimax-h3-fused-turbo-int8-convrot | 200 | OK |
| 4 | IFM__K2-Horizon-MoVA-36B-A4B | 200 | OK |
| 5 | tencent__UI-Mate-9B | 200 | OK |

## 7. 사실 출처 검증

모든 정보(model_id, task, license, params, likes, downloads, created_at, hf_url)가 HF API 필드에서만 도출됨을 확인. 추정·날조 정보 없음. 좋아요/다운로드는 "수집 시점 2026-09-05"로 표기되어 스냅샷 값임을 명시.

## 판정

합격. 발행 글 5개의 frontmatter(model_id·task·license·params·likes·downloads·created_at·hf_url)가 HF API 응답과 전부 일치하고, 신규성 게이트(60일 내)를 통과하며, 5개 섹션(왜 주목받는가·핵심 스펙·요약·라이선스·관련 모델)이 모두 존재하고, "왜 주목받는가"에 선정 이유+수치+기관 비교가 포함되어 있으며, 라이선스 상업 이용 가능 여부가 정확하고, 배포된 상세 페이지의 HF 링크가 200으로 응답한다.