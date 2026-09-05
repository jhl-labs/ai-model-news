판정: 합격 — 2026-09-05

# 종단 검증 보고서(e2e.md) 재검토 및 재수집 실험

작성자가 아닌 팀원이 `docs/verify/e2e.md` 의 주장을 `gh`·`git`·`curl` 로 재확인하고,
발행 이력 1건을 제거한 뒤 publish 워크플로가 새 글을 생성·커밋·배포하는 경로를 실증했다.

## 0. 선행 조건

| 항목 | 결과 |
| --- | --- |
| `gh pr list --state open` | 0건(대기 없음) |
| `git checkout main; git pull --ff-only origin main` | `Already up to date` |
| `git status --short` | clean |
| 시작 HEAD | `c439c90` (`content: 2026-09-05 수집 (새 모델 0개)`) |

## 1부. e2e.md 주장 대조표

| # | e2e.md 주장 | 확인 명령 | 확인 결과 | 일치 |
| --- | --- | --- | --- | --- |
| 1 | run 33940355877 이 workflow_dispatch, success | `gh run view 33940355877 --json conclusion,event,headSha,jobs` | conclusion=success, event=workflow_dispatch, headSha=`be12b877…` | OK |
| 2 | 두 잡 모두 success (7s / 13s) | 같은 명령의 jobs, startedAt/completedAt | 수집 잡 success 7s(02:53:47→02:53:54), 배포 잡 success 13s(02:53:58→02:54:11) | OK |
| 3 | 봇 커밋 원본 sha `97dc38a`, 리베이스 후 `cb80e0f` | `gh run view 33940355877 --log` 의 `[main 97dc38a]`, `git log cb80e0f` | 로그에 `[main 97dc38a] content: 2026-09-05 수집 (새 모델 0개)`, main 에 `cb80e0f github-actions[bot]` 동일 메시지 | OK |
| 4 | 변경 파일 `data/stats_history.json` | `git show --stat cb80e0f` | `data/stats_history.json` 1개 파일 | OK |
| 5 | 변경 규모 27 ins / 27 del | `git show --shortstat cb80e0f` | **1 insertion, 1 deletion** | 불일치(사소) |
| 6 | content/models 47개, published.json 47개 | `ls content/models \| wc -l`, `python3 -c` | 47 / 47 | OK |
| 7 | 루트 200, 카드 47, feed 200·item 47 | `curl -s -w %{http_code}`, `grep -c` | 200 / 47 / 200 / 47 | OK |
| 8 | Qwen/Qwen3.8-2.4T-A95B: text-generation, other | frontmatter vs `api/models/<id>` | 글·API 모두 text-generation / other | OK |
| 9 | MATLOWAI/minimax-h3-fused-turbo-int8-convrot: image-text-to-video, other | 같은 방식 | 일치 | OK |
| 10 | OpenVDN/vdn-minimax-h3: text-to-video, other | 같은 방식 | 일치 | OK |
| 11 | 최종 HEAD == origin/main == `cb80e0f…` | `git log` | `cb80e0f` 가 main 이력에 존재하며 당시 기준 일치 | OK |

