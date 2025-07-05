from fastapi import FastAPI
from app.api import users, auth, google_sheets
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ClubOS API")

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 origin을 지정해야 합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(google_sheets.router)

@app.get("/")
async def root():
    return {"message": "Welcome to ClubOS API"} 