<!-- full-dataset-recheck -->
## 16 October 2026 source recheck

The [full-dataset recheck note](full_dataset_recheck.md) and current canonical JSON/CSV supersede earlier contour counts or blanket exclusions of repeated/illustrative maps. [Review all source pages](../review/full_dataset_audit.html). Prior geometry is archived.

# Measurement methods and scope

Source: Krubitzer LA and Kaas JH (1993), *The Dorsomedial Visual Area of Owl Monkeys: Connections, Myeloarchitecture, and Homologies in Other Primates*, Journal of Comparative Neurology 334:497–528. Source identity and SHA-256 are preserved in `source/manifest.json`.

## Scope and completion

All 21 numbered figures were inspected against source images, captions and relevant methods on 2026-10-15. The remaining eligible figures have been digitized provisionally. Figures 1, 2, 4, 7–10 and 21 were excluded with source-specific reasons in `figure_inventory.csv`: they are illustrative/projected summaries, recording plots, tracer details, or images without complete field envelopes. Exclusion does not mean a measured zero.

The Figure5 pilot was preserved during the initial completion pass. Its contours were subsequently included in the user-requested precision audit; previous geometry is archived and its 18 legacy NA rows remain in place. There are no `not_yet_digitized` rows in the newly assessed views. A `not_measurable` row means the available source does not supply a defensible complete envelope, not that the anatomical field is absent. Figure12B/C retain source crops and local calibration but no invented field ROIs.

## Identity and denominators

Species follow the source methods (PDF p3): Aotus trivirgatus, Callithrix jacchus, Saimiri sciureus, Galago senegalensis, Miopithecus talapoin, Erythrocebus patas and Macaca fascicularis. No modern taxonomic reassignment is inferred. Laterality is unassigned where not reported.

Figures5, 6, 14–18 have independent whole drawn neocortex outlines and enter the within-paper whole-hemisphere summary. Figure3 is explicitly a representative tangential section; Figures12/13 are histological sections; Figure11 contains cropped contralateral views. These retain their own geometry and calibration but do not enter the whole-hemisphere summary. Figure19 explicitly lacks calcarine/frontal/temporal cortex; Figure20 has straight cut edges and a restricted posterior extent. Both are partial reconstructions. The combined17+18 envelope and MT in Figure19, and field17 in Figure20, are measured only to the visible tissue cuts, flagged `partial`, and must not be treated as full field areas. In Figure19 the injection hides too much of the shared17/18 boundary to partition the individual fields reliably: both are NA, with the combined partial envelope recorded separately.

Figure11A is opposite the injected hemisphere of 89-35 (Figure3); Figure11B is opposite 88-32 (Figure5). Figure12 specimens are unidentified and may overlap connection cases. Figure13 is an unidentified marmoset section and may overlap Figure15; no independent animal is inferred. Figure14 case88-16 also occurs in the 1990 dataset: cross-paper pooling remains unresolved. Figure5 is explicitly modified from Krubitzer and Kaas1990a. No cross-publication pooling was performed.

Only eligible whole reconstructions have `percent_of_drawn_neocortex`. `percent_of_drawn_outline` for sections/partial tissue means percent of that specific saved outline, not percent of whole neocortex. Whole cortex denominators are never constructed by adding fields.

## Canonical geometry and calibration

All pages were rendered at 2 pixels per PDF point without stretching. Each view's crop, physical scale endpoints, printed length, source page and polygons are saved in `figures/<map_id>/rois.json`. Endpoints were taken from the printed scale strokes in that same panel. Figure11 panels and Figure12 panels have separate bars; calibration is not borrowed across panels. No shrinkage correction is applied. Short scale bars, especially Figure16, limit precision. Sensitivity bounds were not calculated and remain NA.

For line drawings, closed external contours and selected solid field envelopes were extracted from grayscale<170 pixels, with outside/inside flood filling and 0.8-pixel polygon simplification. This was only an initial selection method. Every traced view was visually checked against the source. Escaped selections through fine or broken lines were replaced by manually placed polygons. Manual polygons follow the visible inked outline, including visible dashes; short intervals between dashes or tracer-obscured segments are documented per field. No open-ended field was completed with a long invented closure. In particular, Figure19 areas17/18 were retained as a compound envelope because their obscured internal border could not be reliably split. Photomicrograph field outlines were traced manually against the thin inked borders rather than thresholding the myelin stain. Interior labels and tracer deposits remain in the field envelope. Figure13 has an independent manual section-tissue outline. Cut gaps remain outside tissue. Disconnected 3b pieces in Figure17 and the dorsal/ventral area17 pieces in Figure16 are unions under one field label.

Fourfold raster supersampling computes fractional coverage. `area_mm2 = area_px2 * (scale_length_mm / scale_length_px)^2`. Regions are clipped to the independent tissue outline when one exists. CSV precision represents the saved geometry, not anatomical certainty. Neighboring hand-drawn polygons can produce narrow raster overlaps near shared borders; overlap diagnostics are retained, not interpreted as disjoint exhaustive cortex subdivisions. Totals across fields are not calculated.

## Verification and review

Rebuild validates PDF identity, crop bounds, scales, polygon bounds and proper segment intersections. The source TIFF, native ROI ZIP, overlay and named mask-stack ZIP are exported through ImageJ; native ImageJ reads them back and checks calibration and pixel equality. CSV areas use fractional coverage; ImageJ selections use >=50% coverage, so small differences are expected and recorded in `imagej_measurements.tsv`.

`review/gallery.html` contains source/tracing pairs and measured values for every saved view. `documentation/validation.json` and `geometry_review.json` retain numerical/native and overlap checks. Every new tracing has received source-image review, but all new manual measurements remain provisional pending anatomical review. This is a completed source-limited digitization pass, not anatomical certification. External reference comparison was not requested and no reference data were supplied.


## Precision audit, 15 October 2026

Earlier contours were reviewed and selected fields retraced more densely against the source. See [precision_audit.md](precision_audit.md) and [precision_audit.csv](precision_audit.csv). The prior geometry is archived; claims above that earlier field coordinates/measurements were retained describe the pre-audit baseline, not the current revised contours. Source calibration, specimen relationships and inclusion rules are unchanged. The 1990 independently measured whole-tissue masks are unchanged.
