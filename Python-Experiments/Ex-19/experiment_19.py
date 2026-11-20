"""Experiment 19: Handoff simulation with hysteresis."""
from pathlib import Path
import csv
import numpy as np
OUT=Path(__file__).resolve().parent
D=2000.0; P0=-30.0; PATH_LOSS=3.5; SHADOW_SD=4.0
X=np.arange(10.0,D,5.0); HYSTERESIS=(0,2,4,6,8,10)
rng=np.random.default_rng(7)
def rss(distance,shadow): return P0-10*PATH_LOSS*np.log10(distance)+shadow
RSS1=rss(X,rng.normal(0,SHADOW_SD,X.size)); RSS2=rss(D-X,rng.normal(0,SHADOW_SD,X.size))
def run(H):
    serving=1; events=[]
    for x,a,b in zip(X,RSS1,RSS2):
        if serving==1 and b>a+H: serving=2; events.append((float(x),'1->2'))
        elif serving==2 and a>b+H: serving=1; events.append((float(x),'2->1'))
    return events
def main():
    summary=[]
    for H in HYSTERESIS:
        e=run(H); summary.append((H,len(e),max(len(e)-1,0)))
    print(f"{'H (dB)':>7}{'Handoffs':>10}{'Ping-pongs':>12}")
    for H,count,ping in summary: print(f"{H:7d}{count:10d}{ping:12d}")
    events=run(6); print("\nHandoff events with H = 6 dB (position in metres):",events)
    with (OUT/'hysteresis_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['hysteresis_db','handoffs','ping_pongs']); w.writerows(summary)
    with (OUT/'handoff_events_6db.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['position_m','transition']); w.writerows(events)
    # Two-panel SVG: RSS traces near the cell boundary and handoffs versus hysteresis.
    W,H=1100,470; svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" fill="white"/><style>text{{font-family:Arial;fill:#172033}}.g{{stroke:#d8e0ec;stroke-dasharray:4 4}}</style><text x="550" y="32" text-anchor="middle" font-size="20" font-weight="bold">Handoff and hysteresis simulation</text>']
    # Left panel: signal traces, sampled every 10 m for a crisp compact SVG.
    x0,y0,pw,ph=70,80,460,300; lo,hi=-155,-80
    for tick in (-150,-140,-130,-120,-110,-100,-90,-80):
        y=y0+ph-(tick-lo)/(hi-lo)*ph; svg += [f'<line class="g" x1="{x0}" y1="{y:.1f}" x2="{x0+pw}" y2="{y:.1f}"/>',f'<text x="{x0-7}" y="{y+4:.1f}" text-anchor="end" font-size="10">{tick}</text>']
    for arr,color,label in ((RSS1,'#2563eb','BS1'),(RSS2,'#e4572e','BS2')):
        pts=[]
        for i in range(0,len(X),2):
            px=x0+(X[i]-10)/(D-20)*pw; py=y0+ph-(arr[i]-lo)/(hi-lo)*ph; pts.append(f'{px:.1f},{py:.1f}')
        svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="1.8"/>')
    for i,(pos,transition) in enumerate(events):
        px=x0+(pos-10)/(D-20)*pw; svg.append(f'<line x1="{px:.1f}" y1="{y0}" x2="{px:.1f}" y2="{y0+ph}" stroke="#6b7280" stroke-opacity=".22"/>')
    svg += [f'<text x="{x0+pw/2}" y="{y0+ph+25}" text-anchor="middle" font-size="12">Mobile position (m)</text>',f'<text x="22" y="{y0+ph/2}" transform="rotate(-90 22 {y0+ph/2})" text-anchor="middle" font-size="12">RSS (dBm)</text>',f'<text x="{x0+pw-80}" y="{y0+15}" fill="#2563eb" font-size="12">BS1</text>',f'<text x="{x0+pw-45}" y="{y0+15}" fill="#e4572e" font-size="12">BS2</text>']
    # Right panel: event counts by hysteresis.
    x0,y0,pw,ph=625,80,410,300; ymax=40
    for tick in range(0,ymax+1,10):
        y=y0+ph-tick/ymax*ph; svg += [f'<line class="g" x1="{x0}" y1="{y:.1f}" x2="{x0+pw}" y2="{y:.1f}"/>',f'<text x="{x0-7}" y="{y+4:.1f}" text-anchor="end" font-size="10">{tick}</text>']
    points=[]
    for H,count,_ in summary:
        px=x0+H/10*pw; py=y0+ph-count/ymax*ph; points.append(f'{px:.1f},{py:.1f}'); svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#2457a7"/>')
    svg.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#2457a7" stroke-width="2.5"/>')
    for H in HYSTERESIS:
        px=x0+H/10*pw; svg.append(f'<text x="{px:.1f}" y="{y0+ph+22}" text-anchor="middle" font-size="10">{H}</text>')
    svg += [f'<text x="{x0+pw/2}" y="{y0+ph+45}" text-anchor="middle" font-size="12">Hysteresis margin (dB)</text>',f'<text x="{x0-43}" y="{y0+ph/2}" transform="rotate(-90 {x0-43} {y0+ph/2})" text-anchor="middle" font-size="12">Number of handoffs</text>','</svg>']
    (OUT/'handoff_hysteresis.svg').write_text('\n'.join(svg),encoding='utf-8')
if __name__=='__main__': main()
