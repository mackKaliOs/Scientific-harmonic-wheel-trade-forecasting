import argparse, yaml
import numpy as np, matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from utils import load_series, kozyrev_bias, normalize

def composite(t, cycles, rate=0.002):
    t=np.asarray(t,float)
    y=np.zeros_like(t)
    for i,P in enumerate(cycles,start=1):
        w=2*np.pi/P
        amp=1.0/i
        y+=amp*np.sin(w*t+kozyrev_bias(t,rate=rate))
    return y

def make_forecast(cfg, save_dir, days_fwd=300):
    t,y_actual,df=load_series(cfg['input']['csv_path'],cfg['input']['date_col'],cfg['input']['price_col'],cfg['input']['date_format'])
    t_ext=np.arange(t[-1]+days_fwd+1,float)
    comp=normalize(composite(t_ext,cfg['cycles_days'],rate=cfg['kozyrev_phase_rate']))

    fig,ax=plt.subplots(figsize=(11,4))
    y_norm=normalize(y_actual)
    ax.plot(df.iloc[:,0],y_norm,lw=0.9,label="Actual (norm)")
    date0=df.iloc[0,0]
    dates_all=pd.date_range(start=date0,periods=len(t_ext),freq="D")
    ax.plot(dates_all,comp,lw=1.0,label="Composite (cycles+Kozyrev)")
    ax.axvline(df.iloc[-1,0],ls='--',color='gray',lw=1.0)
    ax.set_title("Harmonic Composite Forecast (Past + Forward)")
    ax.legend(); fig.autofmt_xdate()
    save_dir.mkdir(parents=True,exist_ok=True)
    fig.savefig(save_dir/"harmonic_forecast.png",dpi=140,bbox_inches='tight',pad_inches=0.2)
    fig.savefig(save_dir/"harmonic_forecast.svg",bbox_inches='tight',pad_inches=0.2)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default="config.yaml")
    args=ap.parse_args()
    cfg=yaml.safe_load(open(args.config))
    make_forecast(cfg,Path("charts"))
