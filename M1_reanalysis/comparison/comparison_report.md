# M1 reanalysis comparison — 30 October 2026

**Calibration follow-up:** All Brecht workbook entries are now flagged. See [Brecht calibration review](Brecht_calibration_review.md) for the published-area comparison, limitations of the printed scale, and possible Felleman-based calibration mechanisms. The sixfold correction is plausible in biological magnitude but remains unverified.

Audited all **208 populated rows** of `M1 surface measurements for reanalysis.xlsx` against current `flatmap_measurements/*/data/measurements.csv`, source-specific methods, and the original Brecht & Freiwald Figure 3 page. The original workbook and canonical measurements were not edited. This is a comparison of existing measurements, not a fresh certification of all anatomical tracings. Item 6 (“Compare to the measurement”) was interpreted as the existing canonical flatmap measurement; no additional unnamed measurement series was supplied.

Open `row_audit.html` for a searchable table or `row_audit.csv` for all evidence columns. `compare_measurements.py` reproduces both from project inputs. Source row means the workbook's **Source row** column, not its Excel row number; both are retained in the CSV.

## Main numerical findings

Difference is 100 × (current flatmap − workbook) / workbook. All areas below are mm² of the calibrated drawing, subject to the original dataset's provisional anatomical status.

| Reference / field | Source row | Workbook | Current flatmap | Difference |
|---|---:|---:|---:|---:|
| Felleman & Van Essen 1991 Fig 2, M1 / area 4 | 96 | 393.850 | 399.207 | +1.36% |
| Krubitzer & Dooley 2013 Fig 1, M1 | 128 | 285.143 | 288.713 | +1.25% |
| Brecht & Freiwald 2012 Fig 3a, human V1 | 57 | 2771 | 2850.521 | +2.87% |
| Same, human drawn outline | 63 | 66231 | 70517.573 | +6.47% |
| Brecht Fig 3b, macaque V1 | 64 | 10492 | 1071.539 | −89.79% |
| Same, macaque drawn outline | 68 | 67253 | 6632.326 | −90.14% |
| Brecht Fig 3d, mole-rat S1 | 69 | 8.209 | 8.191 | −0.22% |
| Same, mole-rat drawn outline | 71 | 26.682 | 26.254 | −1.60% |

There are 94 numerical drawing comparisons, 40 rows with existing geometry but unavailable mm², 7 with explicit unavailable measurement records, 16 with citation mismatches requiring confirmation, one motor-field-definition mismatch, and 50 without an equivalent selected row (including ratios, regression estimates, partial-field differences and absent sources). Of the 94 numerical comparisons, 65 differ by at most 10% and 80 by at most 20%. These are descriptive screening thresholds, not validated agreement limits. Some comparisons involve stated label approximations, such as A1 versus AI, S1 versus 3b, or PV versus PV/IG; numerical agreement does not establish anatomical equivalence.

### Brecht macaque scaling

All five macaque entries are about 8.93–10.64 times the current areas. This coherent discrepancy suggests a calibration or unit problem, although the workbook's original ROI/calibration records are needed to establish its cause. The workbook annotation “6x too big?” does not resolve it: dividing by six would still leave substantial disagreement. Do not replace all five values with one inferred factor.

Figure 3's caption explicitly applies the same bar to side view and flatmap in **a and b**. Panels **c and d use different scales**, with the lower scale for the flatmap. The current macaque measurement therefore already has an applicable local bar; no borrowed reference scale is needed for this comparison. The original page was visually inspected at `flatmap_measurements/Brecht_Freiwald_2012/review/source_pages/page04.png`.

The macaque V1 fraction is much closer: workbook 10492/67253 = 15.60%, current drawing 1071.539/6632.326 = 16.16%. This supports investigating overall scaling before border differences. These are fractions of the drawn outline, not certified biological neocortex percentages. Human A1 and S1 differ by about 12%; human S1-face differs by −4.21%. Mole-rat S1-face differs by −4.40%.

### Conflicting workbook entries

- Felleman V1: rows 72, 86 and 345 contain **1847, 1121.117 and 24**, respectively, with the same figure citation; current V1 is **1133.377**. Row 86 agrees within 1.1%; the others require provenance/unit checks.
- Felleman V2: rows 87 and 346 contain **1154.38 and 10.19787907**, versus **1122.551** currently. The small entry should not be treated as confirmed mm² merely because it occupies that column.
- Felleman M1 row 353 is **637** and explicitly discusses combining area 4, 6, SMA and MEF. It is not an equivalent M1-only value. The M1-only row 96 agrees closely.
- Felleman MST row 339 differs by about +82% from the current MSTd+MSTl sum; verify whether its intended scope is one subdivision. ER row 99 differs by about +61% from the sum of anterior and posterior ER; this may be a component-definition difference and must not be interpreted as an established tracing error.
- Krubitzer & Dooley A1, MTc and SMA differ by approximately −25%, −24% and −32%. These warrant border/field-definition review even though M1 agrees.
- Brecht rows 327/330 cite Fig 1, whereas the sensory maps are Fig 3. Krubitzer & Kaas rows 428–441 cite Fig 2; the corresponding summary-field candidate is Fig 12. Candidate numbers are exposed but flagged rather than silently correcting citations.
- Rows 331/332 cite multiple papers; a unique measurement source cannot be assigned.

## Why measurements are missing or not directly comparable

