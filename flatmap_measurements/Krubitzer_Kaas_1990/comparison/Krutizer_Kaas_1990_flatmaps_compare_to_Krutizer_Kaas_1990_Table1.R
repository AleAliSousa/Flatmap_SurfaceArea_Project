# Krubitzer & Kaas (1990) flatmap digitizations: updated Table 1, internal
# consistency of measurements.csv, and comparison with the printed Table 1.
#
# Krubitzer LA & Kaas JH (1990) Cortical connections of MT in four species of
# primates: areal, modular, and retinotopic patterns. Visual Neuroscience
# 5:165-204. Table 1 (p. 175): surface areas of cortical fields (% of neocortex).
#
# Inputs : data/measurements.csv (combined ImageJ digitizations, all views)
# Outputs: comparison/output/*.csv (+ one PNG), all overwritten on each run.
#
#   flatmap_table.csv                Table 1 layout rebuilt from the flatmaps
#   flatmap_table_long.csv           one row per case x field (analysis form)
#   flatmap_case_key.csv             display case number -> specimen/figure/map
#   table1_published.csv             transcription of the printed Table 1
#   table1_transcription_check.csv   printed mean/SD/Total vs recomputed
#   consistency_recomputation.csv    percent recomputed from pixel areas etc.
#   variance_components.csv          within- vs between-species (flatmaps and
#                                    Table 1), plus within-individual scales
#   within_individual_repeats.csv    same specimen + field seen in two views
#   flatmap_vs_table1_species.csv    species x field: means, SDs, ranges, tests
#   flatmap_vs_table1_cases.csv      each flatmap value vs the printed range
#   table1_nearest_case.csv          heuristic nearest printed case (unmatched)
#   variation_summary.png            within/between variation, flatmap vs table
#
# House rule: an input problem must stop() rather than print a partial result.
# Base R only. Rerun after editing measurements.csv; nothing is cached.

## ---- 0. Paths ---------------------------------------------------------------
dataset_dir <- paste0(
  "/Users/crossmodal/Library/CloudStorage/OneDrive-AllenInstitute/",
  "Evo-M1-Trait-Data-restricted/unpublished_data/____Unpublished__ProjectKaskan/",
  "flatmap_measurements/Krubitzer_Kaas_1990"
)
measurements_path <- file.path(dataset_dir, "data", "measurements.csv")
output_dir <- file.path(dataset_dir, "comparison", "output")
if (!file.exists(measurements_path)) stop("measurements.csv not found: ", measurements_path)
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

write_out <- function(x, name, digits = 4) {
  num <- vapply(x, is.numeric, logical(1))
  x[num] <- lapply(x[num], round, digits)
  write.csv(x, file.path(output_dir, name), row.names = FALSE, na = "")
  invisible(x)
}

## ---- 1. Species / field conventions ----------------------------------------
species_order   <- c("Saimiri sciureus", "Aotus trivirgatus",
                     "Callithrix jacchus", "Galago senegalensis")
species_headers <- c("Squirrel monkey", "Owl monkey", "Marmoset", "Galago")
minimum_case_counts <- c(6L, 4L, 6L, 4L)   # rows printed in Table 1
# Field order follows the printed Table 1. The CSV and the paper print the
# dorsointermediate area as "DI" (letter I); it is displayed as "D1" as
# requested for the flatmap table. field_csv holds the CSV label, field_display
# the column header used in every output so the two tables line up.
field_csv     <- c("17", "18", "DL", "DM", "DI", "FST", "MT", "MST")
field_display <- c("17", "18", "DL", "DM", "D1", "FST", "MT", "MST")
columns <- c(field_display, "Total")

