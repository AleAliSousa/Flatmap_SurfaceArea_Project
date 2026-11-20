# Source PDF coverage audit — 19 November 2026

This is a read-only source and inventory assessment. Page numbers below are **one-based PDF pages**, not printed journal pages. An anatomical contour in a flatmap is a tracing candidate; a drawing, activity footprint, open border, or repeated view is not automatically an independent, metric cortical-field area.

## Primary queue: `papers_to_do/Cortical Image References/`

All 22 PDFs were checked against active dataset sources and the paper inventories. Twenty-one papers have an active dataset. `felleman_vanessen_1991.pdf` and `krubitzer_kaas_1990.pdf` differ in bytes from their dataset source PDFs because of source revisions, but each is the same 47-page or 40-page publication, respectively.

| Unprocessed paper | Candidate source geometry | Why it was missing |
| --- | --- | --- |
| `catania_etal_1999.pdf` — *Cortical Organization in Shrews: Evidence From Five Species* | Fig. 3A p6, *Blarina brevicauda* 97-81; Fig. 4A p7, *B. brevicauda* 97-47; Fig. 5A p8, *Cryptotis parva* 97-75; Fig. 6A p9, *C. parva* 97-79; Fig. 7A p10, *C. parva* 97-80; Fig. 8 p11, *C. parva* 97-77 visual response; Fig. 9A and CO section 9C p12, *C. parva* 97-44 (same animal); Fig. 10A p13, *Sorex palustris* 97-42; Fig. 11A/B p14, two sections of one *S. cinereus* hemisphere; Fig. 12 p15, another *S. cinereus* section; Fig. 13 p16, a *S. longirostris* reconstruction from multiple flattened sections. | The PDF had no `Catania_etal_1999` dataset and no row in `papers_to_do/paper_inventory.csv` or `remaining_work_inventory.csv` at audit start. Figures 3–10B are receptive-field illustrations rather than new cortical views. Fig. 2 p5 is a cross-species summary; Fig. 14 p16 is a composite with earlier corticospinal data. Source scale bars are printed on the candidate maps, including 500 µm in Fig. 12. |

**Felleman and Van Essen (1991) inventory correction:** the full replacement PDF has Figs. 4–8, which the dataset's `documentation/figure_inventory.csv` and `source/manifest.json` had not recorded as assessed. Fig. 4 p30 is a visual-area connection hierarchy; Fig. 5 p31 a histogram; Fig. 6 p32 a pathway bar chart; Fig. 7 p36 a somatosensory/motor hierarchy; Fig. 8 p38 a cat visual hierarchy. All five lack cortical surface geometry and require exclusion entries, not new ROIs. Existing ROI coordinates refer to `paper_measurement_original.pdf`, as the manifest states.

**Krubitzer and Kaas (1990) inventory check:** the existing `paper_figure_inventory.csv` and `excluded_panels.csv` already covered all 29 numbered figures, but this dataset lacked the `figure_inventory.csv` used by the other papers. The source PDF and captions were rechecked for Figs. 3, 5, 7, 8 and 29, which have no new bounded metric cortical fields: CO/myelin modules, a percentage chart, tracer photomicrographs, tracer reconstructions, and an evolutionary schematic, respectively. A 29-row standard inventory now records the 24 measured and five excluded figures. Figure 9's measured V2 strip is panel G; panels A–F remain excluded.

## Recommended and workbook-reference queues

Every one of the 16 PDFs in `papers_to_do/recommended/` and every PDF in `papers_to_do/M1_surface_workbook_figure_references_2026-10-20/PDFs/` has an active dataset with an exact matching PDF SHA-256. Each recommended paper's numbered main-text figures is represented in its `documentation/figure_inventory.csv`; this does **not** mean every region has been traced. The following are already documented outstanding candidates or limitations in `project_review_2026-10-31_pass3/remaining_review_queue.csv` and paper inventories:

