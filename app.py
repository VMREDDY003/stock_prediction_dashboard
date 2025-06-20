# app.py

import streamlit as st
import pandas as pd
import pickle
import datetime
from utils.fetch_data import fetch_stock_data
from utils.prediction import prepare_features, predict_close_price

# Load trained model
MODEL_PATH = "models/stock_price_model.pkl"
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Page settings
st.set_page_config(page_title="📈 Stock Price Predictor", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        html, body, .main {
            overflow-x: hidden;
        }
        .main-title {
            font-size: 26px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 6px;
        }
        .sub-title {
            font-size: 14px;
            text-align: center;
            color: #555;
            margin-bottom: 20px;
        }
        .live-chart iframe {
            border: none;
            border-radius: 12px;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            font-weight: 600;
            border-radius: 6px;
            padding: 8px 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown("<div class='main-title'>📈 Real-Time Stock Price Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Predict stock closing prices using machine learning and view live charts</div>", unsafe_allow_html=True)

# Input layout
col1, col2 = st.columns([2, 3])
with col1:
    st.subheader("🔧 Configure Inputs")
    ticker = st.text_input("Stock Ticker (e.g., AAPL, MSFT):", value="AAPL").upper()
    start_date = st.date_input("Start Date", datetime.date(2023, 1, 1))
    end_date = st.date_input("End Date", datetime.date.today())
    fetch = st.button("🔍 Fetch & Predict")

# Process
if fetch:
    df = fetch_stock_data(ticker, str(start_date), str(end_date))

    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    if df.empty or not all(col in df.columns for col in required_cols):
        st.error("❌ No stock data found or required columns missing: Open, High, Low, Close, Volume.")
    else:
        try:
            df = df.dropna(subset=required_cols)
            close_values = df['Close'].copy().reset_index(drop=True)
            X, _ = prepare_features(df)

            if len(close_values) < len(X):
                X = X.tail(len(close_values))
            else:
                close_values = close_values.tail(len(X))

            pred_values = predict_close_price(model, X)

            df_result = pd.DataFrame({
                'Close': close_values,
                'Predicted_Close': pred_values
            })

            with col2:
                st.success("✅ Prediction Successful")
                st.dataframe(df_result.tail(), use_container_width=True)
                st.line_chart(df_result)

        except Exception as e:
            st.error(f"⚠️ Error during prediction: {e}")

# Live Chart
st.markdown("### 📱 Go Live Stock View")
maximize = st.checkbox("🔝 Maximize Live Chart View")
height = 700 if maximize else 400

st.markdown(f"""
    <div class="live-chart">
        <iframe src="https://s.tradingview.com/widgetembed/?symbol={ticker}&interval=D&theme=light&style=1&locale=en"
                width="100%" height="{height}" allowtransparency="true" scrolling="no" frameborder="0">
        </iframe>
    </div>
""", unsafe_allow_html=True)
