from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from typing import Optional
from app.db import get_db
from app.auth import get_api_key
from app.services.market_service import (
    process_csv_import, recompute_all, get_leaderboard_data,
    get_ticker_detail, get_ticker_history, get_ticker_alerts
)

router = APIRouter(prefix="/api/v1", dependencies=[Depends(get_api_key)])

@router.post("/import/csv")
async def import_csv_data(file: UploadFile = File(...), db = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")
        
    content = await file.read()
    try:
        res = process_csv_import(content, db)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

@router.post("/recompute")
def recompute_indicators(ticker: str = 'ALL', db = Depends(get_db)):
    symbols = [ticker.upper()] if ticker.upper() != 'ALL' else ['ALL']
    try:
        res = recompute_all(symbols, db)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leaderboard")
def get_leaderboard(limit: int = 20, trend: Optional[str] = None, min_score: Optional[float] = None, db = Depends(get_db)):
    if trend and trend not in ['UP', 'DOWN', 'SIDEWAYS', 'ALL']:
        raise HTTPException(status_code=400, detail="Invalid trend state")
    return {"data": get_leaderboard_data(limit, trend, min_score, db)}

@router.get("/tickers/{symbol}/latest")
def get_latest_ticker(symbol: str, db = Depends(get_db)):
    detail = get_ticker_detail(symbol, db)
    if not detail or not detail.get('date'):
        raise HTTPException(status_code=404, detail="Ticker not found or no data")
    return {"data": detail}

@router.get("/tickers/{symbol}/history")
def get_history(symbol: str, days: int = 180, db = Depends(get_db)):
    hist = get_ticker_history(symbol, days, db)
    return {"data": hist}

@router.get("/tickers/{symbol}/alerts")
def get_alerts(symbol: str, db = Depends(get_db)):
    alerts = get_ticker_alerts(symbol, db)
    return {"data": alerts}
