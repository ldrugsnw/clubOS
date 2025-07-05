from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from ..core.database import get_supabase
from ..models.profile import Profile, ProfileCreate, ProfileUpdate
from supabase import Client
from datetime import datetime

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=Profile)
async def read_user_me(supabase: Client = Depends(get_supabase)):
    try:
        # 현재 로그인된 사용자 정보 조회
        user = supabase.auth.get_user()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # profiles 테이블에서 상세 정보 조회
        profile = supabase.table("profiles").select("*").eq("id", user.user.id).single().execute()
        return profile.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Profile])
async def read_users(
    name: Optional[str] = None,
    department: Optional[str] = None,
    supabase: Client = Depends(get_supabase)
):
    try:
        query = supabase.table("profiles").select("*")
        
        if name:
            query = query.ilike("name", f"%{name}%")
        if department:
            query = query.eq("department", department)
            
        result = query.execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/me", response_model=Profile)
async def update_user_me(
    profile_update: ProfileUpdate,
    supabase: Client = Depends(get_supabase)
):
    try:
        # 현재 로그인된 사용자 정보 조회
        user = supabase.auth.get_user()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 업데이트할 데이터 준비
        update_data = profile_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()

        # profiles 테이블 업데이트
        result = supabase.table("profiles").update(update_data).eq("id", user.user.id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Profile not found")

        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 