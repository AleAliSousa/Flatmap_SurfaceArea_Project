# Luethke_etal_1988: source-based surface-area digitization

Luethke, L. E., Krubitzer, L. A., & Kaas, J. H. (1988). Cortical connections of electrophysiologically and architectonically defined subdivisions of auditory cortex in squirrels. Journal of Comparative Neurology, 268(2), 181–203. https://doi.org/10.1002/cne.902680205

## Scope and interpretation

Ipsilateral/contralateral views are opposite hemispheres of the same animal, not extra animals. Actual left/right is not inferred. Only each own printed calibration is used; later unlabelled maps are pixel-only. The enclosed architecturally separate UZ is explicitly subtracted from S-I. Compound TArv+TAcv retained where the internal separator does not uniquely close; no duplicate separate total. Summary selects at most one calibrated complete view per animal and literal field, with hemisphere provenance.

All 19 numbered figures, their panels, captions and methods were assessed. Source pages for every figure are retained in the review; exclusion and non-measurability decisions are recorded in figure_inventory.csv. Source geometry is provisional pending anatomical certification. No denominator is inferred by summing named fields; percentages are NA without an independently established complete-neocortex outline. Missing boundaries and missing scale are NA, never zero.

## Contour method

Canonical sources are rendered at4pixels/PDF point without stretching. Closed source compartments or manually source-guided envelopes are followed with dense vertices. Short symbol interruptions and explicitly estimated borders are documented per ROI. Internal text/recording marks and body-part divisions are retained inside the field rather than treated as anatomical holes; the explicit UZ exclusion is an exception. Morphological gap closure is limited to the ink/symbol scale; ambiguous closures are not accepted as complete borders. Dense vertices do not establish anatomical certainty.

Each rois.json retains page, crop, rendering scale, rotation if used, calibration endpoints, specimen, repeats, extent and boundary notes. Native ImageJ TIFFs, subpixel ROI ZIPs, masks and read-back area tables are generated and checked against canonical polygons. Areas use4x supersampled polygon coverage. Pixel-only measurements remain in the table. Sensitivity columns remain NA; no statistical confidence interval is estimated.

## Summaries

Absolute-area summaries select one calibrated complete observation per explicitly identified animal and literal field; main-map views take priority and repeated views are fallback. Hemisphere is recorded in the selection table. Partial/estimated and composite atlas observations are excluded. No cross-paper species pooling or label homology inference is performed. Sample SD is NA below two animals.

## Rebuild

Run `python scripts/rebuild_all.py --java /path/to/java` from this dataset using Python with numpy, Pillow and pypdfium2, ImageJ and base R. The rebuild validates geometry, native ImageJ read-back, summary inputs and source checksums; generates source-toggle reviews and final checksum verification. No external reference comparison was requested.
