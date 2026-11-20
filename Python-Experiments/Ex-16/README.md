# Experiment 16: Free-Space Path Loss and Received Power

**Tool:** Python  
**Aim:** Calculate free-space path loss (FSPL) and received power for a radio link at several distances and carrier frequencies.

## Link budget

- `FSPL (dB) = 20 log10(d_km) + 20 log10(f_MHz) + 32.44`
- `Pr (dBm) = Pt + Gt + Gr - FSPL`
- `Pr (W) = 10^(Pr_dBm/10) / 1000`

The simulation uses transmit power `Pt = 43 dBm`, transmit antenna gain `Gt = 15 dB`, receive antenna gain `Gr = 0 dB`, distances from `0.1 km` to `10 km`, and carrier frequencies `900 MHz` and `1800 MHz`.

## Run

Install NumPy, then run:

```bash
python experiment_16.py
```

The program prints the full result table and writes `results.csv` and `fspl_received_power.svg` beside the script.

## Result and observation

At 900 MHz and 1 km, FSPL is about `91.52 dB` and received power is about `-33.52 dBm` (`4.441e-7 W`). At 1800 MHz and the same distance, FSPL is about `97.55 dB`, approximately 6 dB higher, so the received power is approximately 6 dB lower. Doubling distance also adds about 6 dB of free-space path loss. These are ideal free-space calculations; buildings, terrain, fading, and other real propagation effects are not modeled.

**Conclusion:** FSPL and received power were calculated successfully for the requested distances and frequencies.

**Reference:** ITA03 Mobile Computing Laboratory Manual, Experiment 16, pages 34–36.

