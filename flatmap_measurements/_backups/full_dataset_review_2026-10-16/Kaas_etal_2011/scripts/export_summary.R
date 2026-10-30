# Run from the dataset folder. No view is pooled as whole neocortex without its flag.
source('scripts/summarize_flatmaps.R')
d <- read.csv('data/measurements.csv', na.strings=c('', 'NA'), stringsAsFactors=FALSE, check.names=FALSE)
s <- build_flatmap_summary(d)
if (!ncol(s$case_key)) s$case_key <- data.frame(species=character(),case=integer(),map_id=character(),specimen=character(),figure=integer())
if (!ncol(s$n)) s$n <- data.frame(species=character(),field=character(),n=integer())
write.csv(s$table, 'data/species_summary_percent.csv', row.names=FALSE, na='NA')
write.csv(s$case_key, 'data/summary_case_key.csv', row.names=FALSE, na='NA')
write.csv(s$n, 'data/summary_observed_n.csv', row.names=FALSE, na='NA')
# Summarize absolute areas of complete fields from identified main cases separately.
# Partial mapped islands/fragments and repeated views do not enter these means.
complete <- !is.na(d$area_mm2) & d$extent == 'complete' & tolower(d$is_outline) == 'false' & is.na(d$repeat_of)
complete[is.na(complete)] <- FALSE
keys <- unique(d[tolower(d$is_outline) == 'false', c('species','label')])
rows <- vector('list', nrow(keys))
for (i in seq_len(nrow(keys))) {
  z <- d[complete & d$species == keys$species[i] & d$label == keys$label[i], , drop=FALSE]
  rows[[i]] <- data.frame(species=keys$species[i], field=keys$label[i], n=nrow(z),
    mean_mm2=if(nrow(z)) mean(z$area_mm2) else NA_real_,
    sample_sd_mm2=if(nrow(z)>1L) sd(z$area_mm2) else NA_real_,
    specimens=if(nrow(z)) paste(z$specimen, collapse=';') else '',
    scope='complete field envelope; no whole-neocortex percentage')
}
empty <- data.frame(species=character(),field=character(),n=integer(),mean_mm2=numeric(),sample_sd_mm2=numeric(),specimens=character(),scope=character())
a <- if(length(rows)) do.call(rbind,rows) else empty
write.csv(a, 'data/field_area_summary.csv', row.names=FALSE, na='NA')
