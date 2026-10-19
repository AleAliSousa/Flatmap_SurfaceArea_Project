# 05_species_summary.R -- species x region summary tables, figures and a markdown report.
# Input : spec_flagged (04), flagged (02)
# Output: data/05_species_region_summary.csv       (literal labels, recommended specimen means only)
#         data/05_species_regiongroup_summary.csv  (alias groups from reference/label_crosswalk.csv)
#         figures/species_region_dotplot_<species>.png, figures/regiongroup_across_species.png
#         reports/analysis_report.md

summarise_species <- function(sf, by = c("species", "label")) {
  sf %>% filter(recommend_use, !is_outline) %>%
    group_by(across(all_of(by))) %>%
    summarise(n_specimens = n_distinct(paste(paper, specimen)), n_papers = n_distinct(paper),
              mean_mm2 = mean(mean_mm2), sd_mm2 = if (n() > 1) sd(mean_mm2) else NA_real_,
              median_mm2 = median(mean_mm2), min_mm2 = min(mean_mm2), max_mm2 = max(mean_mm2),
              mean_fraction_of_neocortex = if (any(!is.na(fraction_of_neocortex))) mean(fraction_of_neocortex, na.rm = TRUE) else NA_real_,
              papers = paste_unique(paper), n_flagged_excluded = NA_integer_, .groups = "drop")
}

plot_species <- function(sf, sp) {
  dd <- sf %>% filter(species == sp, !is_outline, !is.na(mean_mm2)) %>%
    mutate(label = fct_reorder(label, mean_mm2, median), plausibility = factor(plausibility,
      levels = c("plausible", "usable with caution", "FLAG: implausible for species/region")))
  if (!nrow(dd)) return(invisible(NULL))
  p <- ggplot(dd, aes(x = mean_mm2, y = label, colour = plausibility, shape = paper)) +
    geom_point(size = 2.4, alpha = 0.85, position = position_jitter(height = 0.15, width = 0, seed = 1)) +
    scale_x_log10() +
    scale_colour_manual(values = c("plausible" = "grey30", "usable with caution" = "#E69F00",
                                   "FLAG: implausible for species/region" = "#D55E00"), drop = FALSE) +
    labs(title = sp, subtitle = "Per-specimen mean surface area of each labelled region (log scale)",
         x = expression(Area~(mm^2)), y = NULL, colour = NULL, shape = NULL) +
    theme_minimal(base_size = 11) + theme(legend.position = "bottom", legend.box = "vertical")
  f <- file.path(out_fig, paste0("species_region_dotplot_", gsub("[^A-Za-z0-9]+", "_", sp), ".png"))
  ggsave(f, p, width = 8, height = max(3.5, 0.28 * n_distinct(dd$label) + 2.5), dpi = 150, bg = "white")
  invisible(f)
}