## ---- 2. Published Table 1 (transcribed from p. 175) ------------------------
# "Surface areas of cortical fields as a percentage of the total surface of
# neocortex". Column order as printed: 17 18 DL DM DI FST MT MST Total.
# Transcribed from source/paper.pdf (PDF page 11) and verified against the PDF
# text layer (pypdfium2), 2026-09-27. check_table1() verifies the
# transcription: each row's eight fields sum to the printed Total within
# rounding (galago case 1 sums to 37.3 vs printed 37.4), and the printed
# Mean/SD are reproduced from the case rows within rounding tolerance.
table1_rows <- list(
  "Squirrel monkey" = rbind(
    c(19.5, 7.6, 4.4, 1.8, 1.0, 2.7, 1.3, 1.4, 39.7),
    c(19.9, 8.9, 4.7, 1.4, 1.0, 3.1, 1.1, 1.1, 41.2),
    c(17.4, 8.7, 4.2, 1.2, 0.9, 3.0, 1.6, 1.2, 38.2),
    c(19.7, 6.5, 3.4, 1.2, 1.0, 2.6, 1.3, 1.4, 37.1),
    c(19.1, 9.4, 4.0, 1.3, 1.3, 2.4, 1.4, 1.1, 40.0),
    c(13.7, 7.1, 5.7, 1.4, 1.4, 3.2, 1.6, 1.8, 35.9)),
  "Owl monkey" = rbind(
    c(14.6, 9.2, 3.5, 1.7, 1.5, 2.0, 2.1, 1.7, 36.3),
    c(18.4, 8.8, 3.3, 2.4, 1.8, 1.2, 1.8, 1.1, 38.8),
    c(15.0, 5.0, 2.2, 1.5, 1.6, 1.5, 1.3, 1.3, 29.4),
    c( 6.7, 7.5, 4.2, 1.7, 1.3, 2.1, 1.8, 1.8, 27.1)),
  "Marmoset" = rbind(
    c(16.1, 8.2, 4.0, 1.8, 2.8, 2.5, 1.5, 1.1, 38.0),
    c(16.9, 8.8, 3.5, 1.5, 2.2, 2.7, 2.3, 1.6, 39.5),
    c(20.0, 8.8, 3.7, 1.1, 1.9, 2.4, 2.0, 1.5, 41.4),
    c(15.7, 7.5, 4.1, 1.3, 1.7, 2.5, 1.9, 1.7, 36.4),
    c(22.3, 9.6, 3.1, 1.4, 2.0, 1.7, 1.7, 1.3, 43.1),
    c(18.5, 9.3, 4.4, 1.3, 2.2, 2.0, 1.6, 1.1, 40.4)),
  "Galago" = rbind(
    c(19.6, 6.8, 2.9, 0.6, 0.7, 2.2, 2.3, 2.2, 37.4),
    c(15.9, 4.6, 2.0, 0.8, 1.0, 2.7, 1.9, 1.4, 30.3),
    c(13.5, 8.0, 2.5, 1.2, 1.3, 2.7, 2.5, 1.9, 33.6),
    c(16.0, 4.4, 2.6, 0.8, 1.4, 1.8, 2.0, 2.1, 31.1))
)
table1_printed_mean <- rbind(
  "Squirrel monkey" = c(18.2, 8.0, 4.4, 1.4, 1.1, 2.8, 1.4, 1.3, 38.7),
  "Owl monkey"      = c(13.7, 7.6, 3.3, 1.8, 1.6, 1.7, 1.8, 1.5, 32.9),
  "Marmoset"        = c(18.3, 8.7, 3.8, 1.4, 2.1, 2.3, 1.8, 1.4, 39.8),
  "Galago"          = c(16.3, 6.0, 2.5, 0.9, 1.1, 2.4, 2.2, 1.9, 33.1))
table1_printed_sd <- rbind(
  "Squirrel monkey" = c(2.4, 1.1, 0.8, 0.2, 0.2, 0.3, 0.2, 0.3, 2.0),
  "Owl monkey"      = c(4.9, 1.9, 0.8, 0.4, 0.2, 0.4, 0.3, 0.3, 6.3),
  "Marmoset"        = c(2.5, 0.8, 0.5, 0.2, 0.4, 0.4, 0.3, 0.3, 2.4),
  "Galago"          = c(2.5, 1.7, 0.4, 0.2, 0.3, 0.4, 0.2, 0.4, 3.2))
colnames(table1_printed_mean) <- colnames(table1_printed_sd) <- columns

table1_long <- do.call(rbind, lapply(names(table1_rows), function(sp) {
  m <- table1_rows[[sp]]
  colnames(m) <- columns
  data.frame(source = "Table 1", species = sp, case = seq_len(nrow(m)),
             field = rep(columns, each = nrow(m)), value = as.vector(m),
             stringsAsFactors = FALSE)
}))

# Known inconsistency inside the printed table (not a transcription error; the
# PDF text layer prints 6.3): the owl-monkey Total SD recomputed from the four
# printed totals is 5.55. It is listed here so the check passes but the row is
# still reported in table1_transcription_check.csv.
table1_known_discrepancies <- data.frame(species = "Owl monkey", statistic = "sd",
                                         field = "Total", stringsAsFactors = FALSE)
