# Catania et al. (1999): cortical organization in shrews

All 14 numbered figures and their panel roles are listed in [the figure inventory](documentation/figure_inventory.csv). Ten source views now contain 24 provisional field envelopes: individual case drawings from Figures 3–10 and 13, plus the CO-dark V1 oval in Figure 11B. Figures 11A and 12 are preserved as source-only views with explicit missing values because their histological field transitions do not support defensible complete contours in this scan.

- [Source and saved tracing](review/gallery.html)
- [Editable per-view geometry](figures/)
- [Measurements and explicit missing fields](data/measurements.csv)
- [Methods, calibration and specimen identity](documentation/methods.md)

Figures 11A/B are adjacent sections from one hemisphere; Figure 12 is from a second specimen. Receptive-field body drawings and Figure 14's overlay are not additional cortical cases. Each measured view uses its own printed scale bar. No view has an independently defensible whole-neocortex outline, so whole-neocortex percentages and whole-hemisphere case summaries remain unavailable. The calibrated areas measure the printed drawings or visible section geometry; they are not corrected intrinsic cortical surface areas.

Rebuild from the canonical JSON with `python scripts/measure_flatmaps.py --rebuild`, then run `python scripts/measure_flatmaps.py --verify`. Native ImageJ ROI and mask read-back is performed during rebuild when Java 17+ and ImageJ/Fiji are available. The `review/` source/tracing pair is the visual check; file and geometry checks alone do not certify the anatomical border.
