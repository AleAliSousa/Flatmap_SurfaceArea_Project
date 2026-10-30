<!-- full-dataset-recheck -->
## 16 October 2026 source recheck

The [full-dataset recheck note](full_dataset_recheck.md) and current canonical JSON/CSV supersede earlier contour counts or blanket exclusions of repeated/illustrative maps. [Review all source pages](../review/full_dataset_audit.html). Prior geometry is archived.

# Source, measurement decisions and limits

Preuss, T. M., Beck, P. D., & Kaas, J. H. (1993). Areal, modular, and connectional organization of visual cortex in a prosimian primate, the slow loris (Nycticebus coucang). Brain, Behavior and Evolution, 42(6), 321–335. https://doi.org/10.1159/000114169

Source: `source/paper.pdf`, SHA-256 `7a1aee68bcde9bc44718b88d236faf522ca6906cbbebe52a47924d1104fc32ef`. All 7 numbered figures assessed. Status: `eligible_figures_digitized_provisional`.

## Paper-specific decisions

Figure 2 is explicitly a schematic summary incorporating other studies; its closed envelopes are retained as composite geometry, excluded from specimen averages. Figures 5 and 6 identify cases 91-86R and 91-90R; specimen identifiers are 91-86 and 91-90, with R/L stored as hemisphere. Photographs in figures 3–4 identify 91-90L, the opposite hemisphere of the same animal represented in figure 6; figure 7 repeats the right hemisphere. V1, V2 and DL borders end within the reconstructions and remain NA. Figure 5's drawn MT outline includes the zone labelled FST? without an internal separator: label it MT/FST? drawn envelope, approximate, not pure MT. Figure 6's dashed ventrolateral MT border explicitly underestimates possible extension along STS (caption on PDF p.8): approximate only. Aud denotes primary auditory cortex plus neighboring fields, not a pure A1 measure. Photographic stain transitions are not thresholded into anatomical boundaries.

## Contour and calibration workflow

Source pages were rendered directly from the preserved PDF at 4 pixels/PDF point. Canonical JSON stores exact crop coordinates in that rendering, scale endpoints, printed length, literal field names, specimen/hemisphere, repeated-view links and field extent. Guides were placed on the observed printed perimeter, densely sampled and fitted locally to stroke centers. Short dashed/symbol interruptions are explicitly approximate or documented. Shared anatomical borders use a single source-guided path where independently fitted lines disagreed. Small local fitting hooks were removed; no shape was clipped to force a disjoint partition. Internal text, recording dots and tracer stains are retained rather than mistaken for tissue holes. Photographs without a defensible complete anatomical envelope remain NA. No anatomical boundary is generated from a generic stain threshold.

Scale endpoints refer to a local printed stroke/axis and its stated millimeters. An isolated panel without its own recoverable scale retains pixels; calibration is not copied between resized panels. Pixel geometry is retained separately from calibrated mm². Raster coverage uses 4× subpixel sampling; this is numerical precision, not biological uncertainty. Any displayed ±1-pixel sensitivity is a tracing perturbation only.

No independent complete-neocortex boundary is certified in this batch. Cortical percentages remain NA; named fields are never summed into a denominator. Approximate, partial and composite envelopes remain reviewable but are excluded from complete-field animal summaries. Repeated hemispheres/tracer panels do not add animals. One supported calibrated complete view per identified animal and literal label is selected; sample SD uses nonmissing animals and remains NA for n<2. Cross-paper specimen overlap is not resolved or pooled.

## Saved outputs and verification

6 canonical source views; 10 field/component contours; 26 explicit unavailable-field entries. `figures/*/rois.json` is canonical. Where contours exist, native ImageJ ROI ZIPs and masks, TIFF source images with calibration, source PNGs and overlays are rebuilt and read back through ImageJ. An inspected source crop with no ROI retains its source and NA rows, not a spurious zero. An excluded publication with no eligible surface has zero observations.

`review/precision_review.html` permits enlarged field selection and source-overlay toggles; `review/gallery.html` includes every numbered figure assessment and source preview. Vertex bounds/crossings, shared-border/interior overlaps, native ImageJ read-back, R selection rules and file checksums are checked by the rebuild. Automated checks cannot certify anatomical interpretation. All measured geometry remains provisional pending expert/user review. No external reference-data comparison was requested.

Rebuild from this dataset folder using the workspace Python runtime: `python scripts/rebuild_all.py --java /path/to/java`. Fiji/ImageJ jar may be supplied with `--ij-jar`. Verification: `python scripts/measure_flatmaps.py --verify`. Source selection and limitations are recorded in `figure_inventory.csv`; derived exports are reproducible from canonical geometry.