check_table1 <- function(tolerance = 0.1) {
  rows <- list()
  for (sp in names(table1_rows)) {
    m <- table1_rows[[sp]]; colnames(m) <- columns
    if (nrow(m) != minimum_case_counts[match(sp, species_headers)])
      stop("Table 1 transcription: wrong number of cases for ", sp)
    # each row: eight fields vs printed Total (rounding of 8 addends <= 0.4)
    tot_err <- rowSums(m[, field_display]) - m[, "Total"]
    if (any(abs(tot_err) > 0.05 * length(field_display) + 1e-9))
      stop("Table 1 transcription: fields do not sum to Total for ", sp)
    rows[[sp]] <- rbind(
      data.frame(species = sp, statistic = "mean", field = columns,
                 recomputed = colMeans(m), printed = table1_printed_mean[sp, ], stringsAsFactors = FALSE),
      data.frame(species = sp, statistic = "sd", field = columns,
                 recomputed = apply(m, 2, sd), printed = table1_printed_sd[sp, ], stringsAsFactors = FALSE),
      data.frame(species = sp, statistic = "row_sum_minus_total", field = paste0("case ", seq_len(nrow(m))),
                 recomputed = rowSums(m[, field_display]), printed = m[, "Total"], stringsAsFactors = FALSE))
  }
  chk <- do.call(rbind, rows); rownames(chk) <- NULL
  chk$difference <- chk$recomputed - chk$printed
  chk$known_discrepancy <- paste(chk$species, chk$statistic, chk$field) %in%
    paste(table1_known_discrepancies$species, table1_known_discrepancies$statistic, table1_known_discrepancies$field)
  bad <- chk$statistic %in% c("mean", "sd") & abs(chk$difference) > tolerance & !chk$known_discrepancy
  if (any(bad))
    stop("Table 1 transcription: printed mean/SD not reproduced for ",
         paste(chk$species[bad], chk$statistic[bad], chk$field[bad], collapse = "; "))
  chk
}
table1_transcription_check <- check_table1()

## ---- 3. Read and validate measurements.csv ---------------------------------
flatmap_data <- read.csv(measurements_path, stringsAsFactors = FALSE,
                         na.strings = c("", "NA", "NaN"), check.names = FALSE)
required <- c("species", "specimen", "figure", "map_id", "label", "extent",
              "view_type", "linked_main_map", "repeat_of", "area_px2",
              "area_mm2", "sensitivity_low_mm2", "sensitivity_high_mm2",
              "include_in_whole_hemisphere_summary",
              "percent_of_drawn_neocortex", "percent_of_drawn_outline")
missing_columns <- setdiff(required, names(flatmap_data))
if (length(missing_columns)) stop("Missing columns: ", paste(missing_columns, collapse = ", "))
for (v in c("species", "specimen", "map_id", "label", "linked_main_map", "repeat_of"))
  flatmap_data[[v]] <- trimws(as.character(flatmap_data[[v]]))
flatmap_data$field <- field_display[match(flatmap_data$label, field_csv)]
flatmap_data$field[is.na(flatmap_data$field)] <- flatmap_data$label[is.na(flatmap_data$field)]
for (v in c("area_px2", "area_mm2", "sensitivity_low_mm2", "sensitivity_high_mm2",
            "percent_of_drawn_neocortex", "percent_of_drawn_outline")) {
  x <- flatmap_data[[v]]
  if (!is.numeric(x) && !all(is.na(x))) stop(v, " must contain numbers or NA.")
  if (any(!is.finite(x) & !is.na(x))) stop(v, " must be finite or NA.")
}

inclusion <- tolower(flatmap_data$include_in_whole_hemisphere_summary)
valid_flags <- c("true", "false", "t", "f", "1", "0")
if (any(!is.na(inclusion) & !inclusion %in% valid_flags))
  stop("Unrecognized include_in_whole_hemisphere_summary flag.")
flatmap_data$included <- inclusion %in% c("true", "t", "1")

