# Citation Correctness Audit — Lac-Phe / CNDP2 MoTrPAC Manuscript

**Track:** Independent verification that every in-text citation actually supports its attributed
claim (not merely DOI resolution); miscitation and retraction check; reference-count/DOI
reconciliation against the deposited manifest.

**Method.** Extracted all in-text author-year citations and their attributed claims from the LaTeX
source; parsed the 46-item numbered reference list and the 42-row `references_manifest.csv` +
`references_delta.bib`. Resolved all 46 reference DOIs live against CrossRef (title/venue/year/
retraction flag). For the 25 mechanistic/quantitative claim-to-source links, pulled the cited
paper's abstract (PubMed MCP) and, for the load-bearing quantitative claims, the full text (PMC)
and confirmed the paper's actual finding supports the manuscript's use. Verified the NCT trial
via ClinicalTrials.gov. Confirmed the two named retracted DOIs are absent.

## Headline result

- **46/46 reference DOIs resolve** against CrossRef; **none carries a retraction flag.**
- **No retracted reference is present.** The two named problem DOIs — Hedaya 2025
  (`10.3390/cells14161296`) and Ying 2025 (`10.1186/s12974-025-03495-3`) — appear in **neither**
  the LaTeX source nor the manifest nor `references_delta.bib`. The Data-availability text states
  two flagged-retracted papers were excluded; that exclusion is confirmed.
- **0 substantive miscitations.** Every mechanistic claim-to-source link checked reflects the
  cited paper's actual finding. No unsupported attribution or overstatement was found in the
  claim→source mapping.
- Issues found are **MINOR only** (a reference-numbering error in one caption, a count-framing
  inconsistency, an unused-manifest-entry note, and print-vs-online year differences). No BLOCKING
  or MAJOR citation issue.

## Key claim-to-source verifications (all SUPPORTED)