불일치 1건(#5)은 diff 통계 숫자 오기재로, 실제 변경 파일과 커밋 실체는 주장과 같다. 판정에 영향 없음.

## 2부. 재수집 실험

### 2-a. 후보 선정

로컬에서 `gather_candidates` + `select_famous` 를 오늘 날짜로 실행한 결과 선정 47개 전부가 이미 발행 상태였다.
그중 트렌딩 1위이며 세 기준(trending·surge·major-org)을 모두 만족하는 모델을 후보로 골랐다.

| 항목 | 값 |
| --- | --- |
| 후보 model_id | `deepseek-ai/DeepSeek-V4-Flash-Vision-Exp` |
| 슬러그 | `deepseek-ai__DeepSeek-V4-Flash-Vision-Exp` |
| 선정 사유(로컬 dry-run) | trending(1위), surge, major-org |

### 2-b. 발행 이력 제거·push

| 항목 | 값 |
| --- | --- |
| 삭제 | `content/models/deepseek-ai__DeepSeek-V4-Flash-Vision-Exp.md`, `data/published.json` 의 해당 키 |
| 제거 후 개수 | content/models 46, published.json 46 |
| 커밋 sha | `c1b37ea0288d9557cbdd4cb5139a9cf9baa9f90b` (`test(e2e): 재수집 실험용으로 DeepSeek-V4-Flash-Vision-Exp 발행 이력 1건 제거`) |
| push | `git push origin main` 성공 |

### 2-c. publish run 관찰

| 항목 | 값 |
| --- | --- |
| run id | 33940786817 (event=push, headSha=`c1b37ea…`) |
| 1차 시도(attempt 1) | **failure** — 수집 단계에서 `HTTP Error 429: Too Many Requests` (`api/models?sort=trendingScore…`) |
| 조치 | 60초 대기 후 `gh run rerun 33940786817 --failed` (코드·데이터 변경 없음) |
| 2차 시도(attempt 2) | `gh run watch --exit-status` exit 0, conclusion=success, 두 잡 success |
| 로그 `새로 발행한 모델: N개` | **N = 1** |
| 로그 생성 파일 | `content/models/deepseek-ai__DeepSeek-V4-Flash-Vision-Exp.md` |
| 봇 커밋 (로그) | `[main 22da908] content: 2026-09-05 수집 (새 모델 1개)` |
| 봇 커밋 (origin/main) | `22da908ef36b421c6cf027ac191d2cb945749d12`, 작성자 github-actions[bot] |
| `git pull --ff-only` 후 파일 | **복원됨** |
| frontmatter model_id | `deepseek-ai/DeepSeek-V4-Flash-Vision-Exp` (일치) |
| frontmatter hf_url | `https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp` (일치) |
| frontmatter task / license / reason | image-text-to-text / mit / trending, surge, major-org |
| 원본 글과의 차이 | `likes: 596 → 606` 만 다름(실시간 통계), 그 외 frontmatter 동일 |
| 복원 후 개수 | content/models 47, published.json 47 |

1차 실패는 Hugging Face API 의 요청 제한(429)으로 GitHub 호스트 러너 IP 에서 간헐적으로 발생하는 외부 요인이다.
워크플로는 실패를 삼키지 않고 exit 1 로 종료했고 deploy 잡은 skipped 됐다(기존 사이트 유지). 재시도만으로 정상 완료됐다.

### 2-d. 배포 반영

| 항목 | 값 |
| --- | --- |
| 루트 `https://jhl-labs.github.io/ai-model-news/` | HTTP 200 |
| 루트 카드 수(`class="card"`) | 47 (46 → 47 복귀) |
| 상세 `…/models/deepseek-ai__DeepSeek-V4-Flash-Vision-Exp/` | HTTP 200, 페이지 내 HF 링크 존재 |
| `feed.xml` | HTTP 200, item 47, `DeepSeek-V4-Flash-Vision-Exp` 문자열 포함 |

### 2-e. 최종 상태

| 항목 | 값 |
| --- | --- |
| `git status --short` | clean |
| HEAD | `22da908ef36b421c6cf027ac191d2cb945749d12` |
| origin/main | `22da908ef36b421c6cf027ac191d2cb945749d12` |
| HEAD == origin/main | 일치 |

## 3부. 판정 근거

- e2e.md 의 11개 주장 중 10개가 증거와 일치하고, 1개(diff 줄 수)는 판정에 영향 없는 오기재다.
- 발행 이력 1건 제거 → push → publish 워크플로가 같은 모델을 다시 선정해 글 1건을 생성·커밋(`22da908`)·배포했고,
  상세 페이지 200, 루트 카드 수 47 복귀, feed 반영까지 확인됐다.
- 1차 429 실패는 외부 요청 제한이며 재시도로 해결됐다. 운영상 고려 사항으로 수집기 429 재시도(backoff) 추가를 권고한다(판정 조건은 아님).

## 부록: 주요 명령

```bash
gh pr list --state open
git checkout main && git pull --ff-only origin main && git status --short
gh run view 33940355877 --json conclusion,event,headSha,jobs
gh run view 33940355877 --log | grep -aoE "\[main [0-9a-f]+\].*"
git show --shortstat cb80e0f
git rm content/models/deepseek-ai__DeepSeek-V4-Flash-Vision-Exp.md   # + published.json 키 제거
git commit && git pull --rebase origin main && git push origin main
gh run list --workflow=publish.yml --branch main --limit 2
gh run watch 33940786817 --exit-status
gh run view 33940786817 --log-failed
gh run rerun 33940786817 --failed
gh run view 33940786817 --log | grep -aE "새로 발행한 모델|content/models/.*\.md|\[main "
git pull --ff-only origin main
curl -s -o /dev/null -w "%{http_code}" https://jhl-labs.github.io/ai-model-news/models/deepseek-ai__DeepSeek-V4-Flash-Vision-Exp/
curl -s https://jhl-labs.github.io/ai-model-news/feed.xml | grep -c DeepSeek-V4-Flash-Vision-Exp
```