## ---- 4. Updated flatmap Table 1 --------------------------------------------
build_flatmap_table <- function(data, digits = 2) {
  # Only rows flagged for the whole-hemisphere summary enter here. Sections,
  # zooms, partial maps and schematics are excluded by the CSV flag; do not
  # substitute percent_of_drawn_outline, which schematic outlines also use.
  excluded_views <- unique(data[!data$included,
    c("map_id", "figure", "species", "specimen", "view_type",
      "linked_main_map", "repeat_of"), drop = FALSE])
  data <- data[data$included, , drop = FALSE]
  if (any(!nzchar(data$map_id) | is.na(data$map_id)))
    stop("Missing map_id for an included whole-hemisphere map.")
  if (anyNA(data$species) || any(!data$species %in% species_order))
    stop("An included map has a missing or unsupported species; update species_order.")
  if (anyDuplicated(unique(data[c("map_id", "species", "specimen", "figure")])$map_id))
    stop("Inconsistent species, specimen or figure metadata within a map_id.")

  mean_or_na <- function(x) if (all(is.na(x))) NA_real_ else mean(x, na.rm = TRUE)
  sd_or_na   <- function(x) if (sum(!is.na(x)) < 2L) NA_real_ else sd(x, na.rm = TRUE)

  blocks <- case_keys <- longs <- vector("list", length(species_order))
  for (i in seq_along(species_order)) {
    d <- data[data$species == species_order[i], , drop = FALSE]
    if (anyNA(d[c("figure", "specimen")]))
      stop("Missing figure or specimen identifier for ", species_headers[i])
    maps <- unique(d[c("map_id", "figure", "specimen")])
    maps <- maps[order(as.numeric(maps$figure), maps$specimen, maps$map_id), , drop = FALSE]
    n_cases <- max(minimum_case_counts[i], nrow(maps))
    # Display case numbers follow figure order within each species. They are
    # NOT verified matches to the numbered cases in the printed Table 1.
    cases <- matrix(NA_real_, n_cases, length(columns), dimnames = list(NULL, columns))
    for (j in seq_len(nrow(maps))) {
      rows <- d[d$map_id == maps$map_id[j] & d$field %in% field_display, , drop = FALSE]
      if (anyDuplicated(rows$field)) stop("Duplicate field in included map ", maps$map_id[j])
      # Values are already percentages.
      cases[j, field_display] <- rows$percent_of_drawn_neocortex[match(field_display, rows$field)]
    }
    # Total is the sum of the eight fields; any missing field makes Total NA.
    cases[, "Total"] <- rowSums(cases[, field_display, drop = FALSE], na.rm = FALSE)
    block <- rbind(rep(NA_real_, length(columns)), cases,
                   apply(cases, 2, mean_or_na), apply(cases, 2, sd_or_na))
    blocks[[i]] <- data.frame(
      "Case number" = c(species_headers[i], as.character(seq_len(n_cases)), "Mean %", "Std Dev"),
      round(block, digits), check.names = FALSE, row.names = NULL)
    case_keys[[i]] <- data.frame(
      Species = species_headers[i], "Case number" = seq_len(n_cases),
      specimen = maps$specimen[seq_len(n_cases)], figure = maps$figure[seq_len(n_cases)],
      map_id = maps$map_id[seq_len(n_cases)], check.names = FALSE, stringsAsFactors = FALSE)
    k <- seq_len(nrow(maps))
    longs[[i]] <- data.frame(
      source = "Flatmap", species = species_headers[i], case = rep(k, length(columns)),
      specimen = rep(maps$specimen[k], length(columns)), map_id = rep(maps$map_id[k], length(columns)),
      field = rep(columns, each = length(k)), value = as.vector(cases[k, ]),
      stringsAsFactors = FALSE)
  }
  result <- do.call(rbind, blocks); rownames(result) <- NULL
  attr(result, "case_key") <- do.call(rbind, case_keys)
  attr(result, "long") <- do.call(rbind, longs)
  attr(result, "excluded_views") <- excluded_views
  result
}

flatmap_table <- build_flatmap_table(flatmap_data)
flatmap_case_key <- attr(flatmap_table, "case_key")
flatmap_long <- attr(flatmap_table, "long")
flatmap_excluded_views <- attr(flatmap_table, "excluded_views")
write.csv(flatmap_table, file.path(output_dir, "flatmap_table.csv"), row.names = FALSE, na = "")
write_out(flatmap_case_key, "flatmap_case_key.csv")
write_out(flatmap_long[!is.na(flatmap_long$value), ], "flatmap_table_long.csv")
write_out(table1_long, "table1_published.csv")
write_out(table1_transcription_check, "table1_transcription_check.csv")

## ---- 5. Internal consistency of measurements.csv ---------------------------
## 5a. Arithmetic checks: does the CSV agree with itself?
whole <- flatmap_data[flatmap_data$included, ]
outline <- whole[whole$label == "Neocortex outline", c("map_id", "area_px2", "area_mm2")]
if (anyDuplicated(outline$map_id) || !all(unique(whole$map_id) %in% outline$map_id))
  stop("Each included map needs exactly one 'Neocortex outline' row.")
fields_w <- whole[whole$label != "Neocortex outline" & !is.na(whole$area_px2), ]
fields_w <- merge(fields_w, outline, by = "map_id", suffixes = c("", "_outline"))
fields_w$percent_recomputed <- 100 * fields_w$area_px2 / fields_w$area_px2_outline
fields_w$percent_diff <- fields_w$percent_of_drawn_neocortex - fields_w$percent_recomputed
fields_w$mm2_recomputed <- with(fields_w, ifelse(is.na(area_mm2_outline), NA,
                                area_px2 / area_px2_outline * area_mm2_outline))
fields_w$mm2_rel_diff <- with(fields_w, (area_mm2 - mm2_recomputed) / mm2_recomputed)
fields_w$sens_halfwidth_rel <- with(fields_w, (sensitivity_high_mm2 - sensitivity_low_mm2) / 2 / area_mm2)
fields_w$in_sensitivity_band <- with(fields_w, area_mm2 >= sensitivity_low_mm2 & area_mm2 <= sensitivity_high_mm2)
consistency_recomputation <- fields_w[order(fields_w$map_id, fields_w$field),
  c("map_id", "specimen", "species", "field", "extent", "area_px2", "area_mm2",
    "percent_of_drawn_neocortex", "percent_recomputed", "percent_diff",
    "mm2_recomputed", "mm2_rel_diff", "sens_halfwidth_rel", "in_sensitivity_band")]
