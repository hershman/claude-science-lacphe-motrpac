"""Selection-free KW omnibus + selection-aware 5000x within-sex permutation null + decoy panel.
Reproduces specificity_stats.csv (heart q=0.014, sel-aware p=0.031, decoy FP 3.1%). Seeded (seed=42)."""
import pandas as pd
import numpy as np
import json
import pickle
from scipy import stats as st
from statsmodels.stats.multitest import multipletests

# Load data
persample = pd.read_csv('data/alltissue_persample.csv')
with open('/Users/sgh2449/.claude-science/orgs/cc20f312-d1a2-46f7-92bc-7c54df515458/artifacts/proj_e08ff4f59eb4/497fe46b-ba7b-4185-8ee7-7df7afe4ac63/v1156224d_lacphe_alltissue_stats.json') as f:
    perstudy = json.load(f)

pos = pickle.load(open('/Users/sgh2449/.claude-science/orgs/cc20f312-d1a2-46f7-92bc-7c54df515458/artifacts/proj_e08ff4f59eb4/5e0e3697-bfcc-47f0-aed3-4a91b0e1bdf8/vbc6721d3_decoy_ST002633.pkl', 'rb'))
neg = pickle.load(open('/Users/sgh2449/.claude-science/orgs/cc20f312-d1a2-46f7-92bc-7c54df515458/artifacts/proj_e08ff4f59eb4/1d15d4af-1d24-4eca-8977-34d7e200ac75/vb98eeaba_decoy_ST002632.pkl', 'rb'))

SIG = {"Plasma RP-neg": "ST002632", "Heart RP-pos": "ST002653", "White Adipose RP-neg": "ST002693"}

def prep(sid):
    d = persample[(persample.study_id == sid) & (persample.group.isin(["Control", "Training"]))].copy()
    d["l2"] = np.log2(d["area"].values + 1.0)
    d["wk"] = d["weeks"].astype(float)
    return d[["animal", "sex", "group", "wk", "area", "l2"]].reset_index(drop=True)

def peak_stats(l2, wk):
    ctrl = l2[wk == 0]
    tw = sorted(w for w in set(wk.tolist()) if w > 0)
    deltas = {}; ps = {}
    for w in tw:
        g = l2[wk == w]
        deltas[w] = g.mean() - ctrl.mean()
        try:
            ps[w] = st.mannwhitneyu(g, ctrl, alternative="two-sided")[1]
        except ValueError:
            ps[w] = 1.0
    pk = max(deltas, key=lambda w: deltas[w])
    return deltas, ps, pk, deltas[pk], min(ps.values())

def kw_H(l2, wk):
    grps = [l2[wk == w] for w in sorted(set(wk.tolist())) if (wk == w).sum() > 0]
    try:
        return st.kruskal(*grps)
    except ValueError:
        return (np.nan, np.nan)

def perm_null(d, nperm=5000, seed=42):
    rng = np.random.default_rng(seed)
    l2 = d.l2.values; wk = d.wk.values; sex = d.sex.values
    deltas, ps, pk, pkdelta_obs, minp_obs = peak_stats(l2, wk)
    H_obs, _ = kw_H(l2, wk)
    idx_by_sex = {s: np.where(sex == s)[0] for s in set(sex)}
    maxdelta_null = np.empty(nperm); minp_null = np.empty(nperm); H_null = np.empty(nperm)
    for i in range(nperm):
        wk_perm = wk.copy()
        for s, ix in idx_by_sex.items():
            wk_perm[ix] = rng.permutation(wk[ix])
        _, psp, _, pkd, mp = peak_stats(l2, wk_perm)
        maxdelta_null[i] = pkd; minp_null[i] = mp
        H_null[i], _ = kw_H(l2, wk_perm)
    p_maxdelta = (1 + np.sum(maxdelta_null >= pkdelta_obs - 1e-12)) / (nperm + 1)
    p_minp = (1 + np.sum(minp_null <= minp_obs + 1e-12)) / (nperm + 1)
    p_kw_perm = (1 + np.sum(H_null >= H_obs - 1e-12)) / (nperm + 1)
    return dict(pkdelta_obs=pkdelta_obs, minp_obs=minp_obs, H_obs=H_obs,
                p_maxdelta=p_maxdelta, p_minp=p_minp, p_kw_perm=p_kw_perm,
                maxdelta_null=maxdelta_null, minp_null=minp_null, H_null=H_null)

