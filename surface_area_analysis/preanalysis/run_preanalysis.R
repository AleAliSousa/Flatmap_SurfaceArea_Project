# run_preanalysis.R -- assumption-bearing relative->absolute conversions and flatmap-vs-merge comparison.
#   Rscript run_preanalysis.R      (from surface_area_analysis/preanalysis/)
# Requires the merge outputs in ../../../Species/Evo-M1-Trait-Data/__merging_cortical_areas (or set
# CORTICAL_AREAS_MERGE_DIR) and surface_area_analysis/data/04_specimen_region_means_flagged.csv
# (run ../run_all.R first).
a <- commandArgs(trailingOnly = FALSE); f <- sub("^--file=", "", a[grepl("^--file=", a)])
setwd(if (length(f)) dirname(normalizePath(f[1])) else getwd())
preanalysis_dir <- normalizePath(getwd())
source("R/10_relative_to_absolute_external.R")
