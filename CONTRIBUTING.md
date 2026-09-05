# 기여 가이드라인 (Contributing to ai-model-news)

이 저장소는 Hugging Face 에 주목받는 AI 모델 소식을 매일 자동 수집·발행하는
기술 블로그입니다. 기여를 검토해 주셔서 감사합니다.

## 로컬 준비

- Python 3.11 이상만 필요합니다.
- 외부 의존성은 없습니다. 표준 라이브러리만 사용합니다.
- 저장소를 클론한 뒤 별도 설치 단계 없이 바로 실행할 수 있습니다.

## 테스트 실행

```bash
python3 -m unittest discover -s tests -t . -v
```

모든 단위 테스트가 통과하는지 확인합니다.

## 수집기 실행 (드라이 런)

```bash
python3 scripts/collect.py --dry-run
```

네트워크 호출 없이 고정 fixture 로 수집 로직을 검증합니다.

## 사이트 빌드 및 미리보기

```bash
python3 scripts/build.py --content-dir content/models --out dist
python3 -m http.server -d dist 8000
```

브라우저에서 http://localhost:8000 을 열어 결과를 확인합니다.

## 브랜치 및 PR 규칙

- `main` 브랜치에 직접 push 할 수 있는 것은 자동화 봇과 메인테이너뿐입니다.
- 일반 기여자는 저장소를 fork 한 뒤 기능 브랜치에서 작업하고 PR 을 보내주세요.
- CI(테스트·빌드)가 모두 통과해야 병합할 수 있습니다.

## 커밋 메시지 규칙

Conventional Commits 형식을 권장합니다.

- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `chore`: 잡무
- `ci`: CI/CD 변경

예: `feat: 트렌딩 모델 수집 기준 추가`

## '유명 모델' 선정 기준 변경 제안

선정 기준을 바꾸려면 `scripts/collect.py` 의 상수와 README 의 선정 기준 절을
함께 수정하는 PR 을 올려주세요. 한쪽만 바뀌면 안 됩니다.

## content/models/ 글 편집 금지

`content/models/` 아래의 글은 자동 생성물입니다. 손으로 직접 편집하지 마세요.
문제가 있으면 수집기 쪽을 수정해 다시 생성되도록 해주세요.

## 보안 주의사항

- 로컬 절대 경로, 개인 액세스 토큰, 시스템 사용자명·호스트명을 커밋하지 마세요.
- Hugging Face API 는 인증 없이 사용할 수 있으므로 토큰이 필요하지 않습니다.

## 행동 강령

서로 존중하는 태도로 소통해 주세요.

---

## English Summary

This repository is a tech blog that automatically collects and publishes news
about notable AI models on Hugging Face.

- **Setup:** Python 3.11+ only, no external dependencies.
- **Tests:** `python3 -m unittest discover -s tests -t . -v`
- **Collect (dry run):** `python3 scripts/collect.py --dry-run`
- **Build & preview:**
  `python3 scripts/build.py --content-dir content/models --out dist` then
  `python3 -m http.server -d dist 8000`
- **Branching:** Direct push to `main` is reserved for bots and maintainers.
  Contributors should fork and open a PR. CI must pass before merge.
- **Commit style:** Conventional Commits (`feat`/`fix`/`docs`/`chore`/`ci`).
- **Notable-model criteria:** Change both the constants in `scripts/collect.py`
  and the criteria section of the README in the same PR.
- **`content/models/`:** Auto-generated — do not edit by hand.
- **Security:** Never commit local paths, tokens, usernames, or host names.
- **Code of conduct:** Be respectful.