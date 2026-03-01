import pytest
import pandas as pd
from app.scoring import compute_trend_state, _normalize_risk, compute_scores

def test_trend_state():
    assert compute_trend_state(100, 90, 80) == "UP"      # close > sma_50 > sma_200
    assert compute_trend_state(80, 90, 100) == "DOWN"    # close < sma_50 < sma_200
    assert compute_trend_state(95, 90, 100) == "SIDEWAYS" # close > sma_50 but sma_50 < sma_200
    
def test_risk_normalization():
    # Low vol, no drawdown
    risk_low = _normalize_risk(0.01, 0.0)
    # High vol, deep drawdown
    risk_high = _normalize_risk(0.05, -0.30)
    
    assert risk_high > risk_low
    assert 0 <= risk_low <= 1.0
    assert 0 <= risk_high <= 1.0

def test_scoring_stable():
    df = pd.DataFrame([{
        "close": 150, "sma_50": 140, "sma_200": 120, # UP TREND
        "ret_20d": 0.05, "ret_60d": 0.10,          # Positive momentum
        "vol_20d": 0.02, "drawdown_60d": -0.05,    # Moderate risk
        "vol_z_20d": 1.5                           # Good liquidity
    }])
    
    res = compute_scores(df)
    
    assert len(res) == 1
    row = res.iloc[0]
    
    assert row['trend_state'] == 'UP'
    assert 0 <= row['final_score'] <= 100
    
    # Ensure it's deterministic (rerunning gives same)
    res2 = compute_scores(df)
    assert row['final_score'] == res2.iloc[0]['final_score']
