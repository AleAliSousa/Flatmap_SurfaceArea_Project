# Brecht_Freiwald_2012

3 numbered figures assessed; 4 views and 14 provisional field/component measurements saved. Counts are observations, including overlapping domains and repeated drawings, not animals.

Figure 3a–d: human, macaque, mouse and naked mole-rat illustrative maps, all right hemispheres. S1-face is a subset of S1 and must not be added to it. Human, macaque and mole-rat use their own printed bars. The mouse flatmap has no unambiguously assigned local bar and remains pixel-only. The independent gray outline is schematic tissue, not a certified animal neocortex denominator.

[Source-toggle review](review/precision_review.html) · [All-figure assessment](review/gallery.html) · [Measurements](data/measurements.csv) · [Methods](documentation/methods.md) · [Field inventory](documentation/field_inventory.csv)

Rebuild from saved geometry with `python scripts/rebuild_all.py --java /path/to/java --ij-jar /path/to/ij.jar`. Python requires numpy, Pillow and pypdfium2; summaries require base R. `python scripts/measure_flatmaps.py --verify` checks saved outputs. Geometry is editable in each `figures/<map_id>/rois.json` or the corresponding native ImageJ ROI ZIP; coordinate changes must be rebuilt before use.