| Source | Existing coverage and reason |
|---|---|
| Van Essen 2005 Fig 9 | Extensive pixel tracings exist, including BA4 and visual fields. Physical area is NA because the atlas has no valid local scale/areal correction. BA41+42 is not strictly A1, MT+ is broader than MT, and BA3 is not isolated 3b. A whole-neocortex denominator is not established. |
| Wilkinson 2021 Fig 4 | M1, V1 and combined S1 geometry exists, but is unscaled. Individual 3a/3b/1/2 are not separately tabulated; combined S1 includes all four. Workbook cut V1 pieces are not separate rows. |
| Van Essen & Drury 1997 | Existing records explicitly decline physical areas from a single flatmap grid because flattening causes spatially varying areal distortion. Original mesh/per-tile surface metrics are needed for biological areas. |
| Felleman & Van Essen 1991 Fig 2 | Most named fields are traced. Subicular/hippocampal subdivisions are explicitly **not_yet_digitized**, a genuine digitization gap. R has no literal matching label; identity needs checking. V3 components are not separate records. Enclosing tissue includes non-neocortex, preventing an automatic neocortex denominator. Source taxon is Macaca, not an independently verified species assignment. |
| Krubitzer & Dooley 2013 Fig 1 | Most fields exist. FST, V3 and V4 totals can be formed from recorded subdivisions, as explicitly listed in the audit. The workbook's two 3b pieces are not separate rows. R has no literal matching row. SEF exists but is not silently substituted for MEF. Complete neocortex perimeter is not established. |
| Krubitzer & Kaas 1990 Fig 12 | Most fields and a drawn outline exist. Motor and Premotor explicitly lack complete field borders; M1 cannot be recovered by borrowing a scale. PV/IG is broader than literal PV. |
| Rosa et al. 1993 | Fig 11 field geometry exists but is an unscaled schematic. Fig 5A has calibrated visual fields, but Motor/M1 and Somatosensory borders are not closed. A specimen scale from Fig 5A cannot automatically calibrate Fig 11. |
| Mayer et al. 2019 | Four identified cases have measurements of sampled M1 response territory. They are partial territories, not complete M1. Repeated figures are the same cases. Source identification is Sapajus spp.; assignment to Cebus apella is unresolved. The audit lists related case areas without treating them as whole-M1 matches. |
| Haug 1987 | Dataset intentionally has no planar ROI measurements; its figures are histological/statistical. Published cortex estimates and regression-derived values require a separate reported-data comparison. |
| Dea 2016, Young 2013, Collins 2016, Chaplin 2013, Pitzalis 2015 | No corresponding canonical dataset was found. Their workbook observations cannot currently be checked against equivalent flatmap rows. Full source and figure/table provenance are required. |

Most residual missing components are aggregations or subregions of already traced geometry, not missing entire papers. All row-specific reasons and relevant NA boundary notes are retained in the audit.

## Additional estimates and source papers

1. **First obtain original workbook ROI files and calibration records**, particularly for Brecht macaque and the conflicting Felleman entries. These are more diagnostic than choosing a correction factor from numerical agreement.
2. **Orban, Van Essen & Vanduffel (2004)** and **Rosa & Tweedale (2001)** are useful for tracing the primate drawings underlying Brecht Fig 3. They were not found by filename in the project PDF inventory. The supplied references establish a source chain to investigate; they do not establish a panel-by-panel geometric transformation. Orban bibliographic record: https://pubmed.ncbi.nlm.nih.gov/15242691/ .
3. **Airey et al. (2006)** is useful to recover the mouse source map and calibration. It was not found by filename locally. The verified reference is *BMC Neuroscience* **7:63**, DOI **10.1186/1471-2202-7-63** (the supplied “15:63” appears to confuse the date with volume). Record: https://pubmed.ncbi.nlm.nih.gov/16978410/ . Mouse is not represented in the current reanalysis workbook, so this is a lower priority for this particular comparison.
4. **Henry et al. (2006) is already available** at `papers_to_do/cortical_flatmap_bibliography/Henry_etal_2006.pdf`. A canonical measurement dataset for it was not found. It would help verify the original mole-rat field definitions and redraw history; the existing Brecht mole-rat comparison already has a local calibration.
5. **Dea et al. 2016** (workbook DOI 10.1093/cercor/bhv324), **Young et al. 2013**, **Collins et al. 2016**, **Chaplin et al. 2013**, and **Pitzalis et al. 2015** are needed for rows 165, 331–333 and 471–479. These PDFs were not found by filename in the project. For abbreviated citations, resolve full titles and precise figure/table first; authors and year alone are not enough to assert a unique match.
6. **Krubitzer 2009 is already measured locally** and is the stated basis of the 2013 Fig 1 map. Treat the two as reused/composite evidence, not independent animals. Original digital **PALS-B12/Van Essen atlas surfaces and field labels** would help the human atlas comparisons more than another arbitrary scale bar.

A borrowed calibration is defensible only after confirming the same geometry, documenting resizing/rotation and excluding nonuniform distortion. For uniform length scaling s, area changes as s²; for anisotropic transformation, the relevant area factor is its determinant. Such a transform calibrates the drawing, and does not by itself recover the original 3-D cortical area. Within-map area ratios can remove a uniform scale factor, but cannot remove local distortion or repair a missing denominator. No extra scales were imposed in this audit.

## Cortex ratios need a separate denominator check

Rows 471–483 contain dimensionless M1/cortex or area4/cortex values in the column titled Area (mm2); do not include them in absolute-area comparisons. Rows 480–482 numerically correspond to workbook numerator/denominator pairs, but that arithmetic does not validate biological neocortex scope. Row 483 is approximately 4303.848/84869.947, using the Wilkinson denominator rather than the Van Essen 2005 cortex entry 83484.231 cited in that row. This cross-source denominator needs explicit justification or correction. A comparison of M1 fractions requires both a matched field definition and an independently defensible cortex denominator.

All current traced values remain provisional as stated in their canonical data. No confidence interval or universal similarity threshold was inferred. Unresolved specimen identity, taxonomy, field extent, figure reuse and unit problems must be resolved before pooling biological estimates.
