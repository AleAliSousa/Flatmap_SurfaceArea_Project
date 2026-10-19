# 03_specimen_means.R -- average the same cortical region across the different views
# (figures / panels / sections) of one specimen.
# Grouping key: paper x species x specimen x label (literal source label).
# Input : flagged (from 02)   Output: data/03_specimen_region_means.csv  (all identified specimens)
#                                     data/03_multi_view_regions.csv     (regions seen in >1 view)

specimen_region_means <- function(d) {
  cand <- d %>% filter(!is.na(area_mm2), !f_specimen_unident, !f_nonspecimen_view)
  cand %>%
    group_by(paper, species, specimen, label, is_outline) %>%
    summarise(
      n_views_calibrated  = n(),
      n_views_usable      = sum(use_for_specimen_mean),
      mean_mm2            = if (any(use_for_specimen_mean)) mean(area_mm2[use_for_specimen_mean]) else NA_real_,
      sd_mm2              = if (sum(use_for_specimen_mean) > 1) sd(area_mm2[use_for_specimen_mean]) else NA_real_,
      min_mm2             = if (any(use_for_specimen_mean)) min(area_mm2[use_for_specimen_mean]) else NA_real_,
      max_mm2             = if (any(use_for_specimen_mean)) max(area_mm2[use_for_specimen_mean]) else NA_real_,
      mean_mm2_all_views  = mean(area_mm2),            # includes partial/section views: for reference only
      max_mm2_all_views   = max(area_mm2),
      mean_px2_usable     = if (any(use_for_specimen_mean)) mean(area_px2[use_for_specimen_mean]) else NA_real_,
      mean_pct_neocortex  = if (any(use_for_specimen_mean & !is.na(percent_of_drawn_neocortex)))
                              mean(percent_of_drawn_neocortex[use_for_specimen_mean], na.rm = TRUE) else NA_real_,
      map_ids_usable      = paste_unique(map_id[use_for_specimen_mean]),
      map_ids_excluded    = paste_unique(map_id[!use_for_specimen_mean]),
      figures             = paste_unique(figure),
      view_types          = paste_unique(view_type),
      extents             = paste_unique(extent),
      hemisphere_sides    = paste_unique(hemisphere_side[use_for_specimen_mean]),
      n_hemisphere_sides  = n_distinct(hemisphere_side[use_for_specimen_mean & hemisphere_side != "unspecified"]),
      specimen_link_status = paste_unique(specimen_link_status),
      excluded_view_reasons = paste_unique(exclusion_reasons[!use_for_specimen_mean]),
      view_warnings       = paste_unique(warnings[warnings != ""]),
      .groups = "drop"
    ) %>%
    mutate(
      cv_within_specimen   = ifelse(n_views_usable > 1, sd_mm2 / mean_mm2, NA_real_),
      range_ratio          = ifelse(n_views_usable > 1, max_mm2 / min_mm2, NA_real_),
      flag_within_specimen_discordant = !is.na(cv_within_specimen) & cv_within_specimen > cfg$within_specimen_cv_warn,
      flag_mixed_hemispheres = n_hemisphere_sides > 1 |
        (str_detect(hemisphere_sides, "left") & str_detect(hemisphere_sides, "right")) |
        (str_detect(hemisphere_sides, "ipsilateral") & str_detect(hemisphere_sides, "contralateral")),
      flag_partial_views_larger = !is.na(mean_mm2) & max_mm2_all_views > 1.05 * max_mm2,  # an excluded view is bigger than every usable one
      specimen_mean_status = case_when(
        n_views_usable == 0 ~ "no usable complete view",
        flag_within_specimen_discordant ~ "usable; views disagree (check tracings)",
        TRUE ~ "usable")
    ) %>%
    arrange(species, paper, specimen, is_outline, label)
}

if (sys.nframe() == 0L || isTRUE(getOption("flatmap.run_step"))) {
  if (!exists("flagged")) flagged <- read_csv(file.path(out_data, "02_measurements_flagged.csv"), show_col_types = FALSE)
  spec_means <- specimen_region_means(flagged)
  write_out(spec_means, "03_specimen_region_means.csv")
  write_out(spec_means %>% filter(n_views_calibrated > 1), "03_multi_view_regions.csv")
  message(sprintf("%d specimen-region rows; %d with >1 calibrated view; %d with >1 usable view; %d discordant (CV > %.2f)",
                  nrow(spec_means), sum(spec_means$n_views_calibrated > 1), sum(spec_means$n_views_usable > 1),
                  sum(spec_means$flag_within_specimen_discordant, na.rm = TRUE), cfg$within_specimen_cv_warn))
}
