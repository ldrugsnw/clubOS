from fastapi import APIRouter, HTTPException
from ..services.google_sheets import google_sheets_service

router = APIRouter(prefix="/google-sheets", tags=["google-sheets"])

@router.get("/test")
async def test_google_sheets_connection():
    """
    Google Sheets API 연결을 테스트합니다.
    """
    is_connected = await google_sheets_service.test_connection()
    if not is_connected:
        raise HTTPException(status_code=500, detail="Google Sheets connection failed")
    return {"status": "success", "message": "Successfully connected to Google Sheets API"}

@router.get("/spreadsheet/{spreadsheet_id}")
async def get_spreadsheet_info(spreadsheet_id: str):
    """
    특정 스프레드시트의 정보를 가져옵니다.
    
    Args:
        spreadsheet_id: 스프레드시트 ID 또는 URL
    """
    try:
        info = await google_sheets_service.get_spreadsheet_info(spreadsheet_id)
        return {"status": "success", "data": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 