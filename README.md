# Lac-Phe as a Substrate-Driven Exerkine in the MoTrPAC Atlas

### Recovering an "invisible" exercise metabolite from raw spectra, showing its kinetics are substrate- (not enzyme-) driven, and computationally designing hydrolysis-resistant mimetics

Reproducibility package — regeneration code, LaTeX source, figures, deposited analysis-ready data, an independent three-track correctness audit, and Claude Science session logs — for:

> **Multi-Omic Profiling Reveals Lac-Phe as a Substrate-Driven Exerkine Independent of CNDP2 Activation**
> Steven Hershman (Independent Researcher) · Claude Science (Anthropic)

**Built with Claude — Life Sciences Hackathon · Researcher Track**
📺 Demo video (≤3 min): https://youtu.be/iSjRvYeJd44
📦 Repository: https://github.com/hershman/claude-science-lacphe-motrpac

---

## TL;DR

*N*-lactoyl-phenylalanine (Lac-Phe) is a CNDP2-derived, exercise-inducible metabolite that suppresses feeding and adiposity — yet it appears in **no released MoTrPAC metabolomics feature table**. Returning to the raw mass-spectrometry files, this project recovered a Lac-Phe-mass ion across **all 19 PASS1B rat tissues**, showed the training response is **transient and female-predominant** (statistically robust only in the **heart**, q = 0.014, on the selection-free omnibus), and demonstrated that **CNDP2 is not activated** by training at any regulatory layer — implying Lac-Phe production is **substrate-driven flux** (local lactate + phenylalanine), not enzyme induction. Because that makes molecular *persistence* the tractable therapeutic lever, an open-data computational funnel triages **hydrolysis-resistant analogs**, nominating a **1,2,3-triazole isostere** (backups: reduced amide, thioamide), with the two leads corroborated by Boltz-2 co-folding.

The whole pipeline — from raw-spectra extraction to statistics, figures, manuscript, and audit — was orchestrated end-to-end by **Claude Science**.

---

## Why it matters

Exercise delivers profound systemic benefits, but adherence is a major clinical hurdle — motivating "exercise mimetics" that capture some of those benefits pharmacologically. Lac-Phe is among the most compelling candidates. This project contributes two things:

1. **A data rescue that resolves a mechanistic paradox.** By recovering Lac-Phe from raw spectra in the largest molecular map of exercise adaptation, it answers two questions prior work conflated: *is Lac-Phe present and training-responsive in these tissues?* (yes, recovered from raw data) and *if so, is it because CNDP2 is turned up, or because the enzyme is handed more substrate?* (substrate — CNDP2 is silent across chromatin, methylation, protein, and PTM layers).
2. **An end-to-end, open-data design pipeline.** A reusable computational funnel — quantum-chemical stability → pharmacophore alignment → ADMET → docking → Boltz-2 co-fold — that de-risks and prioritizes durable Lac-Phe mimetics *before* costly wet-lab synthesis.

---

## Key findings (stated at their true confidence)

