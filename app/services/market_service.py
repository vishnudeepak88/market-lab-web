import pandas as pd
from typing import List, Optional
from datetime import datetime, date
import io
import math

from app.repositories import get_repository
from app.indicators import compute_indicators
from app.scoring import compute_scores, generate_alerts
from app.models import Ticker, OHLCVDaily, IndicatorsDaily

def process_csv_import(csv_content: bytes, db_session) -> dict:
    repo = get_repository(db_session)
    df = pd.read_csv(io.BytesIO(csv_content))
    
    # Expected columns: date, open, high, low, close, volume, ticker
    required_cols = {"date", "open", "high", "low", "close", "volume", "ticker"}
    if not required_cols.issubset(set(df.columns.str.lower())):
        missing = required_cols - set(df.columns.str.lower())
        raise ValueError(f"Missing required columns: {missing}")
        
    df.columns = df.columns.str.lower()
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    symbols = df['ticker'].unique()
    inserted = 0
    
    for symbol in symbols:
        ticker = repo.upsert_ticker(symbol)
        ticker_df = df[df['ticker'] == symbol]
        
        records = []
        for _, row in ticker_df.iterrows():
            records.append({
                "ticker_id": ticker.id,
                "date": row['date'],
                "open": float(row['open']),
                "high": float(row['high']),
                "low": float(row['low']),
                "close": float(row['close']),
                "volume": float(row['volume'])
            })
        
        count = repo.bulk_save_ohlcv(records)
        inserted += count
        
        # After inserting data, trigger indicator computation for this ticker
        _recompute_ticker(ticker.id, repo)
        
    repo.log_job("import_csv", "SUCCESS", f"Imported {inserted} OHLCV rows for {len(symbols)} tickers.")
    return {"status": "success", "inserted": inserted, "tickers": len(symbols)}

def recompute_all(symbols: list, db_session) -> dict:
    repo = get_repository(db_session)
    if 'ALL' in symbols:
        tickers = repo.get_tickers()
    else:
        tickers = [repo.get_ticker_by_symbol(sym) for sym in symbols]
        tickers = [t for t in tickers if t is not None]
        
    for t in tickers:
        try:
            _recompute_ticker(t.id, repo)
        except Exception as e:
            repo.log_job("recompute", "FAILED", f"Error on {t.symbol}: {str(e)}")
            
    return {"status": "success", "recomputed_tickers": len(tickers)}

def _recompute_ticker(ticker_id: int, repo):
    history = repo.get_ohlcv_history(ticker_id, 500) # Get enough history for 200 SMA
    if not history:
        return
        
    data = []
    for h in history:
        data.append({
            "date": h.date,
            "open": h.open,
            "high": h.high,
            "low": h.low,
            "close": h.close,
            "volume": h.volume
        })
        
    df = pd.DataFrame(data)
    
    # Indicators
    df_ind = compute_indicators(df)
    # Scoring
    df_scores = compute_scores(df_ind)
    
    records = []
    for _, row in df_scores.iterrows():
        # Clean NaNs to None for DB
        r_dict = row.to_dict()
        clean_r = {k: (None if pd.isna(v) else v) for k, v in r_dict.items()}
        
        # Select columns that exist in IndicatorsDaily model
        db_record = {
            "ticker_id": ticker_id,
            "date": clean_r['date'],
            "ret_1d": clean_r.get('ret_1d'),
            "ret_5d": clean_r.get('ret_5d'),
            "ret_20d": clean_r.get('ret_20d'),
            "sma_20": clean_r.get('sma_20'),
            "sma_50": clean_r.get('sma_50'),
            "sma_200": clean_r.get('sma_200'),
            "rsi_14": clean_r.get('rsi_14'),
            "vol_20d": clean_r.get('vol_20d'),
            "vol_z_20d": clean_r.get('vol_z_20d'),
            "trend_state": clean_r.get('trend_state'),
            "momentum_score": clean_r.get('momentum_score'),
            "risk_score": clean_r.get('risk_score'),
            "final_score": clean_r.get('final_score')
        }
        records.append(db_record)
        
    repo.bulk_save_indicators(records)

