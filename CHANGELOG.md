# CHANGELOG

## [Unreleased] — 2026-09-05

### 변경
- **선정 규칙**: 신규성 게이트 추가. 모든 경로(trending·surge·major-org)에서 createdAt 60일 내 신규 공개 또는 lastModified 14일 내 갱신을 충족해야 선정. 고전 모델(gpt2, bert-base-uncased, all-MiniLM-L6-v2, clip-vit-base-patch32, mms-300m, distilbert-base-uncased) 6개 제거.
- **글 품질**: 각 글에 "왜 주목받는가"(선정 이유 + 좋아요/다운로드 수치 + 같은 기관 모델 비교), 핵심 스펙 표, 라이선스 상업 이용 가능 여부, 관련 모델 링크 추가. 기존 41개 글 재생성.
- **첫 화면**: 상단에 "오늘의 하이라이트"(3일 내 likes 상위 3)와 "이번 주 급상승" 섹션 추가. 카드에 신규/갱신/급상승 배지와 "며칠 전" 상대 시각 표시. 360px 반응형·다크/라이트 유지.
- **운영 안정성**: GITHUB_STEP_SUMMARY 실행 요약(수집/신규/제외 건수) 추가. 0건 날 워크플로 실패하지 않음.

### 추가
- 단위 테스트 84개(신규 29개)