- **Signal recovery.** A Lac-Phe-mass ion (C₁₂H₁₅NO₄; [M−H]⁻ 236.0928, [M+H]⁺ 238.1074) is detectable within 5 ppm at a consistent retention time in **every one of the 19 tissues**, from 18 reversed-phase studies (9 tissues, 888 samples) and 10 HILIC-only tissues (492 deposited / 420 analyzed samples).
- **Identity — MSI Level 2.** Four independent MS1 lines of evidence (hydrophobicity-ordered N-lactoyl-amino-acid family ρ = 0.86; co-eluting in-source [Phe−H]⁻ fragment tracking the intact ion at r = 0.96; matching isotope envelope; coherent adduct pattern) place the assignment at a defensible **MSI Level 2 (probable structure)**, pending an authentic-standard, MS/MS-enabled follow-up.
- **Pipeline validated.** A positive-control benchmark on twelve released metabolites reproduces their mass (**11/12 within ±5 ppm**), retention time, and training dose-response (**r = 0.75**).
- **Training response.** Transient (peaks 1–4 weeks, decays by week 8) and **female-predominant**. On a selection-free timecourse omnibus across all 19 tissues and both chromatographic platforms, it is statistically robust **only in the heart (q = 0.014)**; **no tissue survives** the stricter selection-aware permutation correction.
- **Mechanism: substrate, not enzyme.** Across 8 tissues, **0/26 chromatin-accessibility peaks** and **0/125 DNA-methylation clusters** at the CNDP2 locus reach significance (including a strand-corrected promoter CpG island over the TSS), while CNDP2 protein and its modification sites are flat or, in liver, decreasing. Since the same tissues yield thousands of training-responsive epigenetic features genome-wide, this convergent silence is a **positive result**: Lac-Phe is **substrate-driven flux** gated by local lactate and phenylalanine.
- **Design output.** A five-stage computational funnel over the parent plus six analogs nominates a **1,2,3-triazole isostere** (makes amide hydrolysis structurally impossible while preserving shape and the load-bearing carboxylate; one predicted DILI flag to check experimentally). Backups: **reduced amide** (cleanest ADMET, highest Boltz-2 binder probability at 0.73) and **thioamide** (most shape-conservative). The **true receptor is unknown**; HCAR1/GPR81 is the top *candidate* pocket, and Boltz-2 enters the paper as orthogonal structural corroboration, not measured affinity.

---

## Repository structure

```
claude-science-lacphe-motrpac/
├── README.md
├── Makefile                         # stats → figures → transparent backgrounds → compiled PDF
├── requirements.txt                 # pinned Python deps
├── cndp2_lacphe_substrate_not_switch.pdf   # top-level copy of the compiled manuscript
│
├── code/                            # regeneration scripts (run in this order)
│   ├── 01_compute_statistics.py     # selection-free KW omnibus + 5,000× within-sex permutation null + 64-m/z decoy panel (seed=42)
│   ├── 02_response_stats.py         # per-tissue×mode training response: floor-to-min impute, exact Mann–Whitney vs wk0, sex-stratified deltas
│   ├── 03_make_figures.py           # 19-tissue Δlog₂ timecourse (Fig 1) + sex-stratified responder values (Fig 3)
│   ├── 04_transparent_backgrounds.py# border flood-fill → transparent figure backgrounds
│   ├── 05_verify_citations.py       # CrossRef DOI resolution + retraction check (network required)
│   └── 06_boltz_cofold_figure.py    # Boltz-2 co-fold panel (Fig 7) from deposited affinity scores
│
├── data/                            # deposited, analysis-ready inputs (extraction outputs, not raw spectra)
│   ├── alltissue_persample.csv, alltissue19_persample.csv, hilic_persample_master.csv
│   ├── *_response_stats.csv, *_sex_stratified_stats.csv, specificity_stats.csv
│   ├── lacphe_ms1_identity.csv, lacphe_reference_fragments.json, fragment_spectra_pair.json
│   ├── cndp2_markers_extended.csv, cndp2_epigenetic_results.csv, cndp2_multiomic_supplementary.xlsx
│   ├── lacphe_analogs_admet.csv, shortlist_for_boltz.csv, decision_matrix.csv
│   ├── boltz_affinity_scores.csv, boltz_HCAR1_structures.tar.gz, boltz_local.tar.gz
│   ├── references_manifest.csv
│   └── Lac-Phe_analog_report.md     # full computational design-campaign report
│
├── paper/
│   ├── cndp2_lacphe_substrate_not_switch.tex    # manuscript source
│   ├── cndp2_lacphe_substrate_not_switch.pdf
│   ├── references_delta.bib
│   └── figures/                     # figure1_organ_timecourse, figure1c_spectrum, figure2_sex_responders,
│                                    #   figure3_positive_control, figure4_cndp2_multiomic, figure5_drug_design, figure7_boltz_cofold
│
├── audit/                           # independent correctness audit
│   ├── AUDIT_REPORT.md              # consolidated verdict
│   ├── audit_claims.md              # every quantitative claim re-derived
│   ├── audit_pipeline.md            # every figure/table traced from deposited CSVs
│   └── audit_citations.md           # every citation verified against the cited paper
│
├── sessions/                        # Claude Science session logs (JSON) for extra reproducibility
│   ├── *.json
│   └── readme.md
│
└── alt ai slop/                     # earlier candidate projects taken to draft before Lac-Phe was selected
    ├── HCC_subtype_dependency_report.pdf
    ├── SARS_CoV2_interactome_report.pdf
    ├── bc_interactome_report.pdf
    ├── bhlhe40_paper_science.pdf
    └── project_master_report.pdf
```

