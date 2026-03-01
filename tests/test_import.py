import pytest
import pandas as pd
import io
from app.services.market_service import process_csv_import

class DummyMockRepo:
    def __init__(self):
        self.tickers = []
        self.ohlcvs = []
        self.logs = []
        
    def upsert_ticker(self, symbol):
        class Ticker:
            def __init__(self, id, symbol):
                self.id = id
                self.symbol = symbol
        t = Ticker(1, symbol)
        return t
        
    def bulk_save_ohlcv(self, records):
        self.ohlcvs.extend(records)
        return len(records)
        
    def get_ohlcv_history(self, ticker_id, limit):
        return []
        
    def log_job(self, name, status, msg):
        self.logs.append((name, status))

    def bulk_save_indicators(self, records):
        pass

# We monkeypatch the get_repository factory in tests
def test_import_upsert(monkeypatch):
    import app.services.market_service as ms
    dummy = DummyMockRepo()
    monkeypatch.setattr(ms, "get_repository", lambda session: dummy)
    
    csv_data = """date,open,high,low,close,volume,ticker
2026-01-01,100,105,95,102,10000,TEST1
2026-01-02,102,108,100,107,15000,TEST1
2026-01-01,50,55,45,52,5000,TEST2
"""
    res = process_csv_import(csv_data.encode('utf-8'), None)
    
    assert res['status'] == 'success'
    assert res['tickers'] == 2
    assert res['inserted'] == 3
    assert len(dummy.ohlcvs) == 3
    assert len(dummy.logs) == 1
