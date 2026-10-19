<!-- full-dataset-recheck -->
## 16 October 2026 source recheck

The [full-dataset recheck note](full_dataset_recheck.md) and current canonical JSON/CSV supersede earlier contour counts or blanket exclusions of repeated/illustrative maps. [Review all source pages](../review/full_dataset_audit.html). Prior geometry is archived.

# Source, measurement decisions and limits

Lyon, D. C., Jain, N., & Kaas, J. H. (1998). Cortical connections of striate and extrastriate visual areas in tree shrews. Journal of Comparative Neurology, 401(1), 109–128. https://doi.org/10.1002/(SICI)1096-9861(19981109)401:1<109::AID-CNE7>3.0.CO;2-I

Source: `source/paper.pdf`, SHA-256 `375972a7159bf736cb676fdd4dbd92895042f42261f0710e09cc49634cbef199`. All 15 numbered figures assessed. Status: `eligible_figures_digitized_provisional`.

## Paper-specific decisions

Cases are 96-56, 96-81, 96-12, 96-43, 96-66 and 97-18 (literal labels, without tracer suffixes). Figures 4/12, 7/10B/14, 9/11 and 10A/13A-B repeat tissue within animals. Anatomical left/right is not assigned where captions give only ipsilateral/contralateral. The printed horizontal 1-mm coordinate arm is a source calibration; figures 13A-C instead have horizontal 1-mm bars. Panels without a local calibration retain pixels only. Thin lines mark the projected extent of the exposed lateral surface (figure 4 caption): these are not areal borders and cannot close an open field. V1 was recoverable as a closed whole envelope in figures 8B, 9C, 10A and 11A, including reflected medial portions. Figure 9C V2 closes at the tissue edge; figure 11A V2 has a short approximately five-source-pixel continuation at the ventral cut and is approximate. Other V1/V2 extents remain NA. Closed S components are retained as partial components where other S tissue is missing; no sum is promoted to a complete field. TA/TAL/TD/TP/TPI labels do not supply independent closed envelopes.

## Contour and calibration workflow

Source pages were rendered directly from the preserved PDF at 4 pixels/PDF point. Canonical JSON stores exact crop coordinates in that rendering, scale endpoints, printed length, literal field names, specimen/hemisphere, repeated-view links and field extent. Guides were placed on the observed printed perimeter, densely sampled and fitted locally to stroke centers. Short dashed/symbol interruptions are explicitly approximate or documented. Shared anatomical borders use a single source-guided path where independently fitted lines disagreed. Small local fitting hooks were removed; no shape was clipped to force a disjoint partition. Internal text, recording dots and tracer stains are retained rather than mistaken for tissue holes. Photographs without a defensible complete anatomical envelope remain NA. No anatomical boundary is generated from a generic stain threshold.

Scale endpoints refer to a local printed stroke/axis and its stated millimeters. An isolated panel without its own recoverable scale retains pixels; calibration is not copied between resized panels. Pixel geometry is retained separately from calibrated mm². Raster coverage uses 4× subpixel sampling; this is numerical precision, not biological uncertainty. Any displayed ±1-pixel sensitivity is a tracing perturbation only.

No independent complete-neocortex boundary is certified in this batch. Cortical percentages remain NA; named fields are never summed into a denominator. Approximate, partial and composite envelopes remain reviewable but are excluded from complete-field animal summaries. Repeated hemispheres/tracer panels do not add animals. One supported calibrated complete view per identified animal and literal label is selected; sample SD uses nonmissing animals and remains NA for n<2. Cross-paper specimen overlap is not resolved or pooled.

## Saved outputs and verification

20 canonical source views; 33 field/component contours; 168 explicit unavailable-field entries. `figures/*/rois.json` is canonical. Where contours exist, native ImageJ ROI ZIPs and masks, TIFF source images with calibration, source PNGs and overlays are rebuilt and read back through ImageJ. An inspected source crop with no ROI retains its source and NA rows, not a spurious zero. An excluded publication with no eligible surface has zero observations.

`review/precision_review.html` permits enlarged field selection and source-overlay toggles; `review/gallery.html` includes every numbered figure assessment and source preview. Vertex bounds/crossings, shared-border/interior overlaps, native ImageJ read-back, R selection rules and file checksums are checked by the rebuild. Automated checks cannot certify anatomical interpretation. All measured geometry remains provisional pending expert/user review. No external reference-data comparison was requested.

Rebuild from this dataset folder using the workspace Python runtime: `python scripts/rebuild_all.py --java /path/to/java`. Fiji/ImageJ jar may be supplied with `--ij-jar`. Verification: `python scripts/measure_flatmaps.py --verify`. Source selection and limitations are recorded in `figure_inventory.csv`; derived exports are reproducible from canonical geometry.
