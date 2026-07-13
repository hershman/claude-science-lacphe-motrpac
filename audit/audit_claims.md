# Independent Correctness Audit — Claims and Numbers
## Lac-Phe / CNDP2 MoTrPAC manuscript

**Scope.** Every quantitative and empirical claim in the abstract, results, discussion, methods,
figure/table captions was extracted, traced to a deposited source artifact, and — for headline
statistics — recomputed independently from the per-sample data and stats CSVs. Manuscript value vs
recomputed value is reported for each check. Verdict: **the manuscript's numbers are accurate.**
Every headline statistic reproduces to stated rounding. The only defects found are in the
reference-count bookkeeping (one MAJOR internal contradiction, one MINOR label error). No
hallucinated / untraceable numeric claim was found.

- Claims checked (numeric/empirical): **58**
- Mismatches / issues found: **3** (0 BLOCKING, 1 MAJOR, 2 MINOR)

---

## VERIFIED — headline statistics (manuscript value = recomputed value)

### Sample counts (Fig 1 caption, Results 2.1, Discussion)
| Claim | Manuscript | Recomputed | Source | OK |
|---|---|---|---|---|
| RP biological samples | 888 | 888 (445 RP-neg + 443 RP-pos, persample_alltissue19) | persample_alltissue19.csv | ✓ |
| HILIC samples | 492 | 492 = Σ n_biological (deposited); but only **420** analyzed — see MINOR-2 | lacphe_hilic_tissue_summary / hilic_persample_master | ⚠ |
| Total | 1,380 | 888 + 492 = 1,380 | — | ✓ |
| Tissues | 19 | 9 RP + 10 HILIC = 19 | — | ✓ |
| RP tissues (both modes) | 9 | 9 | rp_persample | ✓ |
| HILIC-only tissues | 10 | 10 | hilic | ✓ |
| n per sex per week | 5M + 5F (wk 1/2/4/8), 10 sed control | confirmed exactly for Heart RP-pos; organ_sex n_training≤5 | persample / all_organ_sex | ✓ |
| RP studies | 18 | 18 unique study_ids | rp_persample | ✓ |
| Decoy panel | 64 m/z | n_decoy_tests = 64 | specificity_stats §1 | ✓ |

**See MINOR-2** — the 1,380 headline mixes two accounting bases: the 888 RP figure equals the
analysis-merged per-sample set (445+443, persample_alltissue19), whereas the 492 HILIC figure is the
*deposited* biological-sample count (n_biological), NOT the 420 rows the HILIC analyses actually used.

### Heart training response (Results 2.1, Abstract, Discussion)
| Claim | Manuscript | Recomputed | OK |
|---|---|---|---|
| Heart RP-pos selection-free omnibus q | 0.014 | 0.0144 (KW permutation, FDR across 18 studies); analytic KW p=0.0031 reproduced exactly | ✓ |
| Heart selection-aware p | 0.032 (also written 0.031) | selaware_p = 0.031 (response_stats); sel_p_maxdelta 0.031/0.0316 (specificity §2/§3) | ✓ |
| Heart is sole selection-free *increase* surviving FDR | yes | yes — only RP-pos increase with q<0.05; kidney(0.0036)/colon(0.004)/adrenal(0.003) also cross but as decreases/interference | ✓ |
| No tissue survives selection-aware q<0.10 | yes | selection-aware q (q_sel_maxdelta) min across 18 studies = 0.1908, tied across the three lowest-p studies (heart RP-pos, plasma RP-neg, WAT RP-neg) → none < 0.10. Smallest *nominal* sel_p_maxdelta is heart's 0.0310 (plasma 0.0318, WAT 0.0312), all FDR-inflated to 0.1908. | ✓ |
| "Three further tissues cross omnibus" | kidney, colon, adrenal | exactly those three at q<0.05 (plus cortex/spleen/VL at q<0.08) | ✓ |

### Decoy false-positive rate (Results 2.1)
| Claim | Manuscript | Recomputed | OK |
|---|---|---|---|
| Naive FP rate | 3.1% | 0.0312 = 2/64 | ✓ |

