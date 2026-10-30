# Flatmap surface-area analysis report

Generated 2026-10-21 01:13 from `flatmap_measurements/*/data/measurements.csv`.

## Input coverage

- 31 paper folders read (28 with measurement rows); 3038 measurement rows; 1387 rows with calibrated area (mm2); 54 species.

## Row-level usability tiers (data/02_flag_counts.csv)

| usability_tier | n |
|---|---|
| A_field_complete_identified |  440 |
| A_outline_complete_identified |   19 |
| B_complete_unidentified_specimen |   11 |
| C_incomplete_or_section |  348 |
| D_not_a_specimen_view |  569 |
| X_no_calibrated_area | 1651 |

Only tier `A_*` rows enter per-specimen averages. `C_incomplete_or_section` rows are partial extents, approximate borders, single sections/zooms, insets or component labels: they do not give the full surface area of the region. `D_not_a_specimen_view` rows are illustrative, composite or schematic drawings. `B_*` rows are complete but cannot be attributed to an identified animal.

## Per-specimen averages (data/03_specimen_region_means.csv)

- 618 specimen x region combinations; 88 measured in more than one view; 42 averaged over >1 usable view; 6 where usable views disagree by CV > 0.25.

### Specimens whose repeated views disagree

| species | paper | specimen | label | n_views_usable | mean_mm2 | min_mm2 | max_mm2 | cv_within_specimen | map_ids_usable |
|---|---|---|---|---|---|---|---|---|---|
| Callithrix jacchus | Krubitzer_Kaas_1990 | 87-51 | DL | 2 | 25.090 | 19.070 | 31.110 | 0.3392 | fig21|fig26C |
| Didelphis virginiana | Beck_etal_1996 | 93-59 | PV | 2 |  8.922 |  6.895 | 10.950 | 0.3213 | fig02_93_59|fig08 |
| Didelphis virginiana | Beck_etal_1996 | 93-88 | S1 | 2 | 19.720 | 12.690 | 26.750 | 0.5043 | fig03_93_88|fig16 |
| Didelphis virginiana | Beck_etal_1996 | 93-88 | S2 | 2 | 12.030 |  9.665 | 14.400 | 0.2784 | fig03_93_88|fig16 |
| Sciurus carolinensis | Luethke_etal_1988 | 85-90 | A-I | 2 |  4.832 |  3.900 |  5.764 | 0.2728 | fig03|fig03inset |
| Tupaia belangeri | Lyon_etal_1998 | 96-43 | V1 | 2 | 75.630 | 62.240 | 89.020 | 0.2504 | fig09_C|fig11_A |

## Plausibility given species and region (data/04_specimen_region_means_flagged.csv)

| plausibility | n |
|---|---|
| FLAG: implausible for species/region |  24 |
| no usable value | 212 |
| plausible | 152 |
| usable with caution | 230 |

### Specimens whose regions deviate together (suspected scale/calibration offset)

| species | paper | specimen | n_regions_compared | specimen_median_z | specimen_median_ratio |
|---|---|---|---|---|---|
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | 17 | -2.57 | 0.586 |
| Saimiri sciureus | Krubitzer_Kaas_1993 | 92-8 |  4 |  9.89 | 3.070 |

### Hard flags (recommend_use = FALSE)