if (any(abs(consistency_recomputation$percent_diff) > 0.01, na.rm = TRUE))
  warning("percent_of_drawn_neocortex disagrees with area_px2/outline by > 0.01 in some rows.")
sum_fields <- aggregate(percent_of_drawn_neocortex ~ map_id, fields_w, sum)
if (any(sum_fields$percent_of_drawn_neocortex > 100))
  warning("Summed field percentages exceed 100% in: ",
          paste(sum_fields$map_id[sum_fields$percent_of_drawn_neocortex > 100], collapse = ", "))
write_out(consistency_recomputation, "consistency_recomputation.csv")

## 5b. Within-individual repeats: same specimen, same field, two views.
# Linked views (contralateral partial maps of Figs 25/26, the zoom in 26D) that
# have a *complete* field boundary are paired with the same field in the
# specimen's whole-hemisphere map, in mm2. Partial fragments are never used.
# These pairs mix opposite hemispheres, different drawings and magnifications,
# so their spread is an upper bound on pure re-digitization error.
linked <- flatmap_data[!is.na(flatmap_data$linked_main_map) & nzchar(flatmap_data$linked_main_map) &
                       flatmap_data$extent %in% c("complete", "approximate_complete") &
                       !is.na(flatmap_data$area_mm2), ]
main_mm2 <- whole[!is.na(whole$area_mm2), c("map_id", "field", "area_mm2", "percent_of_drawn_neocortex")]
repeats <- merge(linked, main_mm2, by.x = c("linked_main_map", "field"), by.y = c("map_id", "field"),
                 suffixes = c("_view", "_main"))
if (any(repeats$specimen != whole$specimen[match(repeats$linked_main_map, whole$map_id)]))
  stop("A linked view's specimen differs from its main map's specimen.")
repeats$species_common <- species_headers[match(repeats$species, species_order)]
repeats$ratio_view_over_main <- repeats$area_mm2_view / repeats$area_mm2_main
repeats$log_ratio <- log(repeats$ratio_view_over_main)
repeats$pct_diff <- 100 * (repeats$ratio_view_over_main - 1)
repeats$within_main_sensitivity <- with(repeats,
  area_mm2_view >= flatmap_data$sensitivity_low_mm2[match(paste(linked_main_map, field), paste(flatmap_data$map_id, flatmap_data$field))] &
  area_mm2_view <= flatmap_data$sensitivity_high_mm2[match(paste(linked_main_map, field), paste(flatmap_data$map_id, flatmap_data$field))])
within_individual_repeats <- repeats[order(repeats$species, repeats$specimen, repeats$field),
  c("species", "species_common", "specimen", "field", "map_id", "linked_main_map", "extent", "repeat_of",
    "area_mm2_view", "area_mm2_main", "percent_of_drawn_neocortex_main",
    "ratio_view_over_main", "log_ratio", "pct_diff", "within_main_sensitivity")]
write_out(within_individual_repeats, "within_individual_repeats.csv")

## 5c. Variance components: within-individual vs within-species vs between-species.
# For each field the percent-of-neocortex values (one per hemisphere/case) are
# partitioned by one-way ANOVA on species. Reported on the relative scale so
# fields of different size are comparable:
#   cv_within_species   pooled within-species SD / grand mean
#   cv_between_species  SD of species means / grand mean
#   icc_species         between-species variance component / total (ANOVA
#                       estimator; negative estimates truncated at 0)
# The same is computed from the printed Table 1 so the two sources can be
# compared on their own variance structure, not just on means.
# Within-individual scales come from 5a/5b (mm2 scale, not % of neocortex):
#   cv_within_individual_repeat  sd(log ratio)/sqrt(2): SD of one measurement
#                                implied by paired views of the same specimen
#   cv_sensitivity_halfwidth     median +/-2 px boundary perturbation half-width
#                                relative to area (digitization scenario only)
variance_components_one <- function(long, source_name) {
  out <- lapply(columns, function(f) {
    x <- long[long$field == f & !is.na(long$value), ]
    x$species <- factor(x$species, levels = species_headers)
    n_sp <- tapply(x$value, x$species, length); n_sp[is.na(n_sp)] <- 0
    if (sum(n_sp >= 1) < 2 || sum(n_sp) - sum(n_sp >= 1) < 1)
      return(data.frame(source = source_name, field = f, n_values = nrow(x),
                        n_species = sum(n_sp >= 1), stringsAsFactors = FALSE))
    fit <- anova(lm(value ~ species, data = x))
    ms_b <- fit["species", "Mean Sq"]; ms_w <- fit["Residuals", "Mean Sq"]
    k <- sum(n_sp >= 1); N <- sum(n_sp)
    n0 <- (N - sum(n_sp^2) / N) / (k - 1)         # effective group size
    var_b <- max(0, (ms_b - ms_w) / n0)
    sp_means <- tapply(x$value, x$species, mean)
    data.frame(
      source = source_name, field = f, n_values = N, n_species = k,
      grand_mean = mean(x$value),
      sd_within_species_pooled = sqrt(ms_w),
      sd_between_species_means = sd(sp_means, na.rm = TRUE),
      cv_within_species = sqrt(ms_w) / mean(x$value),
      cv_between_species = sd(sp_means, na.rm = TRUE) / mean(x$value),
      ratio_between_to_within_sd = sd(sp_means, na.rm = TRUE) / sqrt(ms_w),
      icc_species = var_b / (var_b + ms_w),
      anova_F = fit["species", "F value"], anova_p = fit["species", "Pr(>F)"],
      stringsAsFactors = FALSE)
  })
  do.call(rbind, lapply(out, function(z) { z[setdiff(names(out[[1]]), names(z))] <- NA; z }))
}
vc_flat <- variance_components_one(flatmap_long, "Flatmap")
vc_tab1 <- variance_components_one(table1_long, "Table 1")

