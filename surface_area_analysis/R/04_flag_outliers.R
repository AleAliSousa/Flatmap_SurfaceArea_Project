# 04_flag_outliers.R -- flag specimen-region means that fall outside what is reasonable
# given the species and the region.  Three independent checks:
#   (1) robust z-score (median/MAD of log10 area) within species x region_group, across
#       specimens and papers;  needs >= cfg$min_n_for_comparison specimens.
#   (2) fraction of neocortex: region mean / neocortex area of the same specimen (own outline),
#       else the species reference (reference/species_neocortex_reference.csv), else the
#       species median outline measured in this dataset.  Compared against generic bounds and
#       any region-specific bounds in reference/region_fraction_bounds.csv.
#   (3) unusual calibration (mm per pixel) at the view level, propagated to the specimen mean.
# Input : spec_means (03), flagged (02)
# Output: data/04_specimen_region_means_flagged.csv, data/04_plausibility_flags_long.csv,
#         data/04_species_neocortex_from_data.csv, data/04_view_scale_factor_check.csv

read_ref <- function(name) {
  p <- file.path(reference_dir, name)
  if (file.exists(p)) read_csv(p, show_col_types = FALSE, col_types = cols(.default = "c")) else NULL
}

flag_outliers <- function(sm, d) {
  # ---- region groups (explicit aliases only; unmapped labels stay literal) ------------
  xw <- read_ref("label_crosswalk.csv")
  sm <- sm %>% mutate(region_group = label)
  if (!is.null(xw)) {
    xw <- xw %>% select(label, region_group_xw = region_group) %>% distinct(label, .keep_all = TRUE)
    sm <- sm %>% left_join(xw, by = "label") %>%
      mutate(region_group = coalesce(region_group_xw, label)) %>% select(-region_group_xw)
  }

  # ---- neocortex denominators -----------------------------------------------------------
  own_outline <- sm %>% filter(is_outline, !is.na(mean_mm2)) %>%
    group_by(paper, species, specimen) %>% summarise(own_neocortex_mm2 = mean(mean_mm2), .groups = "drop")
  species_from_data <- own_outline %>% group_by(species) %>%
    summarise(n_specimens_with_outline = n(), species_median_neocortex_mm2 = median(own_neocortex_mm2),
              species_min = min(own_neocortex_mm2), species_max = max(own_neocortex_mm2), .groups = "drop")
  ref <- read_ref("species_neocortex_reference.csv")
  if (!is.null(ref)) ref <- ref %>% transmute(species, neocortex_mm2_reference = num(neocortex_mm2_reference),
                                              reference_source = source)
  bounds <- read_ref("region_fraction_bounds.csv")
  if (!is.null(bounds)) bounds <- bounds %>% transmute(region_group, min_fraction = num(min_fraction_of_neocortex),
                                                       max_fraction = num(max_fraction_of_neocortex))

  sm <- sm %>%
    left_join(own_outline, by = c("paper", "species", "specimen")) %>%
    left_join(species_from_data %>% select(species, species_median_neocortex_mm2), by = "species")
  if (!is.null(ref)) sm <- sm %>% left_join(ref, by = "species") else
    sm <- sm %>% mutate(neocortex_mm2_reference = NA_real_, reference_source = NA_character_)
  sm <- sm %>% mutate(
    neocortex_denominator_mm2 = coalesce(own_neocortex_mm2, neocortex_mm2_reference, species_median_neocortex_mm2),
    denominator_source = case_when(!is.na(own_neocortex_mm2) ~ "own specimen outline",
                                   !is.na(neocortex_mm2_reference) ~ "species reference file",
                                   !is.na(species_median_neocortex_mm2) ~ "species median outline in dataset",
                                   TRUE ~ "none"),
    fraction_of_neocortex = ifelse(is_outline, NA_real_, mean_mm2 / neocortex_denominator_mm2)
  )
  if (!is.null(bounds)) sm <- sm %>% left_join(bounds, by = "region_group") else
    sm <- sm %>% mutate(min_fraction = NA_real_, max_fraction = NA_real_)
  sm <- sm %>% mutate(min_fraction = coalesce(min_fraction, cfg$generic_min_fraction),
                      max_fraction = coalesce(max_fraction, cfg$generic_max_fraction))

  # ---- robust z within species x region_group -------------------------------------------
  comp <- sm %>% filter(!is.na(mean_mm2)) %>%
    group_by(species, region_group) %>%
    mutate(n_compare = n(), n_papers_compare = n_distinct(paper),
           log_a = log10(mean_mm2),
           med_log = median(log_a), mad_log = mad(log_a, constant = 1.4826),
           robust_z = ifelse(n_compare >= cfg$min_n_for_comparison & mad_log > 0, (log_a - med_log) / mad_log, NA_real_),
           group_median_mm2 = 10^med_log,
           ratio_to_group_median = mean_mm2 / group_median_mm2) %>%
    ungroup() %>% select(paper, species, specimen, label, is_outline, n_compare, n_papers_compare,
                         robust_z, group_median_mm2, ratio_to_group_median)
  sm <- sm %>% left_join(comp, by = c("paper", "species", "specimen", "label", "is_outline"))

  # ---- scale-factor check at view level --------------------------------------------------
  vs <- d %>% filter(!is.na(mm_per_px), !is.na(area_mm2)) %>% distinct(paper, map_id, mm_per_px) %>%
    mutate(log_s = log10(mm_per_px), z_scale = (log_s - median(log_s)) / mad(log_s, constant = 1.4826),
           flag_unusual_scale = abs(z_scale) > cfg$scale_factor_z)
  scale_by_specimen <- d %>% filter(use_for_specimen_mean) %>% select(paper, map_id, species, specimen, label) %>%
    inner_join(vs, by = c("paper", "map_id")) %>%
    group_by(paper, species, specimen, label) %>%
    summarise(flag_unusual_scale_factor = any(flag_unusual_scale),
              mm_per_px_views = paste(signif(unique(mm_per_px), 3), collapse = "|"), .groups = "drop")
  sm <- sm %>% left_join(scale_by_specimen, by = c("paper", "species", "specimen", "label")) %>%
    mutate(flag_unusual_scale_factor = coalesce(flag_unusual_scale_factor, FALSE))

  # ---- specimen-level scale offset: do most regions of one specimen deviate together? ----
  offs <- sm %>% filter(!is.na(robust_z)) %>% group_by(paper, species, specimen) %>%
    summarise(n_regions_compared = n(), specimen_median_z = median(robust_z),
              specimen_median_ratio = median(ratio_to_group_median),
              share_same_sign = max(mean(robust_z > 0), mean(robust_z < 0)), .groups = "drop") %>%
    mutate(flag_specimen_scale_offset = n_regions_compared >= cfg$specimen_offset_min_regions &
             abs(specimen_median_z) > cfg$specimen_offset_median_z & share_same_sign >= 0.75)
  sm <- sm %>% left_join(offs, by = c("paper", "species", "specimen")) %>%
    mutate(flag_specimen_scale_offset = coalesce(flag_specimen_scale_offset, FALSE))

  # ---- assemble flags ---------------------------------------------------------------------
  fold_ok <- function(r) !is.na(r) & (r >= cfg$min_fold_for_outlier | r <= 1 / cfg$min_fold_for_outlier)
  sm %>% mutate(
    flag_outlier_species_region    = !is.na(robust_z) & abs(robust_z) > cfg$robust_z_outlier & fold_ok(ratio_to_group_median),
    flag_borderline_species_region = !is.na(robust_z) & abs(robust_z) > cfg$robust_z_borderline & !flag_outlier_species_region,
    flag_insufficient_comparison   = !is.na(mean_mm2) & (is.na(n_compare) | n_compare < cfg$min_n_for_comparison),
    flag_exceeds_neocortex         = !is.na(fraction_of_neocortex) & fraction_of_neocortex > 1,
    flag_fraction_above_max        = !is.na(fraction_of_neocortex) & fraction_of_neocortex > max_fraction & !flag_exceeds_neocortex,
    flag_fraction_below_min        = !is.na(fraction_of_neocortex) & fraction_of_neocortex < min_fraction,
    flag_no_denominator            = !is_outline & !is.na(mean_mm2) & denominator_source == "none",
    hard_flags = pmap_chr(list(flag_outlier_species_region, flag_exceeds_neocortex, flag_fraction_above_max,
                               flag_fraction_below_min, flag_unusual_scale_factor, flag_specimen_scale_offset),
      function(a, b, c, d1, e, f) paste(c(
        if (a) sprintf("robust z beyond %.1f and >= %.1f-fold from species x region median", cfg$robust_z_outlier, cfg$min_fold_for_outlier),
        if (f) "all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual)",
        if (b) "region larger than the neocortex denominator",
        if (c) "fraction of neocortex above the maximum bound",
        if (d1) "fraction of neocortex below the minimum bound",
        if (e) "unusual mm/pixel calibration in a contributing view"), collapse = "; ")),
    soft_flags = pmap_chr(list(flag_borderline_species_region, flag_within_specimen_discordant, flag_mixed_hemispheres,
                               flag_partial_views_larger, flag_insufficient_comparison, flag_no_denominator,
                               view_warnings != ""),
      function(a, b, c, d1, e, f, g) paste(c(
        if (a) "borderline within species x region", if (b) "views of the same specimen disagree",
        if (c) "views from different hemispheres averaged", if (d1) "an excluded (partial/section) view is larger than the usable mean",
        if (e) "too few comparable specimens for a species-region check", if (f) "no neocortex denominator for this species",
        if (g) "view-level warnings (see view_warnings)"), collapse = "; ")),
    plausibility = case_when(is.na(mean_mm2) ~ "no usable value",
                             hard_flags != "" ~ "FLAG: implausible for species/region",
                             soft_flags != "" ~ "usable with caution",
                             TRUE ~ "plausible"),
    recommend_use = !is.na(mean_mm2) & hard_flags == ""
  ) %>% relocate(plausibility, recommend_use, hard_flags, soft_flags, .after = mean_mm2)
}

