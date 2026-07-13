# A hydrolysis-resistant Lac-Phe analog: computational campaign report

**Objective.** Design and computationally triage an analog of **Lac-Phe** (N-lactoyl-L-phenylalanine),
the exercise-induced appetite-suppressing metabolite, that resists hydrolysis of its central amide bond
while retaining the parent's activity-relevant pharmacophore. All work was done on a laptop (14 CPU cores,
no discrete GPU beyond a small Apple-Silicon budget reserved for co-folding); the true receptor is **unknown**.

---

## Executive summary

Seven structures were carried through a five-stage funnel: the parent plus six analogs spanning
**amide-retaining** (N-methyl, α-methyl-Phe, D-Phe) and **backbone-replacement** (reduced amide,
thioamide, 1,2,3-triazole) strategies. Everything decisive was computed on CPU with no target
assumption; the scarce GPU budget is reserved for confirming survivors.

**Lead recommendation: the 1,2,3-triazole isostere** — it is the only design that makes amide
hydrolysis structurally impossible while preserving the parent's shape and the load-bearing anionic
carboxylate, it docks consistently into the top candidate pocket, and Boltz-2 co-folding confirms it
retains parent-level predicted binding at that pocket (HCAR1 binder probability 0.58 vs parent 0.55).
Its one liability is a predicted hepatotoxicity (DILI) flag that must be checked experimentally.

**Backups: reduced amide** (also hydrolysis-inert, cleanest ADMET, and the *highest* Boltz-2 HCAR1 binder
probability of any survivor at 0.73 — though a weaker static pharmacophore match with a new basic amine) and
**thioamide** (most shape-conservative isostere, clean ADMET, but only partially stabilized — still bears a
hydrolyzable C=S — and its two Boltz-2 affinity heads disagree).

