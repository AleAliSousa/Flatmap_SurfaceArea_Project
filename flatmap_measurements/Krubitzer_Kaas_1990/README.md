# Krubitzer & Kaas (1990): cortical flatmap measurements

56 saved views: the original 13 individual-case hemispheres plus 43 additional panels/drawings. Figure 20 is included like every other case. These are provisional manual digitizations requiring anatomical review.

## Open the results

- [All measurements](data/measurements.csv)
- [View index, specimen links and repeat-view notes](data/view_index.csv)
- [Original 13 whole-hemisphere summary](data/hemisphere_summary.csv)
- [Original images beside their tracings — PDF](review/comparison.pdf)
- [Interactive comparison gallery](review/gallery.html)
- [Methods, uncertainty and validation](documentation/methods.md)

## Read the scope before using a value

`map_id` identifies a view, not an animal. Use `view_type`, `extent`, `linked_main_map`, `hemisphere_relation` and `repeat_of` to distinguish partial fields and repeated tissue. Partial rows have no percentage of neocortex. Figures 27/28 are scaled illustrative summaries; Figure 1 has no scale. Only the original Figures 12–24 appear in the whole-hemisphere summary. The 86-25/87-25 discrepancy remains unresolved. See the methods and per-row boundary notes before pooling measurements.

## Find a figure or edit it in ImageJ/Fiji

Each folder under **figures/** has the same layout (Figure 4B has no measurable ROI and therefore no ROI/mask ZIPs):

| File | Purpose |
|---|---|
| `source.tif` | Original image pixels with calibration and an editable overlay. |
| `tracing.png` | Colored tracing for visual comparison. |
| `rois.json` | The single saved definition of that figure's coordinates, boundary notes and calibration. |
| `RoiSet.zip` | Native ImageJ selections, plus a whole-tissue outline only when one is defined. |
| `Masks.tif.zip` | Binary mask stack: named slices; the first is whole tissue only in whole/schematic maps. |

For example, the former Figure 20 test is now simply **figures/fig20/**.

In ImageJ/Fiji, use **Plugins > Macros > Run…**, select `Open_in_ImageJ.ijm` from this folder and choose a view folder such as `figures/fig26D`. It opens the image and named selections. Save and clear existing ROI Manager work first if needed.

Alternatively open `source.tif` and choose **Image > Overlay > To ROI Manager**. This overlay contains the same selections as `RoiSet.zip`; load only one to avoid duplicates. Select a region, edit with the Brush Selection Tool (Shift adds; Option/Alt subtracts), and click **Update**. Measure with Area enabled and Limit to Threshold disabled. Deselect all entries, then use ROI Manager **More > Save…** to save the complete edited set under a new ZIP filename. Save Results separately. ROI Manager edits do not automatically rewrite the JSON or the baseline CSV.

To start again from a mask, open `Masks.tif.zip` in ImageJ (or unzip it and open the TIFF), choose its named slice, threshold at 255–255 and use **Edit > Selection > Create Selection**. Add it to ROI Manager, activate the matching source image and refine it. The pixel dimensions must stay unchanged.

## Folder layout

- **data/** — combined measurements, view index and the original hemisphere summary; there are no duplicated per-figure CSVs.
- **figures/** — one folder per saved figure/panel, including editable ImageJ files.
- **review/** — comparison PDF and gallery.
- **source/** — the article and its extraction/calibration provenance.
- **documentation/** — methods, validation, comparison tables and recovery history.
- **scripts/** — one Python workflow and its native ImageJ file-format helper.

No commit is needed to use these local files. They are stored in the OneDrive project folder requested by the user; OneDrive manages cloud synchronization.

## Rebuild only if needed

There is one command for all figures, including Figure 20:

```sh
python3 scripts/rebuild.py --rebuild
```

This reads the local source PDF and each figure's `rois.json`, then regenerates measurements, image comparisons and ImageJ exports. It never recreates the JSON from a second coordinate script. **Rebuilding replaces baseline generated files**; save your ImageJ edits with a different filename first. Editing a JSON and rebuilding recalculates that figure's geometry through the same workflow.

Requirements: Python with numpy, Pillow, pypdfium2 and reportlab; Java 17; and ImageJ/Fiji. The exporter finds the installed Fiji JAR on this Mac. Other installations can pass `--java /path/to/java --ij-jar /path/to/ij.jar`.

Check the saved files without changing them:

```sh
python3 scripts/rebuild.py --verify
```

Create a portable archive only when needed, outside this folder:

```sh
python3 scripts/rebuild.py --zip ../Krubitzer_Kaas_1990.zip
```

This avoids keeping a second full copy of the dataset inside itself. A pre-cleanup recovery archive is stored separately in the parent `_backups/` folder.
