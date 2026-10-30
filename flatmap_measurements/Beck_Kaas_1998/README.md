<!-- full-dataset-recheck-2026-10-16 -->
# Beck_Kaas_1998 · current recheck

**5 field/component observations.** Rechecked all numbered source figures and the existing DM insets. The earlier source-following contours are retained; visual-field plots, projected locators and open or poorly resolved DM envelopes do not supply new complete field totals.

[Latest source review](review/full_dataset_audit.html) · [Recheck findings and limits](documentation/full_dataset_recheck.md) · [Current measurements](data/measurements.csv). Earlier notes below describe the previous processing state; their counts are superseded.

<!-- earlier-processing-notes -->
## Earlier processing notes

# Beck & Kaas (1998): surface-area assessment

All 14 numbered figures assessed; **5 field or mapped-portion measurements**. Eight cortical insets assessed; five supported DM envelopes or visible fragments. Other cortical fields are NA where borders are incomplete or obscured.

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
