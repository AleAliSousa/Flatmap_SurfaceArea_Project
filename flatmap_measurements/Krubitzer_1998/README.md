<!-- missing-region-actions-2026-10-20 -->
**20 October update:** 4 contours added; 0 revised. [Results and remaining limits](documentation/missing_region_actions_2026-10-20.md) · [Before/after review](review/missing_region_actions.html). Earlier counts and generic exclusions below describe the previous state.

<!-- full-dataset-recheck-2026-10-16 -->
# Krubitzer_1998 · current recheck

**61 field/component observations.** Added the two closed Vc/Vr outlines in figure 11B, retaining pixel geometry because this panel has no defensible labelled physical scale. Added 47 selected illustrative field/component observations from figures 13–14. Candidates that followed texture, glyphs or an interior patch of a black field were rejected. Echidna SI components are partial. Illustrative summaries are excluded from animal means.

[Latest source review](review/full_dataset_audit.html) · [Recheck findings and limits](documentation/full_dataset_recheck.md) · [Current measurements](data/measurements.csv). Earlier notes below describe the previous processing state; their counts are superseded.

<!-- earlier-processing-notes -->
## Earlier processing notes

# Krubitzer_1998

All15 numbered figures are assessed. This review repeats older datasets; no cross-paper pooling is permitted. Platypus is Ornithorhynchus anatinus. Echidna is retained as the source label without assigning a species, since the review discusses more than one echidna taxon and does not identify each pictured specimen to species. Only E2 and E3 are explicitly identified cases here. Figure2A is a historical SI envelope (Bohringer & Rowe1977), not equivalent to a modern isolated SI field. Figure11A Vc/Vr are repeated tissue of Figure10A; the bar in11 is unlabeled, so these contours retain pixel area only. Figure10A's open field envelopes stay NA despite its own physical calibration. Figure6's dashed auditory envelope and Figure12's VI? are approximate, excluded from complete-field summaries. VI? includes a tracer-obscured continuation whose approximate coordinate span is recorded in its ROI note. Closed islands in Figures6/7 and the adjacent auditory patch in12 are partial mapped patches, not total fields. Figure9C is a compound auditory mapped envelope, not an isolated A1? total. Literal question marks are preserved. Figures13/14 are derived comparisons, including sources in other project papers; no new animals are inferred.

Saved 9 source views and 12 measured field/fragment contours. All measurements are provisional.

- [Enlarged source-toggle review](review/precision_review.html)
- [All-figure assessment](review/gallery.html)
- [Measurements including NA](data/measurements.csv)
- [Figure inventory](documentation/figure_inventory.csv)
- [Methods and limits](documentation/methods.md)

Canonical geometry is in `figures/<map_id>/rois.json`, in crop coordinates at 4 pixels per PDF point. No image is stretched. Dense contours follow the source ink; closed white compartments and filled silhouettes are used only after visual inspection. Internal labels, recording sites and tracer deposits stay inside their anatomical envelopes. Short symbol-obscured continuations are recorded per ROI; open total fields remain NA. Source resolution and anatomical interpretation limit accuracy despite dense vertices. All manual measurements remain provisional pending anatomical review.

Own printed scale strokes are measured between their visible endpoints. Areas use fractional supersampled coverage and `area_mm2 = area_px2 * (scale_length_mm / scale_length_px)^2`. Unlabeled bars are not assigned lengths. Short bars in the monotreme source are particularly sensitive to endpoint placement. No shrinkage correction is applied. Sensitivity columns are NA; they are not confidence intervals.

No independently certified complete-neocortex outline was established. Whole-neocortex percentages and species percentage summaries remain unavailable. Repeated views are not extra animals; unresolved specimens are not pooled across maps or papers. Complete-field absolute-area summaries select one supported view per explicitly identified specimen and literal field label; main maps take priority, with repeated-view fallback only where the main map is unavailable. Partial and approximate fields, historical pixel-only drawings and specimens reported only as unknown remain per-view observations and do not enter those means. Sample SD is NA for n<2.

Rebuild locally with `python -B scripts/rebuild_all.py --java /path/to/java`. Outputs include long measurements, NA rows, summaries, native ImageJ overlays/ROI ZIPs/mask ZIPs for measured maps, source TIFFs, source-toggle precision review and all-figure assessment. `--verify` checks saved hashes, native ROI/mask/calibration read-back and area calculations. Geometry diagnostics check self-intersections and eroded-mask interior overlaps; visual source checks are separate and necessary.

<!-- project-tracing-review-2026-10-31 -->
## Project-wide tracing review, 31 October 2026

[View this dataset's quality review](../project_review_2026-10-31/index.html?paper=Krubitzer_1998) · [Review methods and changes](../project_review_2026-10-31/README.md)

View-level screening categories: A=2, B=14, N=2. A identifies the clearest source/fit examples; B retains caveats; C needs targeted review/retracing; D is unsuitable for the intended anatomical area inference; N has no saved trace. These are not individual-region certification or independent-specimen counts. See the linked report for each map's notes and proposed improvements.

Atlases and guides: see the [project guide](../ReadMe.md). Use same-specimen panels to resolve obscured lines where correspondence is established; use other specimens and atlases for field identity, adjacency and sulcal plausibility only. They do not supply an observed border, justify copying a shape, or establish a missing physical scale.

<!-- project-tracing-review-2026-10-31-pass2 -->
## Second precision pass, 31 October 2026

[Source / before / after review](../project_review_2026-10-31_pass2/index.html?paper=Krubitzer_1998) · [Change log and areas](../project_review_2026-10-31_pass2/area_changes.csv)

0 revised regions; 1 added components. Original datasets are archived in `../project_review_2026-10-31_pass2/before/`.

**Atlases and comparison guides:** Luethke et al. 1988 squirrel maps corroborate the M/SI arrangement. The new M outline follows the black silhouette in the 1998 Fig.14D summary itself, preserving the internal M lettering. It remains an illustrative summary, not an additional specimen or a whole-neocortex denominator.

Source-based revisions remain provisional. Existing specimen, scale and analysis-eligibility restrictions are preserved. See the review for unresolved fields and source-specific line meanings.

<!-- project-tracing-review-2026-10-31-pass3 -->
## Project recheck, pass 3

[Current project-wide review](../project_review_2026-10-31_pass3/index.html#Krubitzer_1998) · [Scope and methods](../project_review_2026-10-31_pass3/README.md). All inventoried source figures and saved views screened at overview scale; remaining precision/coverage limits are recorded.
