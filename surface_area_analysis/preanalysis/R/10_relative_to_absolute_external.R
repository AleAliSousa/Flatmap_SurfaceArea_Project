# 10_relative_to_absolute_external.R -- ASSUMPTION-BEARING conversions of relative cortical surface
# areas to mm2, kept OUTSIDE the Evo-M1-Trait-Data repo on purpose.
#
# Inside the merge (__merging_cortical_areas), a percentage becomes mm2 only when the denominator
# was measured on the same specimen.  Everything the merge could not convert arrives here as
# cortical_areas_relative_unconverted.csv.  This script offers, for every such row, one derived
# value PER candidate denominator, each labelled with the assumption it rests on.  Nothing here is
# written back into the repo; a downstream analysis picks the assumption it is willing to defend.
#
# Denominator options (column `assumption`):
#   species_mean_same_source      -- mean of the same source's individual whole-neocortex values
#   species_mean_merge_wide       -- the merge's pooled species CorticalSurface_Area.mm2 (active sources;
#                                    mixes flattening and reconstruction methods; see composition sidecar)
#   flatmap_same_paper_median     -- median flatmap-traced neocortex outline of the SAME paper's
#                                    whole-hemisphere cases (same lab, same preparation; animals not
#                                    yet linked one-to-one -> see specimen_links.csv in the merge)
#   flatmap_species_median        -- median flatmap outline across all papers for the species
# Also emitted: flatmap specimen means expressed in merge terms, and flatmap-traced percentages
# compared with the published Krubitzer & Kaas 1990 Table 1 percentages (validation of the tracings).
suppressPackageStartupMessages({ library(dplyr); library(readr); library(tidyr); library(stringr); library(purrr) })

here <- if (exists("preanalysis_dir")) preanalysis_dir else local({   # set by run_preanalysis.R
  a <- commandArgs(trailingOnly = FALSE); f <- sub("^--file=", "", a[grepl("^--file=", a)])
  if (length(f)) normalizePath(file.path(dirname(f[1]), "..")) else normalizePath(getwd())
})
analysis_dir <- normalizePath(file.path(here, ".."))                     # surface_area_analysis/
project_root <- normalizePath(file.path(analysis_dir, ".."))             # Flatmap_SurfaceArea_Project/
merge_dir <- Sys.getenv("CORTICAL_AREAS_MERGE_DIR",
  unset = file.path(dirname(project_root), "Species", "Evo-M1-Trait-Data", "__merging_cortical_areas"))
stopifnot(dir.exists(merge_dir))
out <- file.path(here, "data"); dir.create(out, showWarnings = FALSE)
wr <- function(df, nm) { p <- file.path(out, nm); write_csv(df, p, na = "NA"); message("wrote ", p, " (", nrow(df), " rows)") }

# ---- inputs -------------------------------------------------------------------------------
long   <- read_csv(file.path(merge_dir, "cortical_areas_long.csv"), show_col_types = FALSE)
uncon  <- read_csv(file.path(merge_dir, "cortical_areas_relative_unconverted.csv"), show_col_types = FALSE)
comp   <- read_csv(file.path(merge_dir, "cortical_areas_wide_composition.csv"), show_col_types = FALSE)
fm     <- read_csv(file.path(analysis_dir, "data", "04_specimen_region_means_flagged.csv"), show_col_types = FALSE)

# ---- flatmap -> merge vocabulary ------------------------------------------------------------
# region_group (from the flatmap label crosswalk) -> merge term stem.  Unmapped groups stay NA.
group_to_term <- c("V1 (area 17)" = "V1", "V2 (area 18)" = "V2", "S1 / 3b" = "S1", "S2" = "S2", "A1" = "A1",
                   "MT" = "MT", "DL" = "DL", "DM" = "DM", "DI" = "DI", "FST" = "FST", "MST" = "MST",
                   "Neocortex outline" = "CorticalSurface")
