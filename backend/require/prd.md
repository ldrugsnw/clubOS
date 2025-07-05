ClubOS: FastAPI 백엔드 개발 가이드 (v1.0)

1. 개요 (Overview)

본 문서는 ClubOS 프로젝트의 백엔드 서버를 Python FastAPI 프레임워크로 개발하기 위한 기술 명세 및 구현 가이드를 제공합니다. 기획서(PRD)와 확정된 데이터베이스 스키마를 기반으로, 실제 개발에 필요한 데이터 모델, API 엔드포인트별 로직, 외부 서비스 연동 방안을 구체적으로 기술합니다.

주요 기술 스택

언어: Python 3.9+

웹 프레임워크: FastAPI

데이터베이스: Supabase (PostgreSQL)

인증: JWT via Supabase Auth (해당 기능은 별도 구현 가이드 제외)

외부 연동 라이브러리:

Google Sheets: gspread

Slack: slack_bolt

2. 프로젝트 설정 (Project Setup)

2.1. 환경 변수 (.env_local)

프로젝트 루트에 .env_local 파일을 생성하고 다음 환경 변수를 관리합니다. Supabase 및 외부 API 키는 절대 코드에 하드코딩하지 않습니다.

# -------------------------
# Supabase 설정 (env_local에 보관)
# -------------------------
SUPABASE_URL="YOUR_SUPABASE_URL"
SUPABASE_SERVICE_KEY="YOUR_SUPABASE_SERVICE_ROLE_KEY"

# -------------------------
# JWT 설정 (별도 설정 제외)
# -------------------------
# JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES 등은 별도 가이드에서 제외됨

# -------------------------
# Google Service Account
# -------------------------
# gspread는 JSON 파일 직접 참조 권장, 현재 설정 대기 중
# GOOGLE_CREDENTIALS_PATH="./path/to/credentials.json"

# -------------------------
# Slack
# -------------------------
# SLACK_BOT_TOKEN="xoxb-..."
# SLACK_SIGNING_SECRET="..."

2.2. 필요 라이브러리 (requirements.txt)

fastapi
uvicorn[standard]
pydantic
python-dotenv
supabase
gspread
oauth2client
slack_bolt
passlib[bcrypt]
python-jose[cryptography]

3. 데이터 모델 (Pydantic Models)

FastAPI의 자동 유효성 검사 및 API 문서화를 위해 Pydantic 모델을 사용합니다. 데이터베이스 스키마를 기반으로 모델을 정의합니다.

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

# --- Base Models ---
class ProfileBase(BaseModel):
    name: str
    department: Optional[str] = None
    student_id: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    slack_user_id: Optional[str] = None

class ProfileCreate(ProfileBase):
    id: uuid.UUID  # Supabase auth.users.id
    email: EmailStr

class Profile(ProfileBase):
    id: uuid.UUID
    email: EmailStr
    updated_at: datetime

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    slack_message_ts: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: uuid.UUID
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# --- API Specific Models ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    roles: List[str] = []

class UserInDB(Profile):
    roles: List[str]

class EventWithParticipants(Event):
    participants: List[Profile]

4. API 엔드포인트 명세 및 구현 가이드

4.1. 사용자 (Users) - /users

GET /me

설명: 현재 로그인된 사용자의 상세 정보를 반환합니다.

요청: Header Authorization: Bearer <token>

응답: UserInDB

구현 로직:

Depends로 토큰 검증 후 TokenData 추출

profiles 테이블과 user_roles 테이블에서 이메일로 사용자 정보 조회

UserInDB 모델로 반환

GET /

설명: 모든 회원 목록 조회 (이름, 학과 등 검색 가능)

권한: Executive, Admin

요청: Query name: Optional[str], department: Optional[str]

응답: List[Profile]

구현 로직:

권한 검사

Supabase select 쿼리를 동적으로 구성 (ilike 지원)

결과를 List[Profile]로 반환

4.2. 행사 (Events) - /events

POST /

설명: 신규 행사 생성

권한: Executive, Admin

요청: EventCreate

응답: Event

구현 로직:

권한 검사

EventCreate + 현재 로그인 user_id 합쳐 insert

생성된 데이터를 Event로 반환

GET /{event_id}

설명: 특정 행사 상세 및 참여자 조회

권한: 모든 인증된 사용자

요청: Path event_id: uuid.UUID

응답: EventWithParticipants

구현 로직:

events 테이블에서 event_id 조회

event_participations에서 참여자 user_id 목록 조회

profiles 테이블에서 참여자 프로필 조회

EventWithParticipants 조합 후 반환

4.3. 외부 연동 (Integrations) - /integrations

POST /google/sync-members

설명: Google Sheets 회원 동기화

권한: Admin

구현 로직:

권한 검사

서비스 계정 JSON (GOOGLE_CREDENTIALS_PATH)로 gspread 연결

get_all_records()로 시트 데이터 조회

DB와 비교 후 신규/업데이트 회원 insert

처리 결과 요약 반환 (예: {new_members: 5, updated_members: 2})

POST /slack/events

설명: Slack Events API 웹훅 수신 및 처리

권한: Public (Slack 호출)

구현 로직:

slack_bolt의 SlackRequestHandler를 FastAPI 라우터에 연결

@app.event("reaction_added") 리스너에서 event.item.ts, event.user 추출

slack_message_ts로 행사 조회, slack_user_id로 회원 조회

event_participations에 insert (reaction_added) 또는 delete (reaction_removed)

4.4. 대시보드 (Dashboard) - /dashboard

GET /kpis

설명: 대시보드에 필요한 KPI 일괄 조회

권한: Executive, Admin

구현 로직:

권한 검사

events + event_participations 조인 후 날짜별 참여율 추이 집계

profiles 그룹화로 회원 분포 집계

Supabase에서 최소 쿼리로 데이터 조회 및 가공

정의된 JSON 구조로 조합 후 반환

