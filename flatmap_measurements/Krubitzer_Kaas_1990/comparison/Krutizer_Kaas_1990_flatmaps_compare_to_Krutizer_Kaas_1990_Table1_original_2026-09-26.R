# Surface areas of cortical fields (% of drawn neocortex).
# Uses the combined measurements.csv and its whole-hemisphere inclusion flag.
# Builds flatmap_table in R; does not write a table file.
flatmap_data <- read.csv(
  "/Users/crossmodal/Library/CloudStorage/OneDrive-AllenInstitute/Flatmap_SurfaceArea_Project/flatmap_measurements/Krubitzer_Kaas_1990/data/measurements.csv",
  stringsAsFactors = FALSE,
  na.strings = c("", "NA", "NaN"),
  check.names = FALSE
)

build_flatmap_table <- function(data, digits = 2) {
  required <- c("species", "specimen", "figure", "map_id", "label",
                "include_in_whole_hemisphere_summary",
                "percent_of_drawn_neocortex")
  missing_columns <- setdiff(required, names(data))
  if (length(missing_columns)) {
    stop("Missing columns: ", paste(missing_columns, collapse = ", "))
  }

  species_order <- c("Saimiri sciureus", "Aotus trivirgatus",
                     "Callithrix jacchus", "Galago senegalensis")
  species_headers <- c("Squirrel monkey", "Owl monkey", "Marmoset", "Galago")
  # Keep the requested minimum case rows, and expand as new maps are added.
  minimum_case_counts <- c(6L, 4L, 6L, 4L)
  fields <- c("17", "18", "DL", "DM", "D1", "FST", "MT", "MST")
  columns <- c(fields, "Total")

  # The combined CSV includes sections, zooms, partial maps and schematics.
  # Only rows explicitly eligible for the whole-hemisphere summary enter here.
  # Do not substitute percent_of_drawn_outline: schematic outlines also use it.
  inclusion <- tolower(trimws(as.character(data$include_in_whole_hemisphere_summary)))
  valid_flags <- c("true", "false", "t", "f", "1", "0")
  if (any(!is.na(inclusion) & !inclusion %in% c("", valid_flags))) {
    stop("Unrecognized include_in_whole_hemisphere_summary flag.")
  }
  eligible <- inclusion %in% c("true", "t", "1")
  excluded_columns <- intersect(
    c("map_id", "figure", "panel", "species", "specimen", "view_type",
      "linked_main_map", "repeat_of", "include_in_whole_hemisphere_summary"),
    names(data)
  )
  excluded_views <- unique(data[!eligible, excluded_columns, drop = FALSE])
  data <- data[eligible, , drop = FALSE]
  if (anyNA(data$map_id) || any(!nzchar(trimws(data$map_id)))) {
    stop("Missing map_id for an included whole-hemisphere map.")
  }
  data$map_id <- trimws(data$map_id)
  data$species <- trimws(data$species)
  if (anyNA(data$species) || any(!data$species %in% species_order)) {
    stop("An included map has a missing or unsupported species; update species_order.")
  }
  # map_id distinguishes panels; figure + specimen can merge repeated views.
  # Each included map must have consistent identity metadata.
  identity_columns <- c("map_id", "species", "specimen", "figure")
  if (anyDuplicated(unique(data[identity_columns])$map_id)) {
    stop("Inconsistent species, specimen or figure metadata within a map_id.")
  }
  data$label <- trimws(data$label)
  # The CSV labels this field DI (letter I); display it as requested: D1.
  data$label[data$label %in% "DI"] <- "D1"
  values <- data$percent_of_drawn_neocortex
  if (!is.numeric(values) && !all(is.na(values))) {
    stop("percent_of_drawn_neocortex must contain numbers or NA.")
  }
  data$percent_of_drawn_neocortex <- as.numeric(values)
  values <- data$percent_of_drawn_neocortex
  if (any(!is.finite(values) & !is.na(values))) {
    stop("Percentages must be finite numbers or NA.")
  }

  mean_or_na <- function(x) {
    if (all(is.na(x))) NA_real_ else mean(x, na.rm = TRUE)
  }
  sd_or_na <- function(x) {
    if (sum(!is.na(x)) < 2L) NA_real_ else sd(x, na.rm = TRUE)
  }

  blocks <- case_keys <- vector("list", length(species_order))
  for (i in seq_along(species_order)) {
    d <- data[data$species %in% species_order[i], , drop = FALSE]
    if (anyNA(d[c("figure", "specimen")])) {
      stop("Missing figure or specimen identifier for ", species_headers[i])
    }
    maps <- unique(d[c("map_id", "figure", "specimen")])
    maps <- maps[order(as.numeric(maps$figure), maps$specimen, maps$map_id), , drop = FALSE]
    n_cases <- max(minimum_case_counts[i], nrow(maps))

    # Display case numbers follow figure order within each species.
    # These are NOT verified matches to case numbers in published Table 1.
    cases <- matrix(NA_real_, nrow = n_cases, ncol = length(columns),
                    dimnames = list(NULL, columns))
    for (j in seq_len(nrow(maps))) {
      rows <- d[d$map_id == maps$map_id[j] & d$label %in% fields, , drop = FALSE]
      if (anyDuplicated(rows$label)) {
        stop("Duplicate field in included map ", maps$map_id[j])
      }
      # Already percentages: do not multiply by 100 again.
      cases[j, fields] <- rows$percent_of_drawn_neocortex[match(fields, rows$label)]
    }
    # Total is the sum of the eight fields. Missing fields make Total NA.
    cases[, "Total"] <- rowSums(cases[, fields, drop = FALSE], na.rm = FALSE)

    # Summarize all available case values for each column, excluding NA.
    # Newly added cases or newly filled measurements enter on the next run.
    block <- rbind(rep(NA_real_, length(columns)), cases,
                   apply(cases, 2, mean_or_na), apply(cases, 2, sd_or_na))
    blocks[[i]] <- data.frame(
      "Case number" = c(species_headers[i], as.character(seq_len(n_cases)),
                        "Mean %", "Std Dev"),
      round(block, digits), check.names = FALSE, row.names = NULL
    )
    # Keep a key so each numbered row can be traced to its source flatmap.
    case_keys[[i]] <- data.frame(
      Species = species_headers[i], "Case number" = seq_len(n_cases),
      specimen = maps$specimen[seq_len(n_cases)],
      figure = maps$figure[seq_len(n_cases)],
      map_id = maps$map_id[seq_len(n_cases)], check.names = FALSE
    )
  }
  result <- do.call(rbind, blocks)
  rownames(result) <- NULL
  attr(result, "case_key") <- do.call(rbind, case_keys)
  attr(result, "excluded_views") <- excluded_views
  result
}

# Rerun this script after updating measurements.csv to refresh all results.
# New whole-hemisphere maps are included automatically when their inclusion
# flag is TRUE. Rows beyond the requested minimum case counts are added.
# Total mean/SD use only cases with all eight fields measured.
# Means use every available value; sample SDs require at least two values.
# All-missing summaries stay NA; NA placeholder rows do not affect statistics.
# Statistics are calculated before rounding. Source measurements are provisional.
flatmap_table <- build_flatmap_table(flatmap_data)
flatmap_case_key <- attr(flatmap_table, "case_key")
flatmap_excluded_views <- attr(flatmap_table, "excluded_views")
print(flatmap_table, row.names = FALSE, na.print = "NA")
# View(flatmap_table)       # Optional: open the table in RStudio.
# View(flatmap_case_key)    # Optional: inspect specimen/figure/map assignments.
# View(flatmap_excluded_views)  # Optional: inspect views excluded by the CSV flag.