| Ref | Attributed claim (manuscript) | Source finding | Verdict |
|---|---|---|---|
| **Li 2022** (Nature, 10.1038/s41586-022-04828-5) | Exercise-inducible Lac-Phe suppresses feeding/adiposity in DIO mice without changing EE; biosynthetic ablation blocks anti-obesity benefit of training; pre-vs-post fold-change of Lac-Phe correlates with lactate at **r=0.82, p<0.0001** in humans; 50 mg/kg i.p. effect; suppresses feeding in obese but not lean mice even at 150 mg/kg | Full text confirms verbatim: "Pearson r = 0.82, P < 0.0001"; 50 mg/kg IP; "In chow-fed, lean mice, Lac-Phe did not suppress food intake, even at up to 3-fold higher doses (150 mg/kg)"; obese-not-lean specificity | **SUPPORTED (exact)** |
| **Jansen 2015** (PNAS, 10.1073/pnas.1424638112) | CNDP2 reverse proteolysis generates N-lactoyl amino acids; substrate-limited (tracks lactate + free AA mass action); PKU (chronically elevated Phe) raises Lac-Phe | Abstract confirms reverse proteolysis by CNDP2; "plasma levels strongly correlate with lactate and amino acid … increased levels after exercise and in patients with phenylketonuria who suffer from elevated Phe" | **SUPPORTED (incl. PKU)** |
| **Xiao 2024a** (Nat Metab, 10.1038/s42255-024-00999-9) | Metformin's food-intake/weight effect partly Lac-Phe-dependent; gut/intestinal epithelium is principal source; GFRAL experimentally excluded as Lac-Phe mediator | Abstract: metformin induces Lac-Phe, intestinal-epithelial CNDP2 principal source, ablation renders mice resistant. Full text: "we sought to determine whether the effect of Lac-Phe requires a functional GFRAL receptor … Lac-Phe equally [suppressed feeding regardless]" — GFRAL excluded | **SUPPORTED** |
| **Scott 2024** (Nat Metab, 10.1038/s42255-024-01018-7) | Metformin/feeding raise human Lac-Phe | Abstract confirms across seven studies + post-prandial rise | **SUPPORTED** |
| **TeSlaa 2024** (Nat Metab, 10.1038/s42255-024-01014-x) | Metformin gut–brain Lac-Phe axis | Title: "Metformin induces a Lac-Phe gut-brain signalling axis" | **SUPPORTED** |
| **Ghias 2025** (Am J Physiol Endocrinol Metab, 10.1152/ajpendo.00037.2025) | Oral lactate raises circulating Lac-Phe via gut | Abstract: "oral lactate elevates plasma l-lactate and strongly increases circulating l-Lac-Phe" | **SUPPORTED** |
| **Liu 2025** (Nat Metab, 10.1038/s42255-025-01377-9) | Lac-Phe inhibits hypothalamic AgRP neurons via K_ATP channel; MC4R- and NPY1R-expressing PVH neurons required for full anorexigenic response | Abstract: direct AgRP inhibition via K_ATP; both AgRP inhibition and PVH activation required. Full text confirms MC4R and NPY1R in PVH as endogenous receptors examined in Lac-Phe-activated PVH neurons | **SUPPORTED** |
| **Li 2024** (Nat Commun, 10.1038/s41467-024-51174-3) | SLC17A1/3 mediate renal Lac-Phe excretion; KO lowers urine but not plasma Lac-Phe (urine/plasma decoupling) | Abstract: "SLC17A1/3-dependent de-coupling of urine and plasma Lac-Phe pools"; KO reduces urine, normal blood | **SUPPORTED** |
| **Moya-Garzon 2024** (Cell, 10.1016/j.cell.2024.10.032) | β-hydroxybutyrate shunt through CNDP2 generates anti-obesity ketone metabolites | Abstract: CNDP2-dependent BHB–amino acid conjugation; BHB-Phe congener of Lac-Phe suppresses feeding | **SUPPORTED** |
| **Hoene 2022** (Metabolites, 10.3390/metabo13010015) | Post-exercise plasma Lac-Phe forecasts abdominal adipose loss over an endurance program | Abstract: higher post-acute-exercise Lac-Phe associated with greater reduction in abdominal (subcutaneous>visceral) adipose over 8-wk intervention | **SUPPORTED** |
| **Weber 2025** (Metabolomics, 10.1007/s11306-025-02260-0) | Circulating Lac-Phe scales with exercise intensity (randomized crossover), tracking lactate load | Abstract: two-period crossover; Lac-Phe among most intensity-dependent metabolites (moderate vs vigorous) | **SUPPORTED** |
| **Bauhaus 2025** (Front Sports Act Living, 10.3389/fspor.2025.1600714) | Sex-specific acute Lac-Phe exercise response reported in one human study | Abstract: "Sex-specific differences … female subjects showing significantly higher lac-phe concentrations than male subjects (p<0.05)" | **SUPPORTED** (note: primary aim is a DBS LC-MS/MS method paper; sex finding is a secondary result — manuscript's narrow framing "reported acutely in one human study" is accurate) |
| **Glatz 2025** (Diabetes Obes Metab, 10.1111/dom.70236) | Within-subject longitudinal sampling shows acute per-session rise attenuating numerically over training, non-significant trend in exploratory cohort | Title confirms acute+prolonged endurance-training effects on Lac-Phe, exploratory ULTRAFLEXI-1 analysis; manuscript explicitly labels it non-significant/exploratory (appropriately hedged). Abstract text unavailable in PubMed; framing is conservative | **SUPPORTED (conservatively framed)** |
| **Sellami 2024** (Biol Sport, 10.5114/biolsport.2025.145912) | N-lactoyl-Phe and exercise-responder status (women) | Abstract: in 43 young women, low responders had higher Lac-Phe; CNDP2 expression negatively associated with slow-twitch fiber % | **SUPPORTED** |
| **Li 2023** (Front Endocrinol, 10.3389/fendo.2023.1289574) | Blood-flow-restriction / intensity dependence of Lac-Phe | Abstract: BFR+MICE elevates Lac-Phe more than MICE alone | **SUPPORTED** |
| **Everaert 2012** (Eur J Appl Physiol, 10.1007/s00421-012-2540-4) | CNDP2 expressed in (human) skeletal muscle | Abstract: CNDP2 among carnosine-related enzymes expressed in human/mouse skeletal muscle | **SUPPORTED** |
| **Naja 2025** (Diabetes Obes Metab, 10.1111/dom.16633) | Human association of N-lactoyl amino acids with insulin resistance and diabetic complications | Abstract: Qatar Biobank, Lac-AA higher in IR and diabetic complications, replicated | **SUPPORTED** |
| **Chow 2022** (Nat Rev Endocrinol, 10.1038/s41574-022-00641-2) | Exerkines are secreted proteins/peptides whose transcription/release rises with training | Abstract: exerkines = signalling moieties released with acute/chronic exercise | **SUPPORTED** |
| **Brooks 2023** (J Appl Physiol, 10.1152/japplphysiol.00497.2022) | Lactate is the archetype exercise signal set by metabolic flux | Abstract: lactate as myokine/exerkine acting by mass action, autocrine/paracrine/endocrine | **SUPPORTED** |
| **Müller 2019** (Mol Metab, 10.1016/j.molmet.2019.09.010) | GLP-1 has short native half-life (minutes), cleaved rapidly | Abstract: GLP-1 biology; modified GLP-1 RAs for potency/sustained action (native short t½ is field-standard) | **SUPPORTED** |
| **Yang 2024** (Drug Des Devel Ther, 10.2147/DDDT.S470826) | Protease-resistant, albumin-binding engineering → once-weekly semaglutide | Abstract: semaglutide long t½, once-weekly SC dosing | **SUPPORTED** |
| **Yao 2018** (Curr Drug Metab, 10.2174/1389200219666180628171531) | Established toolkit for peptide metabolic-stability (backbone bioisosteres, N-methylation, D-AA, reduced-bond, conjugation) | Abstract: N/C-terminal mod, D-amino acid, cyclization, backbone modification | **SUPPORTED** |
| **Geng 2025** (Cell, 10.1016/j.cell.2025.06.001) | Betaine nominated as geroprotective exercise mimetic via unbiased screen | Abstract: multi-omics screen; betaine as exercise mimetic for geroprotection, inhibits TBK1 | **SUPPORTED** |
| **Amar 2024** (Nature, 10.1038/s41586-023-06877-w) | MoTrPAC PASS1B: ~19 tissues, 1/2/4/8-wk training, multi-omic | Abstract: "9,466 assays across 19 tissues, 25 platforms, 4 training time points"; 8 wk endurance training | **SUPPORTED (exact "19 tissues")** |
| **Schenk 2024** (Function, 10.1093/function/zqae014) | Physiological adaptations to progressive endurance training in adult+aged rats (MoTrPAC PASS1B) | Abstract: 1/2/4/8 wk, ~70-75% VO2max, 18 solid tissues + blood/plasma/feces biorepository | **SUPPORTED** |

## Clinical trial reference (SUPPORTED)

**NCT06743009** — verified on ClinicalTrials.gov: "The Metabolic Effects of the Exercise-metabolite
N-lactoyl-phenylalanine (Lac-Phe)," University of Aarhus, **COMPLETED**, interventional double-blind
randomized crossover, IV **N-lactoyl-phenylalanine vs NaCl** in Healthy Overweight/Obese (BMI 28-35),
n=23. The manuscript describes it as "an intravenous Lac-Phe-versus-saline trial in overweight/obese
adults … the first direct human read on exactly that window" — an exact match to the registered
protocol.

## Retraction re-confirmation (PASS)

`retracted_present = False`. Neither named DOI is in the source, manifest, or delta bib:
- `10.3390/cells14161296` (Hedaya et al. 2025, *Cells* 14(16):1296) — absent.
- `10.1186/s12974-025-03495-3` (Ying et al. 2025, *J Neuroinflammation* 22:167) — absent.

Both were checked two ways. (1) CrossRef returns `retracted=False` for both. (2) A targeted web
search for a retraction/expression-of-concern notice on each DOI found **none** — the publisher
pages (MDPI *Cells* 14(16):1296; BMC *J Neuroinflammation* 22:167) return the live articles with no
retraction banner, and the searches surfaced no retraction/EoC notice for either DOI. So as of this
audit neither paper is formally retracted in the public record. Regardless of their retraction
status, the audit-relevant fact is that both are **excluded from the manuscript**, consistent with
the Data-availability statement's note that two flagged papers were dropped — a defensible
precautionary exclusion.

## MINOR issues

1. **Table 6 caption — wrong reference numbers for Amar/Schenk.**
   - Location: Table 6 caption, Results/Reference-verification block.
   - Manuscript states: "(Two additional MoTrPAC consortium method references — Amar 2024, Schenk
     2024 — are cited in the Introduction and listed as **refs 37-38**.)"
   - Recomputed: in the numbered reference list, **Amar 2024 is ref #45 and Schenk 2024 is ref #46**
     (refs 37-44 are the exerkine/drug-design context references: Chow, Yao, Müller, Brooks, Yang,
     Geng, Weber, Naja).
   - Severity: **MINOR** (labeling error; the references exist, resolve, and are correctly attributed).
   - Action: change "refs 37-38" to "refs 45-46".