fm_species_alias <- c("Macaca (source label)" = "Macaca sp.")
fm2 <- fm %>%
  mutate(Species = coalesce(unname(fm_species_alias[species]), species),
         term_stem = unname(group_to_term[region_group]),
         abs_term = ifelse(is.na(term_stem), NA, ifelse(term_stem == "CorticalSurface", "CorticalSurface_Area.mm2",
                                                        paste0(term_stem, "_Surface_Area.mm2"))),
         pct_term = ifelse(is.na(term_stem) | term_stem == "CorticalSurface", NA, paste0(term_stem, "_Surface_Area.pct_Neocortex")),
         source = paste0("Flatmap::", paper))
flat_abs <- fm2 %>% filter(!is.na(mean_mm2)) %>%
  transmute(Species, species_label_flatmap = species, Standardized_Term = abs_term, flatmap_label = label, region_group,
            value = mean_mm2, source, specimen, n_views = n_views_usable, recommend_use, plausibility, hard_flags, soft_flags,
            value_basis = "flatmap_traced_mean_over_views", grain = "individual")
flat_pct <- fm2 %>% filter(!is.na(fraction_of_neocortex), denominator_source == "own specimen outline", !is.na(pct_term)) %>%
  transmute(Species, species_label_flatmap = species, Standardized_Term = pct_term, flatmap_label = label, region_group,
            value = 100 * fraction_of_neocortex, source, specimen, n_views = n_views_usable, recommend_use, plausibility,
            hard_flags, soft_flags, value_basis = "flatmap_traced / own traced neocortex outline", grain = "individual")
flat_long <- bind_rows(flat_abs, flat_pct) %>% arrange(Species, specimen, Standardized_Term)
wr(flat_long, "flatmap_long_standardized.csv")
wr(fm2 %>% filter(is.na(term_stem), !is.na(mean_mm2)) %>% count(region_group, label, name = "n_specimen_means"),
   "flatmap_labels_without_merge_term.csv")

# ---- candidate denominators per species ----------------------------------------------------
den_same_source <- long %>%
  filter(Standardized_Term == "CorticalSurface_Area.mm2", status == "active", grain == "individual", value_basis == "printed") %>%
  group_by(Species, source) %>%
  summarise(denominator_mm2 = mean(value), n_individuals = n(), .groups = "drop") %>%
  mutate(assumption = "species_mean_same_source",
         denominator_provenance = paste0("mean of ", n_individuals, " individual neocortex values in ", source))
den_merge <- comp %>% filter(Standardized_Term == "CorticalSurface_Area.mm2") %>%
  transmute(Species, denominator_mm2 = value_mean, n_individuals = n_values, assumption = "species_mean_merge_wide",
            denominator_provenance = paste0("merge _wide pooled mean of ", n_values, " active values from: ", sources,
                                            ifelse(conflict_flag, " [CONFLICT FLAG: sources disagree >15% CV]", "")))
fm_out <- fm2 %>% filter(is_outline, recommend_use, !is.na(mean_mm2))
den_fm_paper <- fm_out %>% group_by(Species, paper) %>%
  summarise(denominator_mm2 = median(mean_mm2), n_individuals = n(), .groups = "drop") %>%
  mutate(assumption = "flatmap_same_paper_median",
         denominator_provenance = paste0("median flatmap-traced neocortex outline of ", n_individuals,
                                         " whole-hemisphere case(s) in ", paper, " (recommend_use only)"))
den_fm_species <- fm_out %>% group_by(Species) %>%
  summarise(denominator_mm2 = median(mean_mm2), n_individuals = n(), .groups = "drop") %>%
  mutate(assumption = "flatmap_species_median",
         denominator_provenance = paste0("median flatmap-traced neocortex outline over ", n_individuals, " case(s), all papers"))
den_all <- bind_rows(den_same_source %>% rename(denominator_source = source),
                     den_merge, den_fm_paper %>% rename(denominator_source = paper), den_fm_species)
wr(den_all %>% arrange(Species, assumption), "denominator_options.csv")

# ---- external conversions: one row per relative value x denominator option ------------------
item_to_paper <- c("Krubitzer_Kaas_1990_Table1" = "Krubitzer_Kaas_1990", "Felleman_VanEssen_1991_Table2" = "Felleman_VanEssen_1991",
                   "Preuss_Kaas_1996_ResultsText" = "Preuss_Kaas_1996", "Krubitzer_etal_1997_ResultsText" = "Krubitzer_etal_1997")
