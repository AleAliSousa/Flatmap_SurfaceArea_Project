# Measurement method and limits

The source PDF is retained with a SHA-256 manifest. Source figures were rendered at four pixels per PDF point. Each crop, printed calibration and editable polygon is recorded in `figures/<map_id>/rois.json`; these saved coordinates are the authoritative measurement inputs.

External leaders were followed to their tissue endpoints. Lettering, numerals, recording circles, tracer deposits and internal shading were retained within anatomical envelopes. Source-guided curves used dense points and local smoothing at approximately one rendered pixel. Nearby dark ink could refine a guide within a bounded normal search; it could not choose an anatomical identity. Dark filled regions were traced at their external boundary rather than treating a white letter as the field. Color separation rejected white background and used local palette/shade information. Short gaps were bridged only where the visible neighboring border supported continuation. Approximate and partial observations retain those extent labels.

Adjacent manual guides were checked for overlap. Only narrow conflicts were reconciled to a common edge; broad conflicts required source review and a corrected perimeter. Exclusion polygons reuse inspected neighboring borders where needed. Explicit parent/subregion overlaps are allowed and non-additive; undeclared interior overlap fails validation. Thin shared-edge raster slivers are reported separately. Neither a successful geometry test nor dense vertices establish anatomical certainty.

Area is computed from the saved geometry at fourfold supersampling. Millimetres squared require an applicable printed bar; unscaled results remain pixels squared with NA physical area. Native ImageJ TIFF calibration, editable ROI ZIPs and saved masks were reopened and checked. Source-toggle reviews display both outer and dashed exclusion boundaries. Complete-field absolute summaries exclude partial/approximate, illustrative and unresolved observations. No view in this batch establishes a certified whole-neocortex denominator; no workbook numeric estimates were used.

## Source-specific assessment

Figure 4 is an unscaled human atlas adaptation. Seven field/component observations include the cut V1 pieces, visual domains, S1, M1 and SII. M1 follows the black boundary; red leader lines are annotations. No scale is borrowed from Van Essen and Drury or from a different paper. This atlas view supplies no independent animal or complete-neocortex denominator.

[Field-by-field inventory](field_inventory.csv) · [All numbered figures](figure_inventory.csv) · [Source-toggle review](../review/precision_review.html)
