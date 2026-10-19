# run_all.R -- rebuild every table, figure and the report from the current measurements.
#   Rscript run_all.R           (from surface_area_analysis/)
# Each numbered script can also be run on its own; it then reads the previous step's CSV.
options(flatmap.run_step = TRUE)
this_dir <- tryCatch({
  a <- commandArgs(trailingOnly = FALSE); f <- sub("^--file=", "", a[grepl("^--file=", a)])
  if (length(f)) dirname(normalizePath(f[1])) else getwd()
}, error = function(e) getwd())
setwd(this_dir)
source("R/00_config.R")
analysis_dir <- this_dir; project_root <- normalizePath(file.path(analysis_dir, ".."))
measurements_root <- file.path(project_root, "flatmap_measurements")
reference_dir <- file.path(analysis_dir, "reference"); out_data <- file.path(analysis_dir, "data")
out_fig <- file.path(analysis_dir, "figures"); out_rep <- file.path(analysis_dir, "reports")
for (s in c("01_load_measurements", "02_flag_completeness", "03_specimen_means",
            "04_flag_outliers", "05_species_summary")) {
  message("\n==== ", s, " ====")
  source(file.path("R", paste0(s, ".R")))
}
message("\nDone. Outputs in data/, figures/, reports/.")
