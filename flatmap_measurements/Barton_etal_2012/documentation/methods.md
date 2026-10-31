# Measurement methods and scope

Date: 31 October 2026. Scope: Brecht alternatives for human/macaque V1, A1 and S1-face. This is not a digitization of every unrelated region in these publications.

Five unique hA1 hemispheres are measurable in the supplied main article: S4 left/right and S3 left in Fig.2B; S2 left and S1 left in Fig.3A. Fig.3 S4 right is additionally traced as a scale/geometry check and excluded from independent summaries. Solid/dotted reversals determine the hA1 perimeter. Each figure has its own common 1-cm scale. Surface areas are 2D flattened-map estimates, not certified native-mesh areas. Only hA1 is in the Brecht target scope; hR, hRT and eight belt fields are inventoried but not digitized. The three remaining subject hemispheres and Fig.S6 numerical benchmark require the supplementary material, which was not in the folder.

## Geometry and reproducibility

Canonical geometry is `figures/<map_id>/rois.json`. Source PDF SHA-256 is in `source/manifest.json`. Render scale is 3 pixels per PDF point. Crops are unscaled rectangles of the rendered page. Perimeter vertices are in crop coordinates; negative/outside scale endpoints occur only when an explicitly documented common figure scale is used. Such scale-reference views preserve the actual printed bar. Bar endpoints refer to the outer stroke edges, not its text.

No inter-paper scale borrowing, inferred whole-cortex denominator, or shrinkage correction is used. No field sum is substituted for whole cortex. All maps are partial fields, display projections, or calibration references; whole-neocortex percentages remain NA. Native paper areas and image tracing areas are separate observations.

Manual and color-assisted outlines remain provisional pending anatomical review. Pixel precision is not anatomical accuracy. Internal annotations remain included where they overlay tissue. Functional response maps preserve inactive gaps; these footprints are threshold- and display-dependent.

Run `python scripts/measure_flatmaps.py --rebuild`, then `--verify`, from this paper directory. This uses the source PDF and saved JSON only. The native Java/ImageJ exporter creates `source.tif` with editable overlay, `RoiSet.zip`, and `Masks.tif.zip`; native read-back checks calibration, image pixels, ROI pixels and masks. Do not import both the TIFF overlay and ROI ZIP as independent sets. Preserve manual ImageJ edits before any rebuild.

## Review

Every processed source/tracing pair was inspected at enlargement. Figure inventory and non-target label inventory are explicit. This does not certify every region of every paper. Native ImageJ and equation/hash checks are in `documentation/validation.json` and `documentation/imagej_measurements.tsv`. Core review is `review/gallery.html`.
