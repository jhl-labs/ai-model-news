판정: 합격

# 수집기 코드 리뷰 및 검증 (Collector Review)

리뷰어: opencode (수집기 작성자 아님)
리뷰 날짜: 2026-09-05
대상: `scripts/collect.py`, `scripts/frontmatter.py`, `tests/test_collect.py`, `tests/test_frontmatter.py`, `tests/fixtures/hf/`, `content/models/`, `data/`

## 1. 파일 실존

명령: `git ls-tree -r origin/main --name-only | grep -E "scripts/collect|scripts/frontmatter|tests/test_collect|tests/test_frontmatter|tests/fixtures/hf|data/published|data/stats"`

결과: **통과**

작업 트리와 origin/main 양쪽에 모두 존재:
- `scripts/collect.py` ✓
- `scripts/frontmatter.py` ✓
- `tests/test_collect.py` ✓
- `tests/test_frontmatter.py` ✓
- `tests/fixtures/hf/` — fixture 6개 (trending.json, by_org_meta-llama.json, detail_Qwen__Qwen3.8-27B.json, detail_deepseek-ai__DeepSeek-V4-Flash-Vision-Exp.json, readme_Qwen__Qwen3.8-27B.md, readme_deepseek-ai__DeepSeek-V4-Flash-Vision-Exp.md) ✓ (4개 이상)
- `data/published.json` ✓
- `data/stats_history.json` ✓

## 2. 테스트

명령: `python3 -m unittest discover -s tests -t . -v 2>&1 | tail -40`

결과: **통과**

```
Ran 48 tests in 0.044s
OK
```

- 전체 48개 테스트 통과
- 수집기 관련 테스트(test_collect, test_frontmatter): **32개** (15개 이상 충족)
  - test_collect: 26개 (HelperTests 8, HistoryTests 1, RunTests 7, SelectFamousTests 10)
  - test_frontmatter: 6개 (ParseDumpTests 5, SlugifyTests 3... 실제로 6개)

네트워크 없이 도는지 확인:
- `grep -n "urlopen\|huggingface.co" tests/*.py` 결과 — `huggingface.co`는 URL 문자열 리터럴로만 사용(실제 호출 아님), `urlopen`은 `mock.patch.object(collect.urllib.request, "urlopen", ...)` 로 mock 처리됨
- `env -i PATH=$PATH HOME=$HOME python3 -m unittest discover -s tests -t .` → 48 tests OK (환경 변수 없이도 통과)

**통과**: 실제 네트워크 호출 없이 fetcher 주입/fixture 기반으로 동작

## 3. 콘텐츠

명령: `ls content/models/*.md | wc -l`

결과: **47개** (10개 이상 충족) — **통과**

글 3개 frontmatter 검사 (`Qwen__Qwen3.8-27B.md`, `deepseek-ai__DeepSeek-V4-Flash-Vision-Exp.md`, `zai-org__GLM-5.3.md`):

- 13개 키(model_id, title, org, task, license, params, likes, downloads, discovered_at, created_at, hf_url, tags, reason) 모두 존재 — **통과**
- 모든 값이 `json.loads` 로 파싱 성공 (JSON 리터럴) — **통과**
- slug 규칙: model_id 의 `/` → `__` 변환, 파일명과 일치 — **통과**
  - `Qwen/Qwen3.8-27B` → `Qwen__Qwen3.8-27B.md` ✓
  - `deepseek-ai/DeepSeek-V4-Flash-Vision-Exp` → `deepseek-ai__DeepSeek-V4-Flash-Vision-Exp.md` ✓
  - `zai-org/GLM-5.3` → `zai-org__GLM-5.3.md` ✓

## 4. 정확성 대조 (HF API)

명령: `curl -s https://huggingface.co/api/models/<id>` for 3 models

결과: **통과**

| model_id | 글 license | HF license | 글 task | HF pipeline_tag | hf_url 일치 |
|---|---|---|---|---|---|
| Qwen/Qwen3.8-27B | apache-2.0 | apache-2.0 | image-text-to-text | image-text-to-text | ✓ |
| deepseek-ai/DeepSeek-V4-Flash-Vision-Exp | mit | mit | image-text-to-text | image-text-to-text | ✓ |
| zai-org/GLM-5.3 | other | other | text-generation | text-generation | ✓ |

모든 필드 일치. hf_url 형식 `https://huggingface.co/<model_id>` 확인.

## 5. 중복 방지

명령: `python3 scripts/collect.py --dry-run`

결과: `No new models` — **통과**

이미 발행된 모델이 신규 후보에 다시 뜨지 않음. `published.json` 과 기존 파일 존재 여부로 중복 방지(`collect.py:508`).

## 6. 코드 리뷰

### imports (표준 라이브러리만)

`scripts/collect.py`: argparse, datetime, json, re, sys, urllib.error, urllib.request, pathlib — **표준 라이브러리만 사용, requests 없음** — **통과**

`scripts/frontmatter.py`: json, re — **통과**

### 선정 기준 상수

