from supabase import create_client
from .config import settings

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def get_supabase():
    try:
        yield supabase
    finally:
        # Supabase 클라이언트는 자동으로 연결을 관리하므로 
        # 별도의 cleanup이 필요하지 않습니다.
        pass 