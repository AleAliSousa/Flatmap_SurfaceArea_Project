# Source, measurement decisions and limits

Preuss, T. M., & Kaas, J. H. (1996). Cytochrome oxidase ‘blobs’ and other characteristics of primary visual cortex in a lemuroid primate, Cheirogaleus medius. Brain, Behavior and Evolution, 47(2), 103–112. https://doi.org/10.1159/000113231

Source: `source/paper.pdf`, SHA-256 `4c53c2019958973b708fd8187f92a938b628942edf4edc7d9e7b298bd0ae6b34`. All 5 numbered figures assessed. Status: `eligible_figures_digitized_provisional`.

## Paper-specific decisions

This paper contains five numbered figures (not three as in the old queue). Figure 2 is a multi-section composite reconstruction of one individual's flattened LEFT hemisphere, not a cross-animal schematic (caption PDF p.5). Methods identify one adult female; no invented case number is assigned. V1 has a closed perimeter including the calcarine cut edge; V2 and S1 do not have a recoverable complete envelope. The closed region denoted Aud is the auditory complex, not an isolated primary auditory field. MT is presumed by location/stain in the source and is retained as approximate presumed MT. Figure 3A is a local flattened left-cortex section; 3B is a coronal right-cortex section and cannot supply surface area. Figure 5 is another section of the same left hemisphere with diffuse stain transitions and presumed homologies; no threshold-defined field contours are invented.

## Contour and calibration workflow

Source pages were rendered directly from the preserved PDF at 4 pixels/PDF point. Canonical JSON stores exact crop coordinates in that rendering, scale endpoints, printed length, literal field names, specimen/hemisphere, repeated-view links and field extent. Guides were placed on the observed printed perimeter, densely sampled and fitted locally to stroke centers. Short dashed/symbol interruptions are explicitly approximate or documented. Shared anatomical borders use a single source-guided path where independently fitted lines disagreed. Small local fitting hooks were removed; no shape was clipped to force a disjoint partition. Internal text, recording dots and tracer stains are retained rather than mistaken for tissue holes. Photographs without a defensible complete anatomical envelope remain NA. No anatomical boundary is generated from a generic stain threshold.

Scale endpoints refer to a local printed stroke/axis and its stated millimeters. An isolated panel without its own recoverable scale retains pixels; calibration is not copied between resized panels. Pixel geometry is retained separately from calibrated mm². Raster coverage uses 4× subpixel sampling; this is numerical precision, not biological uncertainty. Any displayed ±1-pixel sensitivity is a tracing perturbation only.

No independent complete-neocortex boundary is certified in this batch. Cortical percentages remain NA; named fields are never summed into a denominator. Approximate, partial and composite envelopes remain reviewable but are excluded from complete-field animal summaries. Repeated hemispheres/tracer panels do not add animals. One supported calibrated complete view per identified animal and literal label is selected; sample SD uses nonmissing animals and remains NA for n<2. Cross-paper specimen overlap is not resolved or pooled.

## Saved outputs and verification

3 canonical source views; 3 field/component contours; 12 explicit unavailable-field entries. `figures/*/rois.json` is canonical. Where contours exist, native ImageJ ROI ZIPs and masks, TIFF source images with calibration, source PNGs and overlays are rebuilt and read back through ImageJ. An inspected source crop with no ROI retains its source and NA rows, not a spurious zero. An excluded publication with no eligible surface has zero observations.

`review/precision_review.html` permits enlarged field selection and source-overlay toggles; `review/gallery.html` includes every numbered figure assessment and source preview. Vertex bounds/crossings, shared-border/interior overlaps, native ImageJ read-back, R selection rules and file checksums are checked by the rebuild. Automated checks cannot certify anatomical interpretation. All measured geometry remains provisional pending expert/user review. No external reference-data comparison was requested.

Rebuild from this dataset folder using the workspace Python runtime: `python scripts/rebuild_all.py --java /path/to/java`. Fiji/ImageJ jar may be supplied with `--ij-jar`. Verification: `python scripts/measure_flatmaps.py --verify`. Source selection and limitations are recorded in `figure_inventory.csv`; derived exports are reproducible from canonical geometry.
