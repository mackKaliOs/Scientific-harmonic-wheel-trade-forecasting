
import argparse, yaml
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
from utils import load_series, rolling_entropy, normalize

def gann_field(t, amplitudes, periods, phases_deg):
    t = np.asarray(t, float)
    w = 2*np.pi/np.asarray(periods, float)
    phi = np.deg2rad(np.asarray(phases_deg, float))
    G = np.zeros_like(t)
    for A, wi, ph in zip(amplitudes, w, phi):
        G += A * np.sin(wi * t + ph)
    return G

def kozyrev_field(t, alpha, beta):
    t = np.asarray(t, float)
    return np.exp(-alpha*t) * np.cos(beta*t)

def dewey_field(t, cycles):
    t = np.asarray(t, float)
    D = np.zeros_like(t)
    for T in cycles:
        D += np.sin(2*np.pi * t / float(T))
    return D

def coherence_field(entropy, lam):
    return np.exp(-lam * normalize(entropy))

def emerald_uri(G, K, D, C):
    return np.real(G * K * D * C)

def run_engine(cfg, save_dir):
    t, y, df = load_series(cfg["input"]["csv_path"], cfg["input"]["date_col"], cfg["input"]["price_col"], cfg["input"]["date_format"])
    horizon = cfg["time_horizon_days"]
    if len(t) > horizon:
        t = t[-horizon:]; y = y[-horizon:]; df = df.iloc[-horizon:]
    G = gann_field(t, cfg["gann"]["amplitudes"], cfg["gann"]["periods_days"], cfg["gann"]["phases_deg"])
    K = kozyrev_field(t, cfg["kozyrev"]["alpha"], cfg["kozyrev"]["beta"])
    D = dewey_field(t, cfg["dewey"]["cycles_days"])
    H = rolling_entropy(y, win=cfg["coherence"]["entropy_window"])
    C = coherence_field(H, cfg["coherence"]["lambda"])
    URI = normalize(emerald_uri(G, K, D, C))

    fig, ax = plt.subplots(figsize=(11,4))
    ax.plot(df[cfg["input"]["date_col"]], URI, lw=1.0)
    ax.axhline(cfg["uri_threshold_pos"], ls='--', color='green', alpha=0.6)
    ax.axhline(cfg["uri_threshold_neg"], ls='--', color='red', alpha=0.6)
    ax.set_title("Unified Resonance Index (URI) — Emerald Equation")
    ax.set_ylabel("URI (normalized)"); ax.set_xlabel("Date")
    fig.autofmt_xdate()
    save_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_dir/"uri_timeseries.png", dpi=140, bbox_inches='tight', pad_inches=0.2)
    plt.close(fig)

    out = df.copy(); out["URI"]=URI; out["G"]=G; out["K"]=K; out["D"]=D; out["C"]=C
    out.to_csv(save_dir/"uri_components.csv", index=False)
    print("Saved charts/uri_timeseries.png and charts/uri_components.csv")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r"))
    run_engine(cfg, Path("charts"))
