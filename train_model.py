# train_model.py

import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
from utils.fetch_data import fetch_stock_data
from utils.prediction import prepare_features

# Params
TICKER = "AAPL"
START_DATE = "2020-01-01"
END_DATE = "2024-12-31"
MODEL_PATH = "models/stock_price_model.pkl"

# Fetch data
df = fetch_stock_data(TICKER, START_DATE, END_DATE)

# 🔍 Debug print: Show what columns we got
print("📊 Columns from fetched data:", df.columns.tolist())
print("🧪 First few rows:")
print(df.head())

# Ensure essential columns exist before preparing features
required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
if df.empty or not all(col in df.columns for col in required_cols):
    print(f"❌ Missing required columns: {', '.join(col for col in required_cols if col not in df.columns)}")
else:
    # Prepare features (generic: Open_MA, High_MA, etc.)
    X, y = prepare_features(df)

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Save model
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"✅ Model trained and saved to {MODEL_PATH}")
