# Whole-neocortex summaries require an independent eligible outline.
source('scripts/summarize_flatmaps.R')
d <- read.csv('data/measurements.csv',na.strings=c('','NA'),stringsAsFactors=FALSE,check.names=FALSE)
s <- build_flatmap_summary(d)
if (!ncol(s$case_key)) s$case_key <- data.frame(species=character(),case=integer(),map_id=character(),specimen=character(),figure=integer())
if (!ncol(s$n)) s$n <- data.frame(species=character(),field=character(),n=integer())
write.csv(s$table,'data/species_summary_percent.csv',row.names=FALSE,na='NA')
write.csv(s$case_key,'data/summary_case_key.csv',row.names=FALSE,na='NA')
write.csv(s$n,'data/summary_observed_n.csv',row.names=FALSE,na='NA')
# Select one supported complete observation per explicitly identified specimen/label.
# Main maps take priority, with repeated-view fallback when no main-map area exists.
ok <- !is.na(d$area_mm2) & d$extent=='complete' & tolower(d$is_outline)=='false' & !is.na(d$specimen) & d$specimen!='not reported' & !grepl('composite|illustrative|schematic|atlas|summary',d$view_type,ignore.case=TRUE) & !grepl('illustrative|summary|unresolved|not reported|not assigned',d$specimen,ignore.case=TRUE) & !grepl('unresolved',ifelse(is.na(d$specimen_link_status),'',d$specimen_link_status),ignore.case=TRUE)
ok[is.na(ok)] <- FALSE
z <- d[ok,,drop=FALSE]
z <- z[order(!is.na(z$repeat_of),z$map_id),,drop=FALSE]
key <- paste(z$species,z$specimen,z$label,sep='|')
z <- z[!duplicated(key),,drop=FALSE]
selection <- z[,c('species','specimen','label','map_id','repeat_of','hemisphere','hemisphere_relation','area_mm2'),drop=FALSE]
selection$selection_reason <- ifelse(is.na(z$repeat_of),'supported complete main-map observation','repeated-view fallback; main map lacks supported complete area')
write.csv(selection,'data/summary_case_selection.csv',row.names=FALSE,na='NA')
keys <- unique(d[tolower(d$is_outline)=='false',c('species','label')])
rows <- vector('list',nrow(keys))
for (i in seq_len(nrow(keys))) {
 q <- z[z$species==keys$species[i] & z$label==keys$label[i],,drop=FALSE]
 rows[[i]] <- data.frame(species=keys$species[i],field=keys$label[i],n=nrow(q),mean_mm2=if(nrow(q)) mean(q$area_mm2) else NA_real_,sample_sd_mm2=if(nrow(q)>1) sd(q$area_mm2) else NA_real_,specimens=if(nrow(q)) paste(q$specimen,collapse=';') else '',scope='one complete supported view per identified specimen and literal label; no neocortex denominator')
}
a <- if(length(rows)) do.call(rbind,rows) else data.frame(species=character(),field=character(),n=integer(),mean_mm2=numeric(),sample_sd_mm2=numeric(),specimens=character(),scope=character())
write.csv(a,'data/field_area_summary.csv',row.names=FALSE,na='NA')
