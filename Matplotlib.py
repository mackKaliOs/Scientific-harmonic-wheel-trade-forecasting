# Create a print-quality "Scientific Harmonic Wheel — Unified Resonance Map"
# using matplotlib. This is a schematic for publication (3000x3000 px).

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

dpi = 300
size_in = 3000/dpi

fig = plt.figure(figsize=(size_in, size_in), dpi=dpi)
ax = plt.subplot(111, aspect='equal')
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.axis('off')

# Radii for the three rings
R_outer = 1.0
R_mid = 0.78
R_inner = 0.56
R_core = 0.22

# Draw concentric rings
rings = [(R_outer, 0.012), (R_mid, 0.012), (R_inner, 0.012), (R_core, 0.008)]
for r, lw in rings:
    circ = patches.Circle((0,0), r, fill=False, linewidth=lw)
    ax.add_patch(circ)

# Helper to draw radial lines at given degrees
def radial_lines(deg_list, r0, r1, lw=0.008):
    for d in deg_list:
        th = np.deg2rad(d)
        ax.plot([r0*np.cos(th), r1*np.cos(th)],
                [r0*np.sin(th), r1*np.sin(th)], linewidth=lw)

# Gann key angles on middle ring (1x1, 1x2, 2x1, 1x4, etc.)
gann_deg = [0, 45, 90, 135, 180, 225, 270, 315]
radial_lines(gann_deg, 0, R_outer, lw=0.006)

# Minor angles (22.5° increments)
minor_deg = [i*22.5 for i in range(16)]
radial_lines(minor_deg, R_inner, R_outer, lw=0.0035)

# Dewey cycle arcs on the outer ring (schematic labels)
cycle_labels = [
    ("11-Year Solar", 5),
    ("8.6-Year\nBusiness", 25),
    ("6.8-Year", 50),
    ("4-Year Presidential", 85),
    ("3.5-Year Kitchin", 120),
    ("18.6-Year\nLunar Node", 160),
    ("Schumann &\nGeomagnetic", 205),
    ("Annual &\nSeasonal", 250),
    ("Lunar 29.5 d", 300),
    ("Weekly &\nBiological", 335),
]

for txt, deg in cycle_labels:
    th = np.deg2rad(deg)
    r = R_outer + 0.03
    ax.text(r*np.cos(th), r*np.sin(th), txt, ha='center', va='center', fontsize=10)

# Kozyrev flow arrows on inner ring (schematic energy vectors)
def add_arrow(theta_deg, length=0.14, base_r=R_inner-0.04):
    th = np.deg2rad(theta_deg)
    x0 = base_r*np.cos(th)
    y0 = base_r*np.sin(th)
    x1 = (base_r+length)*np.cos(th)
    y1 = (base_r+length)*np.sin(th)
    ax.annotate("", xy=(x1,y1), xytext=(x0,y0),
                arrowprops=dict(arrowstyle="->", lw=1.2))

for d in [30, 120, 210, 300]:
    add_arrow(d)

# Quadrant asset labels (Gold, S&P 500, Oil, EUR/USD)
assets = [("GOLD (GC)", 45),
          ("S&P 500 (ES)", 135),
          ("CRUDE OIL (CL)", 225),
          ("EUR/USD", 315)]
for name, deg in assets:
    th = np.deg2rad(deg)
    r = (R_mid + R_outer)/2
    ax.text(r*np.cos(th), r*np.sin(th), name, ha='center', va='center', fontsize=14, fontweight='bold')

# Center node label
ax.text(0, 0, "Market Field\nCoherence Node", ha='center', va='center', fontsize=13)

# Ring captions
ax.text(0, R_outer+0.08, "DEWEY • CYCLE TAXONOMY (TIME)", ha='center', va='bottom', fontsize=12, fontstyle='italic')
ax.text(0, R_mid-0.02, "GANN • GEOMETRIC STRUCTURE (PRICE/TIME)", ha='center', va='top', fontsize=11, fontstyle='italic')
ax.text(0, R_inner-0.02, "KOZYREV • ENERGY FLOW (PHASE/TIME)", ha='center', va='top', fontsize=11, fontstyle='italic')

# Title and subtitle
ax.text(0, 1.15, "Scientific Harmonic Wheel — Unified Resonance Map", ha='center', va='center', fontsize=18, fontweight='bold')
ax.text(0, 1.10, "Gann • Kozyrev • Dewey", ha='center', va='center', fontsize=13)

# Footer
ax.text(0, -1.15, "Template v1 • For educational/strategy illustration", ha='center', va='center', fontsize=9)

out_path = "/mnt/data/scientific_harmonic_wheel.png"
plt.savefig(out_path, dpi=dpi, bbox_inches='tight', pad_inches=0.25)
out_path
