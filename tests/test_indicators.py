import pytest
import pandas as pd
import numpy as np
from datetime import date, timedelta
from app.indicators import compute_indicators

def create_sample_df(days=100, trend='up'):
    dates = [date.today() - timedelta(days=x) for x in range(days)]
    dates.reverse() # ascending
    
    data = []
    base_price = 100.0
    for d in dates:
        if trend == 'up':
            base_price *= 1.01
        elif trend == 'down':
            base_price *= 0.99
            
        data.append({
            "date": d,
            "open": base_price,
            "high": base_price * 1.02,
            "low": base_price * 0.98,
            "close": base_price,
            "volume": 10000
        })
    return pd.DataFrame(data)

def test_sma_correctness():
    df = create_sample_df(days=50, trend='up')
    res = compute_indicators(df)
    
    # 20-day SMA on day 20 should be mean of previous 20 days
    # (assuming index 19 is day 20 since min_periods=1)
    day20_sma = res.iloc[19]['sma_20']
    manual_mean = res['close'].iloc[0:20].mean()
    assert np.isclose(day20_sma, manual_mean)

def test_rsi_correctness():
    # RSI for pure uptrend should trend towards 100 after 14 days
    df_up = create_sample_df(days=30, trend='up')
    res_up = compute_indicators(df_up)
    rsi_up = res_up.iloc[-1]['rsi_14']
    assert rsi_up > 80 # Highly overbought

    # RSI for pure downtrend should trend towards 0 after 14 days
    df_down = create_sample_df(days=30, trend='down')
    res_down = compute_indicators(df_down)
    rsi_down = res_down.iloc[-1]['rsi_14']
    assert rsi_down < 20 # Highly oversold

def test_no_lookahead():
    df = create_sample_df(days=30, trend='up')
    
    # Compute on full 30 days
    res_full = compute_indicators(df)
    
    # Compute on first 15 days
    res_partial = compute_indicators(df.iloc[:15])
    
    # The values for day 15 should be EXACTLY the same in both 
    # (meaning future days don't affect past days)
    # Check RSI and SMAs
    
    day15_full = res_full.iloc[14]
    day15_partial = res_partial.iloc[14]
    
    assert np.isclose(day15_full['sma_20'], day15_partial['sma_20'])
    assert np.isclose(day15_full['rsi_14'], day15_partial['rsi_14'])
    assert np.isclose(day15_full['vol_20d'], day15_partial['vol_20d'])
