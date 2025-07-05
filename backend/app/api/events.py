from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..core.database import get_supabase
from ..models.event import Event, EventCreate, EventWithParticipants
from supabase import Client
import uuid

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=Event)
async def create_event(
    event: EventCreate,
    supabase: Client = Depends(get_supabase)
):
    try:
        # 현재 로그인된 사용자 ID 가져오기
        user = supabase.auth.get_user()
        if not user:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        # 이벤트 생성
        event_data = event.dict()
        event_data["created_by"] = user.id
        
        result = supabase.table("events").insert(event_data).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{event_id}", response_model=EventWithParticipants)
async def read_event(
    event_id: uuid.UUID,
    supabase: Client = Depends(get_supabase)
):
    try:
        # 이벤트 정보 조회
        event = supabase.table("events").select("*").eq("id", str(event_id)).single().execute()
        if not event.data:
            raise HTTPException(status_code=404, detail="Event not found")
            
        # 참가자 정보 조회
        participants = supabase.table("event_participations")\
            .select("profiles(*)")\
            .eq("event_id", str(event_id))\
            .execute()
            
        # 결과 조합
        event_with_participants = event.data
        event_with_participants["participants"] = [p["profiles"] for p in participants.data]
        
        return event_with_participants
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 