from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import logging

# 로거 설정
logger = logging.getLogger(__name__)

# .env_local 파일 로드
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env_local')
load_dotenv(env_path)

logger.debug(f"Loading environment variables from: {env_path}")
logger.debug(f"GOOGLE_CREDENTIALS_PATH: {os.getenv('GOOGLE_CREDENTIALS_PATH')}")

class Settings(BaseModel):
    # Supabase 설정
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # JWT 설정
    JWT_SECRET_KEY: str = "your-secret-key"  # 실제 운영 환경에서는 안전한 키로 변경
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google Sheets 설정
    GOOGLE_CREDENTIALS_PATH: str = os.getenv("GOOGLE_CREDENTIALS_PATH", "")
    
    # Slack 설정
    SLACK_BOT_TOKEN: Optional[str] = None
    SLACK_SIGNING_SECRET: Optional[str] = None
    
    class Config:
        case_sensitive = True

settings = Settings() 