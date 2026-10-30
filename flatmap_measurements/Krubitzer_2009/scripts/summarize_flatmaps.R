# Base-R summary helper. Source this file or run Rscript with a measurements CSV.
# Reading occurs on each invocation; there are no cached measurements.
build_flatmap_summary <- function(data, fields = NULL, species_order = NULL,
                                 species_headers = NULL, minimum_case_counts = NULL,
                                 field_display = NULL, digits = 2) {
  required <- c("map_id", "species", "specimen", "figure", "label",
                "include_in_whole_hemisphere_summary", "percent_of_drawn_neocortex")
  missing <- setdiff(required, names(data))
  if (length(missing)) stop("Missing columns: ", paste(missing, collapse = ", "))
  flag <- tolower(trimws(as.character(data$include_in_whole_hemisphere_summary)))
  if (any(!is.na(flag) & !flag %in% c("", "true", "false", "t", "f", "1", "0")))
    stop("Invalid whole-hemisphere inclusion flag.")
  d <- data[flag %in% c("true", "t", "1"), , drop = FALSE]
  for (column in c("map_id", "species", "specimen", "label")) {
    d[[column]] <- trimws(as.character(d[[column]]))
    if (anyNA(d[[column]]) || any(!nzchar(d[[column]])))
      stop("Missing identity/label in included rows: ", column)
  }
  if (anyDuplicated(d[c("map_id", "label")])) stop("Duplicate map/field rows.")
  if (anyDuplicated(unique(d[c("map_id", "species", "specimen", "figure")])$map_id))
    stop("Conflicting identity metadata for a map.")
  values <- d$percent_of_drawn_neocortex
  if ((!is.numeric(values) && !all(is.na(values))) ||
      any(!is.finite(as.numeric(values)) & !is.na(values)))
    stop("Percentages must be finite numeric values or NA.")
  d$percent_of_drawn_neocortex <- as.numeric(values)
  if (is.null(species_order)) species_order <- unique(d$species)
  if (any(!d$species %in% species_order)) stop("species_order omits an included species.")
  if (is.null(species_headers)) species_headers <- species_order
  if (is.null(minimum_case_counts)) minimum_case_counts <- rep(0L, length(species_order))
  if (length(species_headers) != length(species_order) ||
      length(minimum_case_counts) != length(species_order) ||
      anyNA(minimum_case_counts) || any(minimum_case_counts < 0) ||
      any(minimum_case_counts != as.integer(minimum_case_counts)))
    stop("Species headers and nonnegative integer minimum counts must align.")
  compute_total <- !is.null(fields)
  if (is.null(fields)) {
    outline <- d$label %in% c("Neocortex outline", "Drawn schematic outline")
    if ("is_outline" %in% names(d))
      outline <- outline | tolower(as.character(d$is_outline)) %in% c("true", "t", "1")
    fields <- unique(d$label[!outline])
  }
  if (is.null(field_display)) field_display <- fields
  if (length(field_display) != length(fields) || anyDuplicated(fields) ||
      anyDuplicated(field_display) || any(field_display %in% c("Case number", "Total")))
    stop("Field labels/display names must be unique and align.")
  columns <- c(field_display, "Total")
  safe_mean <- function(x) if (all(is.na(x))) NA_real_ else mean(x, na.rm = TRUE)
  safe_sd <- function(x) if (sum(!is.na(x)) < 2L) NA_real_ else sd(x, na.rm = TRUE)
  tables <- keys <- counts <- vector("list", length(species_order))
  for (i in seq_along(species_order)) {
    s <- d[d$species == species_order[i], , drop = FALSE]
    maps <- unique(s[c("map_id", "specimen", "figure")])
    maps <- maps[order(suppressWarnings(as.numeric(maps$figure)), maps$map_id), , drop = FALSE]
    nr <- max(minimum_case_counts[i], nrow(maps))
    m <- matrix(NA_real_, nr, length(columns), dimnames = list(NULL, columns))
    for (j in seq_len(nrow(maps))) {
      rows <- s[s$map_id == maps$map_id[j], , drop = FALSE]
      m[j, field_display] <- rows$percent_of_drawn_neocortex[match(fields, rows$label)]
    }
    if (length(fields) && compute_total) m[, "Total"] <- rowSums(m[, field_display, drop = FALSE])
    block <- rbind(rep(NA_real_, length(columns)), m,
                   apply(m, 2, safe_mean), apply(m, 2, safe_sd))
    tables[[i]] <- data.frame("Case number" = c(species_headers[i],
      as.character(seq_len(nr)), "Mean %", "Std Dev"), round(block, digits),
      check.names = FALSE, row.names = NULL)
    keys[[i]] <- data.frame(species = rep(species_order[i], nr), case = seq_len(nr),
      maps[seq_len(nr), , drop = FALSE], row.names = NULL)
    counts[[i]] <- data.frame(species = species_order[i], field = columns,
                             n = colSums(!is.na(m)), row.names = NULL)
  }
  if (!length(tables)) {
    table <- data.frame("Case number" = character(), check.names = FALSE)
    for (column in columns) table[[column]] <- numeric()
    return(list(table = table, case_key = data.frame(), n = data.frame()))
  }
  list(table = do.call(rbind, tables), case_key = do.call(rbind, keys), n = do.call(rbind, counts))
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) != 1L) stop("Usage: Rscript summarize_flatmaps.R path/to/measurements.csv")
  flatmap_data <- read.csv(args[1], na.strings = c("", "NA", "NaN"),
                           stringsAsFactors = FALSE, check.names = FALSE)
  result <- build_flatmap_summary(flatmap_data)
  flatmap_table <- result$table
  flatmap_case_key <- result$case_key
  flatmap_n <- result$n
  print(flatmap_table, row.names = FALSE, na.print = "NA")
}
