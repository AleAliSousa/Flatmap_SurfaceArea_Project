# Run from this dataset folder; all fields discovered and reread on each invocation.
source('scripts/summarize_flatmaps.R')
d <- read.csv('data/measurements.csv', na.strings=c('', 'NA'), stringsAsFactors=FALSE, check.names=FALSE)
s <- build_flatmap_summary(d)
write.csv(s$table, 'data/species_summary_percent.csv', row.names=FALSE, na='NA')
write.csv(s$case_key, 'data/summary_case_key.csv', row.names=FALSE, na='NA')
write.csv(s$n, 'data/summary_observed_n.csv', row.names=FALSE, na='NA')
