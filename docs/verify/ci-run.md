# GitHub Actions·Pages 실행 검증 (CI · publish)

**판정: 합격**

- 일시: 2026-09-05
- 대상: 저장소 `jhl-labs/ai-model-news` 의 `ci.yml`(push·pull_request 테스트) 과 `publish.yml`(수집→커밋→빌드→Pages 배포), 공개 URL `https://jhl-labs.github.io/ai-model-news/`
- 도구: `gh` CLI, `curl`, `python3`(xml.dom.minidom)
- 사전 확인: `git fetch origin --prune` 후 작업 트리 clean, `python3 -m unittest discover -s tests -t .` → 51 tests OK

## 결과 요약

| 항목 | 결과 | 비고 |
| --- | --- | --- |
| CI (push 이벤트) | 통과 | run 33939538525, Python 3.10 / 3.12 매트릭스 모두 success |
| CI (pull_request 이벤트) | 통과 | run 33940356698, PR #1 체크 2건 pass |
| PR 병합 | 통과 | PR #1 rebase 병합, 원격 브랜치 삭제 |
| publish (병합 후) | 통과 | run 33940378028, 두 잡·전 스텝 success, Pages 배포 완료 |
| 공개 URL | 통과 | 루트·about·feed·sitemap·robots·모델 상세 200, 없는 경로 404 |
| 콘텐츠 규모 | 통과 | 루트 모델 47개(기준 10개 이상), RSS item 47, sitemap url 49 |

## CI 워크플로 (`ci.yml`)

| run id | sha | event | conclusion | 매트릭스 | URL |
| --- | --- | --- | --- | --- | --- |
| 33939538525 | e65dfa9 (verify/ci-run) | push | success | 3.10 success, 3.12 success | https://github.com/jhl-labs/ai-model-news/actions/runs/33939538525 |
| 33940356698 | e65dfa9 (PR #1) | pull_request | success | 3.10 success, 3.12 success | https://github.com/jhl-labs/ai-model-news/actions/runs/33940356698 |

`ci.yml` 은 `pull_request` 와 main 이외 브랜치 `push` 에서만 실행되므로, main 직접 push 이력만 있던 상태에서는 실행 기록이 없었다. 검증 브랜치 push 와 PR 생성으로 두 이벤트 모두 실제 실행을 확인했다.

## PR 병합

| 항목 | 값 |
| --- | --- |
| PR | #1 — https://github.com/jhl-labs/ai-model-news/pull/1 |
| 제목 | refactor(collect): 리뷰 지적 반영 — 예외 범위 구체화, gather_candidates 단일 반환, 테스트 3개 추가 |
| 병합 방식 | `gh pr merge 1 --rebase --delete-branch` |
| 병합 후 main sha | 3291edd |
| 봇 후속 커밋 | cb80e0f `content: 2026-09-05 수집 (새 모델 0개)` — publish 워크플로가 `data/stats_history.json` 갱신을 커밋 |

## publish 워크플로 (`publish.yml`)

| run id | sha | event | conclusion | 잡 결과 | 새 모델 |
| --- | --- | --- | --- | --- | --- |
| 33938790991 | be12b87 | push | success | 테스트 및 모델 수집 success / 사이트 빌드 및 Pages 배포 success | 0개 |
| 33940378028 | 3291edd | push (PR 병합) | success | 테스트 및 모델 수집 success / 사이트 빌드 및 Pages 배포 success | 0개 |

run 33940378028 스텝별 conclusion:

| 잡 | 스텝 | conclusion |
| --- | --- | --- |
| 테스트 및 모델 수집 | 단위 테스트 | success |
| 테스트 및 모델 수집 | Hugging Face 모델 수집 | success (`No new models`, `새로 발행한 모델: 0개`) |
| 테스트 및 모델 수집 | 수집 결과 검증 빌드 | success |
| 테스트 및 모델 수집 | 변경 사항 커밋 및 push | success (이력 파일 1건 변경 → `cb80e0f` push) |
| 사이트 빌드 및 Pages 배포 | 정적 사이트 빌드 | success |
| 사이트 빌드 및 Pages 배포 | actions/configure-pages@v5 | success |
| 사이트 빌드 및 Pages 배포 | actions/upload-pages-artifact@v3 | success |
| 사이트 빌드 및 Pages 배포 | actions/deploy-pages@v4 | success |

수집 잡 로그에서 새 모델이 없어도 `stats_history.json` 의 관측 이력이 갱신되어 봇 커밋이 발생했다. 이는 설계 의도(이력은 후보 전체를 대상으로 기록)와 일치한다.

## Pages 공개 URL

`gh api repos/jhl-labs/ai-model-news/pages`:

| 필드 | 값 |
| --- | --- |
| html_url | https://jhl-labs.github.io/ai-model-news/ |
| build_type | workflow |
| status | null (Actions 배포 방식에서는 레거시 빌드 상태를 쓰지 않음) |
| https_enforced | true |

`curl -s -o /dev/null -w '%{http_code}'`:

| 경로 | 기대 | 실제 |
| --- | --- | --- |
| `/` | 200 | 200 |
| `about/` | 200 | 200 |
| `feed.xml` | 200 | 200 |
| `sitemap.xml` | 200 | 200 |
| `robots.txt` | 200 | 200 |
| `models/Qwen__Qwen3.8-27B/` | 200 | 200 |
| `no-such-page/` | 404 | 404 |

| 지표 | 값 |
| --- | --- |
| 루트 페이지 모델 링크 수 | 47 (기준 10 이상) |
| feed.xml `<item>` 수 | 47 |
| sitemap.xml `<url>` 수 | 49 (모델 47 + 루트 + about) |

## 사용한 명령

```
git fetch origin --prune && git status
python3 -m unittest discover -s tests -t .
gh pr create --base main --head verify/ci-run --title "<커밋 제목>" --body "<요약>"
gh pr checks 1 --watch
gh run list --workflow=ci.yml --event pull_request --json databaseId,headSha,event,conclusion,url
gh pr merge 1 --rebase --delete-branch
git checkout main && git pull --ff-only origin main && git branch -D verify/ci-run
gh run list --workflow=publish.yml --branch main --json databaseId,headSha,event,status,conclusion
gh run watch 33940378028 --exit-status
gh run view 33940378028 --json conclusion,jobs
gh run view 33940378028 --log | grep -E "새로 발행한 모델|커밋할 변경 사항 없음"
gh api repos/jhl-labs/ai-model-news/pages --jq '{html_url,build_type,status,https_enforced}'
curl -s -o /dev/null -w '%{http_code}' https://jhl-labs.github.io/ai-model-news/<경로>
curl -s .../feed.xml | python3 -c "import sys,xml.dom.minidom as m; print(len(m.parse(sys.stdin).getElementsByTagName('item')))"
curl -s .../sitemap.xml | python3 -c "import sys,xml.dom.minidom as m; print(len(m.parse(sys.stdin).getElementsByTagName('url')))"
curl -s .../ | grep -o 'href="models/[^"]*/"' | sort -u | wc -l
```
