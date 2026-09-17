"""Reference values for a structureless (uniform) distribution on the simplex.

Gives the null expectations of x_max and N_eff when the three momentum shares
are drawn uniformly from the 2-simplex, i.e. Dirichlet(1,1,1).  These numbers
make the measured values interpretable: they say what "no preference for equal
sharing" would look like.
"""

import random

random.seed(2024)
N = 2_000_000


def main() -> None:
  s_xmax = 0.0
  s_neff = 0.0
  for _ in range(N):
    # uniform point on the 2-simplex via two sorted uniforms
    u, v = sorted((random.random(), random.random()))
    x = (u, v - u, 1.0 - v)
    s_xmax += max(x)
    s_neff += 1.0 / sum(t * t for t in x)
  print(f"samples                 = {N}")
  print(f"<x_max>  uniform simplex = {s_xmax / N:.4f}   (exact 11/18 = {11/18:.4f})")
  print(f"<N_eff>  uniform simplex = {s_neff / N:.4f}")
  print()
  print("Sign sectors, independent symmetric signs:")
  print(f"P(all three same direction) = 2/8 = {2/8:.4f}")


if __name__ == "__main__":
  main()
