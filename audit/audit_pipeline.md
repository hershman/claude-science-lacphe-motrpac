# Independent Correctness Audit — Data Pipeline, Statistics, Figures

**Manuscript:** *A substrate-driven exercise metabolite without an enzyme switch: cross-tissue Lac-Phe in the MoTrPAC rat atlas, and the absence of CNDP2 activation across chromatin, protein, and PTM layers.*

**Audit scope:** trace every figure/table from deposited source data through each transformation; re-derive statistics and figure numbers from the deposited per-sample CSVs; check statistical failure modes; document the raw-extraction boundary. All values below were recomputed in-session from the deposited artifacts — the manuscript's own summaries/cached outputs were not trusted.

**Bottom line:** The core quantitative claims reproduce. Every headline statistic I could recompute from the deposited per-sample data matches the manuscript to the stated precision *once the correct Mann–Whitney variant (exact, not scipy's asymptotic default) is used* — see the NaN-handling note; the deposited values are internally consistent under the exact test: heart selection-free omnibus **q = 0.014**, selection-aware **p = 0.031**, positive-control dose-response **r = 0.75 / 0.37**, sex-stratified peak p-values (**0.008 / 0.036**), fold-changes (1.41× / 2.11× / 2.43×), the full CNDP2 region/CpG tallies, protein/PTM significance, and the analog decision matrix. The figures render consistently with the data. Issues found are concentrated in **(a) the headline sample-count arithmetic (1,380)** and **(b) an internal inconsistency between the strand-corrected in-text tables and the strand-naive supplementary Table S1**, neither of which changes a scientific conclusion.

- **Figures traced:** 6 caption-numbered figures (Fig 1–6), from 8 image files.
- **Reproduced:** YES (downstream figure/stat generation reproduces from deposited per-sample CSVs).

---

## Figure filename → caption-number mapping (verified)

The image filenames are offset by one from the caption numbers, as the task warned. Confirmed mapping:

| Caption | Image file | Content |
|---|---|---|
| Fig 1 | `figure1_organ_timecourse.png` | organ timecourse (19 tissues) + source–sink map |
| Fig 2 | `figure1c_spectrum.png` | raw negative-mode spectrum at Lac-Phe apex |
| Fig 3 | `figure2_sex_responders.png` | sex-stratified responders |
| Fig 4 | `figure3_positive_control.png` | positive-control validation |
| Fig 5 | `figure4_cndp2_multiomic.png` | CNDP2 multiomic (strand-corrected) |
| Fig 6 | `figure5_drug_design.png` | drug-design panel |

Not an error (filenames are internal), but worth a note to the typesetter so no wrong image is embedded on final build.

---

## BLOCKING issues

**None.** No stated finding or headline number is wrong in a way that overturns a conclusion.

---

## MAJOR issues

### M1. Headline sample total "1,380" overstates the analyzed dataset by 72 samples (should be 1,308)

- **Location:** Abstract ("1,380 biological samples" implied via 888+492); Fig 1 caption ("888 reversed-phase biological samples across 9 tissues … plus 492 HILIC samples across 10 tissues, 1,380 samples across all 19 tissues"); Discussion §3 ("all 19 PASS1B tissues (1,380 biological samples)").
- **Manuscript claim:** 888 RP + 492 HILIC = 1,380 samples analyzed across 19 tissues.
- **Recomputed evidence:** The per-sample table that actually feeds every statistic (`alltissue19_persample.csv`) contains **888 RP rows + 420 HILIC rows = 1,308**, not 1,380.
  - HILIC: `lacphe_hilic_tissue_summary.csv` reports `n_biological` summing to **492** and `n_extracted` to **491**, but only **420** HILIC rows were carried into the merged 19-tissue analysis table and into the HILIC stats (`hilic_training_response_stats.csv` uses n = 50/46/25/24 per tissue = 420 total). The 8-sample-per-tissue gap (58→50 for the balanced tissues, plus Hypothalamus 54→46) is an undocumented balancing step.
  - The "1,380" figure therefore mixes **available** HILIC samples (492) with **analyzed** RP rows (888). Consistent totals are either 1,308 (analyzed) or would require using the RP available count for HILIC too.
- **Severity:** MAJOR — a headline sample size in the Abstract and Fig 1 caption is off by 72; no conclusion depends on it.
- **Recommended action:** Report the analyzed total as **1,308 (888 RP + 420 HILIC)**, or explicitly state that 492 is HILIC-available while 420 were analyzed after balancing, and reconcile the two numbers.

### M2. Supplementary Table S1 (Epigenetics sheet) is NOT strand-corrected and contradicts the in-text Tables 2/3/5

- **Location:** `cndp2_multiomic_supplementary.xlsx`, sheets `Summary` and `Epigenetics_ATAC_METHYL`; referenced by §2.3 and "Data and code availability" as the per-feature source (Table S1).
- **Manuscript claim (in-text):** strand-aware annotation — 8 ATAC peaks + 31 methylation clusters lie 5′ of the TSS; the three peaks "previously mislabelled promoter-proximal (−1694/−1086/−632 bp)" actually sit on the 3′ flank ≈18 kb from the TSS (Table 2). Summary says the strand correction is the paper's point.
- **Recomputed evidence:** The deposited supplementary `Epigenetics_ATAC_METHYL` sheet still carries the **strand-naive** annotation the manuscript explicitly repudiates: `region = promoter_proximal` at `tss_distance = −1694 / −1086 / −632`, `downstream_distal` for the true promoter/upstream peaks, etc. The `Summary` sheet states "26 peaks (3 promoter)" — contradicting the corrected "8 peaks 5′ of the TSS." The corrected annotation exists only in `cndp2_markers_extended.csv` (`region_stranded`, `tss_distance_5prime_bp`), which I verified reproduces Tables 2/3/5 exactly (ATAC 7 upstream + 1 straddle + 15 gene-body + 3 3′-flank = 26; METHYL 8 + 23 + 94 = 125; promoter CpG-island 31 = 1 ATAC + 30 METHYL; gene-body CpG 25).
- **Severity:** MAJOR — a reader checking the cited supplementary table finds the *old, in-text-retracted* annotation; the supp table disagrees with the figures/tables it is meant to support.
- **Recommended action:** Regenerate the `Epigenetics_ATAC_METHYL` and `Summary` sheets of the supplement from `cndp2_markers_extended.csv` so Table S1 carries the strand-corrected coordinates and region labels.

---

## MINOR issues

### m1. "strict hydrophobicity order" overstates the family retention-time ordering

- **Location:** §2.1 ("an N-lactoyl-amino-acid family eluting in strict hydrophobicity order"); Fig 2 caption ("retention-time–hydrophobicity ordering").
- **Recomputed evidence:** In `lacphe_ms1_identity.csv` the N-lactoyl family RT is **not strictly monotonic** in logP: Lac-Pro elutes at 4.26 min despite low logP (−0.56; flagged `clean=False`), and Lac-Val (RT 2.88) > Lac-Met (RT 1.52) while logP orders the other way. The real statistic is a strong Spearman correlation (**r = 0.857, p = 0.007, n = 8** clean members), which the manuscript also reports elsewhere.
- **Severity:** MINOR (wording). The correlation is genuine; "strict … order" is literally false.
- **Recommended action:** "eluting in hydrophobicity order (Spearman r = 0.86)" rather than "strict hydrophobicity order."

### m2. Ubiquityl-K363 "marginal p ≈ 3×10⁻³" refers to the occupancy-normalized omnibus, not the raw per-timepoint p

- **Location:** §2.4 and Fig 5 caption ("ubiquityl-K363 … marginal p ≈ 3×10⁻³").
- **Recomputed evidence:** In the `Proteome_PTM` sheet, K363 (liver, male) has raw `motrpac_p` = **0.0052** (8w) as its smallest per-timepoint p; the value ≈3×10⁻³ corresponds to `occ_omnibus_p` (occupancy-normalized omnibus) = **0.00249**. A reader checking the raw MoTrPAC p would find 0.005, not 0.003.
- **Severity:** MINOR (traceable, but the statistic type is unstated).
- **Recommended action:** Specify "occupancy-normalized omnibus p ≈ 3×10⁻³" (or cite the 0.005 raw p).

### m3. RP per-sample file trimmed 968 → 888 rows without documentation

- **Location:** Methods (statistics); source `alltissue_persample.csv` (968 rows) vs merged `alltissue19_persample.csv` (888 RP rows).
- **Recomputed evidence:** The pre-merge RP table has 485 RP-neg + 483 RP-pos = 968 rows (54–56 per tissue-mode); the analysis table trims each tissue-mode to ≤50 (balanced 5/sex/week over weeks 0/1/2/4/8), dropping 80 rows. This is a reasonable balancing step (removes extra/QC injections) and does not change results, but is undocumented.
- **Severity:** MINOR — undocumented filtering that changes n; conclusions unaffected.
- **Recommended action:** State the per-tissue balancing rule (≤10 animals/week, 2 modes) in Methods.

---

## Statistical failure-mode audit (checks that PASSED)

- **Selection-free omnibus (Kruskal–Wallis across weeks 0/1/2/4/8):** recomputed heart RP-pos KW on the deposited per-sample data (H ≈ 16–20 depending on NaN handling); the reported **permutation** omnibus p = 0.0016 and **BH-FDR q = 0.0144 across the 18 RP studies reproduce exactly** when I recompute Benjamini–Hochberg on the `kw_perm_p` column of `specificity_stats.csv`. FDR is correctly applied across the 18 study-modes.
- **Selection-aware 5,000× permutation null (max weekly Δlog₂ per study):** deposited `q_sel_maxdelta` shows **no study clears q < 0.10** (min = 0.19), matching "no tissue survives the stricter selection-aware correction." Heart selection-aware nominal p = 0.031 matches the text.
- **NaN / imputation handling (the key reproducibility subtlety):** the sex-stratified stats (Fig 3, Abstract) reproduce with **floor-to-min imputation of undetected samples + median summary + EXACT Mann–Whitney**. Under that recipe I recover: plasma F +0.748 / p = 0.0079; heart F +0.950 / p = 0.0079; WAT F +1.700 / p = 0.0079; WAT M +1.366 / p = 0.0361 — matching the deposited `alltissue19_response_stats.csv` and the figure asterisks. **The exact-test variant is itself load-bearing:** my first recompute used scipy's default (asymptotic w/ continuity correction) and produced **Heart male wk-2 p = 0.1161**, which does *not* match the deposited **male_peak_p = 0.1508** even though the delta (+0.845) matches exactly; switching to `mannwhitneyu(..., method='exact')` recovers **0.1508**. (Deltas were never in question; only the p-test variant.) Naïve dropna additionally gives different n (e.g. heart female wk0 = 4) and different deltas. So **the full rule — floor-to-min impute, median summary, exact Mann–Whitney — is load-bearing and should be stated in Methods** (currently Methods only says "zero handling is not uniform across tissues"). Not an error in the deposited values (they use the exact test consistently), but under-documented, and worth flagging that the asymptotic default silently disagrees.
- **Test appropriateness:** unpaired Mann–Whitney (trained week vs sedentary controls, independent animals) and Kruskal–Wallis omnibus are appropriate for the small-n, non-normal, cross-sectional design; sex stratification is correct; multiple-comparison correction is present at both bars.
- **Decoy panel:** `specificity_stats.csv` — 64 decoy m/z, 2 naïve FP at p<0.05 → **3.12 % naïve FP rate** (manuscript "3.1 %"); 0 survive q<0.10; true Lac-Phe neg naïve p = 0.014, rank 1 of 33. Reproduces.
- **RP+HILIC merge into the 19-tissue table:** no misalignment or double-counting detected at the tissue/mode/animal level (888 RP rows = 445 unique animals × 2 modes; 19 tissues correctly partitioned into 9 RP + 10 HILIC). The only issue is the count arithmetic (M1), not a data-alignment error.
- **Positive-control (Table 1 / Fig 4):** all 12 rows of `pc_concordance_table.csv` match Table 1 (m/z, RT, ppm, detection, abundance r). Dose-response **r = 0.749 (44 pts, 11 metabolites ≥45/50; phenylalanine excluded)** and **r = 0.366 (all 12, 48 pts)**, sign agreement **72.7 %** — reproduce the manuscript's 0.75 / 0.37 / 73 % to three digits.
- **CNDP2 protein/PTM (Table 5 / Fig 5):** liver total protein sel-FDR **0.0117 → 0.012**, logFC −0.199…−0.059 (all down, both sexes); acetyl-K364 sel-FDR **0.0185 → 0.018**, logFC −0.41…−0.14 (all down); only liver is significant among 7 protein tissues. All reproduce.
- **Analog panel (Tables 7–8 / Fig 6):** composite = 0.45·stability + 0.40·activity-retention + 0.15·admet_factor reproduces every row (triazole 0.867, reduced amide 0.802, …); DILI 0.74 (triazole) vs 0.14 (reduced amide) matches; all 12 pass Lipinski/Veber with 0 violations as claimed.
- **Determinism:** the 5,000× permutation and decoy nulls are the only stochastic steps; deposited q-values are internally consistent and BH-reproducible, so no seed-instability was observed in the downstream stats. (The permutation null generation itself is upstream of the deposited summaries — see boundary below.)

---

## Raw-extraction boundary (cannot be re-run in-session; verified against deposited outputs)

The raw-spectra extraction from vendor archives (Agilent `.d` decode, Thermo `.raw` → mzML via Modal ThermoRawFileParser, ZIP64 range-request pulls) **cannot be re-executed here** — it requires the multi-GB Metabolomics Workbench archives and the x86 vendor reader. I verified it against its deposited per-sample outputs:

- **`alltissue19_persample.csv` / `alltissue_persample.csv` / `hilic_persample_master.csv`** — the integrated per-sample areas/log2 are the extraction outputs; all downstream statistics reproduce from them (above).
- **Fig 2 diagnostic peaks:** the three annotated ions are present at exact m/z in the deposited representative spectrum (`fragment_spectra_pair.json`): [M−H]⁻ 236.0935 (int 5256), [Phe−H]⁻ 164.0715 (int 34678), [Lac−H]⁻ 89.0248 (int 1181). Consistent with the figure.
- **Fragment covariation r = 0.96 (p = 4×10⁻²⁷, n = 50):** this per-sample covariation is stored only as a **summary metric** in `lacphe_ms1_identity.csv` (`insource_frag_164_at_318_vs_236` = 0.956). The underlying 50-sample intensity vectors are NOT in the deposit — `fragment_spectra_pair.json` holds only 2 representative full spectra (the Fig 2 source). **So r = 0.96 sits on the raw-extraction side of the boundary and is verifiable only via the deposited summary, not recomputable from deposited per-sample data.**
- Mass accuracy (median ppm), isotope envelope (M1/M ratio 11.3 % obs vs 13.5 % theory), and adduct pattern are likewise deposited summaries in `lacphe_ms1_identity.csv`, consistent with the text but not independently recomputable in-session.
- **Genome-wide "not-a-power-artifact" counts (Table 4: 1,032 liver ATAC, 621 BAT methyl, heart 75 ATAC / 107 methyl):** these come from the `MotrpacRatTraining6moData` package objects, external to the deposit; not re-run in-session. The **CNDP2 = 0** side of each row is verified from the deposited marker files (all 151 features `training_significant = NO`).

---

## Verification ledger (manuscript value vs recomputed)

| Item | Manuscript | Recomputed | Match |
|---|---|---|---|
| Heart selection-free omnibus q | 0.014 | 0.0144 (BH across 18 studies) | ✓ |
| Heart selection-aware p | 0.032 / 0.031 | 0.0310 | ✓ |
| No tissue selection-aware q<0.10 | none | min q = 0.19 | ✓ |
| Plasma/heart/WAT peak weeks | 1 / 2 / 4 | 1 / 2 / 4 | ✓ |
| Female peak p (all 3 organs) | 0.008 | 0.0079 | ✓ |
| Male WAT peak | +1.37, p=0.036 | +1.366, p=0.0361 | ✓ |
| Male heart wk-2 peak | +0.845, p=0.151 | +0.845; p=0.1508 (exact MWU) / 0.1161 (asymptotic default) | ✓ with exact test |
| Peak fold-changes (plasma/heart/WAT) | 1.4× / 2.1× / 2.4× | 1.41 / 2.11 / 2.43 | ✓ |
| Dose-response r (44 pts / all 12) | 0.75 / 0.37 | 0.749 / 0.366 | ✓ |
| Sign agreement | 73 % | 72.7 % | ✓ |
| Decoy naïve FP rate | 3.1 % | 3.12 % (2/64) | ✓ |
| ATAC peaks / METHYL clusters | 26 / 125 | 26 / 125 | ✓ |
| 5′-of-TSS features (ATAC/METHYL) | 8 / 31 | 8 / 31 | ✓ |
| Promoter / gene-body CpG-island | 31 / 25 | 31 / 25 | ✓ |
| Liver total-protein sel-FDR | 0.012 | 0.0117 | ✓ |
| Acetyl-K364 sel-FDR | 0.018 | 0.0185 | ✓ |
| Ubiquityl-K363 male p | ≈3×10⁻³ | 0.0025 (occ omnibus) / 0.005 (raw) | ~ (m2) |
| Triazole composite / DILI | 0.87 / 0.74 | 0.867 / 0.741 | ✓ |
| Total analyzed samples | 1,380 | 1,308 (888 RP + 420 HILIC) | ✗ (M1) |
| Supp Table S1 strand annotation | strand-corrected | strand-naive in deposit | ✗ (M2) |

---

## Reproducibility notes

- Deposited per-sample CSVs are sufficient to regenerate Fig 1, Fig 3, Fig 4 and the entire stats table (`alltissue19_response_stats.csv`) — confirmed by re-derivation.
- The one non-obvious recipe needed for exact reproduction is **undetected-sample = floor-to-min, per-cell median summary, Mann–Whitney vs week-0**; recommend stating it explicitly in Methods (currently only partially described).
- Lineage note: figure artifacts were located and inspected; the deposited marker file `cndp2_markers_extended.csv` is the strand-corrected source of truth and should also drive the supplementary sheet (M2).
