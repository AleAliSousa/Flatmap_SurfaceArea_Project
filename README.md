# Flatmap Surface Area Project

Reproducible measurements of cortical flatmaps from published or unpublished source material. Each publication has its own folder under `flatmap_measurements/`, with original source provenance, editable ImageJ tracings, measurement tables and visual review.

## Reusable skill

[Read the flatmap-surface-area skill](skills/flatmap-surface-area/SKILL.md). It covers paper inventory, calibration, tracing, measurement, ImageJ exports, missing values, species/case summaries and optional comparison with reference measurements.

For Codex, invoke `$flatmap-surface-area`. Collaborators can copy `skills/flatmap-surface-area/` into their personal Codex skills directory. On macOS/Linux, link this checkout instead to keep the installed skill aligned with the repository. From the repository root, if no installation with this name already exists:

```sh
mkdir -p "$HOME/.codex/skills"
ln -s "$PWD/skills/flatmap-surface-area" "$HOME/.codex/skills/flatmap-surface-area"
```

The instructions and Python/R helpers are also usable without Codex. The [skill's data contract](skills/flatmap-surface-area/references/data-contract.md) documents the inputs. Python helpers need numpy, Pillow and pypdfium2; native ImageJ export uses Java 17+ and ImageJ/Fiji. The summary helper uses base R.

## Optional comparison

Core measurements, ImageJ editing and source-versus-tracing review work without reference values. Create `comparison/` only when reference data are available and comparison is part of the task. Always retain `review/` for checking the actual traces. No reference match is required to process a paper.

## Anatomical tracing rule

Letters, numbers, labels and recording/stimulation symbols are annotations. They do not change surface area and must never create holes, notches or extra boundaries in a field. Trace the anatomical perimeter; where a label covers it, continue the visible anatomical curve smoothly across the overprint. For an external label with a leader, identify and trace the tissue compartment at the other end of that line. The leader and the location of its letters must not define the field boundary.

## Datasets and queue

<!-- workbook-pdf-batch-2026-10-20 -->
[Workbook PDF batch: 10 papers, 91 numbered figures, 57 traced views and 539 provisional field/component measurements](flatmap_measurements/review_workbook_batch_2026-10-20.html). Native ImageJ exports are verified. Thirty-five unresolved Rosa boundaries remain explicit NA; Haug has no eligible planar field contours. [Methods and limits](reports/workbook_batch_2026-10-20/README.md).

<!-- missing-region-actions-completed -->
[Completed missing-region actions: 28 additions and one corrected contour](flatmap_measurements/review_missing_region_actions.html). All listed audit actions now have recorded outcomes; unresolved source boundaries remain explicit NA.

[Tracing method recorded after the Felleman correction](flatmap_measurements/tracing_method.md) · [20 October missing-region audit and review queue](flatmap_measurements/missing_region_audit_2026-10-20/index.html). The new audit identifies unfinished tracings and omissions; the historical recheck below is not evidence that all fields are complete.

[Latest full-dataset contour recheck](flatmap_measurements/review_full_dataset_audit.html): all 21 papers and 370 numbered figures rechecked on 16 October 2026. [Methods and remaining source limits](flatmap_measurements/full_dataset_recheck.md). Counts below are field/component observations, including repeated and illustrative views, not animals.

| Paper | Current contours |
|---|---:|
| [Beck_Kaas_1998](flatmap_measurements/Beck_Kaas_1998/README.md) | 5 |
| [Beck_etal_1996](flatmap_measurements/Beck_etal_1996/README.md) | 58 |
| [Felleman_VanEssen_1991](flatmap_measurements/Felleman_VanEssen_1991/README.md) | 74 |
| [Huffman_etal_1999](flatmap_measurements/Huffman_etal_1999/README.md) | 76 |
| [Kaas_etal_2011](flatmap_measurements/Kaas_etal_2011/README.md) | 0 |
| [Krubitzer_1995](flatmap_measurements/Krubitzer_1995/README.md) | 31 |
| [Krubitzer_1998](flatmap_measurements/Krubitzer_1998/README.md) | 65 |
| [Krubitzer_Kaas_1990](flatmap_measurements/Krubitzer_Kaas_1990/README.md) | 354 |
| [Krubitzer_Kaas_1993](flatmap_measurements/Krubitzer_Kaas_1993/README.md) | 107 |
| [Krubitzer_etal_1993](flatmap_measurements/Krubitzer_etal_1993/README.md) | 100 |
| [Krubitzer_etal_1995](flatmap_measurements/Krubitzer_etal_1995/README.md) | 21 |
| [Krubitzer_etal_1997](flatmap_measurements/Krubitzer_etal_1997/README.md) | 15 |
| [Luethke_etal_1988](flatmap_measurements/Luethke_etal_1988/README.md) | 102 |
| [Luethke_etal_1989](flatmap_measurements/Luethke_etal_1989/README.md) | 41 |
| [Lyon_etal_1998](flatmap_measurements/Lyon_etal_1998/README.md) | 33 |
| [Manger_etal_2002](flatmap_measurements/Manger_etal_2002/README.md) | 6 |
| [Preuss_Kaas_1996](flatmap_measurements/Preuss_Kaas_1996/README.md) | 3 |
| [Preuss_etal_1993](flatmap_measurements/Preuss_etal_1993/README.md) | 10 |
| [Slutsky_etal_2000](flatmap_measurements/Slutsky_etal_2000/README.md) | 15 |
| [VanEssen_Drury_1997](flatmap_measurements/VanEssen_Drury_1997/README.md) | 0 |
| [Zilles_1985](flatmap_measurements/Zilles_1985/README.md) | 0 |
| [Brecht_Freiwald_2012](flatmap_measurements/Brecht_Freiwald_2012/README.md) | 14 |
| [Catania_Remple_2002](flatmap_measurements/Catania_Remple_2002/README.md) | 15 |
| [Haug_1987](flatmap_measurements/Haug_1987/README.md) | 0 |
| [Krubitzer_2009](flatmap_measurements/Krubitzer_2009/README.md) | 109 |
| [Krubitzer_Dooley_2013](flatmap_measurements/Krubitzer_Dooley_2013/README.md) | 135 |
| [Krubitzer_Prescott_2018](flatmap_measurements/Krubitzer_Prescott_2018/README.md) | 34 |
| [Mayer_etal_2019](flatmap_measurements/Mayer_etal_2019/README.md) | 51 |
| [Rosa_etal_1993](flatmap_measurements/Rosa_etal_1993/README.md) | 107 |
| [VanEssen_2005](flatmap_measurements/VanEssen_2005/README.md) | 67 |
| [Wilkinson_2021](flatmap_measurements/Wilkinson_2021/README.md) | 7 |

Editable canonical geometry, ImageJ outputs and per-paper tables are linked from the latest review. Source-limited totals remain NA. Historical batch reviews are retained for provenance.
