"""Compute PDR and routing overhead from a CSV exported from OMNeT++ results."""
import csv, sys
from pathlib import Path
path=Path(sys.argv[1] if len(sys.argv)>1 else "metrics.csv")
with path.open(newline="",encoding="utf-8-sig") as f:
    rows=list(csv.DictReader(f))
print("protocol, pdr, mean_delay_s, routing_overhead")
for protocol in sorted({r["protocol"] for r in rows}):
    group=[r for r in rows if r["protocol"]==protocol]
    sent=sum(int(r["packets_sent"]) for r in group); received=sum(int(r["packets_received"]) for r in group); control=sum(int(r["routing_control_packets"]) for r in group)
    delay=sum(float(r["mean_delay_s"]) for r in group)/len(group)
    print(f"{protocol}, {received/sent:.4f}, {delay:.6f}, {control/max(received,1):.4f}")
