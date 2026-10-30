<!-- full-dataset-recheck -->
## 16 October 2026 source recheck

The [full-dataset recheck note](full_dataset_recheck.md) and current canonical JSON/CSV supersede earlier contour counts or blanket exclusions of repeated/illustrative maps. [Review all source pages](../review/full_dataset_audit.html). Prior geometry is archived.

# Beck_etal_1996: source-based surface-area digitization

Beck, P. D., Pospichal, M. W., & Kaas, J. H. (1996). Topography, architecture, and connections of somatosensory cortex in opossums: Evidence for five somatosensory areas. Journal of Comparative Neurology, 366(1), 109–133. https://doi.org/10.1002/(SICI)1096-9861(19960226)366:1<109::AID-CNE8>3.0.CO;2-7

## Scope and interpretation

Eight identified cases in Figures2/3 retain each figure-wide1mm scale. S1/S2/PV identified by source legend, with body-part subdivisions united. Figures15/16 repeat93-88; Figure17 is92-79. Laterality is not inferred from reflected drawings. Figures16/17 have independently drawn overlapping Aud and PV envelopes, retained explicitly. Photo15 is a single-section repeat, not an extra animal.

All 18 numbered figures, their panels, captions and methods were assessed. Source pages for every figure are retained in the review; exclusion and non-measurability decisions are recorded in figure_inventory.csv. Source geometry is provisional pending anatomical certification. No denominator is inferred by summing named fields; percentages are NA without an independently established complete-neocortex outline. Missing boundaries and missing scale are NA, never zero.

## Contour method

Canonical sources are rendered at4pixels/PDF point without stretching. Closed source compartments or manually source-guided envelopes are followed with dense vertices. Short symbol interruptions and explicitly estimated borders are documented per ROI. Internal text/recording marks and body-part divisions are retained inside the field rather than treated as anatomical holes; the explicit UZ exclusion is an exception. Morphological gap closure is limited to the ink/symbol scale; ambiguous closures are not accepted as complete borders. Dense vertices do not establish anatomical certainty.

Each rois.json retains page, crop, rendering scale, rotation if used, calibration endpoints, specimen, repeats, extent and boundary notes. Native ImageJ TIFFs, subpixel ROI ZIPs, masks and read-back area tables are generated and checked against canonical polygons. Areas use4x supersampled polygon coverage. Pixel-only measurements remain in the table. Sensitivity columns remain NA; no statistical confidence interval is estimated.

## Summaries

Absolute-area summaries select one calibrated complete observation per explicitly identified animal and literal field; main-map views take priority and repeated views are fallback. Hemisphere is recorded in the selection table. Partial/estimated and composite atlas observations are excluded. No cross-paper species pooling or label homology inference is performed. Sample SD is NA below two animals.

## Rebuild

Run `python scripts/rebuild_all.py --java /path/to/java` from this dataset using Python with numpy, Pillow and pypdfium2, ImageJ and base R. The rebuild validates geometry, native ImageJ read-back, summary inputs and source checksums; generates source-toggle reviews and final checksum verification. No external reference comparison was requested.

## Labels crossing anatomical borders

Letters, numbers and stimulation symbols are annotations, not anatomical structures. Interior annotations must never become exclusion holes. Across an overprinted perimeter, interpolate the visible anatomical curve without fitting to the glyph ink. The [figure 12A correction](fig12A_label_correction.md) and [native mask checks](fig12A_annotation_check.json) document this rule in the SR example.
