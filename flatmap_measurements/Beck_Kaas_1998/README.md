# Beck & Kaas 1998 — DM symbol/occlusion recheck, 31 October 2026

**Eight cortical insets now have reviewable outlines:** five closed published DM envelopes, one partial contour, and two explicitly inferred envelopes. Figures4/7 estimates are excluded from observed complete-field analysis. Figure6 was incorrectly excluded wholesale; Figure9 now follows the faint continuous DM border across tracer annotations. Figures9/10/12 had incorrect fragment classifications, now corrected after checking their endpoints.

[Latest DM source toggles and coverage audit](review/dm_recheck_2026-10-31/index.html) · [Current measurements](data/measurements.csv) · [Interpretation and uncertainty](documentation/dm_symbol_recheck.md)

The thirteen other panels in Figure9 and seven in Figure6 depict thalamic cross-sections, not cortical surface maps. Their omission from cortical surface-area measurements is intentional and documented in the new panel inventory. The older notes below describe historical processing states.

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

<!-- project-tracing-review-2026-10-31 -->
## Project-wide tracing review, 31 October 2026

[View this dataset's quality review](../project_review_2026-10-31/index.html?paper=Beck_Kaas_1998) · [Review methods and changes](../project_review_2026-10-31/README.md)

View-level screening categories: A=2, B=2, C=1, N=3. A identifies the clearest source/fit examples; B retains caveats; C needs targeted review/retracing; D is unsuitable for the intended anatomical area inference; N has no saved trace. These are not individual-region certification or independent-specimen counts. See the linked report for each map's notes and proposed improvements.

Atlases and guides: see the [project guide](../ReadMe.md). Use same-specimen panels to resolve obscured lines where correspondence is established; use other specimens and atlases for field identity, adjacency and sulcal plausibility only. They do not supply an observed border, justify copying a shape, or establish a missing physical scale.

<!-- project-tracing-review-2026-10-31-pass2 -->
## Second precision pass, 31 October 2026

[Source / before / after review](../project_review_2026-10-31_pass2/index.html?paper=Beck_Kaas_1998) · [Change log and areas](../project_review_2026-10-31_pass2/area_changes.csv)

1 revised regions; 0 added components. Original datasets are archived in `../project_review_2026-10-31_pass2/before/`.

**Atlases and comparison guides:** The source Fig.9 DM fragment was enlarged, and the same-paper Fig.10 map was used as an identity/topology guide. The revised contour follows the visible perimeter across lettering interruptions. The fragment and uncertain source borders remain provisional.

Source-based revisions remain provisional. Existing specimen, scale and analysis-eligibility restrictions are preserved. See the review for unresolved fields and source-specific line meanings.
