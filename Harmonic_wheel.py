import argparse, yaml
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def plot_scientific_harmonic_wheel(cfg, save_dir):
    cycles = cfg["cycles_days"]
    gann_angles = cfg["gann_angles"]
    rate = cfg["kozyrev_phase_rate"]

    fig = plt.figure(figsize=(8,8))
    ax = plt.subplot(111, projection='polar')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Dewey rings
    r_min, r_max = 0.15, 0.95
    periods = np.array(cycles, dtype=float)
    pn = (np.log(periods)-np.log(periods.min()))/(np.log(periods.max())-np.log(periods.min()))
    radii = r_min + (r_max-r_min)*(1-pn)
    theta = np.linspace(0,2*np.pi,360)
    for r in radii:
        ax.plot(theta, np.full_like(theta,r), linewidth=0.6, color='#AAAAAA')

    # Gann spokes
    for deg in gann_angles:
        th = np.deg2rad(deg)
        ax.plot([th,th],[r_min,r_max],linewidth=1.2,color='#FFD166')

    # Kozyrev spiral
    t = np.linspace(0,1,600)
    th = 2*np.pi*t + 2*np.pi*rate*t
    r = r_min + (r_max-r_min)*t
    ax.plot(th,r,linewidth=1.0,color='#118AB2')

    ax.set_rticks([])
    ax.set_xticks(np.deg2rad(gann_angles))
    ax.set_title("Scientific Harmonic Wheel — Unified Resonance Map\n(Gann • Kozyrev • Dewey)")
    plt.tight_layout()
    save_dir.mkdir(parents=True,exist_ok=True)
    fig.savefig(save_dir/"scientific_harmonic_wheel_1600x1600.png",dpi=100,bbox_inches='tight',pad_inches=0.2)
    fig.savefig(save_dir/"scientific_harmonic_wheel.svg",bbox_inches='tight',pad_inches=0.2)
    plt.close(fig)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config",default="config.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config,"r"))
    plot_scientific_harmonic_wheel(cfg,Path("charts"))
    print("Saved harmonic wheel.")
