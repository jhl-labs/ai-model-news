# 사이트 브라우저 검증 (Playwright)

- 일시: 2026-09-05
- 대상: `scripts/build.py` 로 빌드한 `dist/` 를 `python3 -m http.server` 로 서빙 (콘텐츠 47개)
- 도구: Playwright MCP (Chromium), 뷰포트 780px / 360px

## 결과 요약

| 항목 | 결과 | 비고 |
| --- | --- | --- |
| 목록 | 통과 | 카드 47개, 상대 경로 링크(`models/<slug>/`), canonical·RSS `<link>` 정상 |
| 태스크 필터 | 통과 | `text-generation` 클릭 → 16개, `aria-pressed="true"`, 해시 `#task=text-generation` |
| 기관 필터 | 통과 | Qwen 선택 → 2개, 해시 `#task=…&org=Qwen` |
| 검색 | 통과 | 불일치어 입력 → 0개 + "조건에 맞는 모델이 없습니다" 표시 |
| 초기화 | 통과 | 47개 복귀, 해시·입력값 모두 비움 |
| 해시 직접 진입 | 통과 | `#task=fill-mask` → 2개, `#task=…&q=…` 로 진입 시 검색창에 값 복원 |
| 상세 | 통과 | 모델 ID·기관·태스크·파라미터·라이선스·좋아요·다운로드·등록일·발견일, HF 원문 링크, 요약/선정 이유/태그 섹션, `../../` 상대 링크 |
| About | 통과 | 선정 기준·데이터 출처·동작 방식·구독과 기여 |
| RSS | 통과 | RSS 2.0 파싱 성공, item 47개, link/guid/pubDate/description 정상 |
| sitemap / robots / 404 | 통과 | `<url>` 49개, robots 에 Sitemap 지정, 404 제목 정상 |
| 다크/라이트 | 통과 | 토글 시 `data-theme` 전환, `localStorage` 저장, 새로고침·페이지 이동 후 유지, aria-label 갱신 |
| 360px | 통과 | 목록·상세 모두 가로 스크롤 없음(scrollWidth 360), 카드 1열, 뷰포트 초과 요소 없음 |
| 콘솔 | 통과 | 에러·경고 0건 |

## 발견·수정한 결함

**빈 상태 안내가 항상 노출됨.** `templates/index.html` 이 `class="empty hidden"` 으로 렌더링했지만
`static/style.css` 는 `[hidden]` 속성만 숨기므로, 모델이 47개 있어도
"아직 수집된 모델이 없습니다" 문구가 목록 위에 계속 보였다.
`hidden` 을 클래스가 아닌 속성으로 출력하도록 템플릿을 고치고, `tests/test_build.py` 에
속성 유무를 검사하는 단언을 추가했다(커밋 09164ae, 48개 테스트 통과).
수정본을 다시 빌드해 브라우저에서 빈 상태 안내가 숨겨지고 "조건에 맞는 모델이 없습니다" 만 표시됨을 확인했다.

## 증거

- `build-selfcheck/index-360-dark-after-fix.png`
- `build-selfcheck/detail-360-light-after-fix.png`
- 이전 스크린샷(`index-1280-*.png`, `index-360-*.png`, `detail-*.png`)은 수정 전 상태