if (sys.nframe() == 0L || isTRUE(getOption("flatmap.run_step"))) {
  if (!exists("flagged"))      flagged      <- read_csv(file.path(out_data, "02_measurements_flagged.csv"), show_col_types = FALSE)
  if (!exists("spec_flagged")) spec_flagged <- read_csv(file.path(out_data, "04_specimen_region_means_flagged.csv"), show_col_types = FALSE)
  library(forcats)
  sp_lab <- summarise_species(spec_flagged, c("species", "label"))
  sp_grp <- summarise_species(spec_flagged, c("species", "region_group"))
  excl_counts <- spec_flagged %>% filter(!is_outline, !is.na(mean_mm2), !recommend_use) %>% count(species, label, name = "n_flagged_excluded")
  sp_lab <- sp_lab %>% select(-n_flagged_excluded) %>% left_join(excl_counts, by = c("species", "label")) %>%
    mutate(n_flagged_excluded = coalesce(n_flagged_excluded, 0L)) %>% arrange(species, desc(n_specimens))
  write_out(sp_lab, "05_species_region_summary.csv")
  write_out(sp_grp %>% select(-n_flagged_excluded) %>% arrange(region_group, species), "05_species_regiongroup_summary.csv")

  # figures
  species_with_data <- spec_flagged %>% filter(!is_outline, !is.na(mean_mm2)) %>% count(species) %>% filter(n >= 3) %>% pull(species)
  figs <- map_chr(species_with_data, ~ plot_species(spec_flagged, .x) %||% NA_character_)
  grp <- spec_flagged %>% filter(!is_outline, !is.na(mean_mm2)) %>% add_count(region_group) %>% filter(n >= 6)
  if (nrow(grp)) {
    p <- ggplot(grp, aes(x = species, y = mean_mm2, colour = plausibility)) +
      geom_point(alpha = 0.8, position = position_jitter(width = 0.15, height = 0, seed = 1)) +
      facet_wrap(~ region_group, scales = "free_y") + scale_y_log10() +
      scale_colour_manual(values = c("plausible" = "grey30", "usable with caution" = "#E69F00",
                                     "FLAG: implausible for species/region" = "#D55E00")) +
      labs(x = NULL, y = expression(Specimen~mean~area~(mm^2)), colour = NULL,
           title = "Region groups with >= 6 specimen means, across species") +
      theme_minimal(base_size = 10) + theme(axis.text.x = element_text(angle = 60, hjust = 1), legend.position = "bottom")
    ggsave(file.path(out_fig, "regiongroup_across_species.png"), p, width = 12, height = 9, dpi = 150, bg = "white")
  }

  # report
  tier <- flagged %>% count(usability_tier)
  hard <- spec_flagged %>% filter(hard_flags != "") %>%
    select(species, paper, specimen, label, mean_mm2, n_views_usable, robust_z, fraction_of_neocortex, hard_flags) %>%
    mutate(across(where(is.numeric), ~ signif(.x, 4)))
  disc <- spec_flagged %>% filter(flag_within_specimen_discordant) %>%
    select(species, paper, specimen, label, n_views_usable, mean_mm2, min_mm2, max_mm2, cv_within_specimen, map_ids_usable) %>%
    mutate(across(where(is.numeric), ~ signif(.x, 4)))
  md_table <- function(df) {
    if (!nrow(df)) return("_none_")
    hdr <- paste0("| ", paste(names(df), collapse = " | "), " |")
    sep <- paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|")
    rows <- apply(df, 1, function(r) paste0("| ", paste(ifelse(is.na(r), "", r), collapse = " | "), " |"))
    paste(c(hdr, sep, rows), collapse = "\n")
  }
  rep <- c(
    "# Flatmap surface-area analysis report", "",
    sprintf("Generated %s from `flatmap_measurements/*/data/measurements.csv`.", format(Sys.time(), "%Y-%m-%d %H:%M")), "",
    "## Input coverage", "",
    sprintf("- %d paper folders read (%d with measurement rows); %d measurement rows; %d rows with calibrated area (mm2); %d species.",
            nrow(read_csv(file.path(out_data, "01_paper_ledger.csv"), show_col_types = FALSE)), n_distinct(flagged$paper),
            nrow(flagged), sum(!is.na(flagged$area_mm2)), n_distinct(flagged$species)), "",
    "## Row-level usability tiers (data/02_flag_counts.csv)", "", md_table(tier), "",
    "Only tier `A_*` rows enter per-specimen averages. `C_incomplete_or_section` rows are partial extents, approximate borders, single sections/zooms, insets or component labels: they do not give the full surface area of the region. `D_not_a_specimen_view` rows are illustrative, composite or schematic drawings. `B_*` rows are complete but cannot be attributed to an identified animal.", "",
    "## Per-specimen averages (data/03_specimen_region_means.csv)", "",
    sprintf("- %d specimen x region combinations; %d measured in more than one view; %d averaged over >1 usable view; %d where usable views disagree by CV > %.2f.",
            nrow(spec_flagged), sum(spec_flagged$n_views_calibrated > 1), sum(spec_flagged$n_views_usable > 1),
            sum(spec_flagged$flag_within_specimen_discordant, na.rm = TRUE), cfg$within_specimen_cv_warn), "",
    "### Specimens whose repeated views disagree", "", md_table(disc), "",
    "## Plausibility given species and region (data/04_specimen_region_means_flagged.csv)", "",
    md_table(count(spec_flagged, plausibility)), "",
    "### Specimens whose regions deviate together (suspected scale/calibration offset)", "",
    md_table(spec_flagged %>% filter(flag_specimen_scale_offset) %>%
               distinct(species, paper, specimen, n_regions_compared, specimen_median_z, specimen_median_ratio) %>%
               mutate(across(where(is.numeric), ~ signif(.x, 3)))), "",
    "### Hard flags (recommend_use = FALSE)", "", md_table(hard), "",
    "Checks: robust z on log10 area within species x region_group (>= 3 specimens; aliases in `reference/label_crosswalk.csv`); fraction of the specimen's own neocortex outline (else species reference, else species median outline) against bounds in `reference/region_fraction_bounds.csv` or the generic defaults in `R/00_config.R`; and unusual mm/pixel calibration in a contributing view.", "",
    "## Species x region summary (data/05_species_region_summary.csv)", "",
    md_table(sp_lab %>% filter(n_specimens >= 2) %>% mutate(across(where(is.numeric), ~ signif(.x, 4))) %>%
               select(species, label, n_specimens, n_papers, mean_mm2, sd_mm2, min_mm2, max_mm2, n_flagged_excluded)), "",
    "## Figures", "", paste0("- figures/", basename(na.omit(figs)), collapse = "\n"),
    if (nrow(grp)) "- figures/regiongroup_across_species.png" else NULL
  )
  writeLines(rep, file.path(out_rep, "analysis_report.md"))
  message("wrote ", file.path(out_rep, "analysis_report.md"))
}
