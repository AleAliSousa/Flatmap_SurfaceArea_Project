<!-- full-dataset-recheck-2026-10-16 -->
# Huffman_etal_1999 · current recheck

**76 field/component observations.** Recovered 14 field/component observations in repeated physiological panels 8–12 and 42 observations in comparative/summary figures 14–15. SI lower islands are partial; open upper envelopes are not closed by a display frame. Same-color SII/PV compartments remain separate where a real divider exists. Absolute summaries now allow one supported complete repeated-view fallback for an identified animal when its main map lacks that field, and exclude comparative illustrations.

[Latest source review](review/full_dataset_audit.html) · [Recheck findings and limits](documentation/full_dataset_recheck.md) · [Current measurements](data/measurements.csv). Earlier notes below describe the previous processing state; their counts are superseded.

<!-- earlier-processing-notes -->
## Earlier processing notes

# Huffman et al. (1999): surface-area assessment

All 16 numbered figures assessed; **20 field or mapped-portion measurements**. Figures 2–7 assessed and digitized where supported. Open fields remain NA; closed SI forepaw islands are partial subregions. Figures 8–12 link to repeated main-case geometry.

- [Refined contours: source toggles and before/after review](review/line_refinement.html)
- [Source/tracing review and all-figure assessment](review/gallery.html)
- [Measurements](data/measurements.csv)
- [Complete-field absolute-area summaries](data/field_area_summary.csv)
- [Figure inventory, repeat links and exclusion reasons](documentation/figure_inventory.csv)
- [Methods and limitations](documentation/methods.md)
- [Validation](documentation/validation.json)

Editable ImageJ exports are saved for measured views: open `figures/<map_id>/source.tif`, then **Image > Overlay > To ROI Manager**, or load `RoiSet.zip` (one route only). `Masks.tif.zip` holds named binary masks. Preserve user-edited files separately and reconcile edits into canonical `rois.json` before rebuilding. Views without a defensible ROI retain their source/calibration and explicit NA rows.

From this folder, using Python with numpy, Pillow and pypdfium2, and Java17+/ImageJ:

```sh
python scripts/rebuild_all.py
python scripts/measure_flatmaps.py --verify
```

`rebuild_all.py` regenerates measurements, native exports, overlap audits, summaries, review pages and final hashes in order; it accepts `--java` and `--ij-jar` for explicit runtime locations. No whole-neocortex denominator is established, so whole-neocortex percentages are unavailable. Absolute summaries use only complete field envelopes in main case views, excluding partial islands/fragments and repeats. All new digitizations are provisional pending anatomical review.

Contours refined on 15 October 2026; prior outlines and area changes are archived in `documentation/`.
