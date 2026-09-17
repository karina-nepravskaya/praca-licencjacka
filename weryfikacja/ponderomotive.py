"""Ponderomotive energy and drift-momentum scales for the analysed pulses.

U_p = I / (4 omega^2) in atomic units; 2*sqrt(U_p) is the classical drift
momentum of an electron released at a zero of the vector potential.
"""

import math

I_AU = 3.5094452e16  # atomic unit of intensity, W/cm^2
OMEGA = lambda nm: 45.5633 / nm  # photon frequency in atomic units

PULSES = [
    (1.0, 800.0),
    (1.3, 800.0),
    (1.6, 800.0),
    (1.7, 760.0),
]


def main() -> None:
  print(f"{'I [PW/cm2]':>11} {'lambda [nm]':>12} {'omega [a.u.]':>13} "
        f"{'U_p [a.u.]':>11} {'2sqrt(Up)':>10} {'3x2sqrt(Up)':>12}")
  for i_pw, lam in PULSES:
    i_au = i_pw * 1e15 / I_AU
    w = OMEGA(lam)
    up = i_au / (4.0 * w * w)
    drift = 2.0 * math.sqrt(up)
    print(f"{i_pw:>11.1f} {lam:>12.0f} {w:>13.5f} "
          f"{up:>11.3f} {drift:>10.3f} {3*drift:>12.3f}")


if __name__ == "__main__":
  main()
