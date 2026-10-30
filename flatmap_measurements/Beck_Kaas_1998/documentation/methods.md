<!-- full-dataset-recheck -->
## 16 October 2026 source recheck

The [full-dataset recheck note](full_dataset_recheck.md) and current canonical JSON/CSV supersede earlier contour counts or blanket exclusions of repeated/illustrative maps. [Review all source pages](../review/full_dataset_audit.html). Prior geometry is archived.

# Beck & Kaas (1998): cortical surface assessment

The first unstarted entry in the project queue was assessed across all 14 numbered figures. This is a cortical surface dataset: thalamic/pulvinar coronal nuclear cross-sections are excluded. Figures 3,4,6,7,9–12 have cortical injection-site insets. Five supported DM envelopes/fragments are traced; the other insets retain calibrated source crops with explicit NA fields. Figure 1 is a projected locator and Figure 14 is a connection summary.

The source methods (PDF p.3) identify DM by myeloarchitecture in manually flattened cortex. These insets remain restricted cortical views with uncertain whole-field extent; they are not whole-neocortex reconstructions. DM in Figure 3 has a supported closed envelope. Figures 9–12 retain only the visible DM fragment, flagged partial, because frame contact/cropping prevents a full-extent claim. The source explicitly says the V2 border was most obvious and other DM borders less certain: published boundary estimates remain provisional. The large injections in Figures 4/6/7 hide or replace substantial border intervals; an injection outline is never substituted for an anatomical field.

Case/species labels: galagos95-34 and95-09 are Galago garnetti as reported in the1998methods (do not copy the Galago senegalensis label from the1993paper). Owl cases94-3 and93-36 are Aotus trivirgatus; squirrel cases94-71 and95-01 are Saimiri sciureus. Macaque cases95-74 and96-09 remain Macaca sp.: methods include three M.nemestrina and one M.fascicularis (source spelling fasicularis), without establishing species per illustrated case. No modern taxonomic reassignment or cross-paper pooling is performed. Methods report reuse of three owl brains from Krubitzer & Kaas1993; cross-publication independence remains unresolved.

Every inset has its own printed physical scale. The separate2 mm or1 mm bars beside thalamic sections were not used to calibrate cortical insets. All inset calibration is recorded directly from the4 mm/2 mm stroke printed within that inset.

## Geometry and verification

The original PDF and SHA-256 are retained in `source/`. Source pages are now rendered at 4 pixels per PDF point without stretching. Canonical `figures/<map_id>/rois.json` records the one-based PDF page, crop rectangle in rendered-page coordinates, specimen, physical scale stroke endpoints, printed length, labels, polygons, extent and missing-field reasons. Coordinates are local to the crop, origin upper left. New manual tracings are provisional pending anatomical review.

Outer envelopes follow visible anatomical boundaries, not the sum of named fields or the individual hatch/stipple/tracer patches. Selected closed contours were initialized by pixel flood filling (grayscale<170; the fine gray Beck outlines use<235) and simplified with0.8 pixel tolerance, then visually inspected. Escaped selections, connected tracer/probe marks and internal subdivisions were checked against source images and manually corrected. Interior text, lesions and deposits remain part of the anatomical envelope. Short interpolations are recorded per ROI; open fields without a defensible closure remain NA. Pixel coordinates are the canonical tracing input; rebuilding does not re-segment boundaries.

Fourfold raster supersampling estimates fractional coverage. Area in mm² is `area_px2*(scale_length_mm/scale_length_px)^2`. Binary native ImageJ selections use>=50%coverage and can differ slightly from fractional CSV areas. The native exporter reads back TIFF calibration, overlay/ROI ZIP selections and named mask-stack pixels and checks equality. Area equations, missing values, crop and polygon bounds and intersections are verified; field-overlap diagnostics are retained. `review/gallery.html` pairs source images with saved traces. No shrinkage correction, perturbation confidence interval or anatomical certification is implied. External reference comparison was not requested.

No view is certified as complete neocortex in this dataset. `percent_of_drawn_neocortex` and whole-hemisphere statistics therefore remain unavailable. For Figures 6/7 of Huffman, percent of the drawn tissue outline is a local geometry ratio only. It is not percent of complete neocortex. Fields, drawn tissue, body subregions and partial fragments must not be added as a disjoint partition.


## Line refinement, 2026-10-15

The initial contours were too coarse and in places followed symbols or cut across curves. They have been superseded by the denser source-reviewed contours described in [line_refinement.md](line_refinement.md). Rendering resolution doubled; crop and scale-bar coordinates doubled together, preserving physical calibration. Current canonical ROI definitions determine all reported areas and ImageJ exports.
