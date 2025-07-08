import gspread
from google.oauth2.service_account import Credentials
from ..core.config import settings
from typing import List, Dict, Any
import logging

# 로거 설정
logger = logging.getLogger(__name__)

# 열 이름 매핑
COLUMN_MAPPING = {
    "타임스탬프": "timestamp",
    "IGRUS의 활동에 참여하기 위해선 회비 2만원을 납부해주셔야 합니다. 회비 납부를 완료했습니까? ": "agreement",
    "이름(ex.김아그)": "name",
    "성별": "gender",
    "학번 8자리(ex.12250000)(학번이 나오지 않은 신입생이라면 25학번이라고 적으신 후에 연락주시면 감사하겠습니다!)": "student_id",
    "학년": "grade",
    "학과": "department",
    "재학/휴학 여부": "enrollment_status",
    "연락처(ex.010-1234-5678)": "phone",
    "관심 분야를 모두 체크해주세요.": "interests",
    "IGRUS에 가입하게 된 경로가 어떻게 되나요?": "join_path",
    "IGRUS에 들어오신 목적/이유가 무엇인가요?": "join_purpose",
    "IGRUS에서 원하는 활동이 있다면 알려주세요!": "desired_activities",
    "회비 납부": "payment_status",
    "카톡초대": "kakao_invite"
}

