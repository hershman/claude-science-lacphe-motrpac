"""Regenerate the core data figures from deposited per-sample data and stats.
Reproduces Figure 1 (19-tissue Delta-log2 timecourse) from data/alltissue19_persample.csv
and prints the Figure 3 sex-stratified responder values from data/alltissue19_response_stats.csv.
The publication figures were assembled by the analysis pipeline; this script reproduces the
underlying numbers and a faithful timecourse rendering. Columns: tissue, mode, sex, week, animal,
area, log2 (log2 = log2(area+1), precomputed)."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ps = pd.read_csv("data/alltissue19_persample.csv")
stats = pd.read_csv("data/alltissue19_response_stats.csv")

# ---- Figure 1: 19-tissue Delta-log2 timecourse (heart/plasma/WAT highlighted) ----
# collapse to one series per tissue (mean across modes) of week-mean log2 minus week-0 mean
def dlog2_by_week(df):
    ctrl = df[df.week == 0].groupby("tissue").log2.mean()
    out = {}
    for (tis, wk), g in df.groupby(["tissue", "week"]):
        if wk == 0: continue
        out.setdefault(tis, {})[wk] = g.log2.mean() - ctrl.get(tis, np.nan)
    return out

d = dlog2_by_week(ps)
hi = {"Heart": "red", "Plasma": "green", "White Adipose": "purple"}
fig, ax = plt.subplots(figsize=(7, 4))
for tis, wkd in sorted(d.items()):
    wks = sorted(wkd); y = [wkd[w] for w in wks]
    c = next((v for k, v in hi.items() if k in tis), None)
    ax.plot(wks, y, "-o", color=c or "0.8", lw=2 if c else 0.8,
            zorder=3 if c else 1, label=tis if c else None, ms=4 if c else 2)
ax.axhline(0, color="k", lw=0.6); ax.set_xlabel("Weeks of training")
ax.set_ylabel(r"$\Delta\log_2$ Lac-Phe vs sedentary")
ax.set_title("Lac-Phe organ time-courses (19 tissues)")
ax.legend(fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig("paper/figures/figure1_organ_timecourse.png", dpi=200)
print("wrote paper/figures/figure1_organ_timecourse.png")

# ---- Figure 3: sex-stratified peak deltas for the three responders (print check) ----
cols = [c for c in stats.columns if any(k in c.lower() for k in
        ("tissue","mode","peak","female","male","fold","q","sel"))]
resp = stats[stats.tissue.isin(["Plasma","Heart","White Adipose"])]
print("\nResponder rows (Figure 3 source):")
print(resp[cols].to_string(index=False))
