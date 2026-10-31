# Measurement methods and scope

Date: 31 October 2026. Scope: Brecht alternatives for human/macaque V1, A1 and S1-face. This is not a digitization of every unrelated region in these publications.

Six Fig.4 phase maps inspected; five have resolvable forehead display components. Purple forehead-bin pixels were selected by hue, rejecting blue antialiasing over gray; inactive holes retained. Tiny components under three rendered pixels are omitted as unresolved print speckle. Subject D has no stable printed component to trace; its published 10.1-mm² cluster is retained separately and not replaced with zero. Images lack physical calibration and are not demonstrated area-preserving, so all traced areas remain pixels. Only the glabella was stimulated. The text calls the maps right hemisphere although Table 1 has negative MNI x; preserve that discrepancy.

## Geometry and reproducibility

Canonical geometry is `figures/<map_id>/rois.json`. Source PDF SHA-256 is in `source/manifest.json`. Render scale is 3 pixels per PDF point. Crops are unscaled rectangles of the rendered page. Perimeter vertices are in crop coordinates; negative/outside scale endpoints occur only when an explicitly documented common figure scale is used. Such scale-reference views preserve the actual printed bar. Bar endpoints refer to the outer stroke edges, not its text.

No inter-paper scale borrowing, inferred whole-cortex denominator, or shrinkage correction is used. No field sum is substituted for whole cortex. All maps are partial fields, display projections, or calibration references; whole-neocortex percentages remain NA. Native paper areas and image tracing areas are separate observations.

Manual and color-assisted outlines remain provisional pending anatomical review. Pixel precision is not anatomical accuracy. Internal annotations remain included where they overlay tissue. Functional response maps preserve inactive gaps; these footprints are threshold- and display-dependent.

Run `python scripts/measure_flatmaps.py --rebuild`, then `--verify`, from this paper directory. This uses the source PDF and saved JSON only. The native Java/ImageJ exporter creates `source.tif` with editable overlay, `RoiSet.zip`, and `Masks.tif.zip`; native read-back checks calibration, image pixels, ROI pixels and masks. Do not import both the TIFF overlay and ROI ZIP as independent sets. Preserve manual ImageJ edits before any rebuild.

## Review

Every processed source/tracing pair was inspected at enlargement. Figure inventory and non-target label inventory are explicit. This does not certify every region of every paper. Native ImageJ and equation/hash checks are in `documentation/validation.json` and `documentation/imagej_measurements.tsv`. Core review is `review/gallery.html`.
