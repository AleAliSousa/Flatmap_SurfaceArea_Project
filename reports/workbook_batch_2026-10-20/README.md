# Workbook PDF tracing batch

Completed source assessment on 21 October 2026. The queue directory is `papers_to_do/M1_surface_workbook_figure_references_2026-10-20/PDFs`.

10 papers, 91 numbered figures, 57 traced views and 539 provisional field/component measurements. 35 source boundaries remain explicit NA for anatomical review. Haug has no eligible planar field contours. Counts are not independent animals.

[Open review](../../flatmap_measurements/review_workbook_batch_2026-10-20.html) · [Paper counts](paper_summary.csv) · [Measurements](all_measurements.csv) · [Unresolved boundaries](unresolved_boundaries.csv) · [Validation](validation.json)

The source PDF is retained with a SHA-256 manifest. Source figures were rendered at four pixels per PDF point. Each crop, printed calibration and editable polygon is recorded in `figures/<map_id>/rois.json`; these saved coordinates are the authoritative measurement inputs.

External leaders were followed to their tissue endpoints. Lettering, numerals, recording circles, tracer deposits and internal shading were retained within anatomical envelopes. Source-guided curves used dense points and local smoothing at approximately one rendered pixel. Nearby dark ink could refine a guide within a bounded normal search; it could not choose an anatomical identity. Dark filled regions were traced at their external boundary rather than treating a white letter as the field. Color separation rejected white background and used local palette/shade information. Short gaps were bridged only where the visible neighboring border supported continuation. Approximate and partial observations retain those extent labels.

Adjacent manual guides were checked for overlap. Only narrow conflicts were reconciled to a common edge; broad conflicts required source review and a corrected perimeter. Exclusion polygons reuse inspected neighboring borders where needed. Explicit parent/subregion overlaps are allowed and non-additive; undeclared interior overlap fails validation. Thin shared-edge raster slivers are reported separately. Neither a successful geometry test nor dense vertices establish anatomical certainty.

Area is computed from the saved geometry at fourfold supersampling. Millimetres squared require an applicable printed bar; unscaled results remain pixels squared with NA physical area. Native ImageJ TIFF calibration, editable ROI ZIPs and saved masks were reopened and checked. Source-toggle reviews display both outer and dashed exclusion boundaries. Complete-field absolute summaries exclude partial/approximate, illustrative and unresolved observations. No view in this batch establishes a certified whole-neocortex denominator; no workbook numeric estimates were used.

## Reproduction and drafting provenance

The canonical per-paper `rois.json` files include the accepted shared-border corrections. Rebuild them using each paper’s `scripts/rebuild_all.py`; this does not require OpenCV. The accompanying `views.json`, `build_batch.py`, `render_crops.py`, `reconcile_shared.py` and `fast_audit.py` are drafting provenance, not the authoritative final geometry. They contain original local cache paths and must not be run blindly: regenerating draft guides overwrites later accepted corrections. All temporary drafting conflicts are superseded by the final per-paper geometry audit and native verification. Backups under `documentation/pre_reconciliation` are earlier drafts, not additional measurements.

The saved exports were reopened through native ImageJ and checked against the canonical coordinates, masks and calibration. Final checksums were refreshed after documentation. This validates the files and geometry; anatomical certification remains pending.

Mayer color components are printed-color allocation estimates, not exact half-tile allocation or anatomical parcels; use the combined response territories for the sampled-area result. Every new view remains excluded from whole-hemisphere summaries.
