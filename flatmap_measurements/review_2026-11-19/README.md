# Source-line and figure-inventory recheck — 19 November 2026

[Visual correction gallery](index.html) · [All 19 area changes](area_changes.csv) · [Figure-number coverage](figure_number_coverage.csv) · [Source PDF audit](source_coverage.md) · [Technical verification](technical_verification.csv)

## Result

The 48 processed publication folders have 461 canonical views. Every one has a numbered figure inventory, and each inventory runs continuously from Figure 1 to its last recorded numbered figure. The source audit checked the primary, recommended and workbook-reference PDF queues against their inventories and captions. It found one omitted publication, Catania et al. (1999), and five omitted Felleman and Van Essen (1991) figure entries. Catania now has all 14 figures assessed, 12 canonical source views, and 24 calibrated regional ROIs in 10 traced views. Figures 11A and 12 retain source rasters with explicit unmeasured fields because their stain boundaries do not close reliably. Felleman Figures 4–8 are entered as excluded charts and connection diagrams. The Krubitzer and Kaas (1990) inventory was standardized and its five nonmetric figures were confirmed against the source.

The source-line screen covered **1,906 regional ROIs** in **399 ROI-bearing views**. Enlarged source review classified all 56 initial flagged or manually selected rows: 15 were off line, 31 were intentional or false-positive ink-distance flags, and 10 remain uncertain because the source lacks a unique closed border. Fourteen of the off-line rows were corrected; the fifteenth is an FST trace already rejected and excluded from analysis. Five further corrections came from visual review outside those flagged rows, for **19 corrected ROIs in 16 views across nine papers**. [The gallery](index.html) shows each changed view, and [the area-change table](area_changes.csv) gives the before/after values and links to prior JSON or tracing evidence.

| Paper | Corrected ROIs | Main issue |
| --- | ---: | --- |
| Lyon et al. 1998 | 5 | Shortcuts across blank tissue and shared visual-field borders. |
| Krubitzer et al. 1993 | 5 | Local 3b components and A-I/PV perimeter drift. |
| Krubitzer et al. 1995 | 2 | V outer arc and SI bill-island edge. |
| Remple et al. 2006 | 2 | Shared S1 foot/forelimb separator. |
| Catania et al. 1999 | 1 | V1 notch around a microlesion symbol, rather than the gray field edge. |
| Huffman et al. 1999 | 1 | SII/PV lower-left outer arc. |
| Luethke et al. 1989 | 1 | S-I (3b) contour shortcuts; area changed by +22.16% in source pixels, with no source calibration. |
| Preuss et al. 1993 | 1 | S1 schematic contour shortcut. |
| Rosa et al. 1993 | 1 | V1 schematic border drift. |

## Checks and reproducibility

The [final line-proximity screen](line_proximity_method.md) has 40 automatic flags and 61 final flagged or manually reviewed rows; all 61 now have a documented disposition. This ink-distance method is a triage aid: gray/dashed borders, labels, tracer overprint, and interpolated gaps can defeat a simple pixel threshold. The [pre-final screen snapshot](line_proximity_review_snapshot.csv), [28-row Burman/Felleman review](flagged_review_burman_felleman.csv), [28-row other-paper review](flagged_review_other.csv), [15-row unflagged spot check](unflagged_spotcheck.csv), and [independent Catania review](catania_independent_review.md) preserve the visual decisions. Agreement at view scale is not microscopic or anatomical ground truth.

Edited paper outputs were rebuilt from canonical JSON and passed native ImageJ ROI/mask read-back. The [all-paper verifier](scripts/verify_all.py) reports 48 of 48 datasets passing geometry, measurement and saved-file hash checks. For the older Krubitzer and Kaas (1990) script, the read-only verification calls its own geometry function without the unavailable `reportlab` import and checks its 450-file ledger separately; no tracing was edited there. That ledger was reconciled to files in this checkout: 16 entries for an absent optional `comparison/` directory were removed and the new standard inventory was included. The [figure-number check](scripts/check_figure_numbers.py) reports 48 of 48 contiguous inventories.

The downstream [surface-area analysis](../../surface_area_analysis/reports/analysis_report.md) was regenerated after fixing its loader to read only canonical `paper/data/measurements.csv` paths. Its 3,529 rows contain no duplicated paper/view/label keys or archived review measurements; excluded calibrated rows have explicit reasons. This correction prevents prior-version backups in this review folder from entering aggregate means.

## Source-limited work retained explicitly

Eight Burman Fig. 9A contours remain rejected pending a defensible border, and two Rosa V2/VIP contours remain provisional approximations; their enlarged source decisions are in the two flag-review tables. No new closed line was invented for these fields. The Catania 11A/12 source-only fields remain unmeasured. Other known partial or missing-source candidates are listed in the [source coverage audit](source_coverage.md).

Four papers in the **background bibliography**, outside the active measurement queue, have possible new flatmap material: Henry et al. (2006), Sarko et al. (2011), Seelke et al. (2016), and Saraf et al. (2019). Their candidate figures and specimen/scale limits are listed in the [source audit](source_coverage.md). They have not been pooled into the 48 processed datasets.
