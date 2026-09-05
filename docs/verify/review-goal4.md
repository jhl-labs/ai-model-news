판정: 합격 — 2026-09-05

## 1. CHANGELOG.md 루트 존재

| 항목 | 결과 |
| --- | --- |
| `ls CHANGELOG.md` | 존재 (1054 bytes) |
| 선정 규칙 변경 기록 | OK — "신규성 게이트 추가. 모든 경로에서 createdAt 60일 내 또는 lastModified 14일 내 충족해야 선정. 고전 모델 6개 제거" |
| 글 품질 변경 기록 | OK — "왜 주목받는가, 핵심 스펙 표, 라이선스 상업 이용 여부, 관련 모델 링크 추가. 기존 41개 글 재생성" |
| 첫 화면 변경 기록 | OK — "오늘의 하이라이트, 이번 주 급상승 섹션 추가. 카드에 배지와 상대 시각 표시" |
| 운영 안정성 변경 기록 | OK — "GITHUB_STEP_SUMMARY 실행 요약 추가. 0건 날 워크플로 실패하지 않음" |
| 단위 테스트 기록 | OK — "단위 테스트 84개(신규 29개)" |

## 2. README 키워드 카운트

`grep -c` 결과:

| 키워드 | 카운트 |
| --- | --- |
| 신규성 | 2 |
| 60일 | 2 |
| 14일 | 3 |
| 왜 주목받는가 | 1 |
| 하이라이트 | 1 |
| CHANGELOG | 1 |
| STEP_SUMMARY | 1 |
| GITHUB_STEP_SUMMARY | 1 |

모든 키워드 1개 이상 존재.

## 3. 워크플로 success

| 워크플로 | 최근 run | 이벤트 | conclusion |
| --- | --- | --- | --- |
| publish.yml | 33951170024 | push | success |
| publish.yml | 33951366725 | workflow_dispatch | success |
| ci.yml | 33940356698 | pull_request | success |

### workflow_dispatch run(33951366725) 상세

| job | conclusion |
| --- | --- |
| 테스트 및 모델 수집 | success |
| 사이트 빌드 및 Pages 배포 | success |

수집 스텝: success (새 모델 0개, "No new models"). 0건 날도 워크플로 실패하지 않음 확인.

### push run(33951170024) 상세

| job | conclusion |
| --- | --- |
| 테스트 및 모델 수집 | success (수집·커밋 skipped) |
| 사이트 빌드 및 Pages 배포 | success |

### GITHUB_STEP_SUMMARY 구현

- `scripts/collect.py:877` — `summary_path = os.environ.get("GITHUB_STEP_SUMMARY")` 로 환경변수 읽기
- `scripts/collect.py:801` — `write_summary()` 함수: 수집 일시, 후보 모델 수, 신규 발행, 제외(신규성 게이트), 누적 발행 모델 표를 마크다운으로 생성
- GITHUB_STEP_SUMMARY 환경변수는 GitHub Actions 가 각 스텝에 자동 제공하므로 publish.yml 에 명시 설정 불필요
- STEP_SUMMARY 내용은 Actions summary 탭에 표시되며 CLI 로그에는 출력되지 않음(정상 동작)

## 4. 사이트 화면 (webfetch 증거)

webfetch 로 https://jhl-labs.github.io/ai-model-news/ HTML 가져와 확인:

| 항목 | 결과 |
| --- | --- |
| HTTP | 200 |
| `<section class="highlights">오늘의 하이라이트` | 존재 (3개 카드: Qwen3.8 27B, MiniMax H3, Qwen3.8 Flash Next) |
| `<section class="surge">이번 주 급상승` | 존재 (5개 카드: DeepSeek V4 Flash Vision, GLM 5.3 Flash Uncensored, vdn-minimax-h3, K2 Horizon, MATLOWAI) |
| 전체 목록 카드 수 | 41 |
| 배지 badge-new | 49회 (하이라이트+급상승+전체 목록 중복 카드 포함) |
| 배지 badge-surge | 10회 |
| 고전 모델 부재 (gpt2·bert-base·all-MiniLM·clip-vit·distilbert·mms-300m) | 0건 — 제거 확인 |
| 상대 시각 (`<time>`) | "오늘" 표시 |
| 다크/라이트 테마 토글 | 존재 (theme-toggle 버튼, localStorage 인라인 스크립트) |
| 필터 (태스크 chips, 기관 select, 검색) | 존재 |

### 상세 페이지 글 품질 (Qwen/Qwen3.8-27B)

curl 로 상세 페이지 HTML 확인:

| 섹션 | 존재 |
| --- | --- |
| 왜 주목받는가 | OK |
| 핵심 스펙 | OK |
| 요약 | OK (마크다운 본문) |
| 라이선스 (상업 이용 가능 여부) | OK |
| 관련 모델 | OK |

## 5. 단위 테스트

| 항목 | 결과 |
| --- | --- |
| 명령 | `python3 -m unittest discover -s tests -t .` |
| 총 개수 | 84 |
| 결과 | OK |
| 실행 시간 | 0.074s |

## 6. 민감 정보

| 항목 | 결과 |
| --- | --- |
| 사용자명·로컬 절대경로 grep (scripts·tests·.github·README·CHANGELOG·docs/verify) | 0건 |

## 7. 저장소 상태

| 항목 | 결과 |
| --- | --- |
| `git status --short` | clean |
| HEAD | 427570a |
| origin/main | 427570a |
| HEAD == origin/main | 일치 |
| content/models 글 수 | 41 |
| published.json 항목 수 | 41 |
| 고전 모델 6개 제거 | 확인 (gpt2·bert-base·all-MiniLM·clip-vit·distilbert·mms-300m 부재) |

## 8. 최근 커밋 (origin/main)

```
427570a content: 2026-09-05 수집 (새 모델 0개)
96b9643 docs: CHANGELOG 추가 + README 글 구조·화면 구성 보완
...신규성 게이트·글 품질·첫 화면·운영 안정성 커밋들...
```

## 판정

합격. CHANGELOG 가 선정 규칙·글 품질·첫 화면·운영 안정성 변경을 모두 기록하고, README 가 새 선정 규칙(60일/14일 신규성 게이트)·글 구조(왜 주목받는가·핵심 스펙·라이선스·관련 모델)·화면 구성(하이라이트·급상승·배지)을 반영하며, publish·ci 워크플로가 success 이고 사이트에 새 첫 화면(오늘의 하이라이트·이번 주 급상승)과 고전 모델 제거가 실제 반영돼 있다.