rel <- uncon %>% filter(needed_denominator_term == "CorticalSurface_Area.mm2") %>%
  mutate(paper = unname(item_to_paper[source]), abs_term = sub("\\.pct_.*$", ".mm2", Standardized_Term))
conv <- bind_rows(
  rel %>% inner_join(den_same_source %>% rename(den_source = source), by = c("Species", "source" = "den_source")),
  rel %>% inner_join(den_merge, by = "Species"),
  rel %>% inner_join(den_fm_paper %>% rename(den_paper = paper), by = c("Species", "paper" = "den_paper")),
  rel %>% inner_join(den_fm_species, by = "Species")
) %>%
  mutate(derived_mm2 = value * denominator_mm2 / 100,
         derivation = sprintf("%s %s %% x %s mm2 / 100 [%s]", Standardized_Term, signif(value, 5), signif(denominator_mm2, 6), assumption),
         caveat = case_when(
           status != "active" ~ paste0("relative value is held in the merge (", status, ")"),
           value_status == "approximate" ~ "printed percentage is approximate",
           str_detect(coalesce(denominator_definition, ""), "cortical mantle|adjusted") ~ "source denominator definition differs from neocortex total",
           TRUE ~ "")) %>%
  select(Species, source, specimen, grain, relative_term = Standardized_Term, pct_value = value, value_status, status,
         denominator_definition, assumption, denominator_mm2, denominator_provenance, n_individuals_in_denominator = n_individuals,
         derived_term = abs_term, derived_mm2, derivation, caveat) %>%
  arrange(Species, source, specimen, relative_term, assumption)
wr(conv, "relative_converted_external.csv")
wr(rel %>% anti_join(conv %>% distinct(Species, source, specimen, relative_term),
                     by = c("Species", "source", "specimen", "Standardized_Term" = "relative_term")) %>%
     select(Species, source, specimen, Standardized_Term, value, status, reason),
   "relative_still_unconverted.csv")

# ---- validation: flatmap-traced % vs published % (Krubitzer & Kaas 1990 Table 1) -----------------
pub <- long %>% filter(source == "Krubitzer_Kaas_1990_Table1", str_detect(Standardized_Term, "pct_Neocortex")) %>%
  group_by(Species, Standardized_Term) %>%
  summarise(published_mean_pct = mean(value), published_min = min(value), published_max = max(value), n_cases_published = n(), .groups = "drop")
traced <- flat_pct %>% filter(source == "Flatmap::Krubitzer_Kaas_1990", recommend_use) %>%
  group_by(Species, Standardized_Term) %>%
  summarise(traced_mean_pct = mean(value), traced_min = min(value), traced_max = max(value), n_cases_traced = n(),
            traced_specimens = paste(specimen, collapse = "|"), .groups = "drop")
cmp <- full_join(pub, traced, by = c("Species", "Standardized_Term")) %>%
  mutate(ratio_traced_to_published = traced_mean_pct / published_mean_pct,
         verdict = case_when(is.na(traced_mean_pct) ~ "no usable traced value",
                             is.na(published_mean_pct) ~ "not in Table 1",
                             abs(ratio_traced_to_published - 1) <= 0.15 ~ "agrees within 15%",
                             abs(ratio_traced_to_published - 1) <= 0.30 ~ "15-30% apart",
                             TRUE ~ "DISAGREES (>30%)")) %>%
  arrange(Species, Standardized_Term)
wr(cmp, "flatmap_vs_published_pct_KrubitzerKaas1990.csv")
print(as.data.frame(cmp %>% filter(!is.na(ratio_traced_to_published)) %>%
        transmute(Species, term = sub("_Surface_Area.pct_Neocortex", "", Standardized_Term),
                  published = round(published_mean_pct, 2), traced = round(traced_mean_pct, 2),
                  ratio = round(ratio_traced_to_published, 2), n_pub = n_cases_published, n_traced = n_cases_traced, verdict)))
message("conversions: ", nrow(conv), " derived rows over ", n_distinct(conv$assumption), " assumptions; ",
        n_distinct(paste(conv$Species, conv$source, conv$specimen, conv$relative_term)), " relative values covered")
