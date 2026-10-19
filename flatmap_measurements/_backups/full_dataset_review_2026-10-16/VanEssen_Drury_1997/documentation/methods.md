# Source, measurement decisions and limits

Van Essen, D. C., & Drury, H. A. (1997). Structural and functional analyses of human cerebral cortex using a surface-based atlas. Journal of Neuroscience, 17(18), 7079–7102. https://doi.org/10.1523/JNEUROSCI.17-18-07079.1997

Source: `source/paper.pdf`, SHA-256 `7800cdfcba1c10afb68b74e89bff072b27a5d8181ac42ddfa0233c60d88e9721`. All 13 numbered figures assessed. Status: `assessed_no_defensible_field_contours`.

## Paper-specific decisions

All 13 figures are assessed. PDF pp.5–7 (printed pp.7083–7085), figure 4 and Table 1 distinguish area in the flattened image from 3-D cortical surface area. Table 1 explicitly calculates lobar areas by summing 3-D mesh tiles, not flatmap pixels. Mean areal distortion differs between hemispheres and varies spatially; a grid/scale bar cannot supply the missing tilewise 3-D metric. Therefore no true field area or field/cortex proportion is derived from the raster flatmaps. No 3-D mesh/metric data accompanies this local PDF. Source crops and explicit NA rows are retained for figures 3, 9D, 10D and 13C. The latter reprojects the Felleman & Van Essen (1991) macaque parcellation already represented in this project; it is not a new functional specimen observation. Figures 8, 11 and 12 show activation/uncertainty domains, not anatomical areal boundaries. Published Table 1 areas are source-reported context, not newly traced measurements and are not inserted into the new measurement table. No ROI is fabricated solely to complete the queue.

## Contour and calibration workflow

Source pages were rendered directly from the preserved PDF at 4 pixels/PDF point. Canonical JSON stores exact crop coordinates in that rendering, scale endpoints, printed length, literal field names, specimen/hemisphere, repeated-view links and field extent. Guides were placed on the observed printed perimeter, densely sampled and fitted locally to stroke centers. Short dashed/symbol interruptions are explicitly approximate or documented. Shared anatomical borders use a single source-guided path where independently fitted lines disagreed. Small local fitting hooks were removed; no shape was clipped to force a disjoint partition. Internal text, recording dots and tracer stains are retained rather than mistaken for tissue holes. Photographs without a defensible complete anatomical envelope remain NA. No anatomical boundary is generated from a generic stain threshold.

Scale endpoints refer to a local printed stroke/axis and its stated millimeters. An isolated panel without its own recoverable scale retains pixels; calibration is not copied between resized panels. Pixel geometry is retained separately from calibrated mm². Raster coverage uses 4× subpixel sampling; this is numerical precision, not biological uncertainty. Any displayed ±1-pixel sensitivity is a tracing perturbation only.

No independent complete-neocortex boundary is certified in this batch. Cortical percentages remain NA; named fields are never summed into a denominator. Approximate, partial and composite envelopes remain reviewable but are excluded from complete-field animal summaries. Repeated hemispheres/tracer panels do not add animals. One supported calibrated complete view per identified animal and literal label is selected; sample SD uses nonmissing animals and remains NA for n<2. Cross-paper specimen overlap is not resolved or pooled.

## Saved outputs and verification

5 canonical source views; 0 field/component contours; 27 explicit unavailable-field entries. `figures/*/rois.json` is canonical. Where contours exist, native ImageJ ROI ZIPs and masks, TIFF source images with calibration, source PNGs and overlays are rebuilt and read back through ImageJ. An inspected source crop with no ROI retains its source and NA rows, not a spurious zero. An excluded publication with no eligible surface has zero observations.

`review/precision_review.html` permits enlarged field selection and source-overlay toggles; `review/gallery.html` includes every numbered figure assessment and source preview. Vertex bounds/crossings, shared-border/interior overlaps, native ImageJ read-back, R selection rules and file checksums are checked by the rebuild. Automated checks cannot certify anatomical interpretation. All measured geometry remains provisional pending expert/user review. No external reference-data comparison was requested.

Rebuild from this dataset folder using the workspace Python runtime: `python scripts/rebuild_all.py --java /path/to/java`. Fiji/ImageJ jar may be supplied with `--ij-jar`. Verification: `python scripts/measure_flatmaps.py --verify`. Source selection and limitations are recorded in `figure_inventory.csv`; derived exports are reproducible from canonical geometry.
