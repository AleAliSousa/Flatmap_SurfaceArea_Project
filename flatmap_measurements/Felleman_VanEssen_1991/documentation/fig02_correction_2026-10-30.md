# Figure 2 correction — 30 October 2026

This correction was triggered by the restricted check `Evo-M1-Trait-Data-restricted/restricted_checks/Felleman_VanEssen_1991`. That check compared this tracing with Table 2 and found that the "Pall" ROI was 185 mm² against Table 2's PaI of 25 mm². It also found that the auditory fields summed to 124 of 330 mm².

## Changes

| Label | Change | Area (mm²) | Basis |
|---|---|---:|---|
| `Pall` → `Unlabeled compartment ventral to FEF (holds PaI label text)` | relabelled, geometry unchanged | 184.97 | The PaI letters sit in this compartment, but their **leader line** runs down to the right, crosses Pro and ends in the strip right of Pro. Under [tracing_method.md](../../tracing_method.md) rule 1, the letters do not identify the compartment they sit in. No area name is printed for this compartment. |
| `PaI` | **added** | 22.00 | This is the compartment at the leader endpoint: bounded by Pro, the lower border of 13 and the thick orbitofrontal edge. The dangling leader tip is included as tissue. Table 2 gives 25 mm². |
| `AUDITORY (unlabeled remainder)` | **added** | 173.40 | This compartment carries the regional AUDITORY label and surrounds the separately traced CM, AI, L, PA and RL. It is bounded by Ri, Ig, the STP/MSTl border and the thick lateral edge. With the five named fields it gives 297.4 mm², against Table 2's Auditory 330. |
| `Pro` | boundary note only | 49.98 (unchanged) | The note now records that the PaI leader crosses Pro and is not a Pro border. |

The other 73 ROIs are byte-identical to the previous `rois.json`, and their areas are unchanged.

## Method

The new contours come from `scripts/compartment_contour.py`, which works as follows:

- The white compartment at the seed point is selected.
- Thin strokes are split at their centre line, by nearest white compartment.
- Thick outer-edge strokes are excluded at their inner edge, as the existing 13 and Pro ROIs do.
- **All saved ROIs are subtracted**, so shared borders reuse the neighbours' inspected paths.
- The outline is smoothed at about 1.5 px and resampled every 2 px.

Seeds in fig02 crop coordinates were (1690, 780) for PaI and (1404, 900) for AUDITORY. Both results were inspected over the source at 6× and 3×. The overlap audit (`geometry_review.json`) passed. The new ROIs share only border-raster slivers with their neighbours (0–4 px), and none overlap in the interior.

Two small issues remain. Both are under 1 px² and were left in place:

- Where the PaI leader crosses the Pro/13 junction, the outline has a small notch.
- Where the Y of AUDITORY overprints the lateral edge, the outline has a sub-pixel notch.

## Not yet done: native ImageJ export

This environment had Java 11 and no ImageJ jar. The rebuild therefore used `scripts/rebuild_python_only.py`, which runs the unchanged `measure_flatmaps.rebuild()` but skips `ImageJIO.java`. As a result:

- `data/measurements.csv`, `view_index.csv`, `tracing.png`, `source_preview.png`, `review/gallery.html`, `geometry_review.json`, `vertex_validation.json` and `checksums.json` **are current**.
- `data/field_area_summary.csv` was regenerated with the same n = 0 / NA layout. The generator was first checked to reproduce the previous file exactly, because R was not available.
- `figures/fig02/RoiSet.zip`, `Masks.tif.zip`, `documentation/imagej_measurements.tsv` and `imagej_runtime.txt` are **stale**; they predate this correction. `validation.json` records this as `PENDING`.

To finish, run locally:

```sh
python scripts/rebuild_all.py --java /path/to/java17 --ij-jar /path/to/ij.jar
```

The previous state is preserved in `../_backups/tracing_corrections_2026-10-30/Felleman_VanEssen_1991/`.
