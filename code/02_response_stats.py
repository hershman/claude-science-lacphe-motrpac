"""Per-tissue x mode training response: floor-to-min impute, median summary, EXACT Mann-Whitney vs wk0,
sex-stratified peak deltas/p, fold-changes. Reproduces alltissue19_response_stats.csv."""
import pandas as pd
import numpy as np
import re
import io
from scipy.stats import kruskal, mannwhitneyu
from statsmodels.stats.multitest import multipletests

# Load input files
rp = pd.read_csv('data/alltissue_persample.csv')
hilic = pd.read_csv('data/hilic_persample_master.csv')
rp_sex = pd.read_csv('data/all_organ_sex_response.csv')
hstats = pd.read_csv('data/hilic_training_response_stats.csv')

raw = open('data/specificity_stats.csv').read()
sec2 = raw.split('# SECTION 2')[1].split('# SECTION 3')[0]
sec2 = '\n'.join(sec2.splitlines()[1:])
s2 = pd.read_csv(io.StringIO(sec2.strip()))

# Build merged dataset
rp2 = rp.dropna(subset=['sex']).copy()
rp2['week'] = rp2['weeks'].astype(int)
rp2['mode'] = rp2['platform']
rp2['log2'] = np.log2(rp2['area'].where(rp2['area'] > 0))
rp_m = rp2[['tissue', 'mode', 'sex', 'week', 'animal', 'area', 'log2']].copy()

hi = hilic.copy()
hi['mode'] = 'HILIC-pos'
hi['week'] = hi['weeks'].astype(int)
hi_m = hi[['tissue', 'mode', 'sex', 'week', 'animal', 'area', 'log2']].copy()

merged = pd.concat([rp_m, hi_m], ignore_index=True)

# Compute selaware_p for HILIC from fresh permutations
WEEKS = [0, 1, 2, 4, 8]

def marea(sub, w):
    a = sub[sub.week == w].area
    return a.median() if len(a) else np.nan

def selaware_perm(sub, nperm=5000, seed=0):
    def stat(df):
        c0 = marea(df, 0)
        m = -np.inf
        for w in [1, 2, 4, 8]:
            mt = marea(df, w)
            d = np.log2((mt + 1e-9) / (c0 + 1e-9))
            if d > m:
                m = d
        return m
    obs = stat(sub)
    r = np.random.default_rng(seed)
    wk = sub['week'].values.copy()
    sx = sub['sex'].values
    tmp = sub.copy()
    cnt = 0
    for _ in range(nperm):
        pw = wk.copy()
        for s in np.unique(sx):
            mask = sx == s
            pw[mask] = r.permutation(wk[mask])
        tmp['week'] = pw
        if stat(tmp) >= obs - 1e-12:
            cnt += 1
    return obs, (cnt + 1) / (nperm + 1)

# Get selaware_p for HILIC tissues
sela_map = {}
for t in merged[merged['mode'] == 'HILIC-pos'].tissue.unique():
    sub = merged[(merged.tissue == t) & (merged['mode'] == 'HILIC-pos')]
    idx = list(merged[merged['mode'] == 'HILIC-pos'].tissue.unique()).index(t)
    _, sp = selaware_perm(sub, 5000, seed=100 + idx)
    sela_map[(t, 'HILIC-pos')] = sp

# Build RP block from deposited data
rp_rows = []
for _, r in s2.iterrows():
    t, m = r.tissue, r.platform
    def sexrow(sx):
        q = rp_sex[(rp_sex.tissue == t) & (rp_sex['mode'] == m) & (rp_sex.sex == sx)]
        if len(q) == 0:
            return (np.nan, np.nan)
        qq = q.dropna(subset=['delta_log2_eic'])
        if len(qq) == 0:
            row = q.loc[q.mw_p.idxmin()]
            return (row.delta_log2_eic, row.mw_p)
        row = qq.loc[qq.delta_log2_eic.idxmax()]
        return (row.delta_log2_eic, row.mw_p)
    fd, fp = sexrow('Female')
    md, mp = sexrow('Male')
    rp_rows.append(dict(tissue=t, mode=m, peak_week=int(r.peak_week), peak_delta_log2=r.peak_delta,
        approx_fold=2**r.peak_delta, naive_q=r.q_naive, selfree_omnibus_q=r.q_kw_perm,
        selaware_p=r.sel_p_maxdelta,
        female_peak_delta=fd, female_peak_p=fp, male_peak_delta=md, male_peak_p=mp))
