"""Experiment 17: Frequency reuse, cluster size, capacity and S/I.

Run with: python experiment_17.py
Uses only the Python standard library.
"""
from pathlib import Path
import csv
import math

TOTAL_CHANNELS = 420
REPLICATIONS = 10
PATH_LOSS_EXPONENT = 4
SI_REQUIREMENT_DB = 18.0
OUTPUT_DIR = Path(__file__).resolve().parent


def valid_cluster_sizes(limit=4):
    """Generate the first valid hexagonal cluster sizes from i,j pairs."""
    return sorted({i*i + i*j + j*j for i in range(limit + 1)
                   for j in range(limit + 1)} - {0})[:8]


def calculate(n):
    reuse_ratio = math.sqrt(3*n)
    channels_per_cell = TOTAL_CHANNELS // n
    capacity = REPLICATIONS * channels_per_cell * n
    si_linear = reuse_ratio**PATH_LOSS_EXPONENT / 6
    si_db = 10 * math.log10(si_linear)
    return reuse_ratio, channels_per_cell, capacity, si_db


def write_plot(rows):
    """Create a two-panel SVG plot of co-channel S/I and channels per cell."""
    W,H=1050,440
    panels=[(75,75,390,270,"S/I versus cluster size","S/I (dB)","si_db",0,30),
            (585,75,390,270,"Channels per cell","Channels per cell","channels_per_cell",0,450)]
    color="#2457a7"; out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="white"/>','<style>text{font-family:Arial,sans-serif;fill:#172033}.grid{stroke:#d8e0ec;stroke-dasharray:4 5}.axis{stroke:#556274;stroke-width:1.5}</style>','<text x="525" y="32" text-anchor="middle" font-size="21" font-weight="700">Experiment 17 | Frequency reuse</text>']
    for x,y,w,h,title,ylabel,key,ymin,ymax in panels:
        out.append(f'<text x="{x+w/2}" y="{y-20}" text-anchor="middle" font-size="17" font-weight="700">{title}</text>')
        step=5 if ymax==30 else 75
        for tick in range(ymin,ymax+1,step):
            py=y+h-(tick-ymin)/(ymax-ymin)*h
            out.extend([f'<line class="grid" x1="{x}" y1="{py:.1f}" x2="{x+w}" y2="{py:.1f}"/>',f'<text x="{x-8}" y="{py+4:.1f}" text-anchor="end" font-size="11">{tick}</text>'])
        for n,_,_,si in rows:
            px=x+(n-1)/15*w; val=si if key=="si_db" else calculate(n)[1]; py=y+h-(val-ymin)/(ymax-ymin)*h
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{color}"/>')
        points=[]
        for n,_,_,si in rows:
            val=si if key=="si_db" else calculate(n)[1]; px=x+(n-1)/15*w; py=y+h-(val-ymin)/(ymax-ymin)*h; points.append(f'{px:.1f},{py:.1f}')
        out.extend([f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="2.5"/>',f'<line class="axis" x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}"/>',f'<line class="axis" x1="{x}" y1="{y}" x2="{x}" y2="{y+h}"/>',f'<text x="{x+w/2}" y="{y+h+32}" text-anchor="middle" font-size="13">Cluster size N</text>'])
        for n in (1,3,4,7,9,12,13,16):
            px=x+(n-1)/15*w; out.append(f'<text x="{px:.1f}" y="{y+h+17}" text-anchor="middle" font-size="10">{n}</text>')
        if key=="si_db":
            req_y=y+h-(SI_REQUIREMENT_DB-ymin)/(ymax-ymin)*h
            out.append(f'<line x1="{x}" y1="{req_y:.1f}" x2="{x+w}" y2="{req_y:.1f}" stroke="#cf3e36" stroke-dasharray="6 4"/><text x="{x+w-5}" y="{req_y-6:.1f}" text-anchor="end" font-size="10" fill="#a22">18 dB target</text>')
    out.append('</svg>')
    (OUTPUT_DIR/"frequency_reuse.svg").write_text("\n".join(out),encoding="utf-8")


def main():
    rows=[]
    print(f"{'N':>3}{'D/R':>8}{'ch/cell':>9}{'Capacity C':>12}{'S/I (dB)':>10}")
    with (OUTPUT_DIR/"results.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.writer(f); writer.writerow(["cluster_size_N","reuse_ratio_D_over_R","channels_per_cell","system_capacity","si_db"])
        for n in valid_cluster_sizes():
            q,k,capacity,si=calculate(n); rows.append((n,q,k,si))
            print(f"{n:>3}{q:8.3f}{k:9d}{capacity:12d}{si:10.2f}")
            writer.writerow([n,f"{q:.3f}",k,capacity,f"{si:.2f}"])
    qualifying=[n for n,_,_,si in rows if si>=SI_REQUIREMENT_DB]
    smallest=min(qualifying) if qualifying else None
    print(f"\nSmallest cluster size meeting S/I >= {SI_REQUIREMENT_DB:.1f} dB: N = {smallest}")
    write_plot(rows)
    print("Saved results.csv and frequency_reuse.svg")


if __name__ == "__main__":
    main()
