# Lac-Phe / CNDP2 in the MoTrPAC rat atlas — reproducibility package

Regeneration code, LaTeX source, figures, and an independent correctness audit for:

> *Multi-Omic Profiling Reveals Lac-Phe as a Substrate-Driven Exerkine Independent of
> CNDP2 Activation.*

## Layout

```
.
├── data/         deposited, analysis-ready inputs (per-sample CSVs, stats, markers, supplement)
├── code/         regeneration scripts (statistics → figures → citation check → transparency)
├── paper/        LaTeX source, bibliography, and the seven figures
│   └── figures/
├── audit/        independent correctness audit (consolidated + three component reports)
├── requirements.txt
└── Makefile
```

## Quick start (clean checkout → compiled PDF)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make all            # stats → figures → transparent backgrounds → compiled PDF
```

`make all` runs, in order:

1. `code/01_compute_statistics.py` — selection-free Kruskal–Wallis omnibus + selection-aware
   5,000× **within-sex** permutation null + 64-m/z decoy panel. Reproduces `data/specificity_stats.csv`
   (heart selection-free q = 0.014, heart selection-aware p = 0.031, decoy FP 3.1%). Seeded (`seed=42`).
2. `code/02_response_stats.py` — per-tissue×mode training response: floor-to-min imputation of
   undetected samples, per-cell median, **exact** Mann–Whitney vs week 0, sex-stratified peak
   deltas/p-values, fold-changes. Reproduces `data/alltissue19_response_stats.csv`.
3. `code/03_make_figures.py` — regenerates the 19-tissue Δlog₂ timecourse (Figure 1a) from the
   per-sample data and prints the all-tissue sex-stratified responder values behind Figure 3.
4. `code/06_boltz_cofold_figure.py` — regenerates the Boltz-2 co-fold panel (Figure 7) from
   `data/boltz_affinity_scores.csv` (HCAR1 preferred over MRGPRD for every ligand; triazole 0.58
   and reduced amide 0.73 match/exceed the parent 0.55 binder probability). The co-fold itself is
   run on a local GPU via `data/boltz_local.tar.gz`; the script plots its deposited scores.
5. `code/04_transparent_backgrounds.py` — border flood-fill so figure backgrounds are transparent.
6. `make pdf` — `pdflatex → bibtex → pdflatex ×2` on `paper/cndp2_lacphe_substrate_not_switch.tex`.

Verify citations (network required):

```bash
python3 code/05_verify_citations.py   # 46/46 DOIs resolve against CrossRef, 0 retracted
```

## Reproducibility boundary (read this)

The **raw-spectra extraction** stage — decoding Agilent `.d` and Thermo `.raw`/mzML acquisitions
from the multi-gigabyte Metabolomics Workbench archives (studies **ST002628–ST002916**) via
HTTP range requests and an x86 vendor reader — is **not re-runnable from this package**; it needs
the full vendor archives and platform-specific tooling. This package therefore starts from the
**deposited, analysis-ready per-sample tables** that stage produced (`data/*_persample*.csv`), which
are sufficient to regenerate every downstream statistic and figure. Three identity metrics
(in-source fragment r = 0.96, mass-accuracy ppm, isotope-envelope ratio) live on the extraction side
of this boundary and are provided as deposited summaries (`data/lacphe_ms1_identity.csv`,
`data/fragment_spectra_pair.json`), not recomputed here. Genome-wide feature counts (Fig 5b) come
from the external `MotrpacRatTraining6moData` package; the CNDP2 = 0 side of each is verified from
`data/cndp2_markers_extended.csv`.

## Data provenance

Per the manuscript's Data Availability statement, the underlying data are MoTrPAC PASS1B
(Amar et al. 2024; Schenk et al. 2024), deposited on Metabolomics Workbench under the PASS1B
metabolomics study series and in the `MotrpacRatTraining6moData` R package; consult the manuscript
and Metabolomics Workbench for the exact study accessions.
`data/cndp2_multiomic_supplementary.xlsx` (Supplementary Table S1) carries **strand-corrected**
CNDP2-locus coordinates; the superseded strand-naive annotation is retained in the
`*_strandnaive_OLD` columns for transparency.

## Audit

`audit/AUDIT_REPORT.md` is the consolidated independent correctness audit (0 blocking issues; every
headline statistic reproduces from the deposited data; 46/46 citations supported; no retracted
reference). Component reports: `audit/audit_claims.md`, `audit/audit_pipeline.md`,
`audit/audit_citations.md`.

## Notes

- Figure filenames are offset from caption numbers (e.g. `figure1c_spectrum.png` is Figure 2,
  `figure5_drug_design.png` is Figure 6, `figure7_boltz_cofold.png` is Figure 7); the LaTeX
  `\includegraphics` calls map them correctly.
- Figure 3 (`figure2_sex_responders.png`) is the all-tissue, platform-separated (RP / HILIC),
  sex-stratified response; `data/alltissue19_sex_stratified_stats.csv` holds its per-tissue values.
- The Boltz-2 co-fold (Figure 7, `data/boltz_affinity_scores.csv`, `data/boltz_HCAR1_structures.tar.gz`,
  `data/shortlist_for_boltz.csv`) was run on the shortlist against HCAR1/GPR81 and MRGPRD; it enters
  the paper as orthogonal structural corroboration of the two lead analogs, not as measured affinity.
- Requires a LaTeX toolchain (TeX Live 2024 / MacTeX) for `make pdf`.
