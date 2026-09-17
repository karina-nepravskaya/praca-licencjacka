"""Independent re-analysis and verification of the momentum-sharing observables.

Pure-stdlib re-implementation (no numpy/pandas) of every quantity used in the
thesis, recomputed directly from the raw ECBB momentum files.  On top of the
notebook results it adds:

  * exact orthogonality / invertibility checks of the Jacobi-Helmert transform,
  * a longitudinal momentum-conservation test using the ion momentum,
  * a label-exchange symmetry test between the two initially bound electrons,
  * analytic standard errors and 95% confidence intervals for all means,
  * Welch tests for the direct/delayed differences,
  * a quantitative bridge to the simplex (Dalitz) representation.
"""

import math
import os
from collections import Counter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "praca-licencjacka")

FOLDERS = {
    1.0: os.path.join(ROOT, "ECBB_model/1.0PW_cm^2"),
    1.3: os.path.join(ROOT, "ECBB_model/1.3PW_cm^2"),
    1.6: os.path.join(ROOT, "ECBB_model/1.6PW_cm^2"),
    1.7: os.path.join(ROOT, "ECBB_model/data/data_Neon/ECBB_model/1.7PW_cm^2"),
}
CLASSES = {
    "all": "momenta_all_events.txt",
    "direct": "momenta_direct_events.txt",
    "delayed": "momenta_delayed_events.txt",
}

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)


def load(path):
  """Returns a list of events, each a list of the 12 momentum components."""
  events = []
  with open(path, encoding="utf-8") as f:
    for line in f:
      line = line.strip()
      if not line or line.startswith("#"):
        continue
      parts = [p for p in line.replace(",", " ").split() if p]
      if len(parts) != 12:
        raise ValueError(f"expected 12 columns, got {len(parts)} in {path}")
      events.append([float(p) for p in parts])
  return events


def observables(events):
  """Computes every derived quantity for one dataset."""
  rows = []
  for ev in events:
    p1z = ev[2]
    p2, p3, p4 = ev[5], ev[8], ev[11]
    pe = p2 + p3 + p4
    q = pe / SQRT3
    xi1 = (p2 - p3) / SQRT2
    xi2 = (p2 + p3 - 2.0 * p4) / SQRT6
    k = math.hypot(xi1, xi2)
    a = abs(p2) + abs(p3) + abs(p4)
    x2, x3, x4 = abs(p2) / a, abs(p3) / a, abs(p4) / a
    n_eff = 1.0 / (x2 * x2 + x3 * x3 + x4 * x4)
    sector = "".join("+" if v > 0 else "-" for v in (p2, p3, p4))
    rows.append({
        "p2": p2, "p3": p3, "p4": p4, "p1z": p1z,
        "P_e": pe, "Q": q, "xi1": xi1, "xi2": xi2, "K": k,
        "A": a, "x2": x2, "x3": x3, "x4": x4,
        "N_eff": n_eff, "x_max": max(x2, x3, x4), "x_min": min(x2, x3, x4),
        "K_over_A": k / a,
        "sector": sector,
        "P_total_z": p1z + pe,
        "norm_err": p2**2 + p3**2 + p4**2 - q**2 - xi1**2 - xi2**2,
        "rec_err": abs(p2 - (q / SQRT3 + xi1 / SQRT2 + xi2 / SQRT6)),
        "sum_x_err": abs(x2 + x3 + x4 - 1.0),
    })
  return rows


def col(rows, name):
  return [r[name] for r in rows]


def mean(v):
  return sum(v) / len(v)


def sd(v):
  m = mean(v)
  return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def mean_ci(v):
  """Mean with analytic 95% CI from the central limit theorem."""
  m, s, n = mean(v), sd(v), len(v)
  half = 1.96 * s / math.sqrt(n)
  return m, m - half, m + half


def pearson(a, b):
  ma, mb = mean(a), mean(b)
  num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
  da = math.sqrt(sum((x - ma) ** 2 for x in a))
  db = math.sqrt(sum((y - mb) ** 2 for y in b))
  return num / (da * db)


def fisher_ci(r, n):
  z = math.atanh(r)
  se = 1.0 / math.sqrt(n - 3)
  return math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)


