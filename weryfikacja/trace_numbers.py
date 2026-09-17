"""Trace every number in the thesis back to a named source file.

The point is that you should be able to check each number yourself. For every
\\num{...} in main.tex this reports WHICH file it can be found in, grouped into:

  A. your own notebook output   (PCA_results/*.csv, momentum_sharing_results/*.csv)
  B. the data files themselves  (ECBB_model README event counts)
  C. extra analysis I ran       (verify_output.txt, simplex_reference, ponderomotive)

Numbers in group A you can confirm by opening your own CSV.
Numbers in group C exist only because of scripts added on top of your notebooks.
"""
import glob
import re
from collections import defaultdict

scratch = "/usr/local/google/home/nepravskaya/.gemini/jetski/brain/dcc3adce-ae1f-4d51-bca8-dff7bf3d770f/scratch/"
repo = scratch + "praca-licencjacka/"

groups = {
    "A. twoje notebooki (CSV)": (
        sorted(glob.glob(repo + "PCA_results/*.csv"))
        + sorted(glob.glob(repo + "momentum_sharing_results/*.csv"))
    ),
    "B. dane zrodlowe (README)": sorted(
        glob.glob(repo + "ECBB_model/**/README.txt", recursive=True)
    ),
    "C. dodatkowa analiza (moje skrypty)": [
        scratch + "verify_output.txt",
        scratch + "simplex_reference_output.txt",
        scratch + "ponderomotive_output.txt",
    ],
}

numbers_in = {}
for g, paths in groups.items():
    vals = set()
    for p in paths:
        try:
            blob = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for tok in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", blob):
            try:
                vals.add(float(tok))
            except ValueError:
                pass
    numbers_in[g] = sorted(vals)
    print(f"{g}: {len(paths)} plikow, {len(vals)} liczb")
print()


def found_in(x, decimals, vals):
    tol = 0.5 * 10 ** (-decimals) * 1.0000001
    return any(abs(y - x) <= tol or abs(abs(y) - abs(x)) <= tol for y in vals)


tex = open(repo + "main.tex", encoding="utf-8").read()
seen = set()
counts = defaultdict(int)
only_c = []
nowhere = []

for i, line in enumerate(tex.splitlines(), 1):
    for v in re.findall(r"\\num\{([^}]*)\}", line):
        if v in seen:
            continue
        seen.add(v)
        try:
            x = float(v)
        except ValueError:
            continue
        d = len(v.split(".")[1].split("e")[0]) if "." in v and "e" not in v.lower() else 0
        if "e" in v.lower():
            hits = [g for g, vals in numbers_in.items()
                    if any(abs(y - x) <= abs(x) * 0.05 for y in vals)]
        else:
            hits = [g for g, vals in numbers_in.items() if found_in(x, d, vals)]

        if not hits:
            nowhere.append((i, v, line.strip()[:90]))
            counts["NIGDZIE"] += 1
        else:
            for g in hits:
                counts[g] += 1
            if hits == ["C. dodatkowa analiza (moje skrypty)"]:
                only_c.append((i, v, line.strip()[:90]))

print(f"unikalnych liczb w pracy: {len(seen)}\n")
print("w ilu grupach zrodel da sie je znalezc:")
for g in list(groups) + ["NIGDZIE"]:
    print(f"  {g}: {counts[g]}")

print(f"\n--- liczby dostepne WYLACZNIE z mojej dodatkowej analizy: {len(only_c)} ---")
for i, v, line in only_c:
    print(f"  L{i:5d} {v:>10}  | {line}")

print(f"\n--- liczby nieznalezione nigdzie: {len(nowhere)} ---")
for i, v, line in nowhere:
    print(f"  L{i:5d} {v:>10}  | {line}")
