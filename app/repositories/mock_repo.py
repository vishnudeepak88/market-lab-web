from datetime import datetime, date, timedelta
import random

MOCK_TICKERS = [
    {"id": 1, "symbol": "AAPL", "name": "Apple Inc."},
    {"id": 2, "symbol": "GOOGL", "name": "Alphabet Inc."},
    {"id": 3, "symbol": "MSFT", "name": "Microsoft Corp."},
]

class MockDBTicker:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class MockDBOHLCV:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class MockDBIndicator:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if not hasattr(self, 'trend_state'):
            self.trend_state = random.choice(["UP", "DOWN", "SIDEWAYS"])
        if not hasattr(self, 'final_score'):
            self.final_score = random.uniform(40, 95)
        if not hasattr(self, 'rsi_14'):
            self.rsi_14 = random.uniform(20, 80)
        if not hasattr(self, 'vol_20d'):
            self.vol_20d = random.uniform(0.01, 0.05)
        if not hasattr(self, 'ret_20d'):
            self.ret_20d = random.uniform(-0.1, 0.1)

class MockRepository:
    def __init__(self):
        self.tickers = MOCK_TICKERS

    def get_tickers(self):
        return [MockDBTicker(**t) for t in self.tickers]
        
    def get_ticker_by_symbol(self, symbol: str):
        for t in self.tickers:
            if t['symbol'] == symbol.upper():
                return MockDBTicker(**t)
        return None

    def _generate_mock_ohlcv(self, ticker_id: int, d: date):
        base_price = 100 + ticker_id * 50
        open_p = base_price + random.uniform(-2, 2)
        close_p = open_p + random.uniform(-2, 2)
        return MockDBOHLCV(
            ticker_id=ticker_id,
            date=d,
            open=open_p,
            high=max(open_p, close_p) + random.uniform(0, 1),
            low=min(open_p, close_p) - random.uniform(0, 1),
            close=close_p,
            volume=int(random.uniform(1000, 100000))
        )

    def get_latest_ohlcv(self, ticker_id: int):
        return self._generate_mock_ohlcv(ticker_id, date.today())

    def get_ohlcv_history(self, ticker_id: int, days: int):
        history = []
        today = date.today()
        for i in range(days):
            d = today - timedelta(days=i)
            # Skip weekends
            if d.weekday() < 5:
                history.append(self._generate_mock_ohlcv(ticker_id, d))
        return history

    def get_latest_indicators(self, ticker_id: int):
        return MockDBIndicator(ticker_id=ticker_id, date=date.today())

    def upsert_ticker(self, symbol: str, name: str = None):
        t = self.get_ticker_by_symbol(symbol)
        if t: return t
        new_t = {"id": len(self.tickers) + 1, "symbol": symbol.upper(), "name": name}
        self.tickers.append(new_t)
        return MockDBTicker(**new_t)

    def bulk_save_ohlcv(self, records: list):
        return len(records)

    def bulk_save_indicators(self, records: list):
        return len(records)

    def get_leaderboard(self, limit: int = 20, trend: str = None, min_score: float = None):
        results = []
        for t in self.tickers:
            ind = self.get_latest_indicators(t['id'])
            if trend and trend != 'ALL' and ind.trend_state != trend:
                continue
            if min_score is not None and ind.final_score < min_score:
                continue
            results.append((ind, MockDBTicker(**t)))
        results.sort(key=lambda x: x[0].final_score, reverse=True)
        return results[:limit]

    def log_job(self, name: str, status: str, message: str = None):
        return True