# within-individual scales per field (flatmaps only)
rep_sd <- tapply(repeats$log_ratio, factor(repeats$field, levels = columns),
                 function(z) if (length(z) >= 2) sd(z) else NA_real_)
rep_n <- tapply(repeats$log_ratio, factor(repeats$field, levels = columns), length)
rep_mean_ratio <- tapply(repeats$ratio_view_over_main, factor(repeats$field, levels = columns), mean)
sens_med <- tapply(fields_w$sens_halfwidth_rel, factor(fields_w$field, levels = columns), median, na.rm = TRUE)
all_rep <- if (nrow(repeats) >= 2) sd(repeats$log_ratio) / sqrt(2) else NA_real_
vc_flat$n_within_individual_pairs <- as.integer(rep_n[vc_flat$field]); vc_flat$n_within_individual_pairs[is.na(vc_flat$n_within_individual_pairs)] <- 0L
vc_flat$mean_ratio_view_over_main <- as.numeric(rep_mean_ratio[vc_flat$field])
vc_flat$cv_within_individual_repeat <- as.numeric(rep_sd[vc_flat$field]) / sqrt(2)
vc_flat$cv_within_individual_repeat_all_fields <- all_rep
vc_flat$cv_sensitivity_halfwidth <- as.numeric(sens_med[vc_flat$field])
vc_flat$ratio_within_species_to_within_individual <- vc_flat$cv_within_species / vc_flat$cv_within_individual_repeat
vc_tab1[setdiff(names(vc_flat), names(vc_tab1))] <- NA
variance_components <- rbind(vc_flat, vc_tab1)
write_out(variance_components, "variance_components.csv")

## ---- 6. Comparison with the printed Table 1 ---------------------------------
## 6a. Species x field summary, both sources side by side.
summ <- function(long, prefix) {
  s <- lapply(split(long, list(long$species, long$field), drop = TRUE), function(x) {
    v <- x$value[!is.na(x$value)]
    data.frame(species = x$species[1], field = x$field[1], n = length(v),
               mean = if (length(v)) mean(v) else NA, sd = if (length(v) >= 2) sd(v) else NA,
               min = if (length(v)) min(v) else NA, max = if (length(v)) max(v) else NA,
               stringsAsFactors = FALSE)
  })
  s <- do.call(rbind, s)
  names(s)[-(1:2)] <- paste0(prefix, "_", names(s)[-(1:2)])
  s
}
cmp <- merge(summ(flatmap_long, "flatmap"), summ(table1_long, "table1"), by = c("species", "field"))
cmp$mean_diff_flatmap_minus_table1 <- cmp$flatmap_mean - cmp$table1_mean
cmp$mean_ratio_flatmap_over_table1 <- cmp$flatmap_mean / cmp$table1_mean
cmp$flatmap_mean_within_table1_range <- with(cmp, flatmap_mean >= table1_min & flatmap_mean <= table1_max)
cmp$pooled_sd <- with(cmp, sqrt(((flatmap_n - 1) * flatmap_sd^2 + (table1_n - 1) * table1_sd^2) /
                                 (flatmap_n + table1_n - 2)))
