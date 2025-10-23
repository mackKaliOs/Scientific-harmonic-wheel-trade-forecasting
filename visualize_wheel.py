
import argparse, yaml
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from pathlib import Path

def plot_wheel(cfg, save_dir):
    fig = plt.figure(figsize=(8,8))
    ax = plt.subplot(111, projection='polar')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Gann spokes
    for deg in cfg["wheel"]["gann_angles_deg"]:
        th = np.deg2rad(deg)
        ax.plot([th, th], [0.15, 0.95], lw=1.2)

    # Dewey rings
    r_min, r_max = 0.15, 0.95
    periods = np.array(cfg["dewey"]["cycles_days"], dtype=float)
    pn = (np.log(periods)-np.log(periods.min()))/(np.log(periods.max())-np.log(periods.min()))
    radii = r_min + (r_max-r_min)*(1-pn)
    theta = np.linspace(0, 2*np.pi, 360)
    for r in radii:
        ax.plot(theta, np.full_like(theta, r), lw=0.6)

    # Kozyrev spiral
    t = np.linspace(0,1,800)
    th = 2*np.pi*t + 2*np.pi*cfg["kozyrev"]["beta"]*t*10
    r = r_min + (r_max-r_min)*t
    ax.plot(th, r, lw=1.0)

    ax.set_rticks([]); ax.set_xticks([])
    ax.set_title("Emerald Wheel — Gann • Dewey • Kozyrev")
    save_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_dir/"emerald_wheel.png", dpi=140, bbox_inches='tight', pad_inches=0.2)
    plt.close(fig)
    print("Saved charts/emerald_wheel.png")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, "r"))
    plot_wheel(cfg, Path("charts"))