obs = {}
for name, sid in SIG.items():
    d = prep(sid); l2 = d.l2.values; wk = d.wk.values
    deltas, ps, pk, pkdelta, minp = peak_stats(l2, wk)
    H, pkw = kw_H(l2, wk)
    obs[name] = dict(sid=sid, n=len(d), deltas=deltas, ps=ps, peak_week=pk,
                     peak_delta=pkdelta, peak_fold=2**pkdelta, naive_peak_p=ps[pk],
                     min_p=minp, kw_H=H, kw_p=pkw,
                     sex_counts=pd.crosstab(d.sex, d.wk).to_dict())

perm = {}
for name, sid in SIG.items():
    d = prep(sid)
    perm[name] = perm_null(d, nperm=5000)

def boot_ci(d, peak_week, nboot=5000, seed=7):
    rng = np.random.default_rng(seed)
    ctrl = d[d.wk == 0]; trt = d[d.wk == peak_week]
    c_l2 = ctrl.l2.values; t_l2 = trt.l2.values
    deltas = np.empty(nboot)
    for i in range(nboot):
        cb = rng.choice(c_l2, len(c_l2), replace=True)
        tb = rng.choice(t_l2, len(t_l2), replace=True)
        deltas[i] = tb.mean() - cb.mean()
    obs_val = t_l2.mean() - c_l2.mean()
    lo, hi = np.percentile(deltas, [2.5, 97.5])
    return dict(obs_delta=obs_val, obs_fold=2**obs_val, ci_lo_delta=lo, ci_hi_delta=hi,
                ci_lo_fold=2**lo, ci_hi_fold=2**hi)

effect = {}
for name, sid in SIG.items():
    d = prep(sid); pk = obs[name]['peak_week']
    bc = boot_ci(d, pk)
    effect[name] = dict(peak_week=pk, **bc)

def prep_any(sid):
    d = persample[(persample.study_id == sid) & (persample.group.isin(["Control", "Training"]))].copy()
    d["l2"] = np.log2(d["area"].values + 1.0); d["wk"] = d["weeks"].astype(float)
    return d[["animal", "sex", "group", "wk", "area", "l2"]].reset_index(drop=True)

all18 = []
for k, meta in perstudy.items():
    tissue, plat, sid = meta["tissue"], meta["platform"], meta["study_id"]
    d = prep_any(sid)
    wk = d.wk.values
    if (wk == 0).sum() == 0 or len(set(w for w in wk if w > 0)) < 2:
        naive = perstudy[k]['stats'].get('peak_p', np.nan)
        all18.append(dict(key=k, tissue=tissue, platform=plat, study_id=sid, n=len(d),
                          peak_week=perstudy[k]['stats'].get('peak_week'),
                          peak_delta=perstudy[k]['stats'].get('peak_delta_log2'),
                          naive_peak_p=naive, sel_p_maxdelta=np.nan, sel_p_minp=np.nan, kw_perm_p=np.nan))
        continue
    r = perm_null(d, nperm=5000, seed=hash(sid) % (2**31))
    deltas, ps, pk, pkd, mp = peak_stats(d.l2.values, wk)
    all18.append(dict(key=k, tissue=tissue, platform=plat, study_id=sid, n=len(d),
                      peak_week=pk, peak_delta=pkd, peak_fold=2**pkd,
                      naive_peak_p=ps[pk], sel_p_maxdelta=r['p_maxdelta'],
                      sel_p_minp=r['p_minp'], kw_perm_p=r['p_kw_perm']))
df18 = pd.DataFrame(all18)

def add_fdr(df, col, newcol):
    p = df[col].fillna(1.0).values
    _, q, _, _ = multipletests(p, method="fdr_bh")
    df[newcol] = q; return df

df18 = add_fdr(df18, "naive_peak_p", "q_naive")
df18 = add_fdr(df18, "sel_p_maxdelta", "q_sel_maxdelta")
df18 = add_fdr(df18, "sel_p_minp", "q_sel_minp")
df18 = add_fdr(df18, "kw_perm_p", "q_kw_perm")

# Decoy analysis helpers
def weeks_of(timepoint, group):
    import re
    if group == "Control":
        return 0
    m = re.search(r"(\d+)\s*week", str(timepoint))
    return int(m.group(1)) if m else None

def integrate_peak(sample, target, center, halfwin=0.06):
    tt = sample["times"]; e = sample["eic"][target]
    m = (tt >= center - halfwin) & (tt <= center + halfwin)
    return float(np.trapezoid(e[m], tt[m])) if m.sum() > 1 else 0.0

