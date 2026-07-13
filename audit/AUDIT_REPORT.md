# Independent Correctness Audit — Lac-Phe / CNDP2 MoTrPAC Manuscript

**Manuscript audited:** *A substrate-driven exercise metabolite without an enzyme switch: cross-tissue Lac-Phe in the MoTrPAC rat atlas, and the absence of CNDP2 activation across chromatin, protein, and PTM layers.* (PDF v9, `.tex` v8)

**Method.** Three independent auditors, each in a fresh context and each told to re-derive from the deposited source data rather than trust the manuscript's own summaries or cached outputs: (1) claims & numbers — every quantitative claim extracted, traced to a source artifact, and recomputed; (2) pipeline & figures — every figure/table traced from deposited per-sample CSVs through each transformation, statistical failure modes checked, downstream figures re-run; (3) citations — every in-text citation verified against the cited paper's actual finding (abstract + full text where load-bearing), plus DOI resolution and retraction check.

---

## Headline verdict

**No blocking issues. No conclusion is wrong. No hallucinated statistic.** Every headline number reproduces from the deposited data to the stated precision, every citation supports its attributed claim, and no retracted reference is present. The defects found are **bookkeeping and internal-consistency issues** — a mis-counted reference tally, a headline sample count that mixes two accounting bases, and a supplementary table that was never updated to the strand-corrected coordinates used in the paper body. None changes a finding.

| Track | Checked | Blocking | Major | Minor |
|---|---|---|---|---|
| Claims & numbers | 58 claims | 0 | 1 | 2 |
| Pipeline & figures | 6 figures, Tables 1–8 | 0 | 2 | 3 |
| Citations | 46 refs, 25 claim-links | 0 | 0 | 5 |

The three tracks independently converged on the **same** reference-count and sample-count issues, which raises confidence that those are real and that little else is.

---

## Issues by severity

### BLOCKING
**None.**

### MAJOR

**A1 — Reference count is internally contradictory.** *(claims + citations tracks, independently)*
Location: Abstract & Methods ("46 verified primary sources"); Table 6 caption ("36 of the 36 Lac-Phe literature sources … Amar 2024, Schenk 2024 … listed as refs 37–38"); `references_manifest.csv` (42 rows).
Evidence: the typeset reference list has **46** entries; Amar 2024 and Schenk 2024 are **#45–46, not 37–38**; that leaves 44 non-MoTrPAC references, not 36; the manifest holds 42 verified rows (three of which — Hsu2026, Jermei2025, Wu2025 — are never cited). The four tallies (46 / 38 / 44 / 42) cannot all be right.
Impact: none on the science (the literature synthesis is not a data result); purely bookkeeping.
Action: **FIXED** — Table 6 caption corrected to the true bucketing and "refs 45–46"; abstract/Methods "46" retained as the true total.

**A2 — Headline sample total "1,380" mixes analyzed and deposited counts.** *(pipeline track)*
Location: Abstract, Fig 1 caption, Discussion §3 ("888 RP + 492 HILIC = 1,380 biological samples").
Evidence: the per-sample table feeding every statistic (`alltissue19_persample.csv`) holds **888 RP + 420 HILIC = 1,308** rows. 492 is the HILIC **deposited/extracted** count (Σ `n_biological`); only **420** HILIC samples entered the statistics (`hilic_training_response_stats.csv` n sums to 420), after a near-uniform ~8-sample-per-tissue reduction to the balanced 5/sex/week design. So "1,380" adds 888 *analyzed* RP to 492 *deposited* HILIC — two different bases.
Impact: **none on any statistical result** (all HILIC tests use the 420-sample balanced set); it is a headline-number framing inconsistency.
Action: **FLAGGED for your decision** — this is a headline number, so I did not silently change it. Recommended rewordings below.

**A3 — Supplementary Table S1 (`cndp2_multiomic_supplementary.xlsx`) is strand-naive and contradicts the strand-corrected in-text Tables 2/3/5.** *(pipeline track)*
Location: `Epigenetics_ATAC_METHYL` and `Summary` sheets of the supplement, cited by §2.3 and Data-availability.
Evidence: the deposited supp sheet still carries the *old* annotation the paper explicitly repudiates — `region = promoter_proximal` at `tss_distance = −1694/−1086/−632`, and "26 peaks (3 promoter)" — whereas the corrected annotation (7 upstream + 1 straddle 5′; the three "−1694/−1086/−632" peaks actually ~18 kb 3′) lives only in `cndp2_markers_extended.csv`, which reproduces the in-text tables exactly. A reader checking the cited supp table finds the retracted labeling.
Impact: none on the paper's conclusions (the body tables are correct); the supp artifact is stale.
Action: **FIXED for the reproducibility package** — regenerated the supplement from `cndp2_markers_extended.csv` so Table S1 carries the strand-corrected coordinates; flagged here so you're aware the previously-deposited xlsx was inconsistent.

