# Data contract

## Measurements

One row per `(map_id, label)`. Missing measurements are NA, not zero. Preserve at least:

- Source: figure, panel, one-based pdf_page, printed_page, source_roi_file.
- Identity: map_id, species, specimen, hemisphere, view_type, hemisphere_relation, linked_main_map, repeat_of, relationship_note, specimen_link_status.
- Geometry: label, extent, area_px2, area_mm2, scale_length_mm, scale_length_px, outline_scope.
- Denominators: percent_of_drawn_neocortex, percent_of_drawn_outline, include_in_whole_hemisphere_summary.
- Assessment: status, boundary_note, scale_note, scale_reference_map. Sensitivity bounds, when not calculated, are NA.

`include_in_whole_hemisphere_summary` is true only for eligible individual whole-neocortex reconstructions with an independently measured whole outline. Repeated or summary views are false. Keep sections separate unless a documented scientific analysis explicitly calls for section geometry.

Display case numbering is a convenience linked to source map IDs, not published table identity. All labels and species are paper-specific. Make aliases explicit and do not impose the 1990 visual fields on other papers.

## Canonical per-view JSON for the generic helper

Required metadata: `map_id`, `figure`, `pdf_page`, `species`, `specimen`, `view_type`, `include_in_whole_hemisphere_summary`, `outline_scope`, `render_scale`, `crop_xyxy`, `rois`. Add provenance and relationship fields whenever known.

- `render_scale`: pixels per PDF point, positive.
- `crop_xyxy`: integer `[left, top, right, bottom]` on the rendered PDF page.
- `scale_endpoints_px`: two `[x,y]` points in the crop; `[]` if unavailable.
- `scale_length_mm`: positive printed scale length, or null.
- `outline`: null, or an object with `label`, `polygons`, optional `exclude_polygons`, `boundary_note`.
- `rois`: list of objects with `label`, `polygons`, optional `exclude_polygons`, `extent`, `boundary_note`.
- `unmeasured`: list with `label`, `status` (`not_yet_digitized` or `not_measurable`) and `reason`.
- `supersample`: integer raster supersampling (default 4). Saved measurement precision differs from anatomical accuracy.
- `outline_scope`: `whole_drawn_neocortex`, `schematic_tissue`, or `none`.

A polygon is a list of at least three `[x,y]` vertices; the helper closes it. Multiple polygons form a union. Store exclusions explicitly. Do not repeat the same label in ROI and unmeasured entries. Native ImageJ selections are binary masks at >=50% coverage; CSV areas use fractional coverage.

## Summary helper

Source `scripts/summarize_flatmaps.R` to call `build_flatmap_summary(data, fields, species_order, species_headers, minimum_case_counts, field_display)`. Defaults use eligible species and field labels in file order, without fixed case counts. Explicit fields preserve all-missing columns and define the field set used for Total. When fields are discovered automatically, Total stays NA: choose an explicit, anatomically appropriate nonoverlapping field set before summing. The output list contains `table`, `case_key`, and `n` (observed case counts per species/field).

Mean and sample SD use all available values per field. Total is NA when any selected field is NA; its mean/SD use complete case totals. With no eligible maps, retain the selected species/fields when supplied and report empty/NA summaries; do not substitute section or schematic data. Additions are included when the file is reread.
