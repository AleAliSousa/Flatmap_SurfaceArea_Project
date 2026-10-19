# Surface-area analysis

Summaries and quality flags built from the flatmap measurements in `../flatmap_measurements/*/data/measurements.csv`.
Nothing here edits the measurements; every table is regenerated from the current CSVs.

```sh
cd surface_area_analysis
Rscript run_all.R            # rebuilds data/, figures/, reports/
```

Requires R with dplyr, readr, tidyr, stringr, purrr, forcats, ggplot2. Each `R/0N_*.R` script can also be run
alone (`Rscript R/03_specimen_means.R`); it then reads the previous step's CSV from `data/`.

## Pipeline

| Script | What it does | Main output |
|---|---|---|
| `R/00_config.R` | Paths, controlled vocabularies and all thresholds (`cfg`). Edit thresholds here. | – |
| `R/01_load_measurements.R` | Reads every paper's `measurements.csv`, harmonises columns and vocabulary (extent spellings, link status, hemisphere side), one row per paper × map_id × label. | `data/01_all_measurements.csv` |
| `R/02_flag_completeness.R` | Row-level flags for data that do **not** give the full surface area of a region, and a usability tier. | `data/02_measurements_flagged.csv`, `data/02_excluded_rows.csv`, `data/02_flag_counts.csv` |
| `R/03_specimen_means.R` | Averages the same label across the different views (figures/panels/sections) of one specimen: mean, SD, CV, min/max, contributing and excluded map_ids, hemisphere mixing. | `data/03_specimen_region_means.csv`, `data/03_multi_view_regions.csv` |
| `R/04_flag_outliers.R` | Plausibility of each specimen-region mean given species and region (see below). | `data/04_specimen_region_means_flagged.csv`, `data/04_plausibility_flags_long.csv`, `data/04_specimen_scale_offsets.csv`, `data/04_species_neocortex_from_data.csv`, `data/04_view_scale_factor_check.csv` |
| `R/05_species_summary.R` | Species × region tables from the recommended specimen means; dot plots; markdown report. | `data/05_species_region_summary.csv`, `data/05_species_regiongroup_summary.csv`, `figures/*.png`, `reports/analysis_report.md` |

## Completeness rules (script 02)

A row enters a per-specimen average (`use_for_specimen_mean = TRUE`, tier `A_*`) only if all of these hold:

- `area_mm2` is present (calibrated). Pixel-only, `not_measurable` and `not_yet_digitized` rows are tier `X`.
- `extent == "complete"`. `partial`, `approximate` and `approximate_complete` are tier `C` (set `cfg$include_approximate_complete = TRUE` to admit `approximate_complete`).
- The view is not a single histological/tangential section, zoom or laminar reconstruction (tier `C`; the project data contract keeps sections separate; `cfg$allow_section_views`).
- The view is a measurement of an animal, not an illustrative summary, species/literature summary, composite parcellation, schematic or redrawn map (tier `D`).
- The label does not denote a piece of a field (`... mapped component 2`, `visible fragment`, `mapped extent`, `island`, `?`, `historical`).
- The `boundary_note` does not state that the field is truncated/incomplete/not total.
- Outline rows count only if `outline_scope == "whole_drawn_neocortex"` (they become the neocortex denominator).
- The specimen is identified (`not reported`, `illustrative summary`, `atlas carrier` … are tier `B`: complete but unattributable).

Per-field `extent` and `boundary_note` are the authority; a complete field drawn inside a partial view (inset, contralateral piece, strip) is kept and receives a warning. `exclusion_reasons` and `warnings` columns say exactly why each row was excluded or cautioned.

## Plausibility rules (script 04)

Hard flags (`recommend_use = FALSE`, `plausibility = "FLAG: …"`):

1. **Species × region outlier** — robust z on log10 area (median/MAD) across specimens and papers within `species × region_group`, needing ≥ `cfg$min_n_for_comparison` (3) specimens, |z| > 3 **and** ≥ 2-fold from the group median (the fold rule prevents tiny-MAD artefacts at n = 3–4).
2. **Whole-specimen offset** — ≥ 3 regions of one specimen all deviate in the same direction with |median z| > 2. Reported per specimen in `04_specimen_scale_offsets.csv`; usually a calibration/scale problem, occasionally a genuinely small or large individual — check the source scale bar.
3. **Fraction of neocortex** — region mean ÷ the specimen's own whole-neocortex outline (else `reference/species_neocortex_reference.csv`, else the species median outline in this dataset) outside the bounds in `reference/region_fraction_bounds.csv` or the generic 0.05 %–40 % defaults; or larger than the denominator.
4. **Unusual calibration** — a contributing view's mm/pixel is > 3 robust SD from the dataset median.

Soft flags (`plausibility = "usable with caution"`): borderline z (2.5–3), views of the same specimen disagree (CV > 0.25), views from different hemispheres averaged, an excluded partial/section view is larger than the usable mean, too few comparable specimens, no neocortex denominator, view-level warnings.

## Editable reference tables

- `reference/label_crosswalk.csv` — literal source label → `region_group`. Used **only** for cross-paper comparison and the region-group summary; specimen means always keep the literal label. Defaults: literal label, plus explicit aliases for 17/V1/VI, 18/V2/VII, 3b/S1/SI, S2/SII, A-I/AI and the three outline labels. Edit if a paper's definition differs.
- `reference/region_fraction_bounds.csv` — per-region-group plausible fraction of neocortex; blank = generic defaults.
- `reference/species_neocortex_reference.csv` — optional literature neocortex area (one hemisphere, mm²) per species; overrides the dataset-derived median as denominator.

## Reading the main table

`data/04_specimen_region_means_flagged.csv`, one row per paper × species × specimen × label:
`mean_mm2` (over usable views), `n_views_usable` / `n_views_calibrated`, `sd_mm2`, `cv_within_specimen`, `map_ids_usable`, `map_ids_excluded`, `excluded_view_reasons`, `plausibility`, `recommend_use`, `hard_flags`, `soft_flags`, `robust_z`, `ratio_to_group_median`, `fraction_of_neocortex`, `denominator_source`. `mean_mm2_all_views` additionally averages the partial/section views and is for reference only.
