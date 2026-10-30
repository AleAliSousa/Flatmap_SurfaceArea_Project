# 02_flag_completeness.R -- row-level flags for data that should NOT be used as a full
# surface area of a cortical region, and a usability tier for every row.
# Input : all_meas (from 01)        Output: data/02_measurements_flagged.csv
#                                           data/02_excluded_rows.csv (reasons per excluded row)
#                                           data/02_flag_counts.csv

flag_completeness <- function(d) {
  d <- d %>% mutate(
    f_no_area          = is.na(area_mm2),
    f_uncalibrated     = !is.na(area_px2) & is.na(area_mm2),
    f_status_unmeasur  = str_detect(coalesce(status, ""), regex("not_measurable|not measurable|not_yet_digitized|uncalibrated|no visible calibration", ignore_case = TRUE)),
    f_outline_row      = is_outline,
    f_extent_partial   = coalesce(extent, "") == "partial",
    f_extent_approx    = coalesce(extent, "") %in% extent_approximate_values,
    f_extent_missing   = is.na(extent) & !is.na(area_mm2),
    f_section_view     = view_type %in% section_view_types,
    f_partial_view     = view_type %in% partial_view_types,
    f_nonspecimen_view = view_type %in% nonspecimen_view_types,
    f_partial_label    = !is_outline & str_detect(coalesce(label, ""), partial_label_regex),
    f_partial_note     = str_detect(coalesce(boundary_note, ""), partial_note_regex),
    f_specimen_unident = specimen %in% unidentified_specimen_values |
                         str_detect(specimen, unidentified_specimen_regex),
    f_link_unresolved  = str_detect(coalesce(specimen_link_status, ""), "unresolved|unlinked|cross_publication"),
    f_outline_not_whole = is_outline & !coalesce(outline_scope, "none") %in% "whole_drawn_neocortex",
    f_borrowed_scale   = !is.na(scale_reference_map),
    f_repeated_view    = !is.na(repeat_of) & repeat_of != "illustrative_summary"
  )
  approx_ok <- if (isTRUE(cfg$include_approximate_complete)) d$extent %in% "approximate_complete" else FALSE
  d <- d %>% mutate(
    extent_ok = coalesce(extent, "") %in% extent_complete_values | approx_ok,
    # complete enough to represent the full surface area of the labelled region?
    complete_enough = !f_no_area & extent_ok & (!f_section_view | isTRUE(cfg$allow_section_views)) &
                      !f_nonspecimen_view & !f_partial_label & !f_partial_note & !f_outline_not_whole,
    # usable for a per-specimen average (needs an identified animal)
    use_for_specimen_mean = complete_enough & !f_specimen_unident,
    usability_tier = case_when(
      f_no_area                                   ~ "X_no_calibrated_area",
      f_nonspecimen_view                          ~ "D_not_a_specimen_view",
      !complete_enough                            ~ "C_incomplete_or_section",
      f_specimen_unident                          ~ "B_complete_unidentified_specimen",
      f_outline_row                               ~ "A_outline_complete_identified",
      TRUE                                        ~ "A_field_complete_identified"),
    exclusion_reasons = pmap_chr(
      list(f_no_area, f_uncalibrated, f_nonspecimen_view, f_extent_partial, f_extent_approx & !approx_ok,
           f_extent_missing, f_section_view & !isTRUE(cfg$allow_section_views), f_outline_not_whole,
           f_partial_label, f_partial_note, f_specimen_unident),
      function(a, b, c, d1, e, f, g, h, i, j, k) paste(c(
        if (a & !b) "no calibrated area (NA)", if (b) "pixels only; no physical calibration",
        if (c) "illustrative/composite/schematic view, not an animal",
        if (d1) "extent = partial", if (e) "extent = approximate",
        if (f) "extent not recorded", if (g) "single section/zoom view; not a full field area",
        if (h) "outline is not a whole-neocortex outline (no denominator use)",
        if (i) "label denotes a component/fragment, not the whole field",
        if (j) "boundary note states field is truncated/incomplete",
        if (k) "specimen not identified; cannot attribute to an animal"), collapse = "; ")),
    warnings = pmap_chr(list(f_link_unresolved, f_borrowed_scale, f_repeated_view, f_partial_view & complete_enough,
                             f_section_view & complete_enough),
      function(a, b, c, d1, e) paste(c(if (a) "specimen link unresolved", if (b) "calibration borrowed from another map",
                                if (c) "repeated view of tissue shown in another map",
                                if (d1) "complete field drawn within a partial view of cortex (inset/contralateral/strip)",
                                if (e) "field measured in a single section view (allow_section_views = TRUE)"), collapse = "; "))
  )
  d
}

if (sys.nframe() == 0L || isTRUE(getOption("flatmap.run_step"))) {
  if (!exists("all_meas")) all_meas <- read_csv(file.path(out_data, "01_all_measurements.csv"), show_col_types = FALSE)
  flagged <- flag_completeness(all_meas)
  write_out(flagged, "02_measurements_flagged.csv")
  write_out(flagged %>% filter(!use_for_specimen_mean) %>%
              select(paper, map_id, figure, species, specimen, label, view_type, extent, area_mm2,
                     usability_tier, exclusion_reasons, warnings, boundary_note),
            "02_excluded_rows.csv")
  counts <- flagged %>% count(usability_tier, name = "n_rows") %>% arrange(usability_tier)
  write_out(counts, "02_flag_counts.csv")
  print(as.data.frame(counts))
  print(as.data.frame(flagged %>% filter(!is.na(area_mm2)) %>% count(paper, use_for_specimen_mean) %>%
          pivot_wider(names_from = use_for_specimen_mean, values_from = n, values_fill = 0)))
}
