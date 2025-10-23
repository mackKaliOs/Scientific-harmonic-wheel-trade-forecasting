import numpy as np
import pandas as pd

def load_series(csv_path, date_col="date", price_col="close", date_format=None):
    df = pd.read_csv(csv_path)
    if date_format:
        df[date_col] = pd.to_datetime(df[date_col], format=date_format)
    else:
        df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    t = (df[date_col] - df[date_col].iloc[0]).dt.days.values.astype(float)
    y = df[price_col].values.astype(float)
    y = y - np.poly1d(np.polyfit(t, y, 1))(t)  # detrend
    return t, y, df

def kozyrev_bias(t_days, rate=0.002):
    # simple temporal phase drift proxy
    return 2*np.pi*rate*(t_days - t_days.min())

def normalize(x):
    x = x - np.nanmean(x)
    sd = np.nanstd(x) or 1.0
    return x/sd