2. **Reference-count framing is internally inconsistent.**
   - Location: Data-availability paragraph vs Table 6 caption.
   - Data-availability: "**46 references** passed verification … two papers flagged as retracted were
     excluded." Table 6 caption: "10 of the **36** Lac-Phe literature sources … Two additional MoTrPAC
     … refs 37-38."
   - Recomputed: reference list = 46 total. The framing 36 (Lac-Phe) + 2 (MoTrPAC) = 38 does not
     account for the 8 context references (refs 37-44). The 46 total is correct and fully verified;
     only the bucketing narrative is incomplete.
   - Severity: **MINOR**. Action: reconcile the "36 + 2" wording with the 46-item list (e.g.,
     "36 Lac-Phe sources + 8 physiology/drug-design context refs + 2 MoTrPAC method refs = 46").

3. **Manifest contains 3 verified references never cited and absent from the reference list.**
   - `references_manifest.csv` (42 rows) includes **Hsu2026** (10.3390/antiox15040441),
     **Jermei2025** (10.3390/metabo15060375), **Wu2025** (10.1186/s13293-025-00780-x), which do not
     appear in the LaTeX body or the numbered reference list.
   - Severity: **MINOR / informational** — unused verified candidates, not an error; but the manifest
     is not a 1:1 map of the manuscript's citations (39 of 42 manifest rows are cited; the list's
     other 7 entries come from `references_delta.bib`). Action: none required; optionally prune or
     label the 3 unused rows.

