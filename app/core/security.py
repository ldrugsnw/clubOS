from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from ..core.database import get_supabase
import logging

# 로거 설정
logger = logging.getLogger(__name__)

# HTTPBearer는 "Authorization: Bearer <token>" 헤더를 찾습니다.
# 이것이 더 간단하고 명확한 "Authorize" UI를 생성합니다.
security = HTTPBearer()

async def get_current_user(
    authorization: HTTPAuthorizationCredentials = Depends(security), 
    supabase: Client = Depends(get_supabase)
):
    """
    요청 헤더에서 JWT 토큰을 가져와 유효성을 검사하고,
    유효하다면 해당 사용자 정보를 반환하는 의존성 함수입니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = authorization.credentials
        # Supabase에 토큰이 유효한지 물어봅니다.
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        
        if user is None:
            logger.warning("Invalid token or user not found.")
            raise credentials_exception
        
        logger.info(f"Successfully authenticated user: {user.id}")
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise credentials_exception
