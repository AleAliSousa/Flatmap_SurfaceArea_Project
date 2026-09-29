# Measurement workflow

## Paper setup and inventory

Inspect title, methods, captions and figure images. Identify species as reported, specimens, hemispheres, calibration, complete reconstructions, sections, partial fields, contralateral views, repeated panels and illustrative summaries. Record uncertain identities without inferring them from similar shape or numbering. Keep a per-paper `documentation/figure_inventory.csv` with page, figure/panel, interpretation, processing status and next action. For an explicitly requested first run, a clearly documented pilot subset is sufficient; do not label it a completed paper.

Use `prepare_paper.py` for a new folder, or continue an existing folder. Preserve the PDF and SHA-256 under `source/`. The new dataset contains `source/`, `figures/`, `data/`, `scripts/`, `review/` and `documentation/`. No `comparison/` directory is needed without reference input.

## Geometry and calibration

Render the original PDF pixels at a recorded scale, crop without stretching and visually inspect the crop. Coordinate origin is top-left, x right, y down. Store the crop rectangle in rendered-page coordinates and all ROI/bar coordinates in cropped-image coordinates. Read actual endpoints of the printed scale line, not its text. Uniform render scaling is supported; distortion or anisotropic scaling requires an explicit model.

Trace complete field envelopes, retaining tracer dots, labels and injection patches inside tissue. Keep tears/cut gaps outside tissue. Document any interpolation; a missing boundary does not justify a long invented closure. Whole-tissue outlines are independent of field boundaries. Multiple disconnected tissue pieces may require multiple polygons; holes/artifacts use explicit exclusions.

`area_mm2 = area_px2 * (scale_length_mm / scale_length_px)^2`

`percent_of_drawn_neocortex = 100 * field_area_px2 / whole_neocortex_area_px2`

The latter is valid without a physical scale if a defensible whole-neocortex outline exists. Schematics may have `percent_of_drawn_outline`, but not a specimen neocortex percentage. Partial fields without a denominator retain NA percentages. Do not apply shrinkage corrections without supplied evidence and a separately recorded factor.

## Canonical inputs and output

Keep all geometry and calibration in `figures/<map_id>/rois.json`; rebuild from those definitions and the checked source PDF. Native ImageJ edits are not automatically imported into JSON: preserve edited ROI ZIPs and reconcile them deliberately before rebuilding. Never regenerate hand edits from a second hidden coordinate source.

Generate the combined long measurement CSV, view index, applicable whole-hemisphere summary, calibrated TIFF with editable overlay, native ROI ZIP, mask-stack ZIP, and annotated tracing. Core visual review goes in `review/`. Optional reference comparisons go in `comparison/`.

## Verification

- Check PDF identity, crop dimensions, positive calibration, ROI vertices and self-intersections.
- Report overlaps and distinguish shared boundary rasterization from genuine interior overlap. Do not interpret overlapping field sums as exhaustive or disjoint cortex area.
- Recompute percentage/area equations, ensure NA remains unavailable and restrict whole-hemisphere summaries to flagged eligible views.
- Run native ImageJ read-back checks for calibration and pixel-exact masks/ROI selections. Fractional-pixel CSV area can differ slightly from binary ImageJ ROI area; report this difference.
- Inspect the rendered source/tracing pair for every processed view. Numerical or byte checks alone cannot validate anatomical borders.
- If estimating uncertainty by moving boundaries or scale endpoints, state the pixel perturbations and call them sensitivity scenarios, not confidence intervals. Between-case sample SD is a different quantity.
- Mark manual digitizations provisional until anatomical review. Missing reference data does not prevent completing these checks.
