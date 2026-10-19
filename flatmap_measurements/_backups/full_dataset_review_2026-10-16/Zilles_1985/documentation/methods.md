# Source, measurement decisions and limits

Zilles, K. (1985). The cortex of the rat: A stereotaxic atlas. Springer-Verlag. https://doi.org/10.1007/978-3-642-70573-1

Source: `source/paper.pdf`, SHA-256 `644fc3fa9cb8748a7630626c22874a4510a491e9f596d4d36692f81add9876ed`. All 76 numbered figures assessed. Status: `assessed_no_eligible_specimen_flatmaps`.

## Paper-specific decisions

All 76 numbered figures and all 123 PDF pages were inspected. Figures 2–45 are section atlases. Printed p.55 (PDF p.59) explicitly says cortical maps in figures 46–49 were made by ORTHOGONAL PROJECTION of coronal/horizontal sections; lateral, dorsal and medial views overlap and must not be summed to invent a surface area. Their coordinate grids are spatial coordinates, not an area-preserving flattening. Printed p.61 (PDF p.64) describes figures 50–54 as rotated 3-D perspective reconstructions. Figures 55–67 are coronal Nissl/myelin sections and 68–72 are laminar architecture, not tangential areal maps. Printed pp.103–104 (PDF pp.105–106) describe figures 73–76 as superposed projected maps and cross-strain minimal common core regions; they are not independent unfolded specimens. No source supplies defensible planar cortical surface geometry, so this dataset has zero measurement observations and no fabricated ImageJ ROIs. The complete all-figure exclusion inventory and source previews are the deliverable. Rat strains/cases differ across book sections; none is promoted to a measured animal.

## Contour and calibration workflow

Source pages were rendered directly from the preserved PDF at 4 pixels/PDF point. Canonical JSON stores exact crop coordinates in that rendering, scale endpoints, printed length, literal field names, specimen/hemisphere, repeated-view links and field extent. Guides were placed on the observed printed perimeter, densely sampled and fitted locally to stroke centers. Short dashed/symbol interruptions are explicitly approximate or documented. Shared anatomical borders use a single source-guided path where independently fitted lines disagreed. Small local fitting hooks were removed; no shape was clipped to force a disjoint partition. Internal text, recording dots and tracer stains are retained rather than mistaken for tissue holes. Photographs without a defensible complete anatomical envelope remain NA. No anatomical boundary is generated from a generic stain threshold.

Scale endpoints refer to a local printed stroke/axis and its stated millimeters. An isolated panel without its own recoverable scale retains pixels; calibration is not copied between resized panels. Pixel geometry is retained separately from calibrated mm². Raster coverage uses 4× subpixel sampling; this is numerical precision, not biological uncertainty. Any displayed ±1-pixel sensitivity is a tracing perturbation only.

No independent complete-neocortex boundary is certified in this batch. Cortical percentages remain NA; named fields are never summed into a denominator. Approximate, partial and composite envelopes remain reviewable but are excluded from complete-field animal summaries. Repeated hemispheres/tracer panels do not add animals. One supported calibrated complete view per identified animal and literal label is selected; sample SD uses nonmissing animals and remains NA for n<2. Cross-paper specimen overlap is not resolved or pooled.

## Saved outputs and verification

0 canonical source views; 0 field/component contours; 0 explicit unavailable-field entries. `figures/*/rois.json` is canonical. Where contours exist, native ImageJ ROI ZIPs and masks, TIFF source images with calibration, source PNGs and overlays are rebuilt and read back through ImageJ. An inspected source crop with no ROI retains its source and NA rows, not a spurious zero. An excluded publication with no eligible surface has zero observations.

`review/precision_review.html` permits enlarged field selection and source-overlay toggles; `review/gallery.html` includes every numbered figure assessment and source preview. Vertex bounds/crossings, shared-border/interior overlaps, native ImageJ read-back, R selection rules and file checksums are checked by the rebuild. Automated checks cannot certify anatomical interpretation. All measured geometry remains provisional pending expert/user review. No external reference-data comparison was requested.

Rebuild from this dataset folder using the workspace Python runtime: `python scripts/rebuild_all.py --java /path/to/java`. Fiji/ImageJ jar may be supplied with `--ij-jar`. Verification: `python scripts/measure_flatmaps.py --verify`. Source selection and limitations are recorded in `figure_inventory.csv`; derived exports are reproducible from canonical geometry.