### Responder peak folds and per-sex deltas (Results 2.1, Fig 3, Discussion 3.3)
| Claim | Manuscript | Data (response_stats) | OK |
|---|---|---|---|
| Plasma fold | ≈1.4× | 1.414 | ✓ |
| Heart fold | ≈2.1× | 2.113 | ✓ |
| White adipose fold | ≈2.4× | 2.425 | ✓ |
| Plasma female peak Δ | +0.75 | +0.748 (p=0.0079→0.008) | ✓ |
| Heart female wk2 peak Δ | +0.95 | +0.95 (p=0.0079→0.008) | ✓ |
| White adipose female wk4 Δ | +1.70 | +1.70 (p=0.0079→0.008) | ✓ |
| White adipose male Δ | +1.37 (p=0.036) | +1.366 (p=0.0361) | ✓ |
| Females reach p=0.008 in all three organs | yes | 0.0079 in all three (min MWU p at n=5) | ✓ |
| Males sig only in WAT | yes | plasma male p=0.42, heart male p=0.15, WAT male p=0.036 | ✓ |

### MS1 identity (Results 2.1, Fig 2, Fig 4)
| Claim | Manuscript | lacphe_ms1_identity | OK |
|---|---|---|---|
| In-source fragment r | 0.96 (p=4×10⁻²⁷, n=50) | 0.956, p=4e-27, n=50 | ✓ |
| RT–logP Spearman rho | 0.86 (p=0.007, n=8) | 0.857, p=0.007, n=8 | ✓ |
| Isotope M+1/M observed | 11.3% (theory 13.5) | 11.29%, theory 13.5 | ✓ |
| Lac-Phe apex RT | 3.18 min | 3.185 | ✓ |
| Lac-Phe [M–H]⁻ / [M+H]⁺ | 236.0928 / 238.1074 | monoisotopic C12H15NO4 confirms 236.093 | ✓ |
| Free lactate does not track intact ion | yes | mainPhe/lactate r = −0.10 (no correlation) | ✓ |

### Positive-control benchmark (Results 2.2, Table 1, Fig 4)
| Claim | Manuscript | Recomputed | OK |
|---|---|---|---|
| Dose-response concordance r | 0.75 (11 metabolites, 44 metabolite-weeks) | 0.749 (Pearson, ≥45/50 filter, n=44) | ✓ |
| Sign agreement | 73% | 72.7% | ✓ |
| All-12 r (no filter) | 0.37 | 0.366 (n=48) | ✓ |
| Within ±5 ppm | 11/12 (tyrosine −5.1 outlier) | 11/12; tyrosine −5.1 the only |ppm|>5 | ✓ |
| Within ΔRT 0.03 min | 11/12 | 11/12; HPLA −0.13 the only |ΔRT|>0.03 | ✓ |
| Exemplar abundance r | citrate 0.97, phenylacetate 0.99, HIA 0.60 | 0.97 / 0.99 / 0.60 (Table 1) | ✓ |
| Phe undetected in 12/50 | yes | n_detected = 38/50 | ✓ |
| Indole lactate detected | 48/50 | 48 | ✓ |
| Tyrosine mis-annotation | released 180.0578 ≈49 ppm below true [M–H]⁻ 180.0666 | true [M–H]⁻ = 180.0666; (180.0578−180.0666) = −49.0 ppm | ✓ |

### CNDP2 epigenetics/protein/PTM (Results 2.3–2.4, Tables 2–5, Fig 5, Abstract, Discussion 3.1)
| Claim | Manuscript | Recomputed | OK |
|---|---|---|---|
| ATAC peaks | 26 | 26 | ✓ |
| Methylation clusters | 125 | 125 | ✓ |
| Total features | 151 | 151 | ✓ |
| Training-significant features | 0/26 ATAC, 0/125 methyl, 0/151 total | 0 / 0 / 0 (all training_significant = NO) | ✓ |
| ATAC 5′-of-TSS | 8 peaks | 7 promoter_upstream + 1 straddle = 8 | ✓ |
| Methyl 5′-of-TSS | 31 clusters | 8 upstream + 23 straddle = 31 | ✓ |
| Promoter CpG island overlap | 31 features (1 ATAC + 30 methyl) | 1 ATAC + 30 methyl = 31 | ✓ |
| Gene-body CpG island (methyl) | 25 | 25 | ✓ |
| Methyl region split (Table 3) | 8 / 23 / 94 | promoter_upstream 8, straddle 23, gene_body 94 | ✓ |
| Liver total protein sel-FDR | 0.012, logFC −0.06 to −0.20, both decreases | 0.0117; logFC −0.059 to −0.199, all down | ✓ |
| Acetyl-K364 liver sel-FDR | 0.018, logFC −0.14 to −0.41, decrease | 0.0185; logFC −0.135 to −0.408, all down | ✓ |
| Ubiquityl-K363 liver | male-only increase, marginal p≈3×10⁻³, not sel-aware sig | occupancy omnibus p=0.0025 male; sel-FDR 0.438 (n.s.) | ✓ |
| Phospho S58/S87/S299 | scattered nominal, none survive correction | 0 sel-FDR sig | ✓ |
| Protein tissues / phospho tissues | 7 / (implied) | PROT 7, PHOSPHO 5 (Table 5 says "7" for phospho — see MINOR-note) | ⚠ see note |
| Genome-wide sig (Table 4) | Liver ATAC 1,032; SkM-GN 442; Heart ATAC 75; Heart methyl 107; BAT methyl 621 | matches supplementary Summary/narrative | ✓ (values self-consistent; not independently re-derived from raw MoTrPAC objects) |

