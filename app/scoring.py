import numpy as np
import pandas as pd
from app.config import settings

def compute_trend_state(close, sma_50, sma_200):
    if pd.isna(close) or pd.isna(sma_50) or pd.isna(sma_200):
        return "SIDEWAYS"
    if close > sma_50 and sma_50 > sma_200:
        return "UP"
    elif close < sma_50 and sma_50 < sma_200:
        return "DOWN"
    return "SIDEWAYS"

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def _normalize_momentum(ret_20d, ret_60d):
    ret_20 = ret_20d if not pd.isna(ret_20d) else 0.0
    ret_60 = ret_60d if not pd.isna(ret_60d) else ret_20
    m = ret_20 + 0.5 * ret_60
    # Center around 0, scale so 10% return is meaningful
    # Using a soft sigmoid scaled to 0-1
    return sigmoid(m * 10)

def _normalize_risk(vol_20d, drawdown_60d):
    v = vol_20d if not pd.isna(vol_20d) else 0.02
    dd = drawdown_60d if not pd.isna(drawdown_60d) else 0.0
    # Vol is typically 0.01 to 0.05. DD is negative e.g. -0.10.
    # Risk factor: higher means higher risk
    rf = (v * 10) + abs(dd)
    # Cap and scale to 0-1
    return min(1.0, max(0.0, rf))

def _trend_score(trend_state):
    if trend_state == "UP": return 1.0
    if trend_state == "SIDEWAYS": return 0.5
    return 0.0

def _normalize_liquidity(vol_z):
    z = vol_z if not pd.isna(vol_z) else 0.0
    # z typically between -3 and 3
    # map to 0-1 where high z is better liquidity burst
    sc = (z + 3) / 6.0
    return min(1.0, max(0.0, sc))

def compute_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes scores for the dataframe that already has indicators.
    """
    if len(df) == 0:
        return df
        
    df = df.copy()
    
    # 1. Trend State
    df['trend_state'] = df.apply(lambda row: compute_trend_state(row['close'], row['sma_50'], row['sma_200']), axis=1)
    
    # 2. Components mapping to 0-1
    df['momentum_score'] = df.apply(lambda row: _normalize_momentum(row['ret_20d'], row.get('ret_60d', np.nan)), axis=1)
    df['risk_score'] = df.apply(lambda row: _normalize_risk(row['vol_20d'], row.get('drawdown_60d', np.nan)), axis=1)
    df['trend_component'] = df['trend_state'].apply(_trend_score)
    df['liquidity_component'] = df['vol_z_20d'].apply(_normalize_liquidity)
    
    # 3. Final Score
    df['final_score'] = (
        settings.momentum_w * df['momentum_score'] +
        settings.trend_w * df['trend_component'] -
        settings.risk_w * df['risk_score'] +
        settings.liquidity_w * df['liquidity_component']
    )
    
    # Shift baseline so scores are roughly 0-100 logically
    # Max possible roughly 100 + 60 + 20 = 180, min roughly -80
    # Let's normalize it
    # We will just leave it raw as requested, or apply a simple min-max scaling heuristically
    df['final_score'] = df['final_score'].clip(0, 100) # Simple clip for nice UI
    
    return df

def generate_alerts(row: pd.Series) -> list:
    """
    Generate alerts for a single day row.
    """
    alerts = []
    
    vol_20d = row.get('vol_20d', np.nan)
    vol_median_120d = row.get('vol_median_120d', np.nan)
    
    if not pd.isna(vol_20d) and not pd.isna(vol_median_120d) and vol_median_120d > 0:
        if vol_20d > 1.5 * vol_median_120d:
            alerts.append("VOL_SPIKE")
            
    dd = row.get('drawdown_60d', np.nan)
    if not pd.isna(dd) and dd < -0.10: # >10% below peak
        alerts.append("DRAWDOWN_WARN")
        
    rsi = row.get('rsi_14', np.nan)
    if not pd.isna(rsi):
        if rsi > 75:
            alerts.append("OVERHEATED")
        elif rsi < 25:
            alerts.append("OVERSOLD")
            
    return alerts
