# ClubOS - 동아리 운영 관리 시스템

## 프로젝트 개요

ClubOS는 대학 동아리의 내부 운영을 효율화하는 웹 애플리케이션입니다. Google Sheets와 Slack 연동을 통해 회원 관리, 행사 관리, 그리고 데이터 분석 기능을 제공합니다.

## 현재 구현 상태

### 백엔드 (FastAPI)
- **기본 구조**: FastAPI 기반의 RESTful API
- **데이터베이스**: Supabase (PostgreSQL)
- **구현된 기능**:
  - 사용자 프로필 관리 (`/users` 엔드포인트)
  - Google Sheets 연동 (`/google-sheets` 엔드포인트)
  - 기본 인증 구조 (현재 비활성화)
  - CORS 미들웨어 설정

### 프론트엔드 (React + TypeScript)
- **기술 스택**: React, TypeScript, React Router, Bootstrap
- **구현된 페이지**:
  - 로그인 페이지 (`/login`)
  - 회원가입 페이지 (`/signup`)
  - 회원 목록 페이지 (`/members`)
  - 대시보드 페이지 (`/dashboard`)
  - 재무 관리 페이지 (`/finance`)
- **주요 기능**:
  - JWT 토큰 기반 인증
  - Google Sheets 데이터 표시
  - 회원 검색 및 정렬
  - 페이지네이션
  - 실시간 회원 통계 대시보드
  - 엑셀 기반 재무 관리 시스템

### 외부 연동
- **Google Sheets**: 회원 지원서 데이터 동기화
- **Slack**: 이벤트 API 준비 (미구현)

## 데이터베이스 스키마

### profiles 테이블
- `id`: 사용자 고유 ID
- `name`: 이름
- `email`: 이메일
- `department`: 학과
- `student_id`: 학번
- `gender`: 성별
- `phone_number`: 연락처
- `slack_user_id`: Slack 사용자 ID
- `updated_at`: 업데이트 시간

## 개발 명령어

### 백엔드 실행
```bash
# 가상환경 활성화 후
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 프론트엔드 실행
```bash
cd clubos-frontend
npm install
npm run dev
```

### 빌드 및 배포
```bash
# 프론트엔드 빌드
npm run build

# 타입 체크
npm run lint
```

## 디자인 시스템 (2024 현대적 민트 테마)

### 색상 팔레트
- **Primary**: #00d2aa (Fresh Mint Green)
- **Secondary**: #67e8f9 (Light Cyan) 
- **Accent**: #34d399 (Emerald Green)
- **배경**: 민트 그라데이션 (#f0fdfa → #ccfbf1 → #a7f3d0)
- **그라데이션**: 135도 선형 그라데이션 사용
- **유리 모프즘**: 반투명 배경 + 블러 효과

### 디자인 특징
- **현대적 유리 모프즘 (Glassmorphism)**: 반투명 카드, 블러 효과
- **마이크로 인터랙션**: 호버 시 부드러운 변형 및 그림자 효과
- **그라데이션 중심**: 단색 대신 그라데이션으로 시각적 깊이감 표현
- **타이포그래피**: Inter 폰트 + Pretendard 조합
- **아이콘**: 이모지 기반의 친근한 아이콘 시스템
- **반응형**: 모바일 우선 설계

### 컴포넌트 시스템
- **glass-card**: 유리 모프즘 카드
- **modern-table**: 떠다니는 형태의 테이블 행
- **page-header**: 그라데이션 배경의 페이지 헤더
- **modern-navbar**: 블러 효과를 가진 고정 네비게이션
- **controls-section**: 격자 레이아웃의 컨트롤 섹션

## 재무 관리 시스템 (Finance Management)

### 개요
토스 은행 앱에서 영감을 받은 현대적인 재무 관리 시스템으로, 동아리의 회계 업무를 간편하게 관리할 수 있습니다.

### 주요 기능

#### 1. 엑셀 파일 업로드
- **지원 형식**: .xlsx, .xls, .csv 파일
- **드래그 앤 드롭**: 직관적인 파일 업로드 인터페이스
- **자동 파싱**: 거래 내역 자동 인식 및 분석
- **실시간 처리**: 파일 업로드 즉시 분석 결과 표시

#### 2. 거래 내역 분석
- **거래 데이터 구조**:
  - 거래일자, 적요, 거래유형, 금융기관
  - 계좌번호, 거래금액, 잔액, 메모
- **자동 분류**: 입금/출금 자동 구분
- **실시간 표시**: 최근 10개 거래 내역 표시

#### 3. 재무 통계 대시보드
- **현재 총 잔액**: 최신 통장 잔액 표시
- **이번 학기 수입**: 3월부터 현재까지 총 수입
- **이번 학기 지출**: 총 사용 금액
- **순이익 계산**: 수입 - 지출 자동 계산
- **시각적 표현**: 수익/손실에 따른 색상 구분

#### 4. 사용자 경험
- **토스 스타일 디자인**: 직관적이고 현대적인 UI
- **반응형 디자인**: 모바일 친화적 레이아웃
- **실시간 애니메이션**: 부드러운 데이터 로딩 효과
- **오류 처리**: 파일 형식 오류 시 친절한 안내

### 기술 구현

#### 프론트엔드 기술
- **React Dropzone**: 파일 업로드 인터페이스
- **SheetJS (xlsx)**: 엑셀 파일 파싱
- **TypeScript**: 타입 안전성
- **CSS 애니메이션**: 부드러운 인터랙션

#### 데이터 처리
- **클라이언트 사이드 파싱**: 보안성과 속도 향상
- **실시간 계산**: 학기별 수입/지출 자동 계산
- **통화 포맷팅**: 한국어 숫자 표시 (예: 1,000,000원)

### 파일 구조
```
/pages/FinancePage.tsx      # 메인 재무 관리 페이지
/index.css                  # 재무 관리 전용 스타일
  - .finance-upload-section # 파일 업로드 영역
  - .finance-stats-grid     # 통계 카드 그리드
  - .transactions-table     # 거래 내역 테이블
  - .dropzone              # 드래그 앤 드롭 영역