### MINOR

**m1 — "strict hydrophobicity order" overstates the elution ordering.** §2.1 / Fig 2 caption. The N-lactoyl family RT is *not* strictly monotonic in logP (Lac-Pro, Lac-Val/Lac-Met invert); the real statistic is Spearman ρ = 0.86 (p = 0.007, n = 8). **FIXED** → "hydrophobicity order (Spearman ρ = 0.86)".

**m2 — ubiquityl-K363 "marginal p ≈ 3×10⁻³" is the occupancy-normalized omnibus, not the raw per-timepoint p.** §2.4 / Fig 5 caption. Raw `motrpac_p` = 0.005; the 0.003 value is `occ_omnibus_p` = 0.0025. **FIXED** → labeled "occupancy-normalized omnibus p ≈ 3×10⁻³".

**m3 — undocumented per-tissue balancing (RP 968→888, HILIC ~492→420) and the exact-test recipe are not stated in Methods.** The downstream sex-stratified p-values reproduce **only** with floor-to-min imputation of undetected samples + per-cell median + **exact** Mann–Whitney (scipy's asymptotic default gives Heart-male p = 0.116 vs the deposited 0.151; deltas are unaffected). **FIXED** → Methods now states the balancing rule and the exact-MWU/floor-to-min/median recipe.

**m4 — Table 5 phospho "assay coverage (tissues) = 7" appears to inherit the total-protein tissue count.** The deposited `Proteome_PTM` sheet has CNDP2 phosphosites in **5** tissues, not 7. Does not affect the "no activating phospho change" conclusion (0 sites survive correction regardless). **FLAGGED** — this is a reported data value; recommend confirming against the source object before changing 7→5.

**m5 — Table 6 caption count-framing / 3 uncited manifest rows / print-vs-online year differences / duplicate "Li 2024" keys.** All cosmetic; the 46-item list is correct and fully verified. Folded into the A1 fix where relevant; the rest need no action.

---

## Fix-vs-flag summary

**Fixed directly in the manuscript (mechanical / wording / documentation — no finding, number-of-result, or interpretation changed):**
- A1 reference numbering/framing (Table 6 caption → "refs 45–46", accurate bucketing)
- m1 "strict hydrophobicity order" → "hydrophobicity order (Spearman ρ = 0.86)"
- m2 K363 p-value labeled as occupancy-normalized omnibus
- m3 Methods: per-tissue balancing rule + exact-MWU/floor-to-min/median recipe documented

**Fixed in the reproducibility package (stale artifact brought into agreement with the already-correct paper body):**
- A3 regenerated strand-corrected supplementary Table S1

**Flagged for your review (would alter a reported number — not silently changed):**
- A2 headline "1,380" sample count. Options: (i) "1,380 samples extracted (888 RP and 420 HILIC analyzed; 492 HILIC deposited)"; (ii) report analyzed total 1,308 (888 RP + 420 HILIC); (iii) keep 1,380 but define it explicitly as extracted/deposited and add the analyzed n. Recommendation: (i) or (ii).
- m4 Table 5 phospho coverage 7 → 5 (confirm against source first).

---

## Verified-and-passed checklist

**Claims / numbers (recomputed from deposited data, manuscript = recomputed):**
- [x] Sample partition: 9 RP tissues (both modes) + 10 HILIC = 19; 888 RP (445 neg + 443 pos); 18 RP studies; decoy n = 64
- [x] Heart RP-pos selection-free omnibus **q = 0.014** (BH across 18 studies; analytic KW p = 0.0031)
- [x] Heart selection-aware **p = 0.031/0.032**; **no** tissue clears selection-aware q < 0.10 (min 0.19)
- [x] Heart is the sole selection-free *increase* surviving FDR; kidney/colon are decreases, adrenal interference-suspect
- [x] Decoy naïve FP **3.1%** (2/64); true Lac-Phe rank 1/33
- [x] Peak folds plasma 1.41× / heart 2.11× / white adipose 2.43×
- [x] Female peak Δlog₂ +0.75 / +0.95 / +1.70 (all p = 0.008); male WAT +1.37 (p = 0.036); males n.s. in plasma/heart
- [x] MS1 identity: fragment r = 0.96 (p = 4×10⁻²⁷, n = 50); RT–logP ρ = 0.86; isotope M+1/M 11.3% obs (13.5% theory); apex RT 3.18 min; C₁₂H₁₅NO₄ 236.093 / 238.107
- [x] Positive control: dose-response r = 0.75 (44 pts) / 0.37 (all 12); sign agreement 73%; 11/12 within ±5 ppm (tyrosine −5.1 outlier); citrate 0.97 / phenylacetate 0.99
- [x] Tyrosine mis-annotation: released 180.0578 ≈ 49 ppm below true [M−H]⁻ 180.0666
- [x] CNDP2: 26 ATAC + 125 methyl = 151 features; **0/151** training-significant; 8 ATAC + 31 methyl 5′-of-TSS; promoter CpG-island 31 features; gene-body CpG 25
- [x] Liver total protein sel-FDR 0.012 (all decreases); acetyl-K364 sel-FDR 0.018 (decrease); phospho 0 survive
- [x] Analogs: triazole DILI 0.74 / reduced amide 0.14; composite 0.45·stab+0.40·act+0.15·ADMET reproduces all 7; triazole composite 0.87; all 12 pass Lipinski/Veber

**Pipeline / statistics:**
- [x] All 6 figures traced to source; figure filename↔caption-number mapping verified (files are offset by one — noted for typesetter)
- [x] Selection-free KW omnibus and selection-aware 5,000× permutation null correctly constructed; BH-FDR reproducible across the 18 study-modes
- [x] RP+HILIC merge — no misalignment or double-counting at tissue/mode/animal level
- [x] Tests appropriate for small-n, non-normal, cross-sectional, unpaired design; sex stratification correct; multiple-comparison correction present at both bars
- [x] Downstream Fig 1 / Fig 3 / Fig 4 and full stats table re-derived from deposited per-sample CSVs
- [~] Raw-spectra extraction from vendor archives — **not re-runnable in-session** (multi-GB Metabolomics Workbench archives + x86 vendor reader); verified against deposited per-sample outputs. The fragment r = 0.96, mass-accuracy ppm, and isotope ratios are deposited *summaries* and are verifiable only as such, not recomputable from deposited per-sample data. Genome-wide feature counts (Table 4) come from the external `MotrpacRatTraining6moData` objects; the CNDP2 = 0 side of each row is verified from the deposited marker files.

**Citations:**
- [x] 46/46 reference DOIs resolve against CrossRef; none flagged retracted
- [x] Two named retracted DOIs (Hedaya 2025 10.3390/cells14161296; Ying 2025 10.1186/s12974-025-03495-3) absent from source, manifest, and delta bib
- [x] 25 mechanistic/quantitative claim-to-source links verified against the cited paper's actual finding, including the load-bearing anchors: Li 2022 (r = 0.82, p < 0.0001; 50 mg/kg; obese-not-lean at 150 mg/kg — PMC full text), Amar 2024 ("19 tissues" exact), Xiao 2024a (GFRAL exclusion — full text), Liu 2025 (AgRP/K_ATP + MC4R/NPY1R PVH — full text), Li 2024 (SLC17A1/3 urine/plasma decoupling), Jansen 2015 (CNDP2 reverse proteolysis + PKU), Moya-Garzon 2024 (BHB shunt)
- [x] NCT06743009 verified on ClinicalTrials.gov (Aarhus, IV Lac-Phe vs saline, overweight/obese, completed)

**Overstatement check — all calibrations appropriately hedged and supported:** MSI Level 2 (no MS/MS in deposit, absent from libraries); heart-only selection-free / nothing selection-aware; plasma & white adipose "hypothesis-generating"; CNDP2 convergent-negative framed as direction not magnitude; analog panel "computational prioritisation, not validation," Boltz-2 "prepared, not run, not in ranking." No claim overstates the data.

---

## Component report artifacts
- `audit_claims.md` — claims & numbers (58 claims, full recomputation ledger)
- `audit_pipeline.md` — pipeline, statistics, figures (verification ledger + failure-mode audit + raw-extraction boundary)
- `audit_citations.md` — citations (46-DOI resolution, 25 claim-link verifications, retraction re-check)


---

## Post-audit revision note

After this audit, the manuscript was revised at the authors' direction: the title was changed to
*Multi-Omic Profiling Reveals Lac-Phe as a Substrate-Driven Exerkine Independent of CNDP2 Activation*;
the abstract was shortened to one page; Figure 3 was regenerated to show all 19 tissues with the
reversed-phase and HILIC platforms graphed separately (sex-stratified); the Boltz-2 co-fold was
**run** (previously prepared-not-run) and its results integrated as a new Figure 7, a Table 8
co-fold column, and Discussion §3.3 support for the HCAR1/GPR81 deorphanization hypothesis; the
Methods co-fold subsection and figure float ordering were updated accordingly. The audit findings
above (the A1 reference tally, A3 strand-corrected supplement, m1–m3 wording/documentation fixes)
were applied in that revision. The A2 headline sample-count wording and the m4 Table 5 phospho
coverage remain flagged for author decision.
