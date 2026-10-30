# 01_load_measurements.R -- read every paper's data/measurements.csv into one long table.
# Output: data/01_all_measurements.csv  (one row per paper x map_id x label)
if (!exists("cfg")) source(file.path(dirname(sys.frame(1)$ofile %||% "R/x"), "00_config.R"))

load_all_measurements <- function(root = measurements_root) {
  files <- list.files(root, pattern = "^measurements\\.csv$", recursive = TRUE, full.names = TRUE)
  files <- files[basename(dirname(dirname(files))) != "_backups" & !grepl("/_backups/", files)]
  stopifnot(length(files) > 0)
  read_one <- function(f) {
    d <- read_csv(f, col_types = cols(.default = col_character()), na = c("", "NA", "NaN"),
                  show_col_types = FALSE, progress = FALSE)
    d <- mutate(d, across(everything(), ~ str_trim(str_replace_all(.x, "\r", ""))))
    d$paper <- basename(dirname(dirname(f)))
    d$source_file <- sub(paste0("^", root, "/"), "", f)
    d
  }
  raw <- map_dfr(files, read_one)
  # Papers with no measured rows yet still appear in the paper ledger.
  papers <- tibble(paper = basename(dirname(dirname(files))),
                   n_rows = map_int(files, ~ nrow(read_csv(.x, col_types = cols(.default = "c"), show_col_types = FALSE))))

  d <- raw %>%
    mutate(
      # numeric fields
      across(c(area_px2, area_mm2, scale_length_mm, scale_length_px,
               percent_of_drawn_neocortex, percent_of_drawn_outline,
               sensitivity_low_mm2, sensitivity_high_mm2), num),
      pdf_page = num(pdf_page),
      include_in_whole_hemisphere_summary = as_flag(include_in_whole_hemisphere_summary),
      is_outline = if ("is_outline" %in% names(.)) as_flag(is_outline) else FALSE,
      is_outline = is_outline | label %in% outline_labels,
      # vocabulary harmonisation
      specimen_link_status = str_replace_all(tolower(specimen_link_status), " ", "_"),
      extent = case_when(extent %in% c("approx_complete", "approximate_complete") ~ "approximate_complete",
                         TRUE ~ extent),
      specimen = ifelse(is.na(specimen), "not reported", specimen),
      hemisphere = ifelse(is.na(hemisphere), "not assigned", hemisphere),
      hemisphere_side = case_when(
        str_detect(hemisphere, regex("contra", ignore_case = TRUE)) ~ "contralateral",
        str_detect(hemisphere, regex("ipsi",   ignore_case = TRUE)) ~ "ipsilateral",
        str_detect(hemisphere, regex("^left",  ignore_case = TRUE)) ~ "left",
        str_detect(hemisphere, regex("^right", ignore_case = TRUE)) ~ "right",
        TRUE ~ "unspecified"),
      mm_per_px = scale_length_mm / scale_length_px,
      row_id = paste(paper, map_id, label, sep = "::")
    ) %>%
    relocate(paper, map_id, figure, panel, species, specimen, hemisphere, hemisphere_side,
             view_type, extent, label, is_outline, area_mm2, area_px2)

  dup <- d %>% count(paper, map_id, label) %>% filter(n > 1)
  if (nrow(dup)) warning("Duplicate (paper, map_id, label) rows: ", nrow(dup),
                         " -- see data/01_duplicate_keys.csv")
  attr(d, "papers") <- papers
  attr(d, "duplicates") <- dup
  d
}

if (sys.nframe() == 0L || isTRUE(getOption("flatmap.run_step"))) {
  all_meas <- load_all_measurements()
  write_out(all_meas, "01_all_measurements.csv")
  write_out(attr(all_meas, "papers"), "01_paper_ledger.csv")
  if (nrow(attr(all_meas, "duplicates"))) write_out(attr(all_meas, "duplicates"), "01_duplicate_keys.csv")
  message(sprintf("%d papers, %d rows, %d rows with calibrated area_mm2, %d distinct species",
                  n_distinct(all_meas$paper), nrow(all_meas), sum(!is.na(all_meas$area_mm2)),
                  n_distinct(all_meas$species)))
}
