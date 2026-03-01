from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Ticker(Base):
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    ohlcvs = relationship("OHLCVDaily", back_populates="ticker", cascade="all, delete-orphan")
    indicators = relationship("IndicatorsDaily", back_populates="ticker", cascade="all, delete-orphan")

class OHLCVDaily(Base):
    __tablename__ = "ohlcv_daily"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False) # Float for volume in case it's large/fractional, or use BigInt

    ticker = relationship("Ticker", back_populates="ohlcvs")
    
    __table_args__ = (
        UniqueConstraint('ticker_id', 'date', name='uq_ohlcv_ticker_date'),
    )

class IndicatorsDaily(Base):
    __tablename__ = "indicators_daily"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    
    # Returns
    ret_1d = Column(Float, nullable=True)
    ret_5d = Column(Float, nullable=True)
    ret_20d = Column(Float, nullable=True)
    
    # SMAs
    sma_20 = Column(Float, nullable=True)
    sma_50 = Column(Float, nullable=True)
    sma_200 = Column(Float, nullable=True)
    
    # Other indicators
    rsi_14 = Column(Float, nullable=True)
    vol_20d = Column(Float, nullable=True)
    vol_z_20d = Column(Float, nullable=True)
    
    # Scoring
    trend_state = Column(String, nullable=True) # UP, DOWN, SIDEWAYS
    momentum_score = Column(Float, nullable=True)
    risk_score = Column(Float, nullable=True)
    final_score = Column(Float, nullable=True)

    ticker = relationship("Ticker", back_populates="indicators")
    
    __table_args__ = (
        UniqueConstraint('ticker_id', 'date', name='uq_indicators_ticker_date'),
    )

class JobsLog(Base):
    __tablename__ = "jobs_log"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, nullable=False, index=True)
    ran_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String, nullable=False) # SUCCESS, FAILED
    message = Column(String, nullable=True)
