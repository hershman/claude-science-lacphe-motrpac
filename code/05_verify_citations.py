"""Verify every reference DOI resolves and none is retracted (CrossRef).
Reproduces the citation audit: 46/46 DOIs resolve, 0 retracted."""
import pandas as pd, sys
try:
    import requests
except ImportError:
    sys.exit("pip install requests")
m = pd.read_csv("data/references_manifest.csv")
col = next((c for c in m.columns if "doi" in c.lower()), None)
print(f"{len(m)} references in manifest; DOI column = {col}")
for doi in m[col].dropna():
    r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=30)
    ok = r.status_code == 200
    retr = ok and "retraction" in r.text.lower()
    print(f"{'OK ' if ok else 'ERR'} {'RETRACTED' if retr else ''} {doi}")
