"""Numeric cross-check of every \\num{...} in main.tex.

Builds a corpus of every number produced by the analysis (independent
re-verification, Monte Carlo reference, ponderomotive table, and every result
CSV in the repo) and checks that each number quoted in the thesis matches one
of them at the precision at which it is quoted.
"""
import glob
import re

scratch = "/usr/local/google/home/nepravskaya/.gemini/jetski/brain/dcc3adce-ae1f-4d51-bca8-dff7bf3d770f/scratch/"
repo = scratch + "praca-licencjacka/"

sources = [
    scratch + "verify_output.txt",
    scratch + "ponderomotive_output.txt",
    scratch + "simplex_reference_output.txt",
]
sources += sorted(glob.glob(repo + "PCA_results/*.csv"))
sources += sorted(glob.glob(repo + "momentum_sharing_results/*.csv"))
sources += sorted(glob.glob(repo + "ECBB_model/**/README.txt", recursive=True))

corpus = []
for p in sources:
    try:
        corpus.append(open(p, encoding="utf-8", errors="replace").read())
    except OSError as e:
        print("skip", p, e)
blob = "\n".join(corpus)
print(f"reference sources: {len(corpus)}")

ref = set()
for tok in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", blob):
    try:
        ref.add(float(tok))
    except ValueError:
        pass
ref = sorted(ref)
print(f"distinct reference numbers: {len(ref)}")
print()


def matches(x, decimals):
    """True if some reference number rounds to x at the quoted precision."""
    tol = 0.5 * 10 ** (-decimals) * 1.0000001
    for y in ref:
        if abs(y - x) <= tol:
            return True
        # also allow percentage / fraction interchange
        if abs(y * 100 - x) <= tol or abs(y / 100 - x) <= tol:
            return True
    return False


tex = open(repo + "main.tex", encoding="utf-8").read()
seen, unmatched = set(), []
for i, line in enumerate(tex.splitlines(), 1):
    for v in re.findall(r"\\num\{([^}]*)\}", line):
        if v in seen:
            continue
        seen.add(v)
        try:
            x = float(v)
        except ValueError:
            unmatched.append((i, v, "NOT A NUMBER", line.strip()))
            continue
        d = len(v.split(".")[1].split("e")[0]) if "." in v else 0
        if "e" in v.lower():
            d = 12  # relative scale; handled separately below
            if any(abs(y - x) <= abs(x) * 0.05 for y in ref):
                continue
            unmatched.append((i, v, "sci-notation", line.strip()))
            continue
        if not matches(x, d):
            unmatched.append((i, v, "no match", line.strip()))

print(f"unique \\num values: {len(seen)}")
print(f"UNMATCHED: {len(unmatched)}")
print()
for i, v, why, line in unmatched:
    print(f"L{i:5d}  {v:>10}  [{why}]  | {line[:100]}")
