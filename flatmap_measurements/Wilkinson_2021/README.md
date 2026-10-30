# Wilkinson_2021

4 numbered figures assessed; 1 views and 7 provisional field/component measurements saved. Counts are observations, including overlapping domains and repeated drawings, not animals.

Figure 4 is an unscaled human atlas adaptation. Seven field/component observations include the cut V1 pieces, visual domains, S1, M1 and SII. M1 follows the black boundary; red leader lines are annotations. No scale is borrowed from Van Essen and Drury or from a different paper. This atlas view supplies no independent animal or complete-neocortex denominator.

[Source-toggle review](review/precision_review.html) · [All-figure assessment](review/gallery.html) · [Measurements](data/measurements.csv) · [Methods](documentation/methods.md) · [Field inventory](documentation/field_inventory.csv)

Rebuild from saved geometry with `python scripts/rebuild_all.py --java /path/to/java --ij-jar /path/to/ij.jar`. Python requires numpy, Pillow and pypdfium2; summaries require base R. `python scripts/measure_flatmaps.py --verify` checks saved outputs. Geometry is editable in each `figures/<map_id>/rois.json` or the corresponding native ImageJ ROI ZIP; coordinate changes must be rebuilt before use.