| Dataset | Source figure and PDF page | Remaining source-limited work |
| --- | --- | --- |
| `Barton_etal_2012` | Figs. 2–3, pp3–4; supplemental S3/S4/S6 absent from supplied main PDF | hR/hRT/belt areas and additional participant maps need source material and field-specific border checks. |
| `Burman_etal_2008` | Fig. 6 p9; Fig. 9 pp11–13 | Fig. 6 M1 and remaining Fig. 9 labels; 21 older contours remain rejected, and the physical scale is unresolved. Fig. 9A–D repeat CJ58R anatomy. |
| `Ghosh_1997` | Figs. 14–16, pp17–19 | Further medial/parietal components and case 9 scale evidence; keep bank components separate. |
| `Halley_etal_2025` | Figs. 3–4, pp4–5 | Additional 1/2/PPC sampled components; windows do not close complete fields. Figs. 5–6 are pooled maps, not new animals. |
| `Remple_etal_2006` | Figs. 8–11, pp11–14 | Additional local motor/response components; M1 strips are open and repeated case 320R views must stay linked. |
| `SanchezPanchuelo_etal_2018` | Fig. 3 p7; Fig. 6 p11 | Additional participants/SII or digit responses lie beyond the prior S1-face target subset; native surface vertices are needed for metric area. |

Other existing review priorities include `Neafsey_etal_1986` local grid calibration, but this is a calibration problem rather than a missing source figure. No new missing numbered figure was found in the recommended queue by the source-inventory comparison.

## Background bibliography: `papers_to_do/cortical_flatmap_bibliography/`

This directory has 11 PDFs. `Catania_Remple_2002.pdf` and `Krubitzer_Prescott_2018.pdf` match active datasets exactly. The nine others are **background sources**, absent from the active measurement queue. Four contain possible new tracing material and would need their own dataset/provenance decisions before any measurement is pooled:

| Unprocessed paper | Candidate source geometry | Interpretation limit |
| --- | --- | --- |
| `Henry_etal_2006.pdf` | Naked mole-rat individual maps: Fig. 5A/B p7 case 01-15; Fig. 6A p9 case 01-13; Fig. 7A/B p10 case 01-11; Fig. 8A/B p11 case 01-16; Fig. 9A/B p12 case 01-14. Figs. 10–12 pp13–15 show S2/PV details of cases 01-15, 01-13, and 01-14 again. | Five distinct mapped cases, with repeated local views. Shaded body-part territories, CO modules, S1, S2 and provisional PV need separate label/uncertainty decisions. Fig. 13 p16 is a schematic summary. |
| `Sarko_etal_2011.pdf` | Fig. 3 p5 juvenile grasshopper-mouse SERT flat section with field outlines; Fig. 5A/B p7 adult recording map plus CO section; Fig. 6 p8 S2/PV detail. | Fig. 5 and Fig. 6 specimen linkage is not stated in the main figure captions. Text refers to Supporting Information Figs. 1–4, including the complete Fig. 6 mapping schematic in Suppl. Fig. 4; those files are not in the project. Fig. 7 p8 is composite. |
| `Seelke_etal_2016.pdf` | Fig. 1A/B p3 exemplar prairie-vole myelin flat section and reconstruction of field boundaries. | Fig. 2 p4 is a schematic of the same field layout; the paper's group percentages are not individual source ROIs. Specimen identity and any link between A/B must be resolved before pooling. |
| `Saraf_etal_2019.pdf` | Fig. 1a p3 reconstructed flattened mouse-lemur cortical view; Fig. 2a p4 partial flat section showing V1/V2 border. | Fig. 1b/c are coronal/sagittal projected views, not additional flatmaps. Fig. 1a is a reconstruction from serial sections placed on a matching brain image; its specimen identity and metric fidelity need source review. Fig. 2a cannot supply complete V1/V2 areas. |

The remaining five unmatched bibliography papers do not supply defensible *flatmap cortical-field* areas from the available PDF: `Bronchti_etal_2002.pdf` has 3D activity reconstructions (Fig. 6 p11) and average-brain projections (Fig. 7 p12); `Campos_Welker_1976.pdf` has curved-hemisphere sensory diagrams (Figs. 3–6 pp6–10); `Royce_etal_1975.pdf` has lateral curved-brain projections (Figs. 4–5 pp5,7); `Kaas_2011.pdf` consists of cross-study illustrative brain maps (Figs. 2–7 pp4–6), distinct from the active `Kaas_etal_2011` paper; `Naumann_2015.pdf` Fig. 1b p2 is an illustrated lateral Etruscan-shrew surface map, not a flattened specimen. These can be retained as context or drawing-only sources, with no invented intrinsic surface area.

The repository-root `Flat Map of Macaque Visual Cortex.pdf` is a one-page reproduction crediting Felleman and Van Essen (1991), not an additional publication.
