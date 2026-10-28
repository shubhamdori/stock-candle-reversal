import pandas as pd
import yfinance as yf

def check_candle_reversal(ticker_symbol, interval="1d", period="5d"):
    print(f"Fetching data for {ticker_symbol}...")
    df = yf.download(ticker_symbol, period=period, interval=interval, progress=False)
    
    if df.empty or len(df) < 2:
        print("Error: Not enough data fetched.")
        return
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    c1 = df.iloc[-2]
    c2 = df.iloc[-1]
    
    c1_time = df.index[-2]
    c2_time = df.index[-1]
    
    c1_open, c1_high, c1_low, c1_close = c1['Open'], c1['High'], c1['Low'], c1['Close']
    c2_open, c2_high, c2_low, c2_close = c2['Open'], c2['High'], c2['Low'], c2['Close']
    
    print(f"\n--- Candle Data ---")
    print(f"1st Candle ({c1_time.strftime('%Y-%m-%d')}): Open={c1_open:.2f}, High={c1_high:.2f}, Low={c1_low:.2f}, Close={c1_close:.2f}")
    print(f"2nd Candle ({c2_time.strftime('%Y-%m-%d')}): Open={c2_open:.2f}, High={c2_high:.2f}, Low={c2_low:.2f}, Close={c2_close:.2f}")
    
    cond1 = c1_low > c2_low
    cond2 = c1_close < c2_close
    cond3 = c2_open <= c1_close
    cond4 = c2_open > c1_low
    
    is_reversal = cond1 and cond2 and cond3 and cond4
    result = "Reversal" if is_reversal else "Non Reversal"
    print(f"\nRemarks / Signal: **{result}**")
    return result

if __name__ == "__main__":
    check_candle_reversal("AAPL", interval="1d", period="5d")