def get_ticker_detail(symbol: str, db_session) -> dict:
    repo = get_repository(db_session)
    ticker = repo.get_ticker_by_symbol(symbol.upper())
    if not ticker: return None
    
    latest_ohlcv = repo.get_latest_ohlcv(ticker.id)
    latest_ind = repo.get_latest_indicators(ticker.id)
    
    if not latest_ohlcv or not latest_ind:
        return {"symbol": ticker.symbol, "name": ticker.name, "data": None}
        
    # generate alerts on the fly or pull from DB if we persisted them
    # For now, let's create a Series-like object from ind and ohlcv
    row_data = {
        'vol_20d': latest_ind.vol_20d,
        'rsi_14': latest_ind.rsi_14,
        # For drawdown, we didn't save it to DB directly, 
        # but we can fetch it by recomputing generating alert
        # we'll approximate for now or we could save drawdown to DB
    }
    alerts = generate_alerts(pd.Series(row_data))
    
    return {
        "symbol": ticker.symbol,
        "name": ticker.name,
        "date": latest_ohlcv.date.isoformat() if hasattr(latest_ohlcv.date, 'isoformat') else str(latest_ohlcv.date),
        "open": latest_ohlcv.open, "high": latest_ohlcv.high, 
        "low": latest_ohlcv.low, "close": latest_ohlcv.close, 
        "volume": latest_ohlcv.volume,
        "rsi_14": latest_ind.rsi_14,
        "sma_20": latest_ind.sma_20,
        "sma_50": latest_ind.sma_50,
        "sma_200": latest_ind.sma_200,
        "trend_state": latest_ind.trend_state,
        "final_score": latest_ind.final_score,
        "alerts": alerts
    }

def get_leaderboard_data(limit: int, trend: str, min_score: float, db_session):
    repo = get_repository(db_session)
    results = repo.get_leaderboard(limit=limit, trend=trend, min_score=min_score)
    
    out = []
    # results is list of tuples (IndicatorsDaily, Ticker) if DB Repo
    # mock repo returns tuples too
    for ind, ticker in results:
        # Generate alerts
        # Just as a mock if real data
        alerts = generate_alerts(pd.Series({'vol_20d': ind.vol_20d, 'rsi_14': ind.rsi_14}))
        
        out.append({
            "ticker": ticker.symbol,
            "name": ticker.name,
            "final_score": round(ind.final_score, 2) if ind.final_score else 0,
            "trend_state": ind.trend_state,
            "ret_20d": round(ind.ret_20d, 4) if ind.ret_20d else 0,
            "rsi_14": round(ind.rsi_14, 2) if ind.rsi_14 else 0,
            "vol_20d": round(ind.vol_20d, 4) if ind.vol_20d else 0,
            "alerts": alerts
        })
    return out

def get_ticker_history(symbol: str, days: int, db_session) -> list:
    repo = get_repository(db_session)
    ticker = repo.get_ticker_by_symbol(symbol.upper())
    if not ticker: return []
    
    records = repo.get_ohlcv_history(ticker.id, days)
    return [{
        "date": r.date.isoformat() if hasattr(r.date, 'isoformat') else str(r.date),
        "open": r.open, "high": r.high, "low": r.low, "close": r.close, "volume": r.volume
    } for r in records]

def get_ticker_alerts(symbol: str, db_session) -> list:
    repo = get_repository(db_session)
    ticker = repo.get_ticker_by_symbol(symbol.upper())
    if not ticker: return []
    
    ind = repo.get_latest_indicators(ticker.id)
    if not ind: return []
    return generate_alerts(pd.Series({'vol_20d': ind.vol_20d, 'rsi_14': ind.rsi_14}))
