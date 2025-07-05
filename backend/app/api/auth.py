from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..core.database import get_supabase
from supabase import Client
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    name: str
    department: str
    student_id: str
    gender: str
    phone_number: str
    slack_user_id: str
    email: str
    password: str

@router.post("/signup")
async def create_user(user_data: UserCreate, supabase: Client = Depends(get_supabase)):
    try:
        # 1. Supabase Auth에 사용자 생성
        auth_response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })
        
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Failed to create auth user")
        
        user_id = auth_response.user.id
        
        # 2. profiles 테이블에 사용자 정보 저장
        profile_data = {
            "id": user_id,  # Auth에서 생성된 ID 사용
            "name": user_data.name,
            "department": user_data.department,
            "student_id": user_data.student_id,
            "gender": user_data.gender,
            "phone_number": user_data.phone_number,
            "slack_user_id": user_data.slack_user_id
        }
        
        profile_response = supabase.table("profiles").insert(profile_data).execute()
        
        return {
            "message": "User created successfully",
            "user_id": user_id,
            "profile": profile_response.data[0] if profile_response.data else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signup-batch")
async def create_users_batch(supabase: Client = Depends(get_supabase)):
    """더미 데이터용 배치 사용자 생성"""
    dummy_users = [
        {
            "name": "김영희",
            "email": "younghee.kim@igrus.com",
            "password": "Password123!",
            "department": "컴퓨터공학과",
            "student_id": "20240001",
            "gender": "여성",
            "phone_number": "010-1234-5678",
            "slack_user_id": "SLACK001"
        },
        {
            "name": "이철수",
            "email": "chulsoo.lee@igrus.com",
            "password": "Password123!",
            "department": "소프트웨어학과",
            "student_id": "20240002",
            "gender": "남성",
            "phone_number": "010-2345-6789",
            "slack_user_id": "SLACK002"
        },
        {
            "name": "박지민",
            "email": "jimin.park@igrus.com",
            "password": "Password123!",
            "department": "정보통신공학과",
            "student_id": "20240003",
            "gender": "여성",
            "phone_number": "010-3456-7890",
            "slack_user_id": "SLACK003"
        },
        {
            "name": "최민준",
            "email": "minjun.choi@igrus.com",
            "password": "Password123!",
            "department": "컴퓨터공학과",
            "student_id": "20240004",
            "gender": "남성",
            "phone_number": "010-4567-8901",
            "slack_user_id": "SLACK004"
        },
        {
            "name": "정다은",
            "email": "daeun.jung@igrus.com",
            "password": "Password123!",
            "department": "인공지능학과",
            "student_id": "20240005",
            "gender": "여성",
            "phone_number": "010-5678-9012",
            "slack_user_id": "SLACK005"
        },
        {
            "name": "강현우",
            "email": "hyunwoo.kang@igrus.com",
            "password": "Password123!",
            "department": "소프트웨어학과",
            "student_id": "20240006",
            "gender": "남성",
            "phone_number": "010-6789-0123",
            "slack_user_id": "SLACK006"
        },
        {
            "name": "송지원",
            "email": "jiwon.song@igrus.com",
            "password": "Password123!",
            "department": "컴퓨터공학과",
            "student_id": "20240007",
            "gender": "여성",
            "phone_number": "010-7890-1234",
            "slack_user_id": "SLACK007"
        },
        {
            "name": "임준호",
            "email": "junho.lim@igrus.com",
            "password": "Password123!",
            "department": "정보통신공학과",
            "student_id": "20240008",
            "gender": "남성",
            "phone_number": "010-8901-2345",
            "slack_user_id": "SLACK008"
        },
        {
            "name": "한소희",
            "email": "sohee.han@igrus.com",
            "password": "Password123!",
            "department": "인공지능학과",
            "student_id": "20240009",
            "gender": "여성",
            "phone_number": "010-9012-3456",
            "slack_user_id": "SLACK009"
        },
        {
            "name": "오민석",
            "email": "minseok.oh@igrus.com",
            "password": "Password123!",
            "department": "소프트웨어학과",
            "student_id": "20240010",
            "gender": "남성",
            "phone_number": "010-0123-4567",
            "slack_user_id": "SLACK010"
        }
    ]
    
    created_users = []
    for user_data in dummy_users:
        try:
            # 1. Supabase Auth에 사용자 생성
            auth_response = supabase.auth.sign_up({
                "email": user_data["email"],
                "password": user_data["password"]
            })
            
            if not auth_response.user:
                continue
                
            user_id = auth_response.user.id
            
            # 2. profiles 테이블에 사용자 정보 저장
            profile_data = {
                "id": user_id,
                "name": user_data["name"],
                "department": user_data["department"],
                "student_id": user_data["student_id"],
                "gender": user_data["gender"],
                "phone_number": user_data["phone_number"],
                "slack_user_id": user_data["slack_user_id"]
            }
            
            profile_response = supabase.table("profiles").insert(profile_data).execute()
            
            created_users.append({
                "email": user_data["email"],
                "user_id": user_id,
                "profile": profile_response.data[0] if profile_response.data else None
            })
            
        except Exception as e:
            print(f"Error creating user {user_data['email']}: {str(e)}")
            continue
    
    return {
        "message": f"Created {len(created_users)} users",
        "created_users": created_users
    } 