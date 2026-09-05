판정: 합격 — 2026-09-05

## 리뷰 대상 커밋

| 커밋 | 제목 | 파일 |
| --- | --- | --- |
| `ef9fb7e` | feat(collect): HTTP 429/5xx·일시 네트워크 오류에 지수 backoff 재시도 추가 | scripts/collect.py, tests/test_collect.py, README.md |
| `09a7e54` | ci(publish): push 이벤트에서는 수집·봇 커밋 스텝 생략 | .github/workflows/publish.yml |

## 1. 재시도 로직 (collect.py)

| 점검 항목 | 결과 | 근거 |
| --- | --- | --- |
| 429·500·502·503·504·URLError 만 재시도 | OK | `RETRY_STATUSES = (429, 500, 502, 503, 504)`, `_is_retryable()` 은 HTTPError 는 코드 체크, OSError(URLError 포함) 는 True |
| 404 등 다른 4xx 즉시 실패 | OK | `_is_retryable()` 이 HTTPError 404 → False → `break`, 테스트 `test_default_fetcher_does_not_retry_404` 로 검증 |
| 최대 횟수 상수 | OK | `RETRY_MAX = 4` (총 5회 시도) |
| 지수 backoff 상수 | OK | `RETRY_BASE_SECONDS = 1.0` → 1·2·4·8초 |
| Retry-After 우선(상한 30s) | OK | `_retry_after_seconds()` 가 헤더 파싱, `_retry_delay()` 가 `min(delay, RETRY_MAX_SECONDS=30.0)` 적용, 테스트 `test_default_fetcher_honours_retry_after_header_with_cap` 검증(7s, 30s 캡, 숫자 아님→backoff) |
| sleep 주입 | OK | `default_fetcher(url, sleep=None)`, `sleep = sleep or time.sleep`, 테스트는 `mock.Mock()` 주입 |
| 재시도 소진 시 FETCH_ERRORS 계열 귀결 | OK | `raise RuntimeError(...)` → `FETCH_ERRORS = (RuntimeError, OSError, ValueError)`, `run()` 의 `except Exception` 처리와 맞물림 |
| 표준 라이브러리만 | OK | `import time, urllib.error, urllib.request` 만 추가, 외부 의존성 0 |
| 재시도마다 stderr 경고 | OK | `print("warning: retry %d/%d ...", file=sys.stderr)` |

## 2. 테스트

| 항목 | 결과 |
| --- | --- |
| 명령 | `python3 -m unittest discover -s tests -t . -v` |
| 총 개수 | 55 |
| 결과 | OK |
| 실행 시간 | 0.055s (sleep 주입으로 실제 대기 없음) |
| 429 후 성공 테스트 | `test_default_fetcher_retries_429_with_backoff_then_succeeds` — 429→503→500→성공, opener 4회, sleep [1.0, 2.0, 4.0], warning 3회 |
| Retry-After 테스트 | `test_default_fetcher_honours_retry_after_header_with_cap` — 7s, 120s→30s 캡, unparsable→backoff 4.0s |
| 404 즉시 실패 테스트 | `test_default_fetcher_does_not_retry_404` — opener 1회, sleep 0회, "404" 포함 |
| 재시도 소진 테스트 | `test_default_fetcher_gives_up_after_retry_max` — 502 5회, sleep [1.0, 2.0, 4.0, 8.0] |
| mock 네트워크 | `grep urlopen tests/` → `mock.patch.object(collect.urllib.request, "urlopen", ...)` 5곳, 실제 네트워크 0 |

## 3. 워크플로 (publish.yml)

| 점검 항목 | 결과 | 근거 |
| --- | --- | --- |
| push 에 수집·커밋 스텝 if 조건 | OK | `if: github.event_name != 'push'` (수집 스텝, 커밋 스텝 모두) |
| 단위 테스트·검증 빌드·deploy 항상 실행 | OK | if 조건 없음, deploy 잡은 needs: collect 만 |
| new_count 출력 push 에서 빈 문자열 방지 | OK | `new_count: ${{ steps.collect.outputs.new_count \|\| '0' }}` 폴백 |
| schedule·workflow_dispatch 경로 동일 | OK | if 조건이 push 일 때만 skip, 나머지는 기존 동작 |
| 상단 주석 일치 | OK | push 시 수집·커밋 skip, schedule·workflow_dispatch 만 수집 명시 |

### 실증: GitHub Actions runs

| run ID | 이벤트 | 수집 스텝 | 커밋 스텝 | 검증 빌드 | deploy | 전체 |
| --- | --- | --- | --- | --- | --- | --- |
| 33941175509 | push | skipped | skipped | success | success | success |
| 33941201172 | workflow_dispatch | success | success | success | success | success |

push run: 수집·커밋 skipped, 단위 테스트·검증 빌드·deploy success.
workflow_dispatch run: 수집·커밋·검증 빌드·deploy 전부 success.

## 4. README 정합성

| 문장 | 코드/워크플로 | 일치 |
| --- | --- | --- |
| "main push 시 수집 없이 빌드·배포만 다시 수행" | publish.yml `if: github.event_name != 'push'` | OK |
| "429·5xx ... 최대 4회 지수 backoff(1·2·4·8초, Retry-After 헤더 우선, 상한 30초)... 404 등 다른 4xx 는 즉시 실패" | RETRY_MAX=4, RETRY_BASE_SECONDS=1.0, RETRY_MAX_SECONDS=30.0, RETRY_STATUSES, _is_retryable | OK |

## 5. 민감 정보

| 항목 | 결과 |
| --- | --- |
| 사용자명·로컬 절대경로 grep 검사(스크립트·테스트·워크플로·README·docs/verify) | 0건 (review-collector.md 의 grep 패턴 설명 문자열은 노출 아님) |

## 지적 사항

| 심각도 | 위치 | 내용 | 제안 |
| --- | --- | --- | --- |
| 하 | scripts/collect.py:142 | `except (urllib.error.HTTPError, urllib.error.URLError, OSError)` — URLError 는 OSError 서브클래스라 중복 열거 | 가독성만 문제, 동작 영향 없음. `(urllib.error.HTTPError, OSError)` 로 줄여도 무방 |
| 하 | scripts/collect.py:135 | `sleep = sleep or time.sleep` — falsy 값(0) 주입 시 time.sleep 으로 폴백 | 테스트는 mock.Mock() 사용으로 실제 문제 없음. `sleep if sleep is not None else time.sleep` 가 더 엄격 |

심각도 상·중: 없음.

## 판정

합격. 재시도 로직·테스트·워크플로·README 모두 코드와 일치하고 실제 GitHub Actions 실행 증거가 확인됨.