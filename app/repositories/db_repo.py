from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import Ticker, OHLCVDaily, IndicatorsDaily, JobsLog

class DBRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_tickers(self):
        return self.db.query(Ticker).all()
        
    def get_ticker_by_symbol(self, symbol: str):
        return self.db.query(Ticker).filter(Ticker.symbol == symbol).first()

    def get_latest_ohlcv(self, ticker_id: int):
        return self.db.query(OHLCVDaily).filter(OHLCVDaily.ticker_id == ticker_id).order_by(desc(OHLCVDaily.date)).first()

    def get_ohlcv_history(self, ticker_id: int, days: int):
        return self.db.query(OHLCVDaily).filter(OHLCVDaily.ticker_id == ticker_id).order_by(desc(OHLCVDaily.date)).limit(days).all()

    def get_latest_indicators(self, ticker_id: int):
        return self.db.query(IndicatorsDaily).filter(IndicatorsDaily.ticker_id == ticker_id).order_by(desc(IndicatorsDaily.date)).first()

    def upsert_ticker(self, symbol: str, name: str = None):
        ticker = self.get_ticker_by_symbol(symbol)
        if not ticker:
            ticker = Ticker(symbol=symbol, name=name)
            self.db.add(ticker)
            self.db.flush()
        elif name and ticker.name != name:
            ticker.name = name
            self.db.flush()
        return ticker

    def bulk_save_ohlcv(self, records: list):
        # In a real app we'd use PostgreSQL ON CONFLICT DO UPDATE
        # For simplicity in this demo, we'll iterate
        count = 0
        for r in records:
            existing = self.db.query(OHLCVDaily).filter(
                OHLCVDaily.ticker_id == r['ticker_id'],
                OHLCVDaily.date == r['date']
            ).first()
            if existing:
                existing.open = r['open']
                existing.high = r['high']
                existing.low = r['low']
                existing.close = r['close']
                existing.volume = r['volume']
            else:
                new_record = OHLCVDaily(**r)
                self.db.add(new_record)
            count += 1
        self.db.commit()
        return count

    def bulk_save_indicators(self, records: list):
        count = 0
        for r in records:
            existing = self.db.query(IndicatorsDaily).filter(
                IndicatorsDaily.ticker_id == r['ticker_id'],
                IndicatorsDaily.date == r['date']
            ).first()
            if existing:
                for k, v in r.items():
                    setattr(existing, k, v)
            else:
                new_record = IndicatorsDaily(**r)
                self.db.add(new_record)
            count += 1
        self.db.commit()
        return count

    def get_leaderboard(self, limit: int = 20, trend: str = None, min_score: float = None):
        # Subquery to get latest date per ticker in indicators
        from sqlalchemy import func
        subq = self.db.query(
            IndicatorsDaily.ticker_id,
            func.max(IndicatorsDaily.date).label('max_date')
        ).group_by(IndicatorsDaily.ticker_id).subquery()

        q = self.db.query(IndicatorsDaily, Ticker).join(
            Ticker, Ticker.id == IndicatorsDaily.ticker_id
        ).join(
            subq,
            (IndicatorsDaily.ticker_id == subq.c.ticker_id) & (IndicatorsDaily.date == subq.c.max_date)
        )
        
        if trend and trend != 'ALL':
            q = q.filter(IndicatorsDaily.trend_state == trend)
        if min_score is not None:
            q = q.filter(IndicatorsDaily.final_score >= min_score)
            
        return q.order_by(desc(IndicatorsDaily.final_score)).limit(limit).all()

    def log_job(self, name: str, status: str, message: str = None):
        job = JobsLog(job_name=name, status=status, message=message)
        self.db.add(job)
        self.db.commit()
        return job
