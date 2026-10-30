# Mayer_etal_2019

10 numbered figures assessed; 8 views and 51 provisional field/component measurements saved. Counts are observations, including overlapping domains and repeated drawings, not animals.

Eight views represent four identified left-hemisphere cases, identified by the source as Sapajus spp. Figures 1/2 measure the sampled M1 response territory, not complete M1. Figure 5 measures sampled digit/toe territory, a digit union and printed-color components within the source M1 limits. Color components estimate visible color shares: they do not reproduce the authors’ exact half-tile allocation for mixed responses (PDF page 6), and stripe edges are not anatomical field borders. All these observations are partial and excluded from complete-field means. White electrode circles remain tissue; larger no-response/unsampled gaps are retained. The four figure 10 threshold recodings are repeated views of the same maps. No whole-M1 total is inferred.

[Source-toggle review](review/precision_review.html) · [All-figure assessment](review/gallery.html) · [Measurements](data/measurements.csv) · [Methods](documentation/methods.md) · [Field inventory](documentation/field_inventory.csv)

Rebuild from saved geometry with `python scripts/rebuild_all.py --java /path/to/java --ij-jar /path/to/ij.jar`. Python requires numpy, Pillow and pypdfium2; summaries require base R. `python scripts/measure_flatmaps.py --verify` checks saved outputs. Geometry is editable in each `figures/<map_id>/rois.json` or the corresponding native ImageJ ROI ZIP; coordinate changes must be rebuilt before use.
