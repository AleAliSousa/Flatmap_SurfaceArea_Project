<!-- full-dataset-recheck-2026-10-16 -->
# Krubitzer_Kaas_1993 · current recheck

**106 field/component observations.** Recovered the three closed DM cortical maps in the lower panels of figure 2, distinct from the visual-field plots above. Only panel B has its own defensible 2 mm stroke; A/C remain pixel-only. Owl identities are unresolved and are excluded from independent-animal means. Added 22 selected fields in the figure 1 flattened-cortex illustration, including correctly labelled area 1; area 2 is not falsely closed. Existing case-map geometry from the previous precision audit is preserved.

[Latest source review](review/full_dataset_audit.html) · [Recheck findings and limits](documentation/full_dataset_recheck.md) · [Current measurements](data/measurements.csv). Earlier notes below describe the previous processing state; their counts are superseded.

<!-- earlier-processing-notes -->
## Earlier processing notes

# Krubitzer & Kaas (1993): surface-area measurements

All 21 figures have been assessed; 78 new field measurements were added across 12 additional figures. The remaining eligible figures are digitized provisionally: Figures3, 6, 11, 12A and13–20. Figure12B/C retain calibrated source images with explicit NA fields. Eight unsuitable figures are excluded with reasons in the inventory. Figure5 was also included in the subsequent precision audit; its legacy NA rows remain preserved. Prior contours are archived.

- [Contour precision audit: previous/current source toggles](review/precision_audit.html)
- [Source and tracing review](review/gallery.html)
- [Measurements](data/measurements.csv)
- [Whole-hemisphere percentages and species summaries](data/species_summary_percent.csv)
- [Figure inventory and exclusions](documentation/figure_inventory.csv)
- [Methods, identity and limitations](documentation/methods.md)
- [Numerical and ImageJ validation](documentation/validation.json)

Open a view's `figures/<map_id>/source.tif` in Fiji/ImageJ, then **Image > Overlay > To ROI Manager**, or load its `RoiSet.zip`. Use one route to avoid duplicate ROIs. `Masks.tif.zip` contains the named binary masks. Preserve native edits under a new name and reconcile them into canonical `rois.json` before rebuilding.

Whole-neocortex summaries contain only Figures5, 6 and14–18. Sections, opposite-hemisphere details, and the incomplete cortex of Figures19/20 are kept separate. Missing/open/cropped borders are NA; partial field measurements are flagged. Cross-paper independence of reused specimens remains unresolved. New digitizations require anatomical review.

From this folder, using a Python with numpy, Pillow and pypdfium2:

```sh
python scripts/measure_flatmaps.py --rebuild
python scripts/measure_flatmaps.py --verify
Rscript scripts/export_summary.R
```

Native exports additionally require Java17+ and ImageJ/Fiji (`--java` / `--ij-jar` accept explicit paths). Rebuild uses saved JSON geometry and replaces generated outputs. No external reference comparison was performed.

Precision audit completed 15 October 2026. Earlier coarse contours were refined, all saved views received source review, and areas/native ImageJ outputs were rebuilt. Dotted, obscured and schematic boundaries retain explicit source limitations. See `documentation/precision_audit.md`.