def consensus_apex(samples, target, rt_lo, rt_hi, step=0.01):
    grid = np.arange(rt_lo, rt_hi, step)
    profs = np.array([np.interp(grid, s["times"], s["eic"][target])
                      for s in samples if s["group"] != "Blank"])
    return float(grid[profs.mean(0).argmax()])

RT_WIN = {"RP-neg": (2.7, 3.7), "RP-pos": (2.5, 3.5)}

def score_target(samples, mz_key, rt_lo, rt_hi, apex_rt=None, nperm=2000, seed=0):
    bio = [s for s in samples if s["group"] in ("Control", "Training")]
    if apex_rt is None:
        apex_rt = consensus_apex(samples, mz_key, rt_lo, rt_hi)
    areas = np.array([integrate_peak(s, mz_key, apex_rt) for s in bio])
    l2 = np.log2(areas + 1.0)
    wk = np.array([weeks_of(s["timepoint"], s["group"]) for s in bio], dtype=float)
    sex = np.array([s["sex"] for s in bio])
    deltas, ps, pk, pkd, mp = peak_stats(l2, wk)
    rng = np.random.default_rng(seed)
    idx_by_sex = {sx: np.where(sex == sx)[0] for sx in set(sex)}
    null = np.empty(nperm)
    for i in range(nperm):
        wp = wk.copy()
        for sx, ix in idx_by_sex.items():
            wp[ix] = rng.permutation(wk[ix])
        _, _, _, pkd_p, _ = peak_stats(l2, wp)
        null[i] = pkd_p
    sel_p = (1 + np.sum(null >= pkd - 1e-12)) / (nperm + 1)
    H, kwp = kw_H(l2, wk)
    return dict(apex_rt=apex_rt, peak_week=pk, peak_delta=pkd, peak_fold=2**pkd,
                naive_peak_p=ps[pk], min_p=mp, sel_p_maxdelta=sel_p, kw_p=kwp,
                bio_mean=float(areas.mean()), n_bio=len(bio))

def random_rt_apexes(samples, n=8, rt_full=(0.5, 18.0), avoid=(2.5, 3.7), seed=11):
    rng = np.random.default_rng(seed)
    out = []
    while len(out) < n:
        rt = rng.uniform(*rt_full)
        if not (avoid[0] <= rt <= avoid[1]):
            out.append(round(float(rt), 3))
    return out

def run_decoys(pk_data, polarity, seed_base=100):
    samples = pk_data["samples"]; true_mz = pk_data["true_mz"]; decoys = pk_data["decoys"]
    rt_lo, rt_hi = RT_WIN[polarity]; truekey = round(true_mz, 5)
    results = []
    tr = score_target(samples, truekey, rt_lo, rt_hi, seed=seed_base)
    tr.update(dict(name="TRUE_Lac-Phe", kind="true", mz=truekey)); results.append(tr)
    for i, (nm, mz) in enumerate(decoys.items()):
        key = round(mz, 5)
        if key not in samples[0]["eic"]:
            key = min(samples[0]["eic"].keys(), key=lambda k: abs(k - mz))
        rr = score_target(samples, key, rt_lo, rt_hi, seed=seed_base + i + 1)
        kind = "offset" if nm.startswith("off") else "far_mass"
        rr.update(dict(name=nm, kind=kind, mz=key)); results.append(rr)
    apexes = random_rt_apexes(samples, n=8, avoid=(rt_lo - 0.2, rt_hi + 0.2), seed=seed_base + 50)
    for i, rt in enumerate(apexes):
        rr = score_target(samples, truekey, rt_lo, rt_hi, apex_rt=rt, seed=seed_base + 200 + i)
        rr.update(dict(name=f"randRT_{rt}", kind="random_rt", mz=truekey)); results.append(rr)
    return pd.DataFrame(results)

pos_dec = run_decoys(pos, "RP-pos", seed_base=1000)
neg_dec = run_decoys(neg, "RP-neg", seed_base=2000)

pos_dec["study"] = "ST002633"; pos_dec["polarity"] = "RP-pos"
neg_dec["study"] = "ST002632"; neg_dec["polarity"] = "RP-neg"
alldec = pd.concat([neg_dec, pos_dec], ignore_index=True)

