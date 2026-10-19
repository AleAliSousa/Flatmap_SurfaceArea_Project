<!-- full-dataset-recheck -->
## 16 October 2026 source recheck

The [full-dataset recheck note](full_dataset_recheck.md) and current canonical JSON/CSV supersede earlier contour counts or blanket exclusions of repeated/illustrative maps. [Review all source pages](../review/full_dataset_audit.html). Prior geometry is archived.

# Source, measurement decisions and limits

Luethke, L. E., Krubitzer, L. A., & Kaas, J. H. (1989). Connections of primary auditory cortex in the New World monkey, Saguinus. Journal of Comparative Neurology, 285(4), 487–513. https://doi.org/10.1002/cne.902850406

Source: `source/paper.pdf`, SHA-256 `98c39330b393aa852d0ea80ad428d9bc77094721f263662387bee22176f0a3d3`. All 17 numbered figures assessed. Status: `eligible_figures_digitized_provisional`.

## Paper-specific decisions

Five adult tamarins were studied (methods PDF pp.2–3), but figures with eligible contours identify only 87-22, 87-44 and 87-45. Do not invent maps for the remaining cases. Figure 3 identifies 87-22's injection hemisphere as right; only this case is assigned anatomical right/left. Other case sides remain ipsilateral/contralateral without an inferred anatomical side. Figure 2 remains in its original sideways PDF orientation. Its 2-mm stroke is retained in the 87-22 crop; the separate 87-44 crop has pixels only. Figures 5–6 each contain four repeats of the same ipsilateral tissue; figure 7 includes an opposite hemisphere and its independently scaled enlargement; figure 8 includes two repeats per hemisphere; figure 10A repeats 87-45's ipsilateral reconstruction. Other panels of figure 10 are thalamic. Dashed A-I/R/S-I borders are approximate; frame-clipped MT/S-II are NA. Internal tracer stains are not subtracted from anatomical fields.

## Contour and calibration workflow

Source pages were rendered directly from the preserved PDF at 4 pixels/PDF point. Canonical JSON stores exact crop coordinates in that rendering, scale endpoints, printed length, literal field names, specimen/hemisphere, repeated-view links and field extent. Guides were placed on the observed printed perimeter, densely sampled and fitted locally to stroke centers. Short dashed/symbol interruptions are explicitly approximate or documented. Shared anatomical borders use a single source-guided path where independently fitted lines disagreed. Small local fitting hooks were removed; no shape was clipped to force a disjoint partition. Internal text, recording dots and tracer stains are retained rather than mistaken for tissue holes. Photographs without a defensible complete anatomical envelope remain NA. No anatomical boundary is generated from a generic stain threshold.

Scale endpoints refer to a local printed stroke/axis and its stated millimeters. An isolated panel without its own recoverable scale retains pixels; calibration is not copied between resized panels. Pixel geometry is retained separately from calibrated mm². Raster coverage uses 4× subpixel sampling; this is numerical precision, not biological uncertainty. Any displayed ±1-pixel sensitivity is a tracing perturbation only.

No independent complete-neocortex boundary is certified in this batch. Cortical percentages remain NA; named fields are never summed into a denominator. Approximate, partial and composite envelopes remain reviewable but are excluded from complete-field animal summaries. Repeated hemispheres/tracer panels do not add animals. One supported calibrated complete view per identified animal and literal label is selected; sample SD uses nonmissing animals and remains NA for n<2. Cross-paper specimen overlap is not resolved or pooled.

## Saved outputs and verification

19 canonical source views; 41 field/component contours; 39 explicit unavailable-field entries. `figures/*/rois.json` is canonical. Where contours exist, native ImageJ ROI ZIPs and masks, TIFF source images with calibration, source PNGs and overlays are rebuilt and read back through ImageJ. An inspected source crop with no ROI retains its source and NA rows, not a spurious zero. An excluded publication with no eligible surface has zero observations.

`review/precision_review.html` permits enlarged field selection and source-overlay toggles; `review/gallery.html` includes every numbered figure assessment and source preview. Vertex bounds/crossings, shared-border/interior overlaps, native ImageJ read-back, R selection rules and file checksums are checked by the rebuild. Automated checks cannot certify anatomical interpretation. All measured geometry remains provisional pending expert/user review. No external reference-data comparison was requested.

Rebuild from this dataset folder using the workspace Python runtime: `python scripts/rebuild_all.py --java /path/to/java`. Fiji/ImageJ jar may be supplied with `--ij-jar`. Verification: `python scripts/measure_flatmaps.py --verify`. Source selection and limitations are recorded in `figure_inventory.csv`; derived exports are reproducible from canonical geometry.
