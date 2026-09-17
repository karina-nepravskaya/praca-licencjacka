"""Validate every bibliography entry against Crossref, and look for an open-access copy.

For each entry with a DOI the script resolves it through the Crossref REST API
and compares title, first author, year, volume and first page with what the
.bib claims. Entries without a DOI are reported separately for manual checking.

Open access: Crossref reports licences and any free full-text links; in addition
the arXiv API is searched by title, because most strong-field physics papers
have a freely readable preprint.
"""
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BIB = "/usr/local/google/home/nepravskaya/praca-licencjacka/bibliography.bib"
UA = "thesis-bib-check/1.0 (mailto:nepravskaya@example.org)"


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def parse_bib(path):
    text = open(path, encoding="utf-8").read()
    entries = []
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        kind, key, body = m.group(1), m.group(2).strip(), m.group(3)
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}\s*(?:,|\s*$)", body, re.S):
            fields[fm.group(1).lower()] = " ".join(fm.group(2).split())
        entries.append((kind, key, fields))
    return entries


def norm(s):
    s = re.sub(r"\$[^$]*\$", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    return " ".join(s.split())


def crossref(doi):
    try:
        data = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi)))
        return data["message"]
    except Exception as e:  # noqa: BLE001 - want the reason in the report
        return {"__error__": str(e)}


def arxiv(title):
    q = urllib.parse.urlencode({
        "search_query": 'ti:"' + title[:120].replace('"', "") + '"',
        "max_results": "1",
    })
    try:
        root = ET.fromstring(get("http://export.arxiv.org/api/query?" + q))
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for e in root.findall("a:entry", ns):
            t = " ".join(e.find("a:title", ns).text.split())
            link = e.find("a:id", ns).text
            return t, link
    except Exception:  # noqa: BLE001
        pass
    return None, None


entries = parse_bib(BIB)
print(f"parsed entries: {len(entries)}\n")

problems = []
for kind, key, f in entries:
    doi = f.get("doi")
    print("=" * 78)
    print(f"{key}   ({kind})")
    print(f"  bib: {f.get('author','?')[:70]}")
    print(f"       {f.get('title','?')[:70]}")
    print(f"       {f.get('journal', f.get('publisher', f.get('school','?')))[:60]} "
          f"vol={f.get('volume','-')} p={f.get('pages','-')} ({f.get('year','?')})")

    if not doi:
        print("  DOI: none -> needs manual check")
        problems.append((key, "no DOI"))
    else:
        m = crossref(doi)
        if "__error__" in m:
            print(f"  DOI: {doi}  -> CROSSREF FAILED: {m['__error__']}")
            problems.append((key, f"DOI unresolvable: {doi}"))
        else:
            ct = " ".join(m.get("title", ["?"])[0].split())
            cyear = (m.get("issued", {}).get("date-parts", [[None]])[0][0])
            cvol = m.get("volume", "-")
            cpage = m.get("page", m.get("article-number", "-"))
            cjour = (m.get("container-title") or ["-"])[0]
            cauth = m.get("author", [{}])[0].get("family", "?")
            print(f"  DOI: {doi}  -> RESOLVES")
            print(f"  xref: {cauth} | {ct[:66]}")
            print(f"        {cjour[:60]} vol={cvol} p={cpage} ({cyear})")

            bt, xt = norm(f.get("title", "")), norm(ct)
            if bt and xt and bt not in xt and xt not in bt:
                print("  !! TITLE MISMATCH")
                problems.append((key, "title mismatch"))
            if f.get("year") and cyear and str(cyear) != f["year"]:
                print(f"  !! YEAR: bib {f['year']} vs crossref {cyear}")
                problems.append((key, f"year {f['year']} vs {cyear}"))
            if f.get("volume") and cvol != "-" and f["volume"] != str(cvol):
                print(f"  !! VOLUME: bib {f['volume']} vs crossref {cvol}")
                problems.append((key, f"volume {f['volume']} vs {cvol}"))
            bp = re.sub(r"\(.*\)", "", f.get("pages", "")).strip()
            cp = str(cpage).split("-")[0].strip()
            if bp and cp != "-" and bp != cp:
                print(f"  ?  PAGE: bib {bp} vs crossref {cpage}")
                problems.append((key, f"page {bp} vs {cpage}"))

            lic = m.get("license") or []
            if lic:
                print(f"  licence: {lic[0].get('URL','?')[:60]}")

    if f.get("title") and kind == "article":
        at, alink = arxiv(f["title"])
        if alink:
            same = norm(f["title"])[:40] in norm(at)
            print(f"  arXiv: {alink}  {'(title matches)' if same else '(DIFFERENT TITLE: ' + at[:50] + ')'}")
        else:
            print("  arXiv: not found")
    time.sleep(0.4)

print("\n" + "=" * 78)
print(f"ENTRIES WITH ISSUES: {len(problems)}")
for k, why in problems:
    print(f"  {k}: {why}")
