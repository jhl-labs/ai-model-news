판정: 합격 — 2026-09-05

## 1. 선행: 열린 PR 대기 및 main 동기화

`gh pr list --state open` 결과 열린 PR 0건(즉시 진행).

| 항목 | 값 |
| --- | --- |
| 명령 | `gh pr list --state open` |
| 열린 PR | 0건 |
| 대기 시간 | 0초 |
| `git checkout main; git pull --ff-only origin main` | `Already up to date` |
| 동기화 전 HEAD | `be12b8776407ddb2f0f004b52b18aa708a94c8f5` |

## 2. 워크플로 수동 실행

| 항목 | 값 |
| --- | --- |
| 명령 | `gh workflow run publish.yml --ref main -f max_new=25` |
| run ID | 33940355877 |
| trigger | workflow_dispatch |
| `gh run watch 33940355877 --exit-status` | exit 0 |
| 결론 | success |
| 테스트 및 모델 수집 잡 | success (7s) |
| 사이트 빌드 및 Pages 배포 잡 | success (13s) |

## 3. 봇 커밋·콘텐츠 변화

수집 로그: `No new models` / `새로 발행한 모델: 0개`.
stats_history.json 갱신으로 봇 커밋 1건 생성.

| 항목 | 실행 전 | 실행 후 |
| --- | --- | --- |
| HEAD sha | `be12b877…` | `cb80e0fe…` |
| 봇 커밋 sha | — | `97dc38a`(원본) → 리베이스 후 `cb80e0f` |
| 봇 커밋 작성자 | — | github-actions[bot] |
| 봇 커밋 메시지 | — | `content: 2026-09-05 수집 (새 모델 0개)` |
| 변경 파일 | — | `data/stats_history.json` (27 ins, 27 del) |
| `content/models/` 파일 수 | 47 | 47 (변화 없음) |
| `published.json` 항목 수 | 47 | 47 (변화 없음) |

`git pull --ff-only origin main` 결과: `3291edd..cb80e0f main -> origin/main`, fast-forward.

## 4. 배포 반영

| 항목 | 값 |
| --- | --- |
| `curl -s https://jhl-labs.github.io/ai-model-news/` | HTTP 200 |
| 카드 수(`class="card"`) | 47 |
| 모델 링크 수(`href="models/…/"`) | 47 |
| `curl -s …/feed.xml` | HTTP 200 |
| feed lastBuildDate | `Sat, 05 Sep 2026 00:00:00 +0000` |
| feed item 수 | 47 |

새 글이 0건이므로 새 슬러그 상세 페이지 200 확인은 해당 없음(기존 47개 유지).

## 5. 정확성 대조 (발행 글 3개)

새 글이 없어 `content/models/` 에서 임의 3개 선택.

| 모델 | 필드 | 글(frontmatter) | HF API | 일치 |
| --- | --- | --- | --- | --- |
| Qwen/Qwen3.8-2.4T-A95B | model_id | Qwen/Qwen3.8-2.4T-A95B | Qwen/Qwen3.8-2.4T-A95B | OK |
|  | task | text-generation | pipeline_tag: text-generation | OK |
|  | license | other | cardData.license: other | OK |
|  | hf_url | https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B | id 일치 | OK |
|  | HF 웹 페이지 | — | HTTP 200 | OK |
|  | 배포 상세 페이지 | — | HTTP 200 | OK |
|  | 페이지 내 HF 링크 | https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B | — | OK |
| MATLOWAI/minimax-h3-fused-turbo-int8-convrot | model_id | MATLOWAI/minimax-h3-fused-turbo-int8-convrot | MATLOWAI/minimax-h3-fused-turbo-int8-convrot | OK |
|  | task | image-text-to-video | pipeline_tag: image-text-to-video | OK |
|  | license | other | cardData.license: other | OK |
|  | hf_url | https://huggingface.co/MATLOWAI/minimax-h3-fused-turbo-int8-convrot | id 일치 | OK |
|  | HF 웹 페이지 | — | HTTP 200 | OK |
|  | 배포 상세 페이지 | — | HTTP 200 | OK |
|  | 페이지 내 HF 링크 | https://huggingface.co/MATLOWAI/minimax-h3-fused-turbo-int8-convrot | — | OK |
| OpenVDN/vdn-minimax-h3 | model_id | OpenVDN/vdn-minimax-h3 | OpenVDN/vdn-minimax-h3 | OK |
|  | task | text-to-video | pipeline_tag: text-to-video | OK |
|  | license | other | cardData.license: other | OK |
|  | hf_url | https://huggingface.co/OpenVDN/vdn-minimax-h3 | id 일치 | OK |
|  | HF 웹 페이지 | — | HTTP 200 | OK |
|  | 배포 상세 페이지 | — | HTTP 200 | OK |
|  | 페이지 내 HF 링크 | https://huggingface.co/OpenVDN/vdn-minimax-h3 | — | OK |

대조 전부 일치.

## 6. 최종 상태

| 항목 | 값 |
| --- | --- |
| `git status --short` | 빈 문자열(clean) |
| `git rev-parse HEAD` | `cb80e0fe9e6f53b9e0793b943148b97ac54b4c7b` |
| `git rev-parse origin/main` | `cb80e0fe9e6f53b9e0793b943148b97ac54b4c7b` |
| HEAD == origin/main | 일치 |

## 7. 실패·보류 항목

없음.

## 부록: 주요 명령 기록

```bash
gh pr list --state open
git checkout main && git pull --ff-only origin main
gh workflow run publish.yml --ref main -f max_new=25
gh run watch 33940355877 --exit-status
gh run view --job=101236425549 --log
git pull --ff-only origin main
curl -s -o /tmp/site-index.html -w "HTTP %{http_code}\n" https://jhl-labs.github.io/ai-model-news/
curl -s -o /tmp/feed.xml -w "HTTP %{http_code}\n" https://jhl-labs.github.io/ai-model-news/feed.xml
curl -s "https://huggingface.co/api/models/<model_id>"
curl -s -o /dev/null -w "HTTP %{http_code}\n" "https://huggingface.co/<model_id>"
curl -s -o /tmp/detail-<slug>.html -w "HTTP %{http_code}\n" "https://jhl-labs.github.io/ai-model-news/models/<slug>/"
git status --short
git rev-parse HEAD && git rev-parse origin/main
```