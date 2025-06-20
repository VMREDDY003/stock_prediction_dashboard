import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, start, end):
    try:
        df = yf.download(ticker, start=start, end=end, auto_adjust=False)

        # Flatten multi-level columns if they exist
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if df.empty or not all(col in df.columns for col in required_columns):
            print("⚠️ Missing one or more required columns after flattening.")
            return pd.DataFrame()

        df = df[required_columns].dropna().copy()
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        print("❌ Fetch Error:", e)
        return pd.DataFrame()