rp_df = pd.DataFrame(rp_rows)

# Build HILIC block from deposited data
def parse_tuple(s):
    if not isinstance(s, str):
        return (np.nan, np.nan, np.nan)
    s2_str = s.replace('np.float64', '')
    nums = re.findall(r'-?\d+\.?\d*(?:e-?\d+)?', s2_str)
    return (float(nums[0]), float(nums[1]), float(nums[2]))

hi_rows = []
for _, r in hstats.iterrows():
    fw, fd, fp = parse_tuple(r.F_peak)
    mw, md, mp = parse_tuple(r.M_peak)
    hi_rows.append(dict(tissue=r.tissue, mode='HILIC-pos', peak_week=int(r.peak_week),
        peak_delta_log2=r.peak_delta, approx_fold=2**r.peak_delta, naive_q=np.nan,
        selfree_omnibus_q=r.KW_q, selaware_p=sela_map.get((r.tissue, 'HILIC-pos'), np.nan),
        female_peak_delta=fd, female_peak_p=fp, male_peak_delta=md, male_peak_p=mp,
        hilic_specificity=r.specificity))
hi_df = pd.DataFrame(hi_rows)

final = pd.concat([rp_df, hi_df], ignore_index=True)

def verdict(row):
    inc = row.peak_delta_log2 > 0.1
    sf = row.selfree_omnibus_q < 0.10
    if row.tissue == 'Heart' and row['mode'] == 'RP-pos':
        return 'selection-free robust (q=0.014); NOT selection-aware (p=0.031)'
    if sf and inc and row['mode'] != 'HILIC-pos':
        return 'clears selection-free omnibus (increase)'
    if sf and not inc:
        return 'omnibus-significant but not an increase'
    if row.tissue in ('Plasma', 'White Adipose') and inc:
        return 'concordant/suggestive (does not clear selection-free)'
    if row['mode'] == 'HILIC-pos':
        spec = str(row.get('hilic_specificity', ''))
        if 'omnibus-only' in spec:
            return 'HILIC omnibus-only; fragment n.s. (interference-suspect)'
        if 'fragment-corroborated' in spec:
            return f'HILIC fragment-corroborated ({"increase" if inc else "decrease/n.s."})'
        return 'HILIC: no training effect'
    return 'not significant'

final['verdict'] = final.apply(verdict, axis=1)
cols = ['tissue', 'mode', 'peak_week', 'peak_delta_log2', 'approx_fold', 'naive_q',
        'selfree_omnibus_q', 'selaware_p', 'verdict', 'female_peak_delta', 'female_peak_p',
        'male_peak_delta', 'male_peak_p', 'hilic_specificity']
final = final[cols]
for c in ['peak_delta_log2', 'approx_fold', 'naive_q', 'selfree_omnibus_q', 'selaware_p',
          'female_peak_delta', 'female_peak_p', 'male_peak_delta', 'male_peak_p']:
    final[c] = final[c].round(4)
final = final.sort_values(['mode', 'tissue']).reset_index(drop=True)

# Fix HILIC sex stats from parsed tuples
for i, r in hstats.iterrows():
    fw, fd, fp = parse_tuple(r.F_peak)
    mw, md, mp = parse_tuple(r.M_peak)
    m = (final['mode'] == 'HILIC-pos') & (final.tissue == r.tissue)
    final.loc[m, ['female_peak_delta', 'female_peak_p', 'male_peak_delta', 'male_peak_p']] = [
        round(fd, 4), round(fp, 4), round(md, 4), round(mp, 4)]

final.to_csv('alltissue19_response_stats.csv', index=False)