if (sys.nframe() == 0L || isTRUE(getOption("flatmap.run_step"))) {
  if (!exists("flagged"))    flagged    <- read_csv(file.path(out_data, "02_measurements_flagged.csv"), show_col_types = FALSE)
  if (!exists("spec_means")) spec_means <- read_csv(file.path(out_data, "03_specimen_region_means.csv"), show_col_types = FALSE)
  spec_flagged <- flag_outliers(spec_means, flagged)
  write_out(spec_flagged, "04_specimen_region_means_flagged.csv")
  long <- spec_flagged %>% select(paper, species, specimen, label, region_group, mean_mm2, starts_with("flag_")) %>%
    pivot_longer(starts_with("flag_"), names_to = "flag", values_to = "raised") %>% filter(raised) %>% select(-raised)
  write_out(long, "04_plausibility_flags_long.csv")
  own <- spec_flagged %>% filter(is_outline, !is.na(mean_mm2)) %>% group_by(species) %>%
    summarise(n_specimens_with_outline = n(), median_neocortex_mm2 = median(mean_mm2),
              min_mm2 = min(mean_mm2), max_mm2 = max(mean_mm2), papers = paste_unique(paper), .groups = "drop")
  write_out(own, "04_species_neocortex_from_data.csv")
  vs <- flagged %>% filter(!is.na(mm_per_px), !is.na(area_mm2)) %>% distinct(paper, map_id, species, specimen, mm_per_px, scale_length_mm, scale_length_px) %>%
    mutate(log_s = log10(mm_per_px), z_scale = (log_s - median(log_s)) / mad(log_s, constant = 1.4826)) %>% arrange(desc(abs(z_scale)))
  write_out(vs, "04_view_scale_factor_check.csv")
  offsets <- spec_flagged %>% filter(flag_specimen_scale_offset) %>%
    distinct(paper, species, specimen, n_regions_compared, specimen_median_z, specimen_median_ratio, share_same_sign)
  write_out(offsets, "04_specimen_scale_offsets.csv")
  print(as.data.frame(count(spec_flagged, plausibility)))
  print(as.data.frame(count(long, flag), row.names = FALSE))
}
