"""Experiment 21: OFDMA downlink scheduling throughput and fairness."""
from pathlib import Path
import csv
import numpy as np
OUT=Path(__file__).resolve().parent
U,TTI=6,2000
MEAN_SNR_DB=np.array([25,20,15,10,5,0])
POLICIES=('RR','MaxCI','PF')
def jain(values): return values.sum()**2/(len(values)*(values**2).sum())
def simulate(policy,rate):
    served=np.zeros(U); avg=np.ones(U)
    for t in range(TTI):
        if policy=='RR': user=t%U
        elif policy=='MaxCI': user=int(np.argmax(rate[t]))
        else: user=int(np.argmax(rate[t]/avg))
        served[user]+=rate[t,user]
        instant=np.zeros(U); instant[user]=rate[t,user]
        avg=.99*avg+.01*instant
    return served/TTI
def write_plot(throughputs,totals,fairness):
    W,H=1120,480; svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="white"/><style>text{{font-family:Arial;fill:#172033}}.g{{stroke:#d9e0ec;stroke-dasharray:4 4}}</style><text x="560" y="32" text-anchor="middle" font-size="21" font-weight="700">OFDMA scheduler throughput and fairness</text>']
    colors={'RR':'#2563eb','MaxCI':'#e4572e','PF':'#2a9d8f'}
    # Panel 1: throughput by user.
    x0,y0,pw,ph=78,80,580,290; ymax=7
    for tick in range(0,ymax+1):
        yy=y0+ph-tick/ymax*ph; svg += [f'<line class="g" x1="{x0}" y1="{yy:.1f}" x2="{x0+pw}" y2="{yy:.1f}"/>',f'<text x="{x0-8}" y="{yy+4:.1f}" text-anchor="end" font-size="10">{tick}</text>']
    for u in range(U):
        for j,p in enumerate(POLICIES):
            v=throughputs[p][u]; bw=16; x=x0+u*pw/U+14+j*19; bh=v/ymax*ph; y=y0+ph-bh
            svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{bh:.1f}" fill="{colors[p]}"/>')
        svg.append(f'<text x="{x0+(u+.5)*pw/U}" y="{y0+ph+18}" text-anchor="middle" font-size="10">U{u+1}</text>')
    for j,p in enumerate(POLICIES): svg.append(f'<rect x="{x0+160+j*105}" y="{y0+ph+43}" width="12" height="12" fill="{colors[p]}"/><text x="{x0+178+j*105}" y="{y0+ph+54}" font-size="11">{p}</text>')
    svg.append(f'<text x="{x0+pw/2}" y="{y0-18}" text-anchor="middle" font-size="16" font-weight="700">Per-user throughput (b/s/Hz)</text>')
    # Panel 2: total throughput bars and Jain index labels.
    x0,y0,pw,ph=750,80,300,290; ymax=9
    for tick in range(0,ymax+1,3):
        yy=y0+ph-tick/ymax*ph; svg += [f'<line class="g" x1="{x0}" y1="{yy:.1f}" x2="{x0+pw}" y2="{yy:.1f}"/>',f'<text x="{x0-8}" y="{yy+4:.1f}" text-anchor="end" font-size="10">{tick}</text>']
    for j,p in enumerate(POLICIES):
        x=x0+40+j*88; bh=totals[p]/ymax*ph; y=y0+ph-bh
        svg += [f'<rect x="{x}" y="{y:.1f}" width="48" height="{bh:.1f}" fill="{colors[p]}"/>',f'<text x="{x+24}" y="{y-7:.1f}" text-anchor="middle" font-size="11">{totals[p]:.3f}</text>',f'<text x="{x+24}" y="{y0+ph+18}" text-anchor="middle" font-size="11">{p}</text>',f'<text x="{x+24}" y="{y0+ph+43}" text-anchor="middle" font-size="11">J={fairness[p]:.3f}</text>']
    svg.append(f'<text x="{x0+pw/2}" y="{y0-18}" text-anchor="middle" font-size="16" font-weight="700">Total throughput and Jain fairness</text>')
    svg.append('</svg>'); (OUT/'scheduler_comparison.svg').write_text('\n'.join(svg),encoding='utf-8')
def main():
    rng=np.random.default_rng(1); mean_snr=10**(MEAN_SNR_DB/10)
    rate=np.log2(1+mean_snr*rng.exponential(1.0,(TTI,U)))
    throughput={p:simulate(p,rate) for p in POLICIES}; total={p:float(v.sum()) for p,v in throughput.items()}; fair={p:float(jain(v)) for p,v in throughput.items()}
    print(f"{'Scheduler':>10}  |  "+"  ".join(f"U{i+1:>5}" for i in range(U))+"  |   Total  |  Jain")
    for p in POLICIES: print(f"{p:>10}  |  "+"  ".join(f"{v:6.3f}" for v in throughput[p])+f"  |  {total[p]:6.3f}  |  {fair[p]:.3f}")
    with (OUT/'throughput_results.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['scheduler','user','throughput_bps_hz'])
        for p in POLICIES:
            for i,v in enumerate(throughput[p],1): w.writerow([p,f'U{i}',f'{v:.6f}'])
    with (OUT/'scheduler_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['scheduler','total_throughput_bps_hz','jain_fairness_index'])
        for p in POLICIES: w.writerow([p,f'{total[p]:.6f}',f'{fair[p]:.6f}'])
    write_plot(throughput,total,fair)
if __name__=='__main__': main()
