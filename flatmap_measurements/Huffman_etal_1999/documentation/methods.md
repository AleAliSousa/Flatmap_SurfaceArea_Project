<!-- full-dataset-recheck -->
## 16 October 2026 source recheck

The [full-dataset recheck note](full_dataset_recheck.md) and current canonical JSON/CSV supersede earlier contour counts or blanket exclusions of repeated/illustrative maps. [Review all source pages](../review/full_dataset_audit.html). Prior geometry is archived.

# Huffman etal(1999): cortical surface assessment

All 16 numbered figures were inspected. The main case reconstructions are Figures 2–7, with two panels for Figure 4. They identify NQ3,NQ5,NQ1,NQ2 (Dasyurus hallucatus), SP1 (Dactylopsila trivirgata), and StO1/StO2 (Monodelphis domestica). Figure 13 histological photographs also include Sminthopsis crassicaudata, but no complete field was digitized from diffuse stain alone. All species are source labels.

Visible closed C and SII/PV envelopes in the quolls, the compound SII/PV envelope and A in the striped possum, and VI/SI/A/SI?/CT in the short-tailed opossums were assessed individually. The compound SII/PV in quolls is not split without a drawn divider. The literal labelSI? retains the source uncertainty and is not silently merged with SI. In Figures 2/3/5, totalSI andR lack a closed medial edge in the available drawing; neither a recording-site hull nor a long invented closure is used. Figure 4 forepaw islands have closed mapped boundaries, so they are measured as partial SI subregions. They do not supply complete SI areas.

Figure 4 has one printed1 mm bar at the foot of panelB. The caption supplies the shared scale for the figure. PanelA uses this explicit shared-figure calibration (same rendering, no resizing), with `scale_reference_map=fig04B`; it is not calibrated from a different specimen's independent figure. All other maps use their own printed1 mm scale strokes.

Figures 8–12 repeat the same identified cortical cases (NQ3,NQ5,SP1) with receptive-field progressions and peripheral paw/body drawings. Their cortical geometry is linked to the main maps in the inventory, not counted as additional animals or remeasured independent cases. Figure 13 stains do not provide closed architectonic field envelopes. Figures 14–16 are comparative/derived summary illustrations (including outside publications), excluded as additional specimen data. No cross-paper pooling or comparison to the paper's Table2 values was performed.

Figures 6/7 show a large extent of cortex together with CT and basal darkly myelinated tissue. Their independently traced tissue outline is recorded for review, but the caption and tissue limits do not certify a whole-neocortex denominator.

## Geometry and verification

The original PDF and SHA-256 are retained in `source/`. Source pages are now rendered at 4 pixels per PDF point without stretching. Canonical `figures/<map_id>/rois.json` records the one-based PDF page, crop rectangle in rendered-page coordinates, specimen, physical scale stroke endpoints, printed length, labels, polygons, extent and missing-field reasons. Coordinates are local to the crop, origin upper left. New manual tracings are provisional pending anatomical review.

Outer envelopes follow visible anatomical boundaries, not the sum of named fields or the individual hatch/stipple/tracer patches. Selected closed contours were initialized by pixel flood filling (grayscale<170; the fine gray Beck outlines use<235) and simplified with0.8 pixel tolerance, then visually inspected. For opossum SI in Figures 6/7, interior compartments were unioned and a5x5 morphological closing joined the thin internal dividers before saving the external contour (maximum2 pixel smoothing). This retains orbital/digit compartments within SI. Escaped selections, connected tracer/probe marks and internal subdivisions were checked against source images and manually corrected. Interior text, lesions and deposits remain part of the anatomical envelope. Short interpolations are recorded per ROI; open fields without a defensible closure remain NA. Pixel coordinates are the canonical tracing input; rebuilding does not re-segment boundaries.

Fourfold raster supersampling estimates fractional coverage. Area in mm² is `area_px2*(scale_length_mm/scale_length_px)^2`. Binary native ImageJ selections use>=50%coverage and can differ slightly from fractional CSV areas. The native exporter reads back TIFF calibration, overlay/ROI ZIP selections and named mask-stack pixels and checks equality. Area equations, missing values, crop and polygon bounds and intersections are verified; field-overlap diagnostics are retained. `review/gallery.html` pairs source images with saved traces. No shrinkage correction, perturbation confidence interval or anatomical certification is implied. External reference comparison was not requested.

No view is certified as complete neocortex in this dataset. `percent_of_drawn_neocortex` and whole-hemisphere statistics therefore remain unavailable. For Figures 6/7 of Huffman, percent of the drawn tissue outline is a local geometry ratio only. It is not percent of complete neocortex. Fields, drawn tissue, body subregions and partial fragments must not be added as a disjoint partition.


## Line refinement, 2026-10-15

The initial contours were too coarse and in places followed symbols or cut across curves. They have been superseded by the denser source-reviewed contours described in [line_refinement.md](line_refinement.md). Rendering resolution doubled; crop and scale-bar coordinates doubled together, preserving physical calibration. Current canonical ROI definitions determine all reported areas and ImageJ exports.

Figure 5 correction: although the caption distinguishes SII and PV, the internal line does not close against the outer border. The previously inferred closures were withdrawn. Individual SII and PV areas are NA; only their combined external envelope is measured.
