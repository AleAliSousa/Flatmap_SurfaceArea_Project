# Pre-analysis: relative <-> absolute cortical surface areas (outside the data repo)

This folder holds the **assumption-bearing** step that the Evo-M1-Trait-Data merge deliberately does
not perform. Division of labour:

| Where | What happens | Assumption |
|---|---|---|
| `Evo-M1-Trait-Data/__merging_cortical_areas` | Relative (`*_Surface_Area.pct_*`) and absolute (`*_Surface_Area.mm2`) terms listed side by side in `cortical_areas_long.csv`. A percentage is converted to mm2 **only** with a denominator measured on the **same specimen** (same source, or a `confirmed` row in `specimen_links.csv`). Printed-vs-recomputed checks. Unconvertible rows go to `cortical_areas_relative_unconverted.csv`. | none (exact arithmetic) |
| **here** | Every relative value the merge could not convert is multiplied by each *candidate* species-level denominator, one output row per candidate, labelled with its `assumption`. Flatmap specimen means are expressed in merge terms and compared with published percentages. | explicit, per row |

Run `Rscript run_preanalysis.R` after `../run_all.R` (flatmap summaries) and the merge's
`cortical_areas_compiled.R`. The merge folder is found at
`../../../Species/Evo-M1-Trait-Data/__merging_cortical_areas`; override with the environment
variable `CORTICAL_AREAS_MERGE_DIR`.

## Outputs (`data/`)

- `relative_converted_external.csv` -- one row per (relative value x denominator option): `pct_value`,
  `assumption`, `denominator_mm2`, `denominator_provenance`, `derived_mm2`, `derivation`, `caveat`.
  **Pick one assumption per analysis; never average across assumptions.**
- `denominator_options.csv` -- candidate neocortex denominators per species with provenance.
- `relative_still_unconverted.csv` -- relative rows with no candidate denominator at all (currently the
  60 held Seelke 2016 group means and Preuss & Kaas 1996, whose only denominator is its own inversion).
- `flatmap_long_standardized.csv` -- flatmap per-specimen means (`recommend_use`, plausibility flags
  carried) as `Flatmap::<paper>` sources in merge vocabulary: absolute mm2 and % of the specimen's own
  traced neocortex outline. Not yet a registered dataset item; this file is the staging form.
- `flatmap_labels_without_merge_term.csv` -- flatmap region groups with no standardized term yet.
- `flatmap_vs_published_pct_KrubitzerKaas1990.csv` -- traced % of neocortex vs Krubitzer & Kaas 1990
  Table 1 printed % per species and field; the most direct check of the new tracings.

## Assumptions offered

1. `species_mean_same_source` -- the same paper's individual neocortex totals averaged (Catania & Remple 2002).
2. `species_mean_merge_wide` -- the merge's pooled species mean; may mix flattened (Kaas lab) and
   reconstructed (Mota) surfaces; `conflict_flag` is echoed in the provenance text. For the Krubitzer &
   Kaas species this denominator is 1.7-2.3x the flattened outlines (Saimiri 5,250 vs 3,015 mm2; Aotus
   2,214 vs 1,431; Callithrix 1,534 vs 655), so derived field areas differ by the same factor.
3. `flatmap_same_paper_median` -- median traced neocortex outline of the same paper's whole-hemisphere
   cases: same lab, same preparation, same figures, but animals not yet linked one-to-one to Table 1
   case numbers. Once linked (`specimen_links.csv` -> `confirmed`), those conversions move into the
   merge as exact same-specimen derivations and disappear from here.
4. `flatmap_species_median` -- median traced outline across all papers for the species.

Denominator definitions differ between sources (neocortex total; adjusted cortical sheet minus
cingulate; cortical mantle = isocortex + proisocortex). The `denominator_definition` and `caveat`
columns carry that forward; they are not reconciled here.

## First-run findings (2026-10-21)

- 451 derived rows covering 162 relative values under 4 assumptions.
- Flatmap tracings vs Table 1: 25 of 32 species x field percentages agree within 15%, 6 are 15-30%
  apart (Aotus V1, Callithrix DI/MST/MT, Galago DI, Saimiri MST), 1 disagrees strongly: **Saimiri DM** published
  0.38% (cases 0.2-0.8%) vs traced 1.31% -- check the DM contours in the Krubitzer_Kaas_1990 figures.