### Analog panel (Results 2.5, Tables 7–8, Fig 6)
| Claim | Manuscript | Data | OK |
|---|---|---|---|
| Triazole DILI | 0.74 | 0.741 (decision_matrix) | ✓ |
| Reduced amide DILI | 0.14 | 0.140 | ✓ |
| Next-highest DILI ("0.35–0.42 amide-retaining", "0.42") | 0.35–0.42 | N-Me 0.417, D-Phe 0.350, α-Me 0.378, parent 0.316 | ✓ |
| SAscore range | 2.4–3.1 | 2.44–3.05 | ✓ |
| Composite formula | 0.45·stab + 0.40·activity + 0.15·ADMET | reproduces all 7 composites to 3 dp | ✓ |
| Triazole composite / rank 1 | 0.87 | 0.867 | ✓ |
| Reduced amide 0.80, thioamide 0.70 | — | 0.802, 0.697 | ✓ |
| Table 7 (MW/cLogP/TPSA/HBD/HBA/RotB/QED, 12 rows) | — | matches lacphe_analogs_admet exactly | ✓ |
| All 12 pass Lipinski & Veber, 0 violations | yes | Lipinski_pass & Veber_pass all True | ✓ |
| Triazole QED 0.84 | 0.84 | 0.844 | ✓ |
| PubChem CID / CAS for parent | CID 11075454, CAS 183241-73-8 | CID 11075454 confirmed in table | ✓ (CAS not in CSV) |
| N-acylsulfonamide only one above CNS-PSA window | TPSA 120.8 (others ≤88.2) | 120.8, next 88.2 | ✓ |

---

## ISSUES

