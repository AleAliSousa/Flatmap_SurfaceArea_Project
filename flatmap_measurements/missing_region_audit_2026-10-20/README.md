# Missing-region audit and executed actions — 20 October 2026

All 22 listed actions now have outcomes. **28 contours were added and 1 existing contour revised**, across 11 modified views in 8 papers. Source-limited candidates retain explicit NA with field-specific reasons. This is not an exhaustive new anatomical certification of the dataset.

[New before/source/after review and areas](../review_missing_region_actions.html) · [Audit with completed-action outcomes](index.html) · [Action results](action_results.csv) · [Area changes](action_measurement_changes.csv).

The additions comprise 25 illustrative-map fields, two complete specimen-field observations, and one approximate echidna V contour. Enlarged inspection revealed an undrawn V boundary interval among recording symbols, correcting the initial audit's description of it as fully enclosed. The interpolated V is excluded from complete-field means. Illustrations and repeated views do not create additional animals. Source scales, crops and specimen identities were preserved.

Current inventory: 21 papers, 304 saved views, 1116 ROI records and 1157 unmeasured entries. These are records, not independent specimens. The original visual inspection covered 22 selected views across 18 other papers. Kaas (2011) and Zilles (1985) were documentation-only checks; Felleman (1991) was the preceding correction.

`visual_findings.json` preserves the original human-authored findings. `action_results.json` records their execution. CSV inventories and canonical SHA-256 records reflect the current definitions. The [original audit snapshot](../_backups/missing_region_actions_2026-10-20/missing_region_audit_2026-10-20/README.md) and affected paper snapshots remain under `_backups/missing_region_actions_2026-10-20/`.

Rebuild affected papers with their existing `scripts/rebuild_all.py`, then run `flatmap_measurements/scripts/build_missing_region_actions_review.py` and `flatmap_measurements/scripts/audit_missing_regions.py` to refresh the project reviews. Canonical geometry is in each `rois.json`; no scratch fitting script is required. The review generators do not infer anatomical borders.