---

## Quick start (clean checkout → compiled PDF)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make all            # stats → figures → transparent backgrounds → compiled PDF
```

`make all` runs, in order:

1. **`code/01_compute_statistics.py`** — selection-free Kruskal–Wallis omnibus + selection-aware 5,000× within-sex permutation null + 64-m/z decoy panel. Reproduces `data/specificity_stats.csv` (heart selection-free q = 0.014, heart selection-aware p = 0.031, decoy FP 3.1%). Seeded (`seed=42`).
2. **`code/02_response_stats.py`** — per-tissue×mode training response: floor-to-min imputation of undetected samples, per-cell median, exact Mann–Whitney vs week 0, sex-stratified peak deltas/p-values, fold-changes. Reproduces `data/alltissue19_response_stats.csv`.
3. **`code/03_make_figures.py`** — regenerates the 19-tissue Δlog₂ timecourse (Figure 1) from the per-sample data and prints the all-tissue sex-stratified responder values behind Figure 3.
4. **`code/06_boltz_cofold_figure.py`** — regenerates the Boltz-2 co-fold panel (Figure 7) from `data/boltz_affinity_scores.csv`. The co-fold itself is run separately on a local GPU via `data/boltz_local.tar.gz`; this script plots the deposited scores.
5. **`code/04_transparent_backgrounds.py`** — border flood-fill so figure backgrounds are transparent.
6. **`make pdf`** — `pdflatex → bibtex → pdflatex ×2` on `paper/cndp2_lacphe_substrate_not_switch.tex`.

Verify citations (network required):

```bash
make citations      # runs code/05_verify_citations.py — 46/46 DOIs resolve against CrossRef, 0 retracted
```

**Requirements:** Python deps are pinned in `requirements.txt` (pandas 2.3.3, numpy 2.4.6, scipy 1.17.1, matplotlib 3.11.0, statsmodels 0.14.6, Pillow 12.3.0, openpyxl 3.1.5, requests 2.34.2, seaborn 0.13.2). `make pdf` additionally needs a LaTeX toolchain (TeX Live 2024 / MacTeX).

---

## Reproducibility boundary (read this)

The **raw-spectra extraction** stage — decoding Agilent `.d` and Thermo `.raw`/mzML acquisitions from the multi-gigabyte Metabolomics Workbench archives (studies **ST002628–ST002916**) via HTTP range requests and an x86 vendor reader — is **not re-runnable from this package**; it needs the full vendor archives and platform-specific tooling. This package therefore starts from the **deposited, analysis-ready per-sample tables** that stage produced (`data/*_persample*.csv`), which are sufficient to regenerate every downstream statistic and figure. Three identity metrics (in-source fragment r = 0.96, mass-accuracy ppm, isotope-envelope ratio) live on the extraction side of this boundary and are provided as deposited summaries (`data/lacphe_ms1_identity.csv`, `data/fragment_spectra_pair.json`), not recomputed here. Genome-wide feature counts come from the external `MotrpacRatTraining6moData` package; the CNDP2 = 0 side of each is verified from `data/cndp2_markers_extended.csv`.

The `sessions/` logs are included precisely because the Claude Science export alone is not a complete reproducibility record — they capture the extraction-stage provenance that sits outside the `make` targets.

---

## How Claude was used

This project was run end-to-end with **Claude Science**, which appears as a co-author on the manuscript. Claude contributed across the full research lifecycle:

- **Ideation & selection.** Roughly a dozen candidate projects were each taken to draft stage; Lac-Phe was chosen as the strongest. The alternates are preserved under `alt ai slop/` (HCC subtype-dependency, SARS-CoV-2 interactome, breast-cancer interactome, BHLHE40, and a master report).
- **Execution.** Orchestrating the raw-spectra re-analysis, cross-tissue quantification, CNDP2 multi-omic dissection, and the mimetic-design funnel.
- **Heterogeneous compute.** Running locally for Agilent decoding and statistics, while **dispatching the x86-only Thermo vendor-reader step to ephemeral Linux containers on Modal**, and avoiding multi-gigabyte downloads via ZIP64 HTTP range requests. When Modal spend became a concern, tools like **Boltz-2** were run from the command line on a local **M3 Max** GPU.
- **Write-up, figures & review.** Drafting the manuscript and figures, generating the regeneration scripts, and providing peer-review-style feedback — including the independent three-track audit in `audit/`.

---

## Independent correctness audit

`audit/AUDIT_REPORT.md` consolidates a three-track audit (claims & numbers, pipeline & figures, citations), each performed by an independent auditor working from the deposited source data rather than the manuscript's own summaries.

**Headline verdict: no blocking issues; no conclusion wrong; no hallucinated statistic.** Every headline number reproduces from the deposited data to the stated precision, every citation supports its attributed claim, and no retracted reference is present. The defects found are bookkeeping/internal-consistency issues — a mis-counted reference tally (fixed) and a headline sample count (`1,380`) that mixes analyzed RP with deposited HILIC totals (flagged for author decision; the 420-sample balanced set drives every statistic, so no result changes). Component reports: `audit/audit_claims.md`, `audit/audit_pipeline.md`, `audit/audit_citations.md`.

---

## Data provenance

The underlying data are **MoTrPAC PASS1B** (Amar et al. 2024; Schenk et al. 2024), deposited on **Metabolomics Workbench** (study series ST002628–ST002916) and in the **`MotrpacRatTraining6moData`** R package. `data/cndp2_multiomic_supplementary.xlsx` (Supplementary Table S1) carries **strand-corrected** CNDP2-locus coordinates; the superseded strand-naive annotation is retained in the `*_strandnaive_OLD` columns for transparency. All redistributed material here is derived (per-sample tables, stats, figures) plus pointers to the original public sources.

---

## Notes on figures

- Figure filenames are offset from caption numbers (e.g. `figure1c_spectrum.png` is Figure 2, `figure5_drug_design.png` is Figure 6, `figure7_boltz_cofold.png` is Figure 7); the LaTeX `\includegraphics` calls map them correctly.
- Figure 3 (`figure2_sex_responders.png`) is the all-tissue, platform-separated (RP / HILIC), sex-stratified response; `data/alltissue19_sex_stratified_stats.csv` holds its per-tissue values.
- The Boltz-2 co-fold (Figure 7; `data/boltz_affinity_scores.csv`, `data/boltz_HCAR1_structures.tar.gz`, `data/shortlist_for_boltz.csv`) enters the paper as orthogonal structural corroboration of the two lead analogs, not as measured affinity.

---

## Limitations & caveats

- Findings are **computational**, from re-analysis of public data, and are **hypothesis-generating** — the recovered signal, sex-specific pattern, and analog rankings await experimental validation.
- Metabolite identity is held at **MSI Level 2**; an authentic-standard, MS/MS-enabled confirmation is the natural next step.
- The **receptor is unknown**; HCAR1/GPR81 is a candidate pocket used for docking corroboration, not an established target.
- ADMET / side-effect predictions (including the triazole's DILI flag) are model-based estimates, not clinical determinations.

---

## Citation

```
Hershman, S., & Claude Science. (2026). Multi-Omic Profiling Reveals Lac-Phe as a
Substrate-Driven Exerkine Independent of CNDP2 Activation. Built with Claude —
Life Sciences Hackathon (Researcher Track).
https://github.com/hershman/claude-science-lacphe-motrpac
```

Please also cite the underlying **MoTrPAC** PASS1B resources (Amar et al. 2024; Schenk et al. 2024) per their data-use guidelines.


---

## Acknowledgments

The **MoTrPAC Consortium** and **MoTrPAC Bioinformatics Center** for the open exercise atlas; **Anthropic** and the **Built with Claude: Life Sciences** hackathon; **Modal** (remote compute) and **Boltz-2** (co-folding / affinity corroboration).