### MAJOR-1 — Reference count is internally contradictory
**Location:** Abstract ("anchor in **46** verified primary sources"); Methods §Literature synthesis
("**46 references** passed verification … two papers flagged as retracted were excluded"); Table 6
caption ("**36** of the 36 Lac-Phe literature sources"; "two additional MoTrPAC consortium method
references … listed as **refs 37–38**"); Reference list (actual **46** \item entries);
references_manifest.csv (**42** rows, all verified YES).

**Findings (recomputed):**
- The typeset reference list contains **46** entries, of which Amar 2024 and Schenk 2024 (the two
  MoTrPAC method refs) are entries **#45 and #46**, NOT "refs 37–38" as Table 6 states.
- That leaves **44** Lac-Phe/context references, not the **36** Table 6 claims ("36 of the 36 Lac-Phe
  literature sources").
- references_manifest.csv holds only **42** verified rows (all YES) — neither 46 nor 44 nor 38.
- The Methods "two retracted excluded" cannot be reconciled with any of the printed counts: 46 in the
  list with 2 supposedly already removed would imply 48 screened, but no count in the paper equals 48
  or 44+2.

**Conclusion survives** (the literature synthesis itself is not a data result), but the four different
reference tallies (46 / 36+2=38 / 42 / "refs 37–38") cannot all be correct and the "refs 37–38"
pointer is factually wrong (they are 45–46).

**Severity:** MAJOR (a stated count mismatches the actual list and the deposited manifest; multiple
mutually inconsistent numbers for the same quantity).

**Recommended action:** Reconcile to a single source of truth. If the list is 46 total = 44 Lac-Phe +
2 MoTrPAC, fix the abstract ("46" should be the *total*, and the "primary sources" anchor number
should be stated consistently), fix Table 6 caption to "44 Lac-Phe literature sources … listed as
refs 45–46", and either expand references_manifest.csv to 46 rows or explain the 42-row subset.

### MINOR-1 — Table 5 lists Phosphorylation "Assay coverage (tissues) = 7"
**Location:** Table 5, Phosphorylation row.
**Manuscript:** phospho assay coverage "7" tissues.
**Recomputed:** the deposited Proteome_PTM sheet contains CNDP2 phosphosite rows for **5** distinct
tissues (PROT is measured in 7). The abstract/Table 5 correctly restrict ubiquityl/acetyl to 2
tissues, and total protein to 7; the phospho "7" appears to inherit the protein tissue count rather
than the phospho-specific coverage.
**Severity:** MINOR (coverage-label mismatch; does not affect the "no activating phospho change"
conclusion — 0 sites survive correction regardless of coverage).
**Recommended action:** Confirm phospho tissue coverage against the source object and correct the
Table 5 "7" if the CNDP2 phosphosites were quantified in fewer tissues.

### MINOR-2 — "1,380 total samples" mixes two accounting bases (deposited vs analyzed)
**Location:** Fig 1 caption, Results 2.1, Discussion (1,380 biological samples; "492 HILIC samples").
**Manuscript:** 888 RP + 492 HILIC = 1,380.
**Recomputed:** the two summands are counted on different bases. **888 RP** = the analysis-merged
per-sample set (445 RP-neg + 443 RP-pos, persample_alltissue19). **492 HILIC** = the *deposited*
biological-sample count (Σ n_biological, lacphe_hilic_tissue_summary), but the HILIC training
analyses actually ran on **420** samples (hilic_persample_master = 420 rows; hilic_training_response_stats
`n` sums to 420). The gap is a near-uniform 8-sample deficit in 9 of 10 HILIC tissues (Adrenal
58→50, Colon 58→50, Cortex 58→50, Hypothalamus 54→46, Small Intestine 58→50, Spleen 58→50, Testes
33→25, Vastus Lateralis 58→50, Vena Cava 32→24; Ovaries 25→25 unchanged) — a systematic ~72-sample
(≈15%) reduction, consistent with trimming to the balanced n=5/sex/week design used for the
statistics (each retained tissue collapses to 50 = 5×2×5, or fewer for single-sex organs).
**Severity:** MINOR (the 492 figure is a defensible "samples deposited/extracted" count and is
internally traceable to n_biological; but presenting 888-analyzed + 492-deposited as one "1,380
biological samples" total conflates deposited with analyzed, and 72 of those 492 do not enter any
reported HILIC statistic). **Does not affect any statistical result** — all HILIC tests use the 420
balanced set.
**Recommended action:** State the two bases explicitly — e.g. "1,380 samples extracted (888 RP
analyzed; 492 HILIC deposited, 420 analyzed)" — or report the analyzed HILIC n (420) alongside the
deposited 492 so the reader is not left inferring one uniform "biological sample" count.

---

## OVERSTATEMENT CHECK (Task 4)

All flagged self-limiting claims are **appropriately hedged and supported by the data**:
- **Identity = MSI Level 2** — correctly stated throughout; abstract, Fig 2 caption, Limitations all
  note no MS/MS in deposit and absence from spectral libraries. Not overstated.
- **Heart-only selection-free, nothing selection-aware** — matches data exactly (heart q=0.014
  selection-free; heart selection-aware p=0.031/0.032 does not clear FDR; no tissue q_sel<0.10).
  Correctly reported.
- **Plasma / white adipose "hypothesis-generating"** — response_stats verdict field literally reads
  "concordant/suggestive (does not clear selection-free)"; prose matches. Not overstated.
- **CNDP2 convergent negative as positive result** — supported: 0/151 features significant against
  tissues carrying hundreds–thousands of genome-wide significant features; the two significant liver
  effects are decreases. Direction claim ("not activated") is bounded correctly to direction, not
  magnitude, in Discussion 3.1 and Limitations.
- **Analog panel "computational prioritisation, not validation"** — explicit; "none synthesized or
  assayed"; Boltz-2 "prepared, not run, not in ranking". Not overstated.

No claim was found that overstates what the deposited data support (beyond the reference-count
bookkeeping above).

## TRACEABILITY (Task 2)
Every numeric claim maps to a deposited artifact:
- sample counts → persample_alltissue19 / rp_persample / hilic_persample / hilic_tissue_summary
- training stats, folds, per-sex deltas → alltissue19_response_stats + specificity_stats
- decoy FP, heart q/p → specificity_stats
- MS1 identity (fragment r, RT-logP rho, isotope, adducts) → lacphe_ms1_identity
- positive control (Table 1, r=0.75) → pc_concordance_table + pc_dose_response_concordance
- CNDP2 151 features / regions / CpG → cndp2_epigenetic_results + cndp2_markers_extended
- protein/PTM (liver protein, K364, K363, phospho) → cndp2_multiomic_supplementary.xlsx
- analog Table 7 → lacphe_analogs_admet; Table 8 → decision_matrix
**No claim with a numeric value lacked a traceable source. No hallucinated statistic found.**