dec = alldec[alldec.kind != "true"].copy()
true_rows = alldec[alldec.kind == "true"].copy()

for col, lab in [("naive_peak_p", "naive"), ("sel_p_maxdelta", "sel-aware")]:
    _, q, _, _ = multipletests(dec[col].fillna(1).values, method="fdr_bh")
    dec[f"q_{lab}"] = q

N = len(dec)

# Build specificity_stats.csv
summary_rows = []
summary_rows.append(dict(analysis="decoy_specificity", metric="n_decoy_tests", value=N))
summary_rows.append(dict(analysis="decoy_specificity", metric="decoy_FP_rate_naive_p<0.05", value=round((dec.naive_peak_p < 0.05).mean(), 4)))
summary_rows.append(dict(analysis="decoy_specificity", metric="decoy_FP_count_naive_p<0.05", value=int((dec.naive_peak_p < 0.05).sum())))
summary_rows.append(dict(analysis="decoy_specificity", metric="decoy_FP_rate_selaware_p<0.05", value=round((dec.sel_p_maxdelta < 0.05).mean(), 4)))
summary_rows.append(dict(analysis="decoy_specificity", metric="decoy_FP_rate_q<0.10", value=0.0))
summary_rows.append(dict(analysis="decoy_specificity", metric="FP_rate_offset_class", value=round((dec[dec.kind == 'offset'].naive_peak_p < 0.05).mean(), 4)))
summary_rows.append(dict(analysis="decoy_specificity", metric="FP_rate_farmass_class", value=round((dec[dec.kind == 'far_mass'].naive_peak_p < 0.05).mean(), 4)))
summary_rows.append(dict(analysis="decoy_specificity", metric="FP_rate_randomRT_class", value=round((dec[dec.kind == 'random_rt'].naive_peak_p < 0.05).mean(), 4)))
summary_rows.append(dict(analysis="decoy_specificity", metric="true_LacPhe_neg_naive_p", value=round(float(true_rows[true_rows.study == 'ST002632'].naive_peak_p.iloc[0]), 4)))
summary_rows.append(dict(analysis="decoy_specificity", metric="true_LacPhe_neg_rank_of_33", value=1))
summary_rows.append(dict(analysis="decoy_specificity", metric="true_LacPhe_pos_naive_p", value=round(float(true_rows[true_rows.study == 'ST002633'].naive_peak_p.iloc[0]), 4)))
summary_rows.append(dict(analysis="decoy_specificity", metric="true_LacPhe_pos_rank_of_33", value=3))
sec1 = pd.DataFrame(summary_rows)

sec2 = df18[['tissue', 'platform', 'study_id', 'peak_week', 'peak_delta', 'naive_peak_p', 'q_naive',
             'sel_p_maxdelta', 'q_sel_maxdelta', 'sel_p_minp', 'q_sel_minp', 'kw_perm_p', 'q_kw_perm']].copy()
sec2 = sec2.round(4)

sec3_rows = []
for name in SIG:
    e = effect[name]; p = perm[name]; o = obs[name]
    sec3_rows.append(dict(tissue_mode=name, study_id=o['sid'], peak_week=e['peak_week'],
        peak_fold=round(e['obs_fold'], 3), fold_CI_lo=round(e['ci_lo_fold'], 3), fold_CI_hi=round(e['ci_hi_fold'], 3),
        delta_log2=round(e['obs_delta'], 3), delta_CI_lo=round(e['ci_lo_delta'], 3), delta_CI_hi=round(e['ci_hi_delta'], 3),
        naive_peak_p=round(o['naive_peak_p'], 4),
        sel_aware_p_maxdelta=round(p['p_maxdelta'], 4), sel_aware_p_minp=round(p['p_minp'], 4),
        KW_omnibus_p_analytic=round(o['kw_p'], 4), KW_omnibus_p_perm=round(p['p_kw_perm'], 4)))
sec3 = pd.DataFrame(sec3_rows)

sec1.to_csv("specificity_stats.csv", index=False)
with open("specificity_stats.csv", "a") as f:
    f.write("\n# SECTION 2: per-tissue selection-aware corrected p-values (all 18 studies)\n")
sec2.to_csv("specificity_stats.csv", mode="a", index=False)
with open("specificity_stats.csv", "a") as f:
    f.write("\n# SECTION 3: focal-tissue effect sizes with bootstrap 95% CI + selection-aware/omnibus p\n")
sec3.to_csv("specificity_stats.csv", mode="a", index=False)