`scripts/collect.py:46-63`에 상수 명시 및 docstring(1-23줄)에 주석:
- `TRENDING_TOP_N = 30` (trending 상위 30)
- `SURGE_WINDOW_DAYS = 7`, `SURGE_LIKES_DELTA = 200`, `SURGE_DOWNLOAD_RATIO = 2.0`, `SURGE_MIN_DOWNLOADS = 10_000`
- `MAJOR_ORGS` 리스트 (meta-llama, google, mistralai, Qwen, deepseek-ai, openai, microsoft, nvidia, stabilityai, black-forest-labs 등 20개 기관)
- `MAJOR_ORG_DAYS = 30`, `MAJOR_ORG_MIN_LIKES = 20`
- `FIRST_RUN_NEW_DAYS = 7`, `FIRST_RUN_LIKES = 100`

**통과**

### 민감 정보

`grep -rn "/home/\|vtopia\|gho_\|ghp_" scripts/ tests/` → 0건 — **통과**

### 기타 관찰 (심각도 '하' — 합격에 영향 없음)

1. **[하] `gather_candidates` 반환값 중복** (`collect.py:483`): `return candidates, candidates` — 같은 리스트를 두 번 반환. `seen` 이라고 명명된 두 번째 값이 실제로는 candidates 와 동일 객체. `update_history` 에 `seen` 을 넘기므로 의도대로 동작은 하지만, 변수명과 실체가 불일치. 제안: `return candidates, list(by_id.values())` 또는 `seen` 에 별도 리스트 반환.
2. **[하] `except Exception` 광범위 예외 처리** (`collect.py:124, 475, 481, 518, 547`): `# noqa: BLE001` 주석으로 의도 표시는 돼 있으나, 구체적 예외 타입 지정이 더 안전할 수 있음.
3. **[하] `list_top` 이 `fetcher` 를 기본 인자로 받지 않음** (`collect.py:109`): `list_trending`, `list_recent_by_org`, `fetch_model_detail`, `fetch_readme` 모두 `fetcher` 필수 인자. `fetch_json` 은 `fetcher=None` 기본값. 일관성 차이.

## 지적 사항 목록

| # | 심각도 | 위치 | 내용 | 수정 제안 |
|---|---|---|---|---|
| 1 | 하 | `scripts/collect.py:483` | `gather_candidates` 가 `candidates, candidates` 반환 — `seen` 이 별도 객체 아님 | `return candidates, list(by_id.values())` 로 두 번째 값을 복사본으로 |
| 2 | 하 | `scripts/collect.py:124,475,481,518,547` | 광범위 `except Exception` | 구체적 예외 타입 지정 권장 (이미 `# noqa` 로 의도 표시됨) |
| 3 | 하 | `scripts/collect.py:105-123` | `fetcher` 필수/선택 인자 일관성 | 모든 listing 함수에 `fetcher=None` 기본값 또는 모두 필수로 통일 |

심각도 '상'/'중' 지적 없음 → **합격**

## 요약

- **판정: 합격**
- 테스트 통과: 48개 전체, 수집기 관련 32개 (15개 기준 충족)
- 글 개수: 47개 (10개 기준 충족)
- HF API 대조: 3개 모델 id·license·task·hf_url 일치
- 중복 방지: dry-run 시 "No new models" 확인
- 표준 라이브러리만 사용, 민감 정보 노출 없음
- 지적 3건 모두 심각도 '하'

## 후속 처리 (2026-09-05)

리뷰 지적 3건을 코드베이스와 대조해 검증한 뒤 반영했습니다. 지적의 제안 문구를 그대로 따르지 않은 항목은 이유를 적었습니다.

| # | 조치 | 내용 |
|---|---|---|
| 1 | 반영(수정 방식 변경) | 제안된 `list(by_id.values())` 복사본 반환은 동일 내용을 두 번 돌려주는 구조를 유지하므로 채택하지 않음. `gather_candidates` 가 단일 리스트만 반환하도록 바꾸고, `run()` 은 그 리스트를 선정과 `update_history` 양쪽에 사용. 이력 기록이 "본 모델 전체"를 대상으로 한다는 의도가 코드에서 바로 드러남 |
| 2 | 반영(일부) | `FETCH_ERRORS = (RuntimeError, OSError, ValueError)`, `POST_ERRORS = FETCH_ERRORS + (KeyError, TypeError, AttributeError)` 상수를 두고 README·목록·상세 fetch 지점 4곳을 구체화. `main()` 의 `except Exception` 은 CLI 경계에서 어떤 실패든 종료 코드 1 로 바꿔 워크플로를 멈추게 하는 역할이라 유지하고 주석으로 이유 명시 |
| 3 | 반영 | `fetch_json` 의 `fetcher=None` 기본값 제거로 모든 fetch 함수가 `fetcher` 를 필수로 받도록 통일. 기본 fetcher 해석은 엔트리 포인트 `run()` 한 곳에서만 수행 |

추가 테스트 3개 (총 51개):
- `test_fetch_readme_returns_empty_on_fetch_error` — README fetch 실패 시 빈 문자열 반환과 경고 출력
- `test_gather_candidates_merges_listings_and_ranks_trending` — 목록 병합, trending 순위 부여, 하위 목록 실패 시 경고 후 계속
- `test_run_skips_model_whose_detail_fails_and_records_history_for_all` — 상세 fetch 실패 모델은 건너뛰되 이력은 전체 후보에 기록

검증: `python3 -m unittest discover -s tests -t . -v` → 51 tests OK, `python3 scripts/collect.py --dry-run` 정상 종료.
