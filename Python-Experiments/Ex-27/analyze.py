"""Average selected OMNeT++ scalars by the numUe iteration variable."""
import glob, re, shlex, collections
METRICS=("packetReceived:count","endToEndDelay:mean","packetSent:count")
data=collections.defaultdict(lambda:collections.defaultdict(list))
for filename in glob.glob("results/*.sca"):
    num_ue=None
    with open(filename,encoding="utf-8",errors="replace") as stream:
        for line in stream:
            if line.startswith("attr iterationvars "):
                match=re.search(r"\$numUe=(\d+)",line)
                if match: num_ue=int(match.group(1))
            elif line.startswith("scalar ") and num_ue is not None:
                parts=shlex.split(line)
                if len(parts)>=4 and parts[2] in METRICS:
                    data[num_ue][parts[2]].append(float(parts[3]))
print(f"{'UEs':>6}{'Mean received':>18}{'Mean delay (s)':>18}{'Packet loss':>16}")
for n in sorted(data):
    d=data[n]; rx=sum(d['packetReceived:count'])/max(len(d['packetReceived:count']),1); tx=sum(d['packetSent:count'])/max(len(d['packetSent:count']),1); delay=sum(d['endToEndDelay:mean'])/max(len(d['endToEndDelay:mean']),1); loss=max(0,(tx-rx)/tx) if tx else 0
    print(f"{n:6d}{rx:18.1f}{delay:18.4f}{loss:16.4%}")
if not data: print("No .sca scalar files found in results/; run the parameter study first.")
