<!-- full-dataset-recheck-2026-10-16 -->
# Krubitzer_etal_1997 · current recheck

**15 field/component observations.** Smoothed four supported existing field/component contours against their source strokes. Closed component extents, partial SI status and specimen linkage are retained; no field was manufactured by closing an open map.

[Latest source review](review/full_dataset_audit.html) · [Recheck findings and limits](documentation/full_dataset_recheck.md) · [Current measurements](data/measurements.csv). Earlier notes below describe the previous processing state; their counts are superseded.

<!-- earlier-processing-notes -->
## Earlier processing notes

# Krubitzer_etal_1997

All nine numbered figures are assessed. Cases95-22,95-29 and95-28 retain the publication's labels; species is Echinops telfairi. Figure2B is the flattened reconstruction of95-22; Figures3/4/8 repeat its tissue. Figure6 repeats95-29 in Figure5. Figure7 contributes only a medial mapped S1 portion bounded by its printed body-part divider, not total S1. Long open physiological envelopes stay NA. Figure8 is not segmented by stain intensity: the paper states that multiple sections were necessary to delimit architecture. Enclosing reconstructions include fornix, corpus callosum, hippocampus and olfactory/piriform tissue and therefore are not whole-neocortex denominators. Comparative Figure9 does not create independent observations. The S1/R silhouettes touch in Figure2B; R is separated using the common visible divider.

Saved 7 source views and 15 measured field/fragment contours. All measurements are provisional.

- [Enlarged source-toggle review](review/precision_review.html)
- [All-figure assessment](review/gallery.html)
- [Measurements including NA](data/measurements.csv)
- [Figure inventory](documentation/figure_inventory.csv)
- [Methods and limits](documentation/methods.md)

Canonical geometry is in `figures/<map_id>/rois.json`, in crop coordinates at 4 pixels per PDF point. No image is stretched. Dense contours follow the source ink; closed white compartments and filled silhouettes are used only after visual inspection. Internal labels, recording sites and tracer deposits stay inside their anatomical envelopes. Short symbol-obscured continuations are recorded per ROI; open total fields remain NA. Source resolution and anatomical interpretation limit accuracy despite dense vertices. All manual measurements remain provisional pending anatomical review.

Own printed scale strokes are measured between their visible endpoints. Areas use fractional supersampled coverage and `area_mm2 = area_px2 * (scale_length_mm / scale_length_px)^2`. Unlabeled bars are not assigned lengths. Short bars in the monotreme source are particularly sensitive to endpoint placement. No shrinkage correction is applied. Sensitivity columns are NA; they are not confidence intervals.

No independently certified complete-neocortex outline was established. Whole-neocortex percentages and species percentage summaries remain unavailable. Repeated views are not extra animals; unresolved specimens are not pooled across maps or papers. Complete-field absolute-area summaries select one supported view per explicitly identified specimen and literal field label; main maps take priority, with repeated-view fallback only where the main map is unavailable. Partial and approximate fields, historical pixel-only drawings and specimens reported only as unknown remain per-view observations and do not enter those means. Sample SD is NA for n<2.

Rebuild locally with `python -B scripts/rebuild_all.py --java /path/to/java`. Outputs include long measurements, NA rows, summaries, native ImageJ overlays/ROI ZIPs/mask ZIPs for measured maps, source TIFFs, source-toggle precision review and all-figure assessment. `--verify` checks saved hashes, native ROI/mask/calibration read-back and area calculations. Geometry diagnostics check self-intersections and eroded-mask interior overlaps; visual source checks are separate and necessary.
