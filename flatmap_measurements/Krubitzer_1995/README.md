<!-- missing-region-actions-2026-10-20 -->
**20 October update:** 21 contours added; 1 revised. [Results and remaining limits](documentation/missing_region_actions_2026-10-20.md) · [Before/after review](review/missing_region_actions.html). Earlier counts and generic exclusions below describe the previous state.

<!-- full-dataset-recheck-2026-10-16 -->
# Krubitzer_1995 · current recheck

**10 field/component observations.** Recovered ten clear comparative field outlines in figures 1–2. Merged black fills, lettering-shaped candidates and a tiny quoll auditory candidate crossing the grey/black interface were rejected. Original heavily filled source panels remain unquantified where a separate field perimeter is unresolved. These drawings are illustrative summaries, never additional animals.

[Latest source review](review/full_dataset_audit.html) · [Recheck findings and limits](documentation/full_dataset_recheck.md) · [Current measurements](data/measurements.csv). Earlier notes below describe the previous processing state; their counts are superseded.

<!-- earlier-processing-notes -->
## Earlier processing notes

# Krubitzer_1995

All seven numbered figures are assessed. Ten photographic panels (Figures 3A–F and4A–D) are preserved with explicit not-measurable rows. The supplied scan is saturated: black fills merge and complete individual field perimeters cannot be reproduced defensibly. Zero measured ROIs means no measured observations, not zero anatomical area. A clearer source would be required to recover these boundaries. Figure1/2 review cartoons, modules, projected connectivity and developmental networks are excluded. Unnumbered Box1 phylogeny and Box3 explanatory map/photo add no independent measurable case. No field was created by thresholding a saturated black blob.

Saved 10 source views and 0 measured field/fragment contours. All measurements are provisional.

- [Enlarged source-toggle review](review/precision_review.html)
- [All-figure assessment](review/gallery.html)
- [Measurements including NA](data/measurements.csv)
- [Figure inventory](documentation/figure_inventory.csv)
- [Methods and limits](documentation/methods.md)

Canonical geometry is in `figures/<map_id>/rois.json`, in crop coordinates at 4 pixels per PDF point. No image is stretched. Dense contours follow the source ink; closed white compartments and filled silhouettes are used only after visual inspection. Internal labels, recording sites and tracer deposits stay inside their anatomical envelopes. Short symbol-obscured continuations are recorded per ROI; open total fields remain NA. Source resolution and anatomical interpretation limit accuracy despite dense vertices. All manual measurements remain provisional pending anatomical review.

Own printed scale strokes are measured between their visible endpoints. Areas use fractional supersampled coverage and `area_mm2 = area_px2 * (scale_length_mm / scale_length_px)^2`. Unlabeled bars are not assigned lengths. Short bars in the monotreme source are particularly sensitive to endpoint placement. No shrinkage correction is applied. Sensitivity columns are NA; they are not confidence intervals.

No independently certified complete-neocortex outline was established. Whole-neocortex percentages and species percentage summaries remain unavailable. Repeated views are not extra animals; unresolved specimens are not pooled across maps or papers. Complete-field absolute-area summaries select one supported view per explicitly identified specimen and literal field label; main maps take priority, with repeated-view fallback only where the main map is unavailable. Partial and approximate fields, historical pixel-only drawings and specimens reported only as unknown remain per-view observations and do not enter those means. Sample SD is NA for n<2.

Rebuild locally with `python -B scripts/rebuild_all.py --java /path/to/java`. Outputs include long measurements, NA rows, summaries, native ImageJ overlays/ROI ZIPs/mask ZIPs for measured maps, source TIFFs, source-toggle precision review and all-figure assessment. `--verify` checks saved hashes, native ROI/mask/calibration read-back and area calculations. Geometry diagnostics check self-intersections and eroded-mask interior overlaps; visual source checks are separate and necessary.
