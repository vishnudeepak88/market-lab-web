from datetime import datetime, timedelta
import random

# Sample in-memory data for Demo Mode
MOCK_TICKERS = [
    {"symbol": "AAPL", "name": "Apple Inc."},
    {"symbol": "GOOGL", "name": "Alphabet Inc."},
    {"symbol": "MSFT", "name": "Microsoft Corp."},
]

def generate_mock_ohlcv(symbol: str):
    now = datetime.utcnow()
    base_price = sum(ord(c) for c in symbol)  # deterministic-ish baseline
    open_p = base_price + random.uniform(-2, 2)
    close_p = open_p + random.uniform(-2, 2)
    return {
        "symbol": symbol,
        "timestamp": now.isoformat(),
        "open": round(open_p, 2),
        "high": round(max(open_p, close_p) + random.uniform(0, 1), 2),
        "low": round(min(open_p, close_p) - random.uniform(0, 1), 2),
        "close": round(close_p, 2),
        "volume": int(random.uniform(1000, 100000))
    }

def get_tickers(db=None):
    if db:
        from app.models import Ticker
        return db.query(Ticker).all()
    else:
        return MOCK_TICKERS

def get_latest_ohlcv(symbol: str, db=None):
    if db:
        from app.models import Ticker, OHLCV
        ticker = db.query(Ticker).filter(Ticker.symbol == symbol.upper()).first()
        if not ticker:
            return None
        row = db.query(OHLCV).filter(OHLCV.ticker_id == ticker.id).order_by(OHLCV.timestamp.desc()).first()
        if not row:
            return None
        return {
            "symbol": ticker.symbol,
            "timestamp": row.timestamp.isoformat(),
            "open": row.open,
            "high": row.high,
            "low": row.low,
            "close": row.close,
            "volume": row.volume
        }
    else:
        if any(t["symbol"] == symbol.upper() for t in MOCK_TICKERS):
            return generate_mock_ohlcv(symbol.upper())
        return None
