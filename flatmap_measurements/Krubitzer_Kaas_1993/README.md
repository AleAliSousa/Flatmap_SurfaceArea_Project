# Krubitzer & Kaas (1993): first tracing pass

**Status: started, not a completed paper.** Figure 5 (owl monkey 88-32) has an independently traced cortex outline and provisional MT, FST and AI + R fields. Eighteen other field labels are NA; most await digitization, and MST lacks a closed rostral boundary in this drawing. The other figures remain undigitized.

- [Source and tracing review](review/gallery.html)
- [Measurements](data/measurements.csv)
- [Figure inventory](documentation/figure_inventory.csv)
- [Methods and limitations](documentation/methods.md)
- [Numerical and ImageJ validation](documentation/validation.json)

Open `figures/fig05/source.tif` in ImageJ/Fiji, then **Image > Overlay > To ROI Manager**. The overlay and `RoiSet.zip` contain the same selections; use one route. `Masks.tif.zip` contains the corresponding named binary masks. Save edited ROIs under a new filename; editing in ImageJ does not automatically update `rois.json`.

From this folder:

```sh
python scripts/measure_flatmaps.py --rebuild
python scripts/measure_flatmaps.py --verify
Rscript scripts/summarize_flatmaps.R data/measurements.csv
```

Python needs numpy, Pillow and pypdfium2. Native exports use Java 17+ and ImageJ/Fiji; pass `--java` and `--ij-jar` if they are not found automatically. Rebuild replaces generated outputs using saved JSON geometry. Preserve any ImageJ edits first.

No reference comparison was performed; there is no `comparison/` folder. Tracing review and internal validation are included. Next: anatomically review the pilot fields, assess the remaining Figure 5 fields, then continue through `documentation/figure_inventory.csv`.
