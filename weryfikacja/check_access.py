"""Check open-access status and a free full-text link for every reference.

Uses OpenAlex (no API key required). Reports, per entry, whether a legally free
full text exists and where, so it is clear which references a reader without a
university subscription can actually open.
"""
import json
import re
import time
import urllib.parse
import urllib.request

BIB = "/usr/local/google/home/nepravskaya/praca-licencjacka/bibliography.bib"
UA = "thesis-access-check/1.0"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


text = open(BIB, encoding="utf-8").read()
entries = []
for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
    f = {}
    for fm in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}\s*(?:,|\s*$)", m.group(3), re.S):
        f[fm.group(1).lower()] = " ".join(fm.group(2).split())
    entries.append((m.group(2).strip(), f))

rows = []
for key, f in entries:
    doi, title = f.get("doi"), f.get("title", "")
    w = None
    try:
        if doi:
            w = get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi))
        else:
            q = urllib.parse.urlencode({"filter": "title.search:" + re.sub(r"[^\w ]", " ", title)[:90]})
            res = get("https://api.openalex.org/works?" + q).get("results", [])
            w = res[0] if res else None
    except Exception as e:  # noqa: BLE001
        rows.append((key, "LOOKUP FAILED", str(e)[:50], ""))
        time.sleep(0.3)
        continue

    if not w:
        rows.append((key, "NOT IN OPENALEX", "-", ""))
    else:
        oa = w.get("open_access", {})
        status = oa.get("oa_status", "?")
        url = oa.get("oa_url") or ""
        cites = w.get("cited_by_count", "?")
        rows.append((key, status, f"cyt.:{cites}", url))
    time.sleep(0.3)

print(f"{'klucz':<20} {'OA status':<16} {'cytowania':<12} link")
print("-" * 110)
for key, status, cites, url in rows:
    print(f"{key:<20} {status:<16} {cites:<12} {url[:60]}")

print()
free = [r for r in rows if r[1] in ("gold", "green", "hybrid", "bronze", "diamond")]
closed = [r for r in rows if r[1] == "closed"]
other = [r for r in rows if r not in free and r not in closed]
print(f"darmowo dostepne online : {len(free)}")
print(f"za paywallem            : {len(closed)}")
print(f"do sprawdzenia recznie  : {len(other)}  -> {[r[0] for r in other]}")
