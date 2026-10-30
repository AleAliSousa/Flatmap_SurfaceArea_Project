# Line refinement — 2026-10-15

The initial saved polygons cut corners and sometimes drifted off the anatomical stroke. All measured views in this dataset were re-examined on enlarged source images and retraced more densely. The original source PDFs and printed calibrations are unchanged.

Pages now render at 4 pixels per PDF point rather than 2. Crop coordinates and scale-bar endpoints doubled together. Dense guided contours were locally fitted to grayscale strokes, inspected against the original, and corrected where the tracking followed recording symbols, hatching, internal body-part lines or text. Closed-path loops introduced by tracking were removed and the resulting contours checked again. Simplification tolerance for the fitted contours is 0.5 new pixels (0.25 old pixels); this is a representation tolerance, not an estimate of anatomical accuracy. More vertices alone do not certify a boundary.

Short gaps or symbol-overprinted continuations are interpolated between visible borders. Beck Figure 10 uses a short interpolation through the injection circle; Beck Figure 11 has a legend-obscured continuation. Huffman recording marks crossing field edges are excluded from the border shape. These limitations remain visible in the source-toggle review. No statistical confidence interval or correction for shrinkage is claimed.

The previous polygons and measurements are archived in `rois_before_line_refinement.json` and `measurements_before_line_refinement.csv`. The full pre-edit dataset ZIP is in `flatmap_measurements/_backups/line_refinement_2026-10-15/`. `line_refinement_changes.csv` reports physical area changes. The review page displays current and previous contours separately over the same higher-resolution source; toggle them off to inspect the printed line.

Calibration, specimen identities, partial extents and independent tissue-denominator limitations are preserved. Polygon, numeric, ImageJ ROI/mask read-back and overlap checks establish reproducibility, not anatomical certification.