class GoogleSheetsService:
    def __init__(self):
        self._client = None
        self._creds = None
        
    @property
    def client(self):
        if not self._client:
            try:
                logger.debug(f"Attempting to initialize Google Sheets client with credentials from: {settings.GOOGLE_CREDENTIALS_PATH}")
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                if settings.GOOGLE_CREDENTIALS_PATH:
                    self._creds = Credentials.from_service_account_file(
                        settings.GOOGLE_CREDENTIALS_PATH, scopes=scopes
                    )
                    self._client = gspread.authorize(self._creds)
                    logger.debug("Successfully initialized Google Sheets client")
                else:
                    logger.error("GOOGLE_CREDENTIALS_PATH is not set")
            except Exception as e:
                logger.error(f"Failed to initialize Google Sheets client: {str(e)}")
                raise
        return self._client

    async def get_spreadsheet_info(self, spreadsheet_id: str) -> Dict[str, Any]:
        """
        스프레드시트의 기본 정보와 데이터를 가져옵니다.
        """
        try:
            logger.debug(f"Attempting to open spreadsheet: {spreadsheet_id}")
            
            if not self.client:
                raise ValueError("Google Sheets client is not initialized")
            
            # URL이 주어진 경우 ID 추출
            if "spreadsheets/d/" in spreadsheet_id:
                spreadsheet_id = spreadsheet_id.split("spreadsheets/d/")[1].split("/")[0]
            
            # 스프레드시트 열기
            spreadsheet = self.client.open_by_key(spreadsheet_id)
            worksheet = spreadsheet.sheet1  # 첫 번째 시트 사용
            
            # 데이터 가져오기
            records = worksheet.get_all_records()
            
            # 열 이름 매핑 적용
            mapped_records = []
            for record in records:
                mapped_record = {}
                for old_key, value in record.items():
                    if old_key.startswith("학번 8자리"):
                        new_key = "student_id"
                    elif old_key == "연락처(ex.010-1234-5678)": # 전화번호 컬럼 처리
                        new_key = "phone"
                        processed_phone = str(value).replace('-', '').replace(' ', '') # 하이픈과 공백 제거
                        if len(processed_phone) == 10 and processed_phone.startswith('10'):
                            # 10자리 숫자이고 '10'으로 시작하면, 앞에 '0'이 빠졌다고 가정하고 추가
                            value = '0' + processed_phone
                        else:
                            value = processed_phone # 정리된 값 사용
                    else:
                        new_key = COLUMN_MAPPING.get(old_key, old_key)
                    mapped_record[new_key] = value
                mapped_records.append(mapped_record)
            
            # 기본 정보 수집
            info = {
                "title": spreadsheet.title,
                "sheet_names": [sheet.title for sheet in spreadsheet.worksheets()],
                "url": f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}",
                "total_sheets": len(spreadsheet.worksheets()),
                "total_rows": len(mapped_records),
                "columns": list(COLUMN_MAPPING.values()),
                "data": mapped_records  # 모든 행 반환
            }
            
            logger.debug(f"Successfully retrieved spreadsheet info: {info}")
            return info
            
        except Exception as e:
            logger.error(f"Failed to get spreadsheet info: {str(e)}")
            raise Exception(f"Failed to get spreadsheet info: {str(e)}")

    async def sync_members(self, sheet_name: str) -> Dict[str, int]:
        """
        Google Sheets에서 회원 정보를 동기화합니다.
        """
        if not self.client:
            raise ValueError("Google Sheets credentials not configured")

        try:
            # 시트 열기
            sheet = self.client.open(sheet_name).sheet1
            records = sheet.get_all_records()

            # 결과 통계
            stats = {
                "new_members": 0,
                "updated_members": 0
            }

            # TODO: Supabase와 동기화 로직 구현
            # 이 부분은 실제 데이터 구조에 맞춰 구현해야 합니다.

            return stats

        except Exception as e:
            logger.error(f"Failed to sync members: {str(e)}")
            raise Exception(f"Failed to sync members: {str(e)}")

    async def test_connection(self) -> bool:
        """
        Google Sheets API 연결을 테스트합니다.
        """
        try:
            logger.debug("Starting Google Sheets connection test")
            if not self.client:
                logger.error("Google Sheets client is not initialized")
                return False
                
            # 사용 가능한 스프레드시트 목록을 가져와봅니다
            spreadsheets = self.client.list_spreadsheet_files()
            logger.debug(f"Successfully retrieved {len(spreadsheets)} spreadsheets")
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

    async def get_multiple_spreadsheets_info(self, spreadsheet_ids: List[str]) -> List[Dict[str, Any]]:
        """
        여러 스프레드시트의 데이터를 가져옵니다.
        """
        all_mapped_records = []
        for spreadsheet_id in spreadsheet_ids:
            try:
                logger.debug(f"Attempting to open spreadsheet: {spreadsheet_id}")
                
                if not self.client:
                    raise ValueError("Google Sheets client is not initialized")
                
                # URL이 주어진 경우 ID 추출
                if "spreadsheets/d/" in spreadsheet_id:
                    spreadsheet_id = spreadsheet_id.split("spreadsheets/d/")[1].split("/")[0]
                
                # 스프레드시트 열기
                spreadsheet = self.client.open_by_key(spreadsheet_id)
                worksheet = spreadsheet.sheet1  # 첫 번째 시트 사용
                
                # 데이터 가져오기
                records = worksheet.get_all_records()
                
                # 열 이름 매핑 적용
                mapped_records = []
                for record in records:
                    mapped_record = {}
                    for old_key, value in record.items():
                        if old_key.startswith("학번 8자리"):
                            new_key = "student_id"
                        elif old_key == "연락처(ex.010-1234-5678)": # 전화번호 컬럼 처리
                            new_key = "phone"
                            processed_phone = str(value).replace('-', '').replace(' ', '') # 하이픈과 공백 제거
                            if len(processed_phone) == 10 and processed_phone.startswith('10'):
                                # 10자리 숫자이고 '10'으로 시작하면, 앞에 '0'이 빠졌다고 가정하고 추가
                                value = '0' + processed_phone
                            else:
                                value = processed_phone # 정리된 값 사용
                        else:
                            new_key = COLUMN_MAPPING.get(old_key, old_key)
                        mapped_record[new_key] = value
                    mapped_records.append(mapped_record)
                
                all_mapped_records.extend(mapped_records)
                logger.debug(f"Successfully retrieved data from spreadsheet: {spreadsheet_id}")
                
            except Exception as e:
                logger.error(f"Failed to get spreadsheet info for {spreadsheet_id}: {str(e)}")
                # 특정 스프레드시트에서 오류가 발생해도 다른 스프레드시트 처리는 계속 진행
                continue
        
        return all_mapped_records

google_sheets_service = GoogleSheetsService()
 