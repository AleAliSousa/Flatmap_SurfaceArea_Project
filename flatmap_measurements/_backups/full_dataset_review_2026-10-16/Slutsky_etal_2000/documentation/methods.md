# Slutsky_etal_2000: source-based surface-area digitization

Slutsky, D. A., Manger, P. R., & Krubitzer, L. (2000). Multiple somatosensory areas in the anterior parietal cortex of the California ground squirrel (Spermophilus beecheyii). Journal of Comparative Neurology, 416(4), 521–539. https://doi.org/10.1002/(SICI)1096-9861(20000124)416:4<521::AID-CNE8>3.0.CO;2-#

## Scope and interpretation

Literal source taxonomy Spermophilus beecheyii retained. Main architectural map is an unidentified case; later captions identify repeated physiological cases. Dashed PM is approximate; open physiological borders remain NA. A section stain alone is not thresholded to field area.

All 14 numbered figures, their panels, captions and methods were assessed. Source pages for every figure are retained in the review; exclusion and non-measurability decisions are recorded in figure_inventory.csv. Source geometry is provisional pending anatomical certification. No denominator is inferred by summing named fields; percentages are NA without an independently established complete-neocortex outline. Missing boundaries and missing scale are NA, never zero.

## Contour method

Canonical sources are rendered at4pixels/PDF point without stretching. Closed source compartments or manually source-guided envelopes are followed with dense vertices. Short symbol interruptions and explicitly estimated borders are documented per ROI. Internal text/recording marks and body-part divisions are retained inside the field rather than treated as anatomical holes; the explicit UZ exclusion is an exception. Morphological gap closure is limited to the ink/symbol scale; ambiguous closures are not accepted as complete borders. Dense vertices do not establish anatomical certainty.

Each rois.json retains page, crop, rendering scale, rotation if used, calibration endpoints, specimen, repeats, extent and boundary notes. Native ImageJ TIFFs, subpixel ROI ZIPs, masks and read-back area tables are generated and checked against canonical polygons. Areas use4x supersampled polygon coverage. Pixel-only measurements remain in the table. Boundary sensitivity is a geometric diagnostic, not a statistical confidence interval.

## Summaries

Absolute-area summaries select one calibrated complete observation per explicitly identified animal and literal field; main-map views take priority and repeated views are fallback. Hemisphere is recorded in the selection table. Partial/estimated and composite atlas observations are excluded. No cross-paper species pooling or label homology inference is performed. Sample SD is NA below two animals.

## Rebuild

Run `python scripts/rebuild_all.py --java /path/to/java` from this dataset using Python with numpy, Pillow and pypdfium2, ImageJ and base R. The rebuild validates geometry, native ImageJ read-back, summary inputs and source checksums; generates source-toggle reviews and final checksum verification. No external reference comparison was requested.
