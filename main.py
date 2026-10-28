import pandas as pd
import yfinance as yf

def check_candle_reversal(ticker_symbol, interval="1d", period="5d"):
    # Clean up input
    ticker_symbol = ticker_symbol.strip().upper()
    
    # Optional helper: if user enters common Indian tickers without suffix, add .NS
    indian_common = ["RELIANCE", "TCS", "INFY", "SBIN", "HDFCBANK", "ICICIBANK", "TATAMOTORS", "ITC"]
    if ticker_symbol in indian_common:
        ticker_symbol += ".NS"
        print(f"[INFO] Automatically added exchange suffix -> Using {ticker_symbol}")

    print(f"\n[INFO] Fetching live data for '{ticker_symbol}' (Interval: {interval}, Period: {period})...")
    
    try:
        df = yf.download(ticker_symbol, period=period, interval=interval, progress=False)
    except Exception as e:
        print(f"[ERROR] Exception occurred while fetching data: {e}")
        return
    
    if df.empty or len(df) < 2:
        print(f"[ERROR] Not enough data fetched for '{ticker_symbol}'.")
        print("Tip: Ensure the ticker symbol is correct (e.g., use 'RELIANCE.NS' for NSE, or 'AAPL' for US stocks).")
        return
    
    # Handle multi-index columns if returned by yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Extract the last two completed candles
    c1 = df.iloc[-2]
    c2 = df.iloc[-1]
    
    c1_time = df.index[-2]
    c2_time = df.index[-1]
    
    c1_open, c1_high, c1_low, c1_close = c1['Open'], c1['High'], c1['Low'], c1['Close']
    c2_open, c2_high, c2_low, c2_close = c2['Open'], c2['High'], c2['Low'], c2['Close']
    
    print("-" * 50)
    print("CANDLESTICK DATA:")
    print(f"1st Candle ({c1_time.strftime('%Y-%m-%d %H:%M')}):")
    print(f"  Open={c1_open:.2f} | High={c1_high:.2f} | Low={c1_low:.2f} | Close={c1_close:.2f}")
    print(f"2nd Candle ({c2_time.strftime('%Y-%m-%d %H:%M')}):")
    print(f"  Open={c2_open:.2f} | High={c2_high:.2f} | Low={c2_low:.2f} | Close={c2_close:.2f}")
    print("-" * 50)
    
    # Applying Excel Formula Logic: AND(D2>D3, E2<E3, B3<=E2, B3>D2)
    cond1 = c1_low > c2_low         # 1st Low > 2nd Low
    cond2 = c1_close < c2_close     # 1st Close < 2nd Close
    cond3 = c2_open <= c1_close     # 2nd Open <= 1st Close
    cond4 = c2_open > c1_low        # 2nd Open > 1st Low
    
    is_reversal = cond1 and cond2 and cond3 and cond4
    
    result = "Reversal" if is_reversal else "Non Reversal"
    print(f"Remarks / Signal: **{result}**")
    print("-" * 50)
    
    return result

if __name__ == "__main__":
    print("=== LIVE STOCK CANDLE REVERSAL CHECKER ===")
    user_ticker = input("Enter Stock Ticker (e.g., AAPL, RELIANCE.NS, TSLA): ").strip()
    if not user_ticker:
        user_ticker = "AAPL"
        
    user_interval = input("Enter Time Interval [1m, 5m, 15m, 1h, 1d] (default '1d'): ").strip()
    if not user_interval:
        user_interval = "1d"
        
    user_period = input("Enter Period [1d, 5d, 1mo, 6mo] (default '5d'): ").strip()
    if not user_period:
        user_period = "5d"
        
    check_candle_reversal(user_ticker, interval=user_interval, period=user_period)