| species | paper | specimen | label | mean_mm2 | n_views_usable | robust_z | fraction_of_neocortex | hard_flags |
|---|---|---|---|---|---|---|---|---|
| Aotus trivirgatus | Krubitzer_Kaas_1990 | 88-7 | DM |   49.400 | 1 |   5.302 | 0.027250 | robust z beyond 3.0 and >= 2.0-fold from species x region median |
| Callithrix jacchus | Krubitzer_Kaas_1993 | 89-78 | PV |    5.669 | 1 |  11.790 | 0.006659 | robust z beyond 3.0 and >= 2.0-fold from species x region median |
| Galago senegalensis | Krubitzer_Kaas_1993 | 89-11 | SII |    8.901 | 1 |   3.814 | 0.015740 | robust z beyond 3.0 and >= 2.0-fold from species x region median |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | 1 |   18.160 | 1 |  -2.979 | 0.008507 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | 17 |  360.600 | 1 | -11.410 | 0.168900 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | 18 |  155.600 | 1 |  -1.390 | 0.072870 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | 2 |   15.910 | 1 |  -3.041 | 0.007454 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | 3a |   15.480 | 1 |  -2.570 | 0.007252 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | 3b |   28.020 | 1 |  -3.288 | 0.013120 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | DI |   14.730 | 1 |  -4.728 | 0.006899 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | DL |   96.030 | 1 |  -1.015 | 0.044980 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | DM |   23.720 | 1 |  -6.228 | 0.011110 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | FEF |    7.380 | 1 |  -1.820 | 0.003456 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | FST |   37.790 | 1 |  -5.185 | 0.017700 | robust z beyond 3.0 and >= 2.0-fold from species x region median; all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | FV |    5.388 | 1 |  -1.353 | 0.002524 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | MST |   13.320 | 1 |  -1.671 | 0.006241 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | MT |   18.610 | 1 |  -2.504 | 0.008717 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | PV/IG |    9.123 | 1 |  -1.495 | 0.004273 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | SII |    7.798 | 1 |  -1.842 | 0.003652 | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1990 | 87-25 | Neocortex outline | 2135.000 | 1 |  -3.678 |  | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1993 | 92-8 | 17 | 2202.000 | 1 |  30.540 | 0.367600 | robust z beyond 3.0 and >= 2.0-fold from species x region median; all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1993 | 92-8 | DM |  112.100 | 1 |  12.460 | 0.018720 | robust z beyond 3.0 and >= 2.0-fold from species x region median; all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1993 | 92-8 | MT |  129.800 | 1 |   4.040 | 0.021670 | robust z beyond 3.0 and >= 2.0-fold from species x region median; all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |
| Saimiri sciureus | Krubitzer_Kaas_1993 | 92-8 | Neocortex outline | 5989.000 | 1 |   7.322 |  | all regions of this specimen offset from species medians in the same direction (check calibration; may also be an unusually small/large individual) |

Checks: robust z on log10 area within species x region_group (>= 3 specimens; aliases in `reference/label_crosswalk.csv`); fraction of the specimen's own neocortex outline (else species reference, else species median outline) against bounds in `reference/region_fraction_bounds.csv` or the generic defaults in `R/00_config.R`; and unusual mm/pixel calibration in a contributing view.

## Species x region summary (data/05_species_region_summary.csv)

