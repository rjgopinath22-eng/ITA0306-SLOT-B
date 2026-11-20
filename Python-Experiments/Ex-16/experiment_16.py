"""Experiment 16: Free-Space Path Loss and Received Power.

Run with: python experiment_16.py
Requires: numpy
"""
from pathlib import Path
import csv
import numpy as np

DISTANCES_KM = np.array([0.1, 0.5, 1.0, 2.0, 5.0, 10.0])
FREQUENCIES_MHZ = (900, 1800)
TX_POWER_DBM, TX_GAIN_DB, RX_GAIN_DB = 43.0, 15.0, 0.0
OUT = Path(__file__).resolve().parent


def fspl_db(distance_km, frequency_mhz):
    """Free-space path loss in dB, with distance in km and frequency in MHz."""
    if distance_km <= 0 or frequency_mhz <= 0:
        raise ValueError("Distance and frequency must be positive.")
    return 20 * np.log10(distance_km) + 20 * np.log10(frequency_mhz) + 32.44


def make_svg(results):
    """Write a lightweight vector plot without extra plotting libraries."""
    width, height = 1120, 480
    panels = [(60, 80, 460, 320, "Free-space path loss", "FSPL (dB)"),
              (600, 80, 460, 320, "Received power", "Pr (dBm)")]
    colors = {900: "#2563eb", 1800: "#e4572e"}
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="#ffffff"/>',
           '<style>text{font-family:Arial,sans-serif;fill:#172033}.grid{stroke:#d9e0ea;stroke-dasharray:4 5}.axis{stroke:#556274;stroke-width:1.5}</style>',
           '<text x="560" y="34" text-anchor="middle" font-size="22" font-weight="700">Experiment 16 | Free-space radio link</text>']
    for panel_index, (x, y, w, h, title, ylabel) in enumerate(panels):
        is_loss = panel_index == 0
        lows, highs = ((65, 125) if is_loss else (-65, -5))
        svg.append(f'<text x="{x+w/2}" y="{y-22}" text-anchor="middle" font-size="18" font-weight="700">{title}</text>')
        for tick in range(lows, highs + 1, 10):
            py = y + h - (tick-lows)/(highs-lows)*h
            svg.append(f'<line class="grid" x1="{x}" y1="{py:.1f}" x2="{x+w}" y2="{py:.1f}"/>')
            svg.append(f'<text x="{x-9}" y="{py+4:.1f}" text-anchor="end" font-size="12">{tick}</text>')
        for tick in (0, 2, 4, 6, 8, 10):
            px = x + tick/10*w
            svg.append(f'<line class="grid" x1="{px:.1f}" y1="{y}" x2="{px:.1f}" y2="{y+h}"/>')
            svg.append(f'<text x="{px:.1f}" y="{y+h+22}" text-anchor="middle" font-size="12">{tick}</text>')
        svg.extend([f'<line class="axis" x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}"/>',
                    f'<line class="axis" x1="{x}" y1="{y}" x2="{x}" y2="{y+h}"/>',
                    f'<text x="{x+w/2}" y="{y+h+48}" text-anchor="middle" font-size="14">Distance (km)</text>',
                    f'<text x="{x-48}" y="{y+h/2}" text-anchor="middle" font-size="14" transform="rotate(-90 {x-48} {y+h/2})">{ylabel}</text>'])
        for frequency, rows in results.items():
            points=[]
            for distance, loss, power in rows:
                value = loss if is_loss else power
                px=x+float(distance)/10*w; py=y+h-(value-lows)/(highs-lows)*h
                points.append(f'{px:.1f},{py:.1f}')
            svg.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{colors[frequency]}" stroke-width="3"/>')
            for pair in points:
                px,py=pair.split(','); svg.append(f'<circle cx="{px}" cy="{py}" r="4" fill="{colors[frequency]}"/>')
            ly=y+20+(frequency==1800)*22
            svg.extend([f'<line x1="{x+w-95}" y1="{ly-4}" x2="{x+w-70}" y2="{ly-4}" stroke="{colors[frequency]}" stroke-width="3"/>',
                        f'<text x="{x+w-64}" y="{ly}" font-size="12">{frequency} MHz</text>'])
    svg.append('</svg>')
    (OUT/"fspl_received_power.svg").write_text("\n".join(svg), encoding="utf-8")


def main():
    results={}
    with (OUT/"results.csv").open("w", newline="", encoding="utf-8") as stream:
        writer=csv.writer(stream); writer.writerow(["frequency_mhz","distance_km","fspl_db","received_power_dbm","received_power_w"])
        for frequency in FREQUENCIES_MHZ:
            print(f"\nFrequency = {frequency} MHz")
            print(f"{'d (km)':>8}{'FSPL (dB)':>12}{'Pr (dBm)':>11}{'Pr (W)':>14}")
            rows=[]
            for distance in DISTANCES_KM:
                loss=float(fspl_db(float(distance),frequency))
                power=TX_POWER_DBM+TX_GAIN_DB+RX_GAIN_DB-loss
                watts=10**(power/10)/1000
                rows.append((float(distance),loss,power))
                writer.writerow([frequency,f"{distance:.1f}",f"{loss:.2f}",f"{power:.2f}",f"{watts:.6e}"])
                print(f"{distance:8.1f}{loss:12.2f}{power:11.2f}{watts:14.3e}")
            results[frequency]=rows
    make_svg(results)
    print("\nSaved results.csv and fspl_received_power.svg")


if __name__ == "__main__":
    main()
