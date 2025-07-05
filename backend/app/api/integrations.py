from fastapi import APIRouter, Depends, HTTPException, Request
from ..services.google_sheets import google_sheets_service
from ..services.slack import get_slack_handler
from typing import Dict

router = APIRouter(prefix="/integrations", tags=["integrations"])

@router.post("/google/sync-members", response_model=Dict[str, int])
async def sync_members(sheet_name: str):
    """
    Google Sheets에서 회원 정보를 동기화합니다.
    """
    try:
        result = await google_sheets_service.sync_members(sheet_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/slack/events")
async def slack_events(request: Request):
    """
    Slack 이벤트를 처리합니다.
    """
    try:
        handler = await get_slack_handler()
        return await handler.handle(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 