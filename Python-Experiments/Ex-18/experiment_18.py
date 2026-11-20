"""Experiment 18: Erlang B call blocking probability."""
from pathlib import Path
import csv, math
OUT=Path(__file__).resolve().parent
LOADS=(2,5,10,20); CHANNELS=(5,10,15,20,25,30)
def erlang_b(E,m):
    """Blocking probability using the stable recursive Erlang-B formula."""
    B=1.0
    for k in range(1,m+1): B=E*B/(k+E*B)
    return B
def main():
    rows=[]
    print("Blocking probability (%)")
    print("E \\ m  "+"".join(f"{m:>9}" for m in CHANNELS))
    with (OUT/"results.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["offered_traffic_erlangs","channels","blocking_probability_percent"])
        for E in LOADS:
            vals=[100*erlang_b(E,m) for m in CHANNELS]; print(f"{E:>5}  "+"".join(f"{v:9.3f}" for v in vals))
            for m,v in zip(CHANNELS,vals): rows.append((E,m,v)); w.writerow([E,m,f"{v:.6f}"])
    E,target=10,.02; m=1
    while erlang_b(E,m)>target: m+=1
    print(f"\nFor E = {E} Erlangs and GoS = {target*100:.0f}% -> channels required = {m}")
    # Plot blocking probability in percent against channels for each offered load.
    W,H=880,450; x0,y0,pw,ph=80,70,730,300
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" fill="white"/><style>text{{font-family:Arial;fill:#172033}}.g{{stroke:#d8e0ec;stroke-dasharray:4 4}}</style><text x="440" y="32" text-anchor="middle" font-size="20" font-weight="bold">Erlang B Blocking Probability</text>']
    for tick in (0,20,40,60,80):
        y=y0+ph-tick/80*ph; svg += [f'<line class="g" x1="{x0}" y1="{y}" x2="{x0+pw}" y2="{y}"/><text x="{x0-8}" y="{y+4}" text-anchor="end" font-size="12">{tick}</text>']
    colors={2:'#2a9d8f',5:'#2563eb',10:'#e76f51',20:'#7b2cbf'}
    for E in LOADS:
        pts=[]
        for m in range(5,31):
            x=x0+(m-5)/25*pw; y=y0+ph-(100*erlang_b(E,m))/80*ph; pts.append(f'{x:.1f},{y:.1f}')
        svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colors[E]}" stroke-width="2.5"/>')
        svg.append(f'<text x="{x0+pw-100}" y="{y0+18*(LOADS.index(E)+1)}" font-size="12" fill="{colors[E]}">E={E} Erlangs</text>')
    for m in (5,10,15,20,25,30):
        x=x0+(m-5)/25*pw; svg.append(f'<text x="{x}" y="{y0+ph+22}" text-anchor="middle" font-size="11">{m}</text>')
    svg += [f'<text x="{x0+pw/2}" y="{y0+ph+48}" text-anchor="middle">Channels</text>',f'<text x="24" y="{y0+ph/2}" transform="rotate(-90 24 {y0+ph/2})" text-anchor="middle">Blocking probability (%)</text>','</svg>']
    (OUT/"erlang_b_blocking.svg").write_text("\n".join(svg),encoding="utf-8")
if __name__=="__main__": main()
