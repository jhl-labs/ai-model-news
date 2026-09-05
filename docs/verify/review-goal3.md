판정: 합격 — 2026-09-05

## 검증 명령

```bash
grep -n "write_summary\|GITHUB_STEP_SUMMARY" scripts/collect.py
grep -n "RETRY_STATUSES\|RETRY_MAX" scripts/collect.py
gh run list --workflow publish.yml --limit 3
python3 -m unittest discover -s tests -t . 2>&1 | tail -3
```

## 1. GITHUB_STEP_SUMMARY 구현

| 위치 | 코드 | 확인 |
| --- | --- | --- |
| scripts/collect.py:801 | `def write_summary(stats: dict, path: Path \| None = None) -> str:` | OK |
| scripts/collect.py:877 | `summary_path = os.environ.get("GITHUB_STEP_SUMMARY")` | OK |
| scripts/collect.py:880 | `write_summary(stats, Path(summary_path))` | OK |

write_summary 함수 내용: 수집 일시, 후보 모델 수, 신규 발행, 제외(신규성 게이트), 누적 발행 모델을 마크다운 표로 생성하여 `$GITHUB_STEP_SUMMARY` 파일에 추가 기록. GITHUB_STEP_SUMMARY 환경변수는 GitHub Actions 가 각 스텝에 자동 제공.

## 2. 429/5xx 백오프 재시도

| 위치 | 코드 | 확인 |
| --- | --- | --- |
| scripts/collect.py:56 | `RETRY_MAX = 4` | OK |
| scripts/collect.py:58 | `RETRY_MAX_SECONDS = 30.0` | OK |
| scripts/collect.py:59 | `RETRY_STATUSES = (429, 500, 502, 503, 504)` | OK |
| scripts/collect.py:129 | `return min(delay, RETRY_MAX_SECONDS)` | OK (상한 30s) |
| scripts/collect.py:134 | `return exc.code in RETRY_STATUSES` | OK (429/5xx만 재시도) |
| scripts/collect.py:148 | `for attempt in range(RETRY_MAX + 1):` | OK (최대 5회 시도) |
| scripts/collect.py:155 | `if not _is_retryable(exc) or attempt >= RETRY_MAX:` | OK (404 등 즉시 실패) |

## 3. 단위 테스트

| 항목 | 결과 |
| --- | --- |
| 명령 | `python3 -m unittest discover -s tests -t .` |
| 총 개수 | 84 |
| 결과 | OK |
| 실행 시간 | 0.075s |

## 4. 워크플로 success (최근 3개)

| run ID | 이벤트 | conclusion | 비고 |
| --- | --- | --- | --- |
| 33951642690 | push | success | 수집·커밋 skipped, 빌드·배포만 |
| 33951450008 | push | success | 수집·커밋 skipped, 빌드·배포만 |
| 33951366725 | workflow_dispatch | success | 수집 success (새 모델 0개), 0건 날도 실패 없음 |

### workflow_dispatch run(33951366725) 상세

| job | conclusion |
| --- | --- |
| 테스트 및 모델 수집 | success |
| 사이트 빌드 및 Pages 배포 | success |

수집 스텝: success, "No new models" / "새로 발행한 모델: 0개". 0건 날도 워크플로가 실패하지 않음 확인.

### push run(33951642690) 상세

| job | conclusion |
| --- | --- |
| 테스트 및 모델 수집 | success (수집·커밋 skipped) |
| 사이트 빌드 및 Pages 배포 | success |

push 이벤트에서는 수집·커밋 스텝이 `if: github.event_name != 'push'` 조건으로 skipped 되고, 단위 테스트·검증 빌드·배포만 실행. new_count 는 `|| '0'` 폴백으로 안전.

## 5. 0건 날 안정성

- workflow_dispatch run(33951366725): 수집 결과 0건, 워크플로 success
- collect.py: `if not new_posts: print("No new models")` — 0건일 때 exit 0 (정상 종료)
- publish.yml: `if git diff --cached --quiet; then echo "커밋할 변경 사항 없음"; exit 0` — 변경 없어도 실패하지 않음

## 6. 부분 실패 허용

- collect.py: `gather_candidates()` 에서 개별 listing 실패 시 `print("warning: ...")` 로 경고하고 계속 진행
- collect.py: 개별 모델 fetch 실패 시 `print("warning: skipping %s: %s")` 로 건너뛰고 계속
- 429/5xx: 최대 4회 backoff 재시도 후 RuntimeError, run()에서 catch하여 전체 실패 처리

## 판정

합격.
- GITHUB_STEP_SUMMARY 실행 요약(수집/신규/제외 건수)이 collect.py에 구현됨
- 429/5xx 백오프 재시도(RETRY_MAX=4, RETRY_STATUSES, 상한 30s) 구현됨
- 단위 테스트 84개 OK
- publish 워크플로 최근 3개 전부 success (push 2개, workflow_dispatch 1개)
- 0건 날도 워크플로 실패하지 않음 확인
- 부분 실패 허용(개별 listing·모델 fetch 실패 시 경고 후 계속)