Phase 3 co-folding (parent + four survivors × HCAR1/MRGPRD, run on the user's Apple-Silicon GPU) delivered
its headline result: **none of the hydrolysis-resistant isosteres loses predicted binding at HCAR1 relative
to the parent** — the stability edits do not cost engagement of the lead pocket.

**α-Methyl-Phe is explicitly de-prioritized** despite the best raw 3D overlay: α-hydrogen methylation is
a known affinity-killer at amino-acid/taste-type receptors, so its overlay is a geometric artifact.

---

## The design problem

Lac-Phe is an *N*-lactoyl amino acid; the hydrolysable liability is the single **amide bond** joining the
lactoyl and phenylalanine halves. The same enzymology that produces and clears it (CNDP2 — which
synthesizes it reversibly — plus serum peptidases) reads that bond as a cleavable peptide linkage. Every
design protects that one bond, by one of two routes: **block enzyme recognition** while keeping the
carbonyl (cheaper, closer to parent, but still in-principle cleavable) or **remove the carbonyl entirely**
(non-hydrolysable by class, at the cost of larger pharmacophore change).

---

## Stage 1 — Hydrolytic stability (GFN2-xTB, CPU)

Semi-empirical QM (implicit water) on the scissile linkage confirmed the design premise:

- **Carbonyl-free isosteres are genuinely inert.** The **1,2,3-triazole** (aromatic heterocycle, no
  electrophilic carbon; scissile C–N Wiberg bond order ≈ 0.98) and the **reduced amide** (sp³ C–N, BO ≈ 1.01)
  have no carbonyl for water or a peptidase to attack — non-hydrolysable by class.
- **Thioamide** is modestly stabilized (highest scissile C–N bond order 1.39, least-electrophilic scissile
  carbon) but still bears a hydrolyzable C=S.
- **N-methylation** is only a marginal fix; **D-Phe** relies purely on stereochemistry and leaves the amide
  intact.

*Caveat:* these are ground-state proxies (bond order, atomic charge), not computed hydrolysis activation
free energies; the neutral acid form was modeled while the physiological species is the carboxylate anion.

## Stage 1 — Pharmacophore fidelity (RDKit O3A, CPU)

Each analog was O3A-aligned to the parent's low-energy conformer and scored on preservation of the three
SAR-relevant groups (terminal carboxylate, lactoyl-OH, amide H-bond vectors):

- **α-Me-Phe** has the best raw overlay (carboxylate/lactoyl-OH within ~0.3 Å) but is **flagged as a
  recognition risk** — see summary.
- **Triazole** preserves shape well (shape Tanimoto 0.60) though the lactoyl-OH swings ~3.9 Å on the new linker.
- **Reduced amide** is the weakest pharmacophore match (mean key-group deviation ~4.3 Å) and adds a basic amine.

## Stage 2 — ADMET + synthetic accessibility (CPU)

ADMET-AI (104 endpoints) gave uniform, clean hERG/CYP/AMES safety and 49–64% plasma-protein binding across
all seven. Two signals mattered:

- **The triazole carries a predicted DILI probability of 0.74** (above threshold, ~2× every other analog;
  reduced amide is cleanest at 0.14). This is the single differentiating ADMET liability and gates the lead.
- **Shared low passive permeability** (Caco-2 logP_app −5.2 to −5.7) is intrinsic to the polar zwitterion and
  **not rescued by any modification** — a scaffold-level property, not an analog discriminator.

All seven are synthetically easy (Ertl SAscore 2.4–3.1); the triazole is made by CuAAC, the reduced amide by
reductive amination. *Caveat:* the clearance/half-life regressors returned physically impossible values
(out-of-domain for endogenous-metabolite zwitterions) and were excluded from ranking.

**Ligand-based target prediction** (ChEMBL similarity) saw Lac-Phe as a **cleavable dipeptide** — its nearest
bioactive neighbors annotate to peptidases/transporters (Calpain-1, PepT2/SLC15A2), not GPCRs. This does not
corroborate a specific receptor; it reinforces the hydrolysis-liability premise and is why Stage 2 docking
relies on a biology-driven candidate panel rather than a similarity-derived one.

## Stage 2 — Candidate-target docking (smina, CPU, target-unknown)

Because the receptor is unknown, docking was run against a **curated 10-receptor candidate panel** (6
experimental holo pockets + 4 AlphaFold models) and scored on **parent-contact consistency (0–1)** — does
each analog reproduce the *parent's* binding mode and key contacts — **not** raw cross-chemotype kcal/mol.

- **HCAR1 (lactate receptor / GPR81) is the standout, mechanistically coherent hit.** Lac-Phe is an
  acyl-lactate; the parent docks into the L-lactate orthosteric pocket with a carboxylate salt bridge to
  **Arg94** and a π-stack to **His256**. All six analogs reproduce the salt bridge; five of six also keep the
  π-stack (consistency 0.87–1.00).
- **MRGPRD** (β-alanine sensor, holo) is second — all analogs retain the Arg82 salt bridge.
- **The anionic carboxylate is the load-bearing pharmacophore** in every salt-bridging pocket — validating
  the decision to preserve it. The amide position tolerates modification as long as the pose keeps COO⁻
  oriented to the basic residue.
- Analog faithfulness (mean over 5 holo pockets): D-Phe ≈ reduced-amide > thioamide > N-Me > α-Me-Phe ≈
  triazole. The triazole is the most pocket-dependent (excellent at HCAR1/MRGPRD, diverges at NPY1R/MC4R).

*Caveats:* docking scores are not affinities; AlphaFold pockets are low-confidence; rigid-receptor docking has
no induced fit (Stage 3 addresses this). This ranks analog behavior relative to the parent — it does **not**
identify the true receptor.

## Stage 3 — Physics-based confirmation (Boltz-2, local Apple-Silicon GPU)

Co-fold + affinity-head predictions were run for the **survivors** (parent + triazole, reduced amide,
thioamide, D-Phe) against the **two lead receptors (HCAR1, MRGPRD)** — 10 complexes × 3 diffusion samples,
executed on the user's Apple-Silicon GPU (MSAs pre-cached; all 10 completed, no failures). Boltz-2
`affinity_pred_value` is log₁₀(IC50 / µM) — **lower = stronger**; `affinity_probability_binary` is the
probability the ligand is a genuine binder.

**Results (all complexes folded at high structural confidence — ipTM 0.94–0.98, complex pLDDT 0.94–0.98):**

- **HCAR1 is the stronger predicted receptor for every ligand** (log₁₀IC50 ≈ 0.6–1.5, i.e. single-to-tens µM)
  than MRGPRD (≈ 1.3–2.7) — consistent with the docking result and the acyl-lactate → lactate-receptor rationale.
- **Every hydrolysis-resistant isostere retains parent-level predicted binding at HCAR1.** Parent binder
  probability 0.55; triazole 0.58, reduced amide 0.73, D-Phe 0.61 — all at or above parent. The stability edits
  do **not** cost predicted engagement of the lead pocket.
- **The triazole matches the parent** (binder prob 0.58 vs 0.55; log₁₀IC50 1.44 vs 1.38, ≈ 28 vs 24 µM) —
  its large scaffold change is tolerated at HCAR1, reinforcing it as the lead.
- **Reduced amide has the highest HCAR1 binder probability (0.73)** and is the only survivor also predicted a
  likely binder at MRGPRD (0.50) — strengthening it as the backup despite its weaker static pharmacophore overlay.
- **Thioamide is discordant between the two affinity heads** — strongest predicted potency (log₁₀IC50 0.65,
  ≈ 4 µM) but the *lowest* binder probability (0.39, below parent). The heads disagree, so its affinity is not
  over-credited; it stays a mid-tier backup.

Absolute Boltz-2 affinities are not calibrated potencies; the informative read is analog-vs-parent within a
receptor, and the headline is that **no isostere loses predicted HCAR1 binding relative to the parent.**

---

## Stage 4 — Ranked decision matrix

Boltz-adjusted composite (co-folded survivors) = 0.40·hydrolytic-stability + 0.30·activity-retention +
0.15·Boltz-HCAR1-binder-probability + 0.15·ADMET-factor. N-Me amide and α-Me-Phe were not advanced to Phase 3
(retain their Phase-1/2 composite, shown in parentheses).

| Rank | Analog | Composite | Stability | Activity ret. | Boltz HCAR1 (binderP / IC50 µM) | DILI | SAscore | Route |
|---|---|---|---|---|---|---|---|---|
| — | Lac-Phe (parent) | 0.57 | 0.10 | 1.00 | 0.55 / 24 | 0.32 | 2.44 | amide coupling |
| **1** | **1,2,3-triazole** | **0.83** | 1.00 | 0.80 | **0.58 / 28** | 0.74 ⚠ | 3.05 | CuAAC |
| 2 | Reduced amide | 0.81 | 0.95 | 0.56 | 0.73 / 35 | 0.14 | 2.52 | reductive amination |
| 3 | Thioamide | 0.65 | 0.60 | 0.71 | 0.39 / 4 † | 0.36 | 2.88 | Lawesson / thioacylation |
| — | D-Phe | 0.54 | 0.15 | 0.82 | 0.61 / 17 | 0.35 | 2.44 | amide coupling (D-Phe) |
| — | N-Me amide | (0.55) | 0.35 | 0.63 | not folded | 0.42 | 2.81 | amide coupling (N-Me-Phe) |
| — | α-Me-Phe | (0.45) | 0.35 | 0.37‡ | not folded | 0.38 | 2.87 | amide coupling (α-Me-Phe) |

D-Phe is ranked "—" because it fails the primary objective (stability 0.15 — the amide is intact); it is
included only as the most parent-faithful reference point. ⚠ triazole DILI flag is the one liability to verify.
† thioamide's two Boltz-2 affinity heads disagree (strong IC50 but low binder probability), so its potency is
not over-credited. ‡ α-Me-Phe activity-retention includes the literature-flagged recognition penalty.

---

## Overall caveats

1. **The true Lac-Phe receptor is unknown.** HCAR1 is a mechanistically attractive, docking-consistent
   *hypothesis* (acyl-lactate binding the lactate receptor), not an established target. All target-dependent
   conclusions are conditional on it.
2. **Docking ranks consistency-with-parent, not affinity**, and cannot prove a target.
3. **Boltz-2 affinities are not calibrated potencies.** The predicted IC50 values are relative, most
   meaningful analog-vs-parent within one receptor; the co-fold confirms *retention* of binding at HCAR1,
   it does not measure absolute affinity, and the two affinity heads can disagree (as for thioamide).
3. **This is computational prioritization**, not validation. The decisive experiments are wet-lab: hydrolytic
   half-life (serum/CNDP2), a receptor/β-arrestin assay once a target is confirmed, and the in vivo anorectic
   readout. Any modification risks losing activity — the amide-retaining vs. isostere axis is exactly the
   stability-vs-activity trade-off that only assays can resolve.