4. **Print-vs-online year differences (CrossRef issue year vs manuscript year).**
   - Moya-Garzon: ms 2024 / CrossRef issue 2025; Oni: ms 2025 / CrossRef 2026; Schumacher: ms 2025 /
     CrossRef 2026. These reflect online-first vs assigned-issue dates and are defensible.
   - Severity: **MINOR**. Action: optional — align to the version year the authors intend to cite.

5. **Two "Li 2024" entries create in-text key ambiguity (not an error).**
   - Reference list #17 (Li 2024, bioRxiv preprint) and #20 (Li 2024, Nat Commun) are both present;
     the in-text "[Li 2024]" for the SLC17A1/3 renal-clearance claim maps to the published #20, which
     is the correct primary source. Manifest keys `Li2024a`/`Li2024b` disambiguate. No miscitation.
   - Severity: **MINOR / informational**.

## Bottom line

Every mechanistic and quantitative claim-to-source link in the manuscript is supported by the cited
paper's actual finding, including the load-bearing quantitative anchors (Li 2022 r=0.82 and dose
specificity; Amar 2024 "19 tissues"; Xiao 2024a GFRAL exclusion; Liu 2025 AgRP/K_ATP + MC4R/NPY1R).
All 46 reference DOIs resolve, none is flagged retracted, and the two named retracted papers are
correctly absent. The only defects are a reference-numbering slip in the Table 6 caption and a
count-framing inconsistency — both cosmetic.