cmp$standardized_diff <- cmp$mean_diff_flatmap_minus_table1 / cmp$pooled_sd
cmp$welch_p <- mapply(function(sp, f) {
  a <- flatmap_long$value[flatmap_long$species == sp & flatmap_long$field == f]
  b <- table1_long$value[table1_long$species == sp & table1_long$field == f]
  a <- a[!is.na(a)]
  if (length(a) < 2 || length(b) < 2 || sd(a) == 0 && sd(b) == 0) return(NA_real_)
  t.test(a, b)$p.value
}, cmp$species, cmp$field)
cmp$species <- factor(cmp$species, levels = species_headers); cmp$field <- factor(cmp$field, levels = columns)
cmp <- cmp[order(cmp$species, cmp$field), ]; cmp$species <- as.character(cmp$species); cmp$field <- as.character(cmp$field)
flatmap_vs_table1_species <- cmp
write_out(flatmap_vs_table1_species, "flatmap_vs_table1_species.csv")

## 6b. Every flatmap case value against the printed species range.
rng <- summ(table1_long, "table1")[c("species", "field", "table1_min", "table1_max", "table1_mean", "table1_sd")]
cases_cmp <- merge(flatmap_long[!is.na(flatmap_long$value), ], rng, by = c("species", "field"))
cases_cmp$within_table1_range <- with(cases_cmp, value >= table1_min & value <= table1_max)
cases_cmp$z_vs_table1 <- with(cases_cmp, ifelse(table1_sd > 0, (value - table1_mean) / table1_sd, NA))
cases_cmp$species <- factor(cases_cmp$species, levels = species_headers); cases_cmp$field <- factor(cases_cmp$field, levels = columns)
cases_cmp <- cases_cmp[order(cases_cmp$species, cases_cmp$case, cases_cmp$field), ]
cases_cmp$species <- as.character(cases_cmp$species); cases_cmp$field <- as.character(cases_cmp$field)
flatmap_vs_table1_cases <- cases_cmp[c("species", "case", "specimen", "map_id", "field", "value",
                                       "table1_min", "table1_max", "table1_mean", "table1_sd",
                                       "within_table1_range", "z_vs_table1")]
write_out(flatmap_vs_table1_cases, "flatmap_vs_table1_cases.csv")

## 6c. Heuristic nearest printed case for each flatmap case (identities are NOT
# matched in the paper; this only asks whether any printed row resembles the
# digitized profile). Distance: root-mean-square over the eight fields of the
# difference divided by that field's Table 1 species SD (floored at 0.1).
nearest <- lapply(split(flatmap_long, flatmap_long$map_id), function(x) {
  sp <- x$species[1]
  fv <- x$value[match(field_display, x$field)]
  m <- table1_rows[[sp]]; colnames(m) <- columns
  s <- pmax(table1_printed_sd[sp, field_display], 0.1)
  ok <- !is.na(fv)
  dist <- apply(m[, field_display, drop = FALSE], 1, function(r) sqrt(mean(((fv[ok] - r[ok]) / s[ok])^2)))
  o <- order(dist)
  data.frame(species = sp, case = x$case[1], specimen = x$specimen[1], map_id = x$map_id[1],
             n_fields_used = sum(ok), nearest_table1_case = o[1], nearest_distance = dist[o[1]],
             second_table1_case = o[2], second_distance = dist[o[2]],
             margin = dist[o[2]] - dist[o[1]], stringsAsFactors = FALSE)
})
table1_nearest_case <- do.call(rbind, nearest)
table1_nearest_case <- table1_nearest_case[order(match(table1_nearest_case$species, species_headers),
                                                 table1_nearest_case$case), ]
# A printed case claimed by more than one flatmap is flagged: at most one can be right.
dup <- duplicated(table1_nearest_case[c("species", "nearest_table1_case")]) |
       duplicated(table1_nearest_case[c("species", "nearest_table1_case")], fromLast = TRUE)
table1_nearest_case$nearest_case_claimed_by_other_flatmap <- dup
write_out(table1_nearest_case, "table1_nearest_case.csv")

## ---- 7. Figure: variation within and between, flatmap vs Table 1 -----------
png(file.path(output_dir, "variation_summary.png"), width = 2400, height = 1600, res = 200)
op <- par(mfrow = c(2, 2), mar = c(4.5, 4.5, 3, 1))
cols <- c(Flatmap = "#1f77b4", "Table 1" = "#d62728")
# (a) species means with ranges, per field, both sources
plot(NA, xlim = c(0.5, length(field_display) + 0.5), ylim = c(0, 25), xaxt = "n", log = "",
     xlab = "Field", ylab = "% of neocortex (species mean, min-max)", main = "(a) Species means: flatmaps vs Table 1")
