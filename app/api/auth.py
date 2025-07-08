from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from ..core.database import get_supabase
from supabase import Client
import logging

# 로거 설정
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

class SignUpRequest(BaseModel):
    username: str  # 이메일 대신 username 사용
    password: str
    name: str
    department: Optional[str] = None
    phone: Optional[str] = None

class SignInRequest(BaseModel):
    username: str  # 이메일 대신 username 사용
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/signup", response_model=AuthResponse)
def signup(request: SignUpRequest, supabase: Client = Depends(get_supabase)):
    try:
        logger.info(f"Attempting to sign up user with username: {request.username}")
        
        # 1. Supabase Auth로 사용자 생성
        # username을 이메일 형식으로 변환 (Supabase 요구사항)
        email = f"{request.username}@igrus.com"
        
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": request.password,
            "options": {
                "data": {
                    "username": request.username,
                    "name": request.name
                }
            }
        })

        if not auth_response.user:
            logger.error(f"Failed to create user: {auth_response}")
            raise HTTPException(status_code=400, detail="Failed to create user")

        # 2. 생성된 사용자로 바로 로그인
        login_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": request.password
        })

        if not login_response.session:
            logger.error(f"Failed to login after signup: {login_response}")
            raise HTTPException(status_code=400, detail="User created but failed to login")

        # 3. profiles 테이블에 추가 정보 저장
        profile_data = {
            "id": auth_response.user.id,
            "name": request.name,
            "department": request.department,
            "phone_number": request.phone
        }
        
        logger.info(f"Creating profile for user: {auth_response.user.id}")
        profile_response = supabase.table("profiles").insert(profile_data).execute()
        
        if not profile_response.data:
            # 프로필 생성 실패 시 사용자도 삭제
            logger.error(f"Failed to create profile: {profile_response}")
            supabase.auth.admin.delete_user(auth_response.user.id)
            raise HTTPException(status_code=400, detail="Failed to create profile")

        # 4. 로그인 세션의 액세스 토큰 반환
        return {
            "access_token": login_response.session.access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signin", response_model=AuthResponse)
def signin(request: SignInRequest, supabase: Client = Depends(get_supabase)):
    try:
        # username을 이메일 형식으로 변환
        email = f"{request.username}@igrus.com"
        
        # Supabase Auth로 로그인
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": request.password
        })

        if not response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "access_token": response.session.access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signout")
def signout(supabase: Client = Depends(get_supabase)):
    try:
        supabase.auth.sign_out()
        return {"message": "Successfully signed out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 