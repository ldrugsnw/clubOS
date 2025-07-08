from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from datetime import datetime, date
import pandas as pd
import io
from pydantic import BaseModel

from ..core.database import supabase
from ..models.transaction import Transaction, TransactionCreate, TransactionStats

router = APIRouter()

# 테스트 엔드포인트
@router.get("/test")
async def test_connection():
    """DB 연결 및 기본 기능 테스트"""
    try:
        # Supabase 연결 테스트
        result = supabase.table('transactions').select('count', count='exact').execute()
        return {
            "status": "success",
            "message": "Supabase 연결 성공",
            "transaction_count": result.count
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"연결 실패: {str(e)}"
        }

class TransactionResponse(BaseModel):
    id: str
    transaction_date: datetime
    description: str
    transaction_type: Optional[str]
    institution: Optional[str]
    account_number: Optional[str]
    amount: int
    balance: int
    memo: Optional[str]
    file_name: Optional[str]
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime

class TransactionStatsResponse(BaseModel):
    total_balance: int
    this_term_income: int
    this_term_expense: int
    this_term_profit: int
    previous_balance: int
    total_transactions: int
    latest_transaction_date: Optional[datetime]

@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    limit: int = 100,
    offset: int = 0,
    search: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """거래 내역 조회"""
    try:
        query = supabase.table('transactions').select('*')
        
        # 검색 조건 추가
        if search:
            query = query.or_(f"description.ilike.%{search}%,memo.ilike.%{search}%,transaction_type.ilike.%{search}%")
        
        # 날짜 범위 조건 추가
        if start_date:
            query = query.gte('transaction_date', start_date.isoformat())
        
        if end_date:
            query = query.lte('transaction_date', end_date.isoformat())
        
        # 정렬 및 페이지네이션
        result = query.order('transaction_date', desc=True).range(offset, offset + limit - 1).execute()
        
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 조회 실패: {str(e)}")

@router.get("/stats", response_model=TransactionStatsResponse)
async def get_transaction_stats(
    term_start: Optional[date] = None
):
    """거래 통계 조회"""
    try:
        # 기본값: 이번 학기 시작 (3월 1일)
        if not term_start:
            current_year = datetime.now().year
            term_start = date(current_year, 3, 1)
        
        # 최신 잔액 조회
        latest_result = supabase.table('transactions').select('balance').order('transaction_date', desc=True).order('created_at', desc=True).limit(1).execute()
        total_balance = latest_result.data[0]['balance'] if latest_result.data else 0
        
        # 모든 거래 내역 조회 (통계 계산용)
        all_transactions = supabase.table('transactions').select('*').execute()
        
        # 전체 거래 수
        total_transactions = len(all_transactions.data)
        
        # 이번 학기 거래 필터링
        term_transactions = [
            t for t in all_transactions.data 
            if datetime.fromisoformat(t['transaction_date'].replace('Z', '+00:00')).date() >= term_start
        ]
        
        # 수입과 지출 계산
        this_term_income = sum(t['amount'] for t in term_transactions if t['amount'] > 0)
        this_term_expense = sum(abs(t['amount']) for t in term_transactions if t['amount'] < 0)
        this_term_profit = this_term_income - this_term_expense
        previous_balance = total_balance - this_term_profit
        
        # 최신 거래 날짜
        latest_date = max([datetime.fromisoformat(t['transaction_date'].replace('Z', '+00:00')) for t in term_transactions]) if term_transactions else None
        
        return TransactionStatsResponse(
            total_balance=total_balance,
            this_term_income=this_term_income,
            this_term_expense=this_term_expense,
            this_term_profit=this_term_profit,
            previous_balance=previous_balance,
            total_transactions=total_transactions,
            latest_transaction_date=latest_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")

@router.post("/upload", response_model=dict)
async def upload_transactions(
    file: UploadFile = File(...)
):
    """엑셀 파일에서 거래 내역 업로드"""
    try:
        print(f"파일 업로드 시작: {file.filename}")
        
        if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
            raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")
        
        # 파일 읽기
        contents = await file.read()
        print(f"파일 크기: {len(contents)} bytes")
        
        # 간단한 테스트를 위해 DB 연결 확인
        test_result = supabase.table('transactions').select('count', count='exact').execute()
        print(f"DB 연결 테스트 성공, 기존 레코드 수: {test_result.count}")
        
        # 파일 파싱
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
        
        print(f"DataFrame 생성 성공, 행 수: {len(df)}, 컬럼: {list(df.columns)}")
        
        # 일단 첫 번째 행만 테스트
        if len(df) > 0:
            first_row = df.iloc[0]
            print(f"첫 번째 행 데이터: {dict(first_row)}")
            
            # 간단한 테스트 레코드 삽입
            test_record = {
                'transaction_date': '2025-07-08T10:00:00',
                'description': '테스트 거래',
                'transaction_type': '테스트',
                'institution': '테스트 은행',
                'account_number': '123456789',
                'amount': 1000,
                'balance': 100000,
                'memo': '테스트 메모',
                'file_name': file.filename
            }
            
            result = supabase.table('transactions').insert(test_record).execute()
            print(f"테스트 레코드 삽입 성공: {result.data}")
            
            return {
                "status": "success",
                "message": "테스트 업로드 성공",
                "test_record": result.data[0] if result.data else None,
                "file_info": {
                    "name": file.filename,
                    "size": len(contents),
                    "rows": len(df),
                    "columns": list(df.columns)
                }
            }
        else:
            return {"status": "error", "message": "파일에 데이터가 없습니다."}
            
    except Exception as e:
        print(f"업로드 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"파일 처리 중 오류 발생: {str(e)}")

@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: str):
    """거래 내역 삭제"""
    try:
        result = supabase.table('transactions').delete().eq('id', transaction_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="거래 내역을 찾을 수 없습니다.")
        
        return {"message": "거래 내역이 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"삭제 실패: {str(e)}")

@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str, 
    transaction: TransactionCreate
):
    """거래 내역 수정"""
    try:
        update_data = {
            'description': transaction.description,
            'transaction_type': transaction.transaction_type,
            'institution': transaction.institution,
            'account_number': transaction.account_number,
            'amount': transaction.amount,
            'balance': transaction.balance,
            'memo': transaction.memo
        }
        
        result = supabase.table('transactions').update(update_data).eq('id', transaction_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="거래 내역을 찾을 수 없습니다.")
        
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"수정 실패: {str(e)}")