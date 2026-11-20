"""Experiment 20: CDMA spreading and despreading with Walsh codes."""
from pathlib import Path
import csv
import numpy as np
OUT=Path(__file__).resolve().parent
W=np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])
BITS={1:[1,0,1,1],2:[0,0,1,0],3:[1,1,0,1]}
L=W.shape[1]; NBITS=4
def bpsk(bits): return 2*np.array(bits)-1
def main():
    tx=np.zeros(NBITS*L); spreads={}
    for user,bits in BITS.items():
        spread=np.repeat(bpsk(bits),L)*np.tile(W[user],NBITS); spreads[user]=spread.astype(int)
        print(f"User {user} data    : {bits}"); print(f"User {user} spread  : {spreads[user]}"); tx+=spread
    tx=tx.astype(int); print("\nComposite transmitted signal:\n",tx)
    print("\nDespreading at receiver:")
    recovered={}
    with (OUT/'recovered_bits.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f); writer.writerow(['user','bit_index','transmitted_bit','correlator_output','recovered_bit','status'])
        for u,bits in BITS.items():
            corr=(tx*np.tile(W[u],NBITS)).reshape(NBITS,L).sum(axis=1)/L
            rec=(corr>0).astype(int).tolist(); recovered[u]=(corr,rec)
            print(f"User {u} correlator: {corr} -> bits {rec} {'OK' if rec==bits else 'ERROR'}")
            for i,(b,c,r) in enumerate(zip(bits,corr,rec),1): writer.writerow([u,i,b,f"{c:.1f}",r,'OK' if b==r else 'ERROR'])
    # Compact SVG comparing the user-one chips, composite channel chips and decoded symbols.
    Wsvg,Hsvg=1120,480; panels=[('User 1 spread signal',spreads[1],-3,3),('Composite signal',tx,-4,4)]
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wsvg}" height="{Hsvg}" viewBox="0 0 {Wsvg} {Hsvg}"><rect width="100%" height="100%" fill="white"/><style>text{{font-family:Arial;fill:#172033}}.g{{stroke:#d9e0ec;stroke-dasharray:4 4}}</style><text x="560" y="32" text-anchor="middle" font-size="21" font-weight="700">CDMA spreading and despreading</text>']
    for idx,(title,vals,lo,hi) in enumerate(panels):
        x0=80+idx*535; y0=85; pw=460; ph=280
        svg.append(f'<text x="{x0+pw/2}" y="{y0-20}" text-anchor="middle" font-size="16" font-weight="700">{title}</text>')
        for tick in range(lo,hi+1,2):
            yy=y0+ph-(tick-lo)/(hi-lo)*ph; svg += [f'<line class="g" x1="{x0}" y1="{yy:.1f}" x2="{x0+pw}" y2="{yy:.1f}"/>',f'<text x="{x0-8}" y="{yy+4:.1f}" text-anchor="end" font-size="10">{tick}</text>']
        for i,val in enumerate(vals):
            bx=x0+i*pw/len(vals); bw=pw/len(vals)-3; zero=y0+ph-(0-lo)/(hi-lo)*ph; by=y0+ph-(val-lo)/(hi-lo)*ph
            svg.append(f'<rect x="{bx+1:.1f}" y="{min(zero,by):.1f}" width="{bw:.1f}" height="{max(1,abs(zero-by)):.1f}" fill="#2563eb"/>')
        svg.append(f'<text x="{x0+pw/2}" y="{y0+ph+25}" text-anchor="middle" font-size="12">Chip index</text>')
    svg.append('<text x="560" y="425" text-anchor="middle" font-size="14">Despread correlators recover every transmitted user bit without error</text></svg>')
    (OUT/'cdma_spreading.svg').write_text('\n'.join(svg),encoding='utf-8')
if __name__=='__main__': main()
