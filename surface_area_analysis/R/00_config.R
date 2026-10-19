# 00_config.R -- paths, vocabularies and thresholds shared by every script.
# Source this first. All other scripts assume the objects defined here exist.
suppressPackageStartupMessages({
  library(dplyr); library(readr); library(tidyr); library(stringr)
  library(purrr); library(ggplot2)
})

# ---- locate the analysis folder relative to this file -------------------------
locate_analysis_dir <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  f <- sub("^--file=", "", args[grepl("^--file=", args)])
  if (length(f)) return(normalizePath(file.path(dirname(f[1]), "..")))
  if (!is.null(sys.frames()) && length(sys.frames()) > 0) {
    of <- tryCatch(sys.frame(1)$ofile, error = function(e) NULL)
    if (!is.null(of)) return(normalizePath(file.path(dirname(of), "..")))
  }
  wd <- normalizePath(getwd())
  if (basename(wd) == "R") return(dirname(wd))
  wd
}
analysis_dir      <- locate_analysis_dir()
project_root      <- normalizePath(file.path(analysis_dir, ".."))
measurements_root <- file.path(project_root, "flatmap_measurements")
reference_dir     <- file.path(analysis_dir, "reference")
out_data          <- file.path(analysis_dir, "data")
out_fig           <- file.path(analysis_dir, "figures")
out_rep           <- file.path(analysis_dir, "reports")
for (d in c(out_data, out_fig, out_rep)) dir.create(d, showWarnings = FALSE, recursive = TRUE)

# ---- thresholds (edit here, not in the scripts) --------------------------------
cfg <- list(
  # treat "approximate_complete" extents as complete enough for specimen means?
  include_approximate_complete = FALSE,
  # within-specimen agreement: CV of the same region across views above this is flagged
  within_specimen_cv_warn      = 0.25,
  # robust z (median/MAD on log10 area) within species x region_group
  robust_z_outlier             = 3.0,
  robust_z_borderline          = 2.5,
  min_n_for_comparison         = 3L,
  # generic bounds for any single named field as a fraction of neocortex area
  generic_min_fraction         = 0.0005,
  generic_max_fraction         = 0.40,
  # a hard outlier additionally needs at least this fold departure from the group median
  min_fold_for_outlier         = 2.0,
  # specimen-level scale offset: >= this many regions and |median robust z| above this
  specimen_offset_min_regions  = 3L,
  specimen_offset_median_z     = 2.0,
  # scale factor (mm per rendered pixel) robust z across all calibrated views
  scale_factor_z               = 3.0,
  # histological/tangential section views: the data contract keeps sections separate
  allow_section_views          = FALSE
)

# ---- controlled vocabularies -----------------------------------------------------
# View types where one view is a histological/tangential section, zoom or detail:
# a single section does not establish the full area of a field.
section_view_types <- c(
  "histological_section", "tangential_section", "tangential_section_detail",
  "repeated_laminar_reconstruction", "section_zoom_reconstruction",
  "semi_flattened_callosal_section", "histological_detail", "histological_zoom",
  "review_histological_panel"
)
# View types that are not measurements of an individual animal.
nonspecimen_view_types <- c(
  "illustrative_summary_flatmap", "species_summary", "literature_summary",
  "composite_parcellation", "unscaled_schematic", "redrawn_historical_map",
  "redrawn_case_map", "cortical_map_geometry"
)
# View types that show only part of the cortex. A field drawn *within* such a view can
# still be complete: the per-field `extent` and `boundary_note` decide; the view type only
# raises a warning.
partial_view_types <- c(
  "contralateral_partial", "contralateral_zoom", "partial_areal_strip",
  "partial_reconstruction", "partial_case_reconstruction", "cortical_inset",
  "physiological_inset"
)
outline_labels <- c("Neocortex outline", "Drawn tissue outline", "Drawn schematic outline")
unidentified_specimen_values <- c("", "not reported", "illustrative summary",
                                  "not applicable", "unknown", "NA")
unidentified_specimen_regex <- regex("atlas carrier|composite|summary|not reported",
                                     ignore_case = TRUE)
partial_label_regex <- regex(
  "component|fragment|mapped extent|visible|island|partial|historical|strip|\\?",
  ignore_case = TRUE)
partial_note_regex <- regex(
  "not a complete field|not total|partial extent|truncat|not a whole-field|incomplete|open or missing|not an additional animal measurement|not a complete|not a whole",
  ignore_case = TRUE)
extent_complete_values    <- "complete"
extent_approximate_values <- c("approximate_complete", "approx_complete", "approximate")

# ---- small helpers -----------------------------------------------------------------
as_flag <- function(x) tolower(trimws(as.character(x))) %in% c("true", "t", "1")
num     <- function(x) suppressWarnings(as.numeric(x))
`%||%`  <- function(a, b) if (is.null(a)) b else a
paste_unique <- function(x, sep = "|") paste(sort(unique(na.omit(as.character(x)))), collapse = sep)
write_out <- function(df, name) {
  p <- file.path(out_data, name); write_csv(df, p, na = "NA"); message("wrote ", p, "  (", nrow(df), " rows)"); invisible(p)
}
