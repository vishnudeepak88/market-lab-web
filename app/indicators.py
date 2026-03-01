import pandas as pd
import numpy as np

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes technical indicators for a given DataFrame of OHLCV data.
    Input df must have columns: date, open, high, low, close, volume.
    Sorted by date ascending.
    """
    if len(df) == 0:
        return df
        
    df = df.copy()
    df.sort_values('date', inplace=True)
    
    # Returns (NO LOOKAHEAD - using past data to compute current day return)
    # ret_1d on day T is (close_T / close_{T-1}) - 1
    df['ret_1d'] = df['close'].pct_change(1)
    df['ret_5d'] = df['close'].pct_change(5)
    df['ret_20d'] = df['close'].pct_change(20)
    df['ret_60d'] = df['close'].pct_change(60) # For momentum scoring
    
    # SMAs
    df['sma_20'] = df['close'].rolling(window=20, min_periods=1).mean()
    df['sma_50'] = df['close'].rolling(window=50, min_periods=1).mean()
    df['sma_200'] = df['close'].rolling(window=200, min_periods=1).mean()
    
    # RSI 14
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    # Wilder's smoothing (exponential moving average with alpha=1/14)
    avg_gain = gain.ewm(com=13, adjust=False, min_periods=1).mean()
    avg_loss = loss.ewm(com=13, adjust=False, min_periods=1).mean()
    
    rs = avg_gain / avg_loss
    # Handle division by zero
    rs = rs.replace([np.inf, -np.inf], 1000)
    df['rsi_14'] = 100 - (100 / (1 + rs))
    # Where avg_loss is 0, RSI is 100
    df.loc[avg_loss == 0, 'rsi_14'] = 100
    
    # Volatility
    df['vol_20d'] = df['ret_1d'].rolling(window=20, min_periods=1).std()
    
    # Volume Z-Score 20d
    vol_mean = df['volume'].rolling(window=20, min_periods=1).mean()
    vol_std = df['volume'].rolling(window=20, min_periods=1).std()
    
    # Avoid div by zero
    df['vol_z_20d'] = np.where(vol_std > 0, (df['volume'] - vol_mean) / vol_std, 0)
    
    # Drawdown 60d proxy (peak to trough within 60 days)
    # Peak over last 60d
    roll_max_60 = df['high'].rolling(window=60, min_periods=1).max()
    df['drawdown_60d'] = (df['close'] - roll_max_60) / roll_max_60
    
    # 120d volume median for alerts
    df['vol_median_120d'] = df['vol_20d'].rolling(window=120, min_periods=1).median()
    
    return df