```

### 사용 방법
1. 네비게이션 바에서 "💰 재무관리" 클릭
2. 엑셀 파일을 드래그하거나 클릭하여 업로드
3. 자동으로 파싱된 재무 통계 확인
4. 최근 거래 내역을 테이블에서 확인

## 향후 개발 계획

### 1단계: 핵심 기능 완성
- [ ] 인증 시스템 활성화
- [ ] 역할 기반 접근 제어 (RBAC) 구현
- [ ] Slack 연동 완성
- [ ] 행사 관리 기능
- [x] 기본 대시보드 (완료)
- [x] 재무 관리 시스템 (완료)

### 2단계: 고급 기능 추가
- [ ] 자동 Google Sheets 동기화
- [ ] 고급 분석 대시보드
- [ ] 회원 승인/거절 시스템
- [ ] 알림 시스템

### 3단계: 사용자 경험 개선
- [x] 모바일 최적화 (반응형 디자인 완료)
- [ ] 실시간 업데이트
- [ ] 고급 검색 및 필터링
- [ ] 데이터 내보내기
- [x] 현대적 UI/UX 디자인 (완료)

## 주요 설정 파일

### 환경 변수 (.env)
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GOOGLE_CREDENTIALS_PATH=./credentials/google_sheets_credentials.json
```

### 주요 디렉토리 구조
```
clubOS/
├── app/                    # FastAPI 백엔드
│   ├── api/               # API 라우터
│   ├── core/              # 핵심 설정
│   ├── models/            # 데이터 모델
│   └── services/          # 외부 서비스
├── clubos-frontend/       # React 프론트엔드
│   ├── src/
│   │   ├── components/    # 재사용 컴포넌트
│   │   ├── pages/         # 페이지 컴포넌트
│   │   └── services/      # API 서비스
├── credentials/           # 인증 파일
└── sql/                   # SQL 스크립트
```

## 문제 해결

### 일반적인 문제
1. **CORS 에러**: 백엔드 서버가 실행 중인지 확인
2. **Google Sheets 연동 실패**: 인증 파일 경로 확인
3. **Supabase 연결 실패**: 환경 변수 설정 확인

### 디버깅 팁
- 백엔드 로그: FastAPI 자동 문서 `/docs` 활용
- 프론트엔드 디버깅: 브라우저 개발자 도구 네트워크 탭 확인
- 데이터베이스: Supabase 대시보드에서 직접 확인

## 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [React 공식 문서](https://react.dev/)
- [Supabase 공식 문서](https://supabase.com/docs)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Slack Events API](https://api.slack.com/events-api)