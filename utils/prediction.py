import pandas as pd

def prepare_features(df):
    df = df.copy()

    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        if col not in df.columns:
            df[col] = 0.0

    df = df.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'])

    df['Open_MA'] = df['Open'].rolling(window=3).mean()
    df['High_MA'] = df['High'].rolling(window=3).mean()
    df['Low_MA'] = df['Low'].rolling(window=3).mean()
    df['Volume_MA'] = df['Volume'].rolling(window=3).mean()

    df.dropna(inplace=True)

    features = df[['Open_MA', 'High_MA', 'Low_MA', 'Volume_MA']]
    target = df['Close']
    return features, target

def predict_close_price(model, X):
    return model.predict(X)