| species | label | n_specimens | n_papers | mean_mm2 | sd_mm2 | min_mm2 | max_mm2 | n_flagged_excluded |
|---|---|---|---|---|---|---|---|---|
| Aotus trivirgatus | DM | 6 | 2 |  23.820 |  |  23.820 |  23.820 | 1 |
| Aotus trivirgatus | 17 | 5 | 2 | 219.000 |  | 219.000 | 219.000 | 0 |
| Aotus trivirgatus | FST | 5 | 2 |  26.010 |  |  26.010 |  26.010 | 0 |
| Aotus trivirgatus | MT | 5 | 2 |  29.150 |  |  29.150 |  29.150 | 0 |
| Aotus trivirgatus | FEF | 3 | 2 |   5.469 |  |   5.469 |   5.469 | 0 |
| Aotus trivirgatus | FV | 3 | 2 |   6.054 |  |   6.054 |   6.054 | 0 |
| Aotus trivirgatus | MST | 3 | 2 |  24.930 |  |  24.930 |  24.930 | 0 |
| Aotus trivirgatus | 18 | 2 | 1 | 137.000 |  | 137.000 | 137.000 | 0 |
| Aotus trivirgatus | 3b | 2 | 2 |  40.220 |  |  40.220 |  40.220 | 0 |
| Aotus trivirgatus | AI | 2 | 2 |  13.350 |  |  13.350 |  13.350 | 0 |
| Aotus trivirgatus | DI | 2 | 1 |  25.460 |  |  25.460 |  25.460 | 0 |
| Aotus trivirgatus | DL | 2 | 1 |  53.490 |  |  53.490 |  53.490 | 0 |
| Aotus trivirgatus | PV | 2 | 2 |   9.483 |  |   9.483 |   9.483 | 0 |
| Aotus trivirgatus | SII | 2 | 2 |  10.430 |  |  10.430 |  10.430 | 0 |
| Callithrix jacchus | 17 | 3 | 2 | 121.300 |  | 121.300 | 121.300 | 0 |
| Callithrix jacchus | 18 | 3 | 2 |  61.600 |  |  61.600 |  61.600 | 0 |
| Callithrix jacchus | 3a | 3 | 2 |  11.530 |  |  11.530 |  11.530 | 0 |
| Callithrix jacchus | 3b | 3 | 2 |  20.810 |  |  20.810 |  20.810 | 0 |
| Callithrix jacchus | AI | 3 | 2 |   4.551 |  |   4.551 |   4.551 | 0 |
| Callithrix jacchus | DM | 3 | 2 |  10.550 |  |  10.550 |  10.550 | 0 |
| Callithrix jacchus | FEF | 3 | 2 |   2.653 |  |   2.653 |   2.653 | 0 |
| Callithrix jacchus | FST | 3 | 2 |  12.710 |  |  12.710 |  12.710 | 0 |
| Callithrix jacchus | FV | 3 | 2 |   3.862 |  |   3.862 |   3.862 | 0 |
| Callithrix jacchus | MT | 3 | 2 |  14.440 |  |  14.440 |  14.440 | 0 |
| Callithrix jacchus | SII | 3 | 2 |   3.807 |  |   3.807 |   3.807 | 0 |
| Callithrix jacchus | DI | 2 | 1 |  11.130 |  |  11.130 |  11.130 | 0 |
| Callithrix jacchus | DL | 2 | 1 |  24.580 |  |  24.580 |  24.580 | 0 |
| Callithrix jacchus | MST | 2 | 1 |  10.340 |  |  10.340 |  10.340 | 0 |
| Callithrix jacchus | PV | 2 | 1 |   2.422 |  |   2.422 |   2.422 | 1 |
| Cebus apella (source taxonomy) | V1 | 6 | 1 | 792.700 |  | 792.700 | 792.700 | 0 |
| Dasyurus hallucatus | C | 2 | 1 |   2.896 |  |   2.896 |   2.896 | 0 |
| Dasyurus hallucatus | SII/PV | 2 | 1 |   3.055 |  |   3.055 |   3.055 | 0 |
| Didelphis virginiana | PV | 9 | 1 |   9.640 |  |   9.640 |   9.640 | 0 |
| Didelphis virginiana | S1 | 9 | 1 |  20.990 |  |  20.990 |  20.990 | 0 |
| Didelphis virginiana | S2 | 9 | 1 |  14.150 |  |  14.150 |  14.150 | 0 |
| Didelphis virginiana | Aud | 2 | 1 |   8.934 |  |   8.934 |   8.934 | 0 |
| Didelphis virginiana | CT | 2 | 1 |   6.757 |  |   6.757 |   6.757 | 0 |
| Didelphis virginiana | SC | 2 | 1 |  18.630 |  |  18.630 |  18.630 | 0 |
| Didelphis virginiana | SR | 2 | 1 |   9.582 |  |   9.582 |   9.582 | 0 |
| Didelphis virginiana | V1 | 2 | 1 |  42.440 |  |  42.440 |  42.440 | 0 |
| Didelphis virginiana | V2 | 2 | 1 |  19.760 |  |  19.760 |  19.760 | 0 |
| Echinops telfairi | A | 2 | 1 |   1.194 |  |   1.194 |   1.194 | 0 |
| Echinops telfairi | PV/S2 | 2 | 1 |   1.366 |  |   1.366 |   1.366 | 0 |
| Echinops telfairi | S1 | 2 | 1 |   2.545 |  |   2.545 |   2.545 | 0 |
| Echinops telfairi | V | 2 | 1 |   1.607 |  |   1.607 |   1.607 | 0 |
| Galago senegalensis | 17 | 4 | 2 | 102.700 |  | 102.700 | 102.700 | 0 |
| Galago senegalensis | 18 | 4 | 2 |  37.730 |  |  37.730 |  37.730 | 0 |
| Galago senegalensis | 3b | 4 | 2 |  35.270 |  |  35.270 |  35.270 | 0 |
| Galago senegalensis | AI | 4 | 2 |   7.095 |  |   7.095 |   7.095 | 0 |
| Galago senegalensis | DL | 4 | 2 |  16.560 |  |  16.560 |  16.560 | 0 |
| Galago senegalensis | DM | 4 | 2 |   7.234 |  |   7.234 |   7.234 | 0 |
| Galago senegalensis | FST | 4 | 2 |  13.880 |  |  13.880 |  13.880 | 0 |
| Galago senegalensis | MST | 4 | 2 |  11.890 |  |  11.890 |  11.890 | 0 |
| Galago senegalensis | MT | 4 | 2 |  14.750 |  |  14.750 |  14.750 | 0 |
| Galago senegalensis | PV | 3 | 2 |   5.472 |  |   5.472 |   5.472 | 0 |
| Galago senegalensis | SII | 3 | 1 |   3.367 |  |   3.367 |   3.367 | 1 |
| Galago senegalensis | DI | 2 | 1 |   4.498 |  |   4.498 |   4.498 | 0 |
| Galago senegalensis | FV | 2 | 1 |   3.291 |  |   3.291 |   3.291 | 0 |
| Galago senegalensis | M | 2 | 1 |  13.050 |  |  13.050 |  13.050 | 0 |
| Monodelphis domestica | A | 2 | 1 |   2.152 |  |   2.152 |   2.152 | 0 |
| Monodelphis domestica | CT | 2 | 1 |   3.860 |  |   3.860 |   3.860 | 0 |
| Monodelphis domestica | SI | 2 | 1 |   7.854 |  |   7.854 |   7.854 | 0 |
| Monodelphis domestica | VI | 2 | 1 |  13.080 |  |  13.080 |  13.080 | 0 |
| Nycticebus coucang | Aud (auditory complex) | 2 | 1 |  24.380 |  |  24.380 |  24.380 | 0 |
| Pteropus poliocephalus | MT | 7 | 1 |  11.270 |  |  11.270 |  11.270 | 0 |
| Pteropus poliocephalus | A-I | 5 | 1 |   5.015 |  |   5.015 |   5.015 | 0 |
| Pteropus poliocephalus | 17 | 3 | 1 | 100.700 |  | 100.700 | 100.700 | 0 |
| Pteropus poliocephalus | FV | 3 | 1 |   2.487 |  |   2.487 |   2.487 | 0 |
| Pteropus poliocephalus | SII | 3 | 1 |   6.694 |  |   6.694 |   6.694 | 0 |
| Saguinus fuscicollis | MT | 2 | 1 |  15.580 |  |  15.580 |  15.580 | 0 |
| Saimiri sciureus | MT | 5 | 1 |  37.120 |  |  37.120 |  37.120 | 2 |
| Saimiri sciureus | 1 | 4 | 1 |  29.230 |  |  29.230 |  29.230 | 1 |
| Saimiri sciureus | 17 | 4 | 1 | 591.200 |  | 591.200 | 591.200 | 2 |
| Saimiri sciureus | 18 | 4 | 1 | 243.500 |  | 243.500 | 243.500 | 1 |
| Saimiri sciureus | 2 | 4 | 1 |  24.060 |  |  24.060 |  24.060 | 1 |
| Saimiri sciureus | 3a | 4 | 1 |  39.930 |  |  39.930 |  39.930 | 1 |
| Saimiri sciureus | 3b | 4 | 1 |  50.630 |  |  50.630 |  50.630 | 1 |
| Saimiri sciureus | DI | 4 | 1 |  30.600 |  |  30.600 |  30.600 | 1 |
| Saimiri sciureus | DL | 4 | 1 | 127.400 |  | 127.400 | 127.400 | 1 |
| Saimiri sciureus | DM | 4 | 1 |  40.050 |  |  40.050 |  40.050 | 2 |
| Saimiri sciureus | FEF | 4 | 1 |  18.300 |  |  18.300 |  18.300 | 1 |
| Saimiri sciureus | FST | 4 | 1 |  84.270 |  |  84.270 |  84.270 | 1 |
| Saimiri sciureus | MST | 4 | 1 |  33.820 |  |  33.820 |  33.820 | 1 |
| Saimiri sciureus | PV/IG | 4 | 1 |  16.840 |  |  16.840 |  16.840 | 1 |
| Saimiri sciureus | SII | 4 | 1 |  17.640 |  |  17.640 |  17.640 | 1 |
| Saimiri sciureus | FV | 3 | 1 |  18.250 |  |  18.250 |  18.250 | 1 |
| Sciurus carolinensis | R | 3 | 1 |   3.298 |  |   3.298 |   3.298 | 0 |
| Sciurus carolinensis | 17 | 2 | 1 |  25.230 |  |  25.230 |  25.230 | 0 |
| Sciurus carolinensis | A-I | 2 | 1 |   3.930 |  |   3.930 |   3.930 | 0 |
| Sciurus carolinensis | M | 2 | 1 |  27.070 |  |  27.070 |  27.070 | 0 |
| Sciurus carolinensis | S-II | 2 | 1 |   4.896 |  |   4.896 |   4.896 | 0 |
| Sciurus carolinensis | TAi | 2 | 1 |   3.299 |  |   3.299 |   3.299 | 0 |
| Sciurus carolinensis | TArv + TAcv | 2 | 1 |   5.739 |  |   5.739 |   5.739 | 0 |
| Sciurus carolinensis | TP | 2 | 1 |  22.920 |  |  22.920 |  22.920 | 0 |
| Sciurus carolinensis | UZ | 2 | 1 |   1.857 |  |   1.857 |   1.857 | 0 |
| Tachyglossus aculeatus | A | 3 | 1 |  10.590 |  |  10.590 |  10.590 | 0 |
| Tupaia belangeri | TI | 4 | 1 |   6.555 |  |   6.555 |   6.555 | 0 |
| Tupaia belangeri | A | 3 | 1 |  13.670 |  |  13.670 |  13.670 | 0 |
| Tupaia belangeri | V1 | 3 | 1 |  74.580 |  |  74.580 |  74.580 | 0 |
| Tupaia belangeri | S | 2 | 1 |  30.280 |  |  30.280 |  30.280 | 0 |

## Figures

- figures/species_region_dotplot_Aotus_trivirgatus.png
- figures/species_region_dotplot_Callithrix_jacchus.png
- figures/species_region_dotplot_Cebus_apella_source_taxonomy_.png
- figures/species_region_dotplot_Dactylopsila_trivirgata.png
- figures/species_region_dotplot_Dasyurus_hallucatus.png
- figures/species_region_dotplot_Didelphis_virginiana.png
- figures/species_region_dotplot_Echinops_telfairi.png
- figures/species_region_dotplot_Galago_senegalensis.png
- figures/species_region_dotplot_Heterocephalus_glaber.png
- figures/species_region_dotplot_Miopithecus_talapoin.png
- figures/species_region_dotplot_Monodelphis_domestica.png
- figures/species_region_dotplot_Pteropus_poliocephalus.png
- figures/species_region_dotplot_Saguinus_fuscicollis.png
- figures/species_region_dotplot_Saimiri_sciureus.png
- figures/species_region_dotplot_Sciurus_carolinensis.png
- figures/species_region_dotplot_Tachyglossus_aculeatus.png
- figures/species_region_dotplot_Tupaia_belangeri.png
- figures/regiongroup_across_species.png
