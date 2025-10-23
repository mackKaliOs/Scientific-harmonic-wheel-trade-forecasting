import argparse, yaml, json
import numpy as np, matplotlib.pyplot as plt
from pathlib import Path
from utils import load_series, normalize

def lomb_scargle(t, y, freqs):
    y = y - np.mean(y)
    P = np.zeros_like(freqs)
    for i, w in enumerate(freqs):
        tau = 0.5*np.arctan2(np.sum(np.sin(2*w*t)), np.sum(np.cos(2*w*t)))/w
        cos_wt = np.cos(w*(t - tau)); sin_wt = np.sin(w*(t - tau))
        C, S = np.sum(cos_wt**2), np.sum(sin_wt**2)
        yc, ys = np.sum(y*cos_wt), np.sum(y*sin_wt)
        P[i] = 0.5*((yc**2)/C + (ys**2)/S)
    return P

def scan_cycles(cfg, save_dir):
    t, y, df = load_series(cfg['input']['csv_path'], cfg['input']['date_col'], cfg['input']['price_col'], cfg['input']['date_format'])
    periods = np.linspace(5,720,3000)
    freqs = 2*np.pi/periods
    Pxx = normalize(lomb_scargle(t,y,freqs))

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(periods,Pxx,lw=1.0)
    ax.set_xlim(5,720)
    ax.set_xlabel("Period (days)"); ax.set_ylabel("Power (norm)")
    ax.set_title("Lomb–Scargle Cycle Scan"); ax.grid(True,alpha=0.3)

    k=8
    peak_idx=np.argsort(Pxx)[-k:][::-1]
    peaks=[(periods[i],Pxx[i]) for i in peak_idx]
    for P,val in peaks:
        ax.axvline(P,color='orange',lw=0.7,alpha=0.5)
        ax.text(P,val,f"{P:.1f}d",rotation=90,va='bottom',ha='right',fontsize=8)

    save_dir.mkdir(parents=True,exist_ok=True)
    fig.savefig(save_dir/"lomb_scargle_scan.png",dpi=140,bbox_inches='tight',pad_inches=0.2)
    fig.savefig(save_dir/"lomb_scargle_scan.svg",bbox_inches='tight',pad_inches=0.2)

    peaks_json=[{"period_days":float(P),"power":float(val)} for P,val in peaks]
    (save_dir/"dominant_cycles.json").write_text(json.dumps(peaks_json,indent=2))
    print("Top cycles (days):",[round(p['period_days'],1) for p in peaks_json[:5]])

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default="config.yaml")
    args=ap.parse_args()
    cfg=yaml.safe_load(open(args.config))
    scan_cycles(cfg,Path("charts"))
