from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import users, google_sheets, auth, transactions

app = FastAPI(
    title="ClubOS API",
    description="ClubOS Backend API built with FastAPI",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 origin으로 변경해야 함
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(google_sheets.router)
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Welcome to ClubOS API"} 