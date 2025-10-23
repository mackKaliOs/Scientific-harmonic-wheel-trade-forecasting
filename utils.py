
import numpy as np
import pandas as pd

def load_series(csv_path, date_col="date", price_col="close", date_format=None):
    df = pd.read_csv(csv_path)
    if date_format:
        df[date_col] = pd.to_datetime(df[date_col], format=date_format)
    else:
        df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)
    t = (df[date_col] - df[date_col].iloc[0]).dt.days.values.astype(float)
    y = df[price_col].values.astype(float)
    if len(t) > 2:
        y = y - np.poly1d(np.polyfit(t, y, 1))(t)
    return t, y, df

def rolling_entropy(x, win=30, bins=20):
    x = np.asarray(x, float)
    ent = np.full_like(x, np.nan, dtype=float)
    for i in range(win, len(x)):
        seg = x[i-win:i]
        hist, edges = np.histogram(seg, bins=bins, density=True)
        p = hist * (edges[1]-edges[0])
        p = p[p>0]
        H = -np.sum(p*np.log2(p)) if len(p)>0 else 0.0
        ent[i] = H
    # fill edges
    first_valid = np.nanmin(ent[np.isfinite(ent)]) if np.any(np.isfinite(ent)) else 0.0
    ent[:win] = first_valid
    # normalize
    m = np.nanmean(ent); s = np.nanstd(ent) or 1.0
    ent = (ent - m)/s
    ent[np.isnan(ent)] = 0.0
    return ent

def normalize(x):
    x = x - np.nanmean(x)
    sd = np.nanstd(x) or 1.0
    return x/sd
