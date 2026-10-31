<!-- full-dataset-recheck -->
## 16 October 2026 source recheck

The [full-dataset recheck note](full_dataset_recheck.md) and current canonical JSON/CSV supersede earlier contour counts or blanket exclusions of repeated/illustrative maps. [Review all source pages](../review/full_dataset_audit.html). Prior geometry is archived.

# Felleman_VanEssen_1991: source-based surface-area digitization

Felleman, D. J., & Van Essen, D. C. (1991). Distributed hierarchical processing in the primate cerebral cortex. Cerebral Cortex, 1(1), 1–47. https://doi.org/10.1093/cercor/1.1.1

## Scope and interpretation

The80G-R carrier is a macaque hemisphere with literature-composite parcellation, not an independently delineated new animal. All composite fields are excluded from biological case/species summaries. The 20 October 2026 figure 2 revision uses the preserved Harvard color reference to resolve merged monochrome field identities and external leader endpoints; all 74 field envelopes remain in original PDF coordinates. See [revision details](fig02_revision_2026-10-20.md). The scale already includes the source shrinkage estimate; no second correction. Figure1 encloses allo-/paleocortex as well as neocortex, so cannot supply a neocortex denominator. Pages 20–47 render blank in the preserved original measurement PDF, despite ghost text. The replacement primary PDF restores these pages; figures 1–3 retain their prior assessments and additional restored pages await eligibility assessment. See [source replacement](source_update_2026-10-20.md).

The existing inventory covers figures 1–3, their panels, captions and methods. Source pages for those figures are retained in the review; exclusion and non-measurability decisions are recorded in figure_inventory.csv. Source geometry is provisional pending anatomical certification. No denominator is inferred by summing named fields; percentages are NA without an independently established complete-neocortex outline. Missing boundaries and missing scale are NA, never zero.

## Contour method

Canonical measurement crops are rendered from source/paper_measurement_original.pdf at4pixels/PDF point without stretching. Closed source compartments or manually source-guided envelopes are followed with dense vertices. Short symbol interruptions and explicitly estimated borders are documented per ROI. Internal text/recording marks and body-part divisions are retained inside the field rather than treated as anatomical holes; the explicit UZ exclusion is an exception. Morphological gap closure is limited to the ink/symbol scale; ambiguous closures are not accepted as complete borders. Dense vertices do not establish anatomical certainty.

Each rois.json retains page, crop, rendering scale, rotation if used, calibration endpoints, specimen, repeats, extent and boundary notes. Native ImageJ TIFFs, subpixel ROI ZIPs, masks and read-back area tables are generated and checked against canonical polygons. Areas use4x supersampled polygon coverage. Pixel-only measurements remain in the table. Sensitivity columns remain NA; no statistical confidence interval is estimated.

## Summaries

Absolute-area summaries select one calibrated complete observation per explicitly identified animal and literal field; main-map views take priority and repeated views are fallback. Hemisphere is recorded in the selection table. Partial/estimated and composite atlas observations are excluded. No cross-paper species pooling or label homology inference is performed. Sample SD is NA below two animals.

## Rebuild

Run `python scripts/rebuild_all.py --java /path/to/java` from this dataset using Python with numpy, Pillow and pypdfium2, ImageJ and base R. The rebuild validates geometry, native ImageJ read-back, summary inputs and source checksums; generates source-toggle reviews and final checksum verification. No external reference comparison was requested.

## External label leaders

A leader identifies the compartment at its endpoint. Its line and its letters are not anatomical borders. Regions may contain labels from neighboring fields; area follows the visible anatomical envelope. Dark fills remain included tissue, with border placement based on the fill edge and neighboring compartments.