axis(1, at = seq_along(field_display), labels = field_display)
pch_sp <- c(15, 16, 17, 18)
for (i in seq_along(species_headers)) for (src in names(cols)) {
  z <- cmp[cmp$species == species_headers[i] & cmp$field %in% field_display, ]
  p <- if (src == "Flatmap") "flatmap" else "table1"
  xx <- match(z$field, field_display) + (i - 2.5) * 0.12 + ifelse(src == "Flatmap", -0.03, 0.03)
  ok <- !is.na(z[[paste0(p, "_min")]]) & z[[paste0(p, "_max")]] > z[[paste0(p, "_min")]]
  # ranges narrower than a pixel (e.g. two near-identical marmoset MT values) are skipped silently
  if (any(ok)) suppressWarnings(arrows(xx[ok], z[[paste0(p, "_min")]][ok], xx[ok], z[[paste0(p, "_max")]][ok],
                                       angle = 90, code = 3, length = 0.02, col = cols[src]))
  points(xx, z[[paste0(p, "_mean")]], pch = pch_sp[i], col = cols[src], cex = 0.9)
}
legend("topright", bty = "n", cex = 0.8, legend = c(names(cols), species_headers),
       col = c(cols, rep("grey30", 4)), pch = c(15, 15, pch_sp))
# (b) flatmap mean vs table 1 mean
plot(cmp$table1_mean, cmp$flatmap_mean, log = "xy", pch = pch_sp[match(cmp$species, species_headers)],
     xlab = "Table 1 species mean (%)", ylab = "Flatmap species mean (%)", main = "(b) Species x field means")
abline(0, 1, lty = 2); text(cmp$table1_mean, cmp$flatmap_mean, cmp$field, pos = 3, cex = 0.6)
# (c) CV components per field
vf <- vc_flat[vc_flat$field %in% field_display, ]; vt <- vc_tab1[vc_tab1$field %in% field_display, ]
mat <- rbind("Flatmap within-species" = vf$cv_within_species, "Table 1 within-species" = vt$cv_within_species,
             "Flatmap between-species" = vf$cv_between_species, "Table 1 between-species" = vt$cv_between_species,
             "Flatmap within-individual (repeat views)" = vf$cv_within_individual_repeat,
             "Flatmap sensitivity half-width" = vf$cv_sensitivity_halfwidth)
colnames(mat) <- vf$field
barplot(mat, beside = TRUE, col = c("#9ecae1", "#fcae91", "#08519c", "#a50f15", "#31a354", "#bdbdbd"),
        ylab = "Coefficient of variation", main = "(c) Variation components by field", ylim = c(0, max(mat, na.rm = TRUE) * 1.25))
legend("topleft", bty = "n", cex = 0.7, fill = c("#9ecae1", "#fcae91", "#08519c", "#a50f15", "#31a354", "#bdbdbd"), legend = rownames(mat))
# (d) within-individual repeats
plot(repeats$area_mm2_main, repeats$area_mm2_view, log = "xy", pch = pch_sp[match(repeats$species_common, species_headers)],
     xlab = "Whole-hemisphere map area (mm2)", ylab = "Linked view area (mm2)", main = "(d) Same specimen, same field, two views")
abline(0, 1, lty = 2); text(repeats$area_mm2_main, repeats$area_mm2_view, paste(repeats$specimen, repeats$field), pos = 3, cex = 0.55)
legend("bottomright", bty = "n", cex = 0.8, legend = species_headers, pch = pch_sp)
par(op); dev.off()

## ---- 8. Console summary -----------------------------------------------------
cat("\nUpdated flatmap Table 1 (", nrow(flatmap_case_key[!is.na(flatmap_case_key$map_id), ]), " hemispheres):\n", sep = "")
print(flatmap_table, row.names = FALSE, na.print = "NA")
cat("\nWithin- vs between-species (CV), flatmaps and Table 1:\n")
print(variance_components[variance_components$field %in% columns,
      c("source", "field", "n_values", "cv_within_species", "cv_between_species", "icc_species",
        "cv_within_individual_repeat", "cv_sensitivity_halfwidth")], row.names = FALSE, digits = 3)
cat("\nSpecies means, flatmap vs Table 1 (standardized difference and Welch p):\n")
print(flatmap_vs_table1_species[c("species", "field", "flatmap_n", "flatmap_mean", "table1_n", "table1_mean",
                                  "mean_ratio_flatmap_over_table1", "flatmap_mean_within_table1_range",
                                  "standardized_diff", "welch_p")], row.names = FALSE, digits = 3)
cat("\nFlatmap values outside the printed species range: ",
    sum(!flatmap_vs_table1_cases$within_table1_range), " of ", nrow(flatmap_vs_table1_cases), "\n", sep = "")
cat("Within-individual repeat pairs: ", nrow(repeats), "; SD of one measurement implied by repeats (log scale): ",
    round(all_rep, 3), "\n", sep = "")
cat("Outputs written to ", output_dir, "\n", sep = "")
# View(flatmap_table); View(flatmap_vs_table1_species); View(variance_components)