def welch(a, b):
  """Welch t statistic and two-sided p-value (normal approximation)."""
  ma, mb = mean(a), mean(b)
  va, vb = sd(a) ** 2 / len(a), sd(b) ** 2 / len(b)
  t = (ma - mb) / math.sqrt(va + vb)
  p = math.erfc(abs(t) / math.sqrt(2.0))
  return t, p


def main():
  data = {}
  for intensity, folder in FOLDERS.items():
    for cls, fname in CLASSES.items():
      data[(intensity, cls)] = observables(load(os.path.join(folder, fname)))
  keys = sorted(data)

  print("#" * 78)
  print("# 1. VALIDATION of the orthogonal transformation (p2,p3,p4)->(Q,xi1,xi2)")
  print("#" * 78)
  print(f"{'max |norm error|':<34}"
        f"{max(max(abs(x) for x in col(d,'norm_err')) for d in data.values()):.3e}")
  print(f"{'max |reconstruction error|':<34}"
        f"{max(max(col(d,'rec_err')) for d in data.values()):.3e}")
  print(f"{'max |x2+x3+x4-1|':<34}"
        f"{max(max(col(d,'sum_x_err')) for d in data.values()):.3e}")

  print()
  print("#" * 78)
  print("# 2. LONGITUDINAL MOMENTUM CONSERVATION  (p1z + p2z + p3z + p4z)")
  print("#" * 78)
  for key in keys:
    d = data[key]
    tot = col(d, "P_total_z")
    r = pearson(col(d, "p1z"), col(d, "P_e"))
    print(f"I={key[0]:<4} {key[1]:<8} n={len(d):>6}  mean={mean(tot):+.4f}  "
          f"sd={sd(tot):.4f}  max|.|={max(abs(x) for x in tot):.3f}  "
          f"corr(p1z,P_e)={r:+.4f}")

  print()
  print("#" * 78)
  print("# 3. LABEL-EXCHANGE SYMMETRY  (electrons 2 and 3 are both 'initially bound')")
  print("#" * 78)
  for key in keys:
    d = data[key]
    p2, p3, p4 = col(d, "p2"), col(d, "p3"), col(d, "p4")
    _, p23 = welch(p2, p3)
    print(f"I={key[0]:<4} {key[1]:<8} "
          f"<p2>={mean(p2):+.3f} <p3>={mean(p3):+.3f} <p4>={mean(p4):+.3f} | "
          f"sd2={sd(p2):.3f} sd3={sd(p3):.3f} sd4={sd(p4):.3f} | "
          f"p(2 vs 3)={p23:.3f}")

  print()
  print("#" * 78)
  print("# 4. MAIN OBSERVABLES with 95% confidence intervals")
  print("#" * 78)
  print(f"{'I':<5}{'class':<9}{'n':>7}  {'<P_e>':<22}{'sd(P_e)':<9}"
        f"{'<K>':<22}{'<N_eff>':<22}{'<x_max>':<22}")
  for key in keys:
    d = data[key]
    pe = mean_ci(col(d, "P_e"))
    k = mean_ci(col(d, "K"))
    ne = mean_ci(col(d, "N_eff"))
    xm = mean_ci(col(d, "x_max"))
    print(f"{key[0]:<5}{key[1]:<9}{len(d):>7}  "
          f"{pe[0]:+.3f} [{pe[1]:+.3f},{pe[2]:+.3f}]  {sd(col(d,'P_e')):<9.3f}"
          f"{k[0]:.3f} [{k[1]:.3f},{k[2]:.3f}]     "
          f"{ne[0]:.3f} [{ne[1]:.3f},{ne[2]:.3f}]     "
          f"{xm[0]:.3f} [{xm[1]:.3f},{xm[2]:.3f}]")

  print()
  print("#" * 78)
  print("# 5. PAIR CORRELATIONS of longitudinal momenta with Fisher 95% CI")
  print("#" * 78)
  for key in keys:
    d = data[key]
    n = len(d)
    out = [f"I={key[0]:<4} {key[1]:<8} n={n:>6}"]
    for a, b, name in (("p2", "p3", "r23"), ("p2", "p4", "r24"),
                       ("p3", "p4", "r34")):
      r = pearson(col(d, a), col(d, b))
      lo, hi = fisher_ci(r, n)
      out.append(f"{name}={r:+.3f}[{lo:+.3f},{hi:+.3f}]")
    print("  ".join(out))

  print()
  print("#" * 78)
  print("# 6. SIGN SECTORS: same-direction versus mixed emission")
  print("#" * 78)
  for key in keys:
    d = data[key]
    n = len(d)
    c = Counter(col(d, "sector"))
    f_ppp, f_mmm = c["+++"] / n, c["---"] / n
    same = f_ppp + f_mmm
    print(f"I={key[0]:<4} {key[1]:<8} n={n:>6} "
          f"+++={f_ppp:.4f} ---={f_mmm:.4f} same={same:.4f} mixed={1-same:.4f}")

  print()
  print("#" * 78)
  print("# 7. DIRECT versus DELAYED at fixed intensity (Welch test)")
  print("#" * 78)
  for intensity in sorted(FOLDERS):
    dd, de = data[(intensity, "direct")], data[(intensity, "delayed")]
    for obs in ("K", "N_eff", "x_max", "K_over_A"):
      a, b = col(dd, obs), col(de, obs)
      t, p = welch(a, b)
      pstr = "<1e-16" if p < 1e-16 else f"{p:.2e}"
      print(f"I={intensity:<4} {obs:<9} direct={mean(a):.3f} "
            f"delayed={mean(b):.3f} diff={mean(a)-mean(b):+.3f} "
            f"t={t:+.1f} p={pstr}")
    print()

  print("#" * 78)
  print("# 8. RANGE CHECKS of the bounded observables")
  print("#" * 78)
  for key in keys:
    d = data[key]
    ne, xm = col(d, "N_eff"), col(d, "x_max")
    print(f"I={key[0]:<4} {key[1]:<8} "
          f"N_eff in [{min(ne):.4f},{max(ne):.4f}]  "
          f"x_max in [{min(xm):.4f},{max(xm):.4f}]")

  print()
  print("#" * 78)
  print("# 9. SIMPLEX EQUIVALENCE: shares grouped by sign sector")
  print("#    (x2,x3,x4) are the barycentric coordinates of the Dalitz triangle,")
  print("#    the sign sectors are the 8 faces of the octahedron.")
  print("#    centre of a face -> N_eff = 3, x_max = 1/3 = 0.333")
  print("#    middle of an edge -> N_eff = 2, x_max = 1/2, x_min = 0")
  print("#" * 78)
  for intensity in sorted(FOLDERS):
    for cls in ("direct", "delayed"):
      d = data[(intensity, cls)]
      groups = {
          "same-dir": [r for r in d if r["sector"] in ("+++", "---")],
          "mixed": [r for r in d if r["sector"] not in ("+++", "---")],
      }
      for name, sub in groups.items():
        if not sub:
          continue
        print(f"I={intensity:<4} {cls:<8} {name:<9} n={len(sub):>6} "
              f"<N_eff>={mean(col(sub,'N_eff')):.3f} "
              f"<x_max>={mean(col(sub,'x_max')):.3f} "
              f"<x_min>={mean(col(sub,'x_min')):.3f}")
    print()

  print("#" * 78)
  print("# 10. MINORITY ELECTRON in the mixed sectors")
  print("#     tests the simplex-method claim that the electron moving against")
  print("#     the other two carries only a small share of the momentum")
  print("#" * 78)
  for intensity in sorted(FOLDERS):
    for cls in ("direct", "delayed"):
      d = data[(intensity, cls)]
      minor, major = [], []
      for r in d:
        if r["sector"] in ("+++", "---"):
          continue
        signs = [r["p2"] > 0, r["p3"] > 0, r["p4"] > 0]
        shares = [r["x2"], r["x3"], r["x4"]]
        n_pos = sum(signs)
        idx = signs.index(True) if n_pos == 1 else signs.index(False)
        minor.append(shares[idx])
        major.extend(s for i, s in enumerate(shares) if i != idx)
      if not minor:
        continue
      minor_sorted = sorted(minor)
      med = minor_sorted[len(minor_sorted) // 2]
      print(f"I={intensity:<4} {cls:<8} n_mixed={len(minor):>6} "
            f"<x_minority>={mean(minor):.3f} median={med:.3f} "
            f"<x_majority>={mean(major):.3f} "
            f"frac(x_minority<0.15)={sum(1 for x in minor if x < 0.15)/len(minor):.3f}")
    print()

  print("#" * 78)
  print("# 11. INVARIANCE of the scalar observables under label permutations")
  print("#     N_eff and x_max are symmetric functions of (x2,x3,x4), so averaging")
  print("#     over the 3! permutations must leave them unchanged")
  print("#" * 78)
  perms = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
  for key in [(1.3, "direct"), (1.3, "delayed")]:
    d = data[key]
    ne_sym, xm_sym = [], []
    for r in d:
      s = [r["x2"], r["x3"], r["x4"]]
      for p in perms:
        v = [s[i] for i in p]
        ne_sym.append(1.0 / sum(t * t for t in v))
        xm_sym.append(max(v))
    print(f"I={key[0]} {key[1]:<8} "
          f"<N_eff>: original={mean(col(d,'N_eff')):.10f} "
          f"symmetrised={mean(ne_sym):.10f} "
          f"diff={abs(mean(col(d,'N_eff'))-mean(ne_sym)):.2e}")
    print(f"{'':>13} "
          f"<x_max>: original={mean(col(d,'x_max')):.10f} "
          f"symmetrised={mean(xm_sym):.10f} "
          f"diff={abs(mean(col(d,'x_max'))-mean(xm_sym)):.2e}")

  print()
  print("#" * 78)
  print("# 12. SHAPE OF THE RELATIVE PLANE (xi1, xi2)")
  print("#     exchanging electrons 2 and 3 maps xi1 -> -xi1 and leaves xi2 fixed,")
  print("#     so the distribution must be symmetric in xi1 (skewness ~ 0).")
  print("#     sd(xi2) > sd(xi1) measures how strongly the labelling separates")
  print("#     the initially bound pair from the initially tunnelling electron.")
  print("#" * 78)
  for key in keys:
    d = data[key]
    x1, x2v = col(d, "xi1"), col(d, "xi2")
    s1, s2 = sd(x1), sd(x2v)
    m1 = mean(x1)
    skew1 = (sum((v - m1) ** 3 for v in x1) / len(x1)) / s1**3
    print(f"I={key[0]:<4} {key[1]:<8} "
          f"<xi1>={m1:+.3f} <xi2>={mean(x2v):+.3f} | "
          f"sd(xi1)={s1:.3f} sd(xi2)={s2:.3f} ratio={s2/s1:.3f} | "
          f"skew(xi1)={skew1:+.3f}")

  print()
  print("#" * 78)
  print("# 13. WHICH ELECTRON IS THE MINORITY ONE IN THE MIXED SECTORS?")
  print("#     If the three labels were statistically equivalent each electron")
  print("#     would play the minority role in 1/3 = 0.333 of the mixed events.")
  print("#" * 78)
  for key in keys:
    d = data[key]
    counts = [0, 0, 0]
    for r in d:
      signs = [r["p2"] > 0, r["p3"] > 0, r["p4"] > 0]
      n_pos = sum(signs)
      if n_pos in (0, 3):
        continue
      idx = signs.index(True) if n_pos == 1 else signs.index(False)
      counts[idx] += 1
    tot = sum(counts)
    if tot == 0:
      continue
    f2, f3, f4 = (c / tot for c in counts)
    # binomial standard error for the tunnelling electron fraction
    se4 = math.sqrt(f4 * (1 - f4) / tot)
    print(f"I={key[0]:<4} {key[1]:<8} n_mixed={tot:>6}  "
          f"e2={f2:.3f}  e3={f3:.3f}  e4(tunnelling)={f4:.3f}+-{se4:.3f}  "
          f"ratio e4/[(e2+e3)/2]={f4/((f2+f3)/2):.3f}")


if __name__ == "__main__":
  main()
