<!-- full-dataset-recheck-2026-10-16 -->
# Krubitzer_Kaas_1990 · current recheck

**354 field/component observations.** Rechecked the numbered-figure inventory and retained the prior accepted canonical geometry and calibration. Dense contours refined in the earlier precision audit were not smoothed again unnecessarily. Existing section/local-panel observations retain their source view types; a two-dimensional section or projected image does not establish an unfolded whole-field surface or an independent animal. Existing denominator eligibility and specimen-link limits are preserved.

[Latest source review](review/full_dataset_audit.html) · [Recheck findings and limits](documentation/full_dataset_recheck.md) · [Current measurements](data/measurements.csv). Earlier notes below describe the previous processing state; their counts are superseded.

<!-- earlier-processing-notes -->
## Earlier processing notes

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

[Contour precision audit: source toggles and area changes](review/precision_audit.html).

Precision audit completed 15 October 2026. Earlier coarse contours were refined, all saved views received source review, and areas/native ImageJ outputs were rebuilt. Dotted, obscured and schematic boundaries retain explicit source limitations. See `documentation/precision_audit.md`.

<!-- project-tracing-review-2026-10-31 -->
## Project-wide tracing review, 31 October 2026

[View this dataset's quality review](../project_review_2026-10-31/index.html?paper=Krubitzer_Kaas_1990) · [Review methods and changes](../project_review_2026-10-31/README.md)

View-level screening categories: A=4, B=48, C=3, N=1. A identifies the clearest source/fit examples; B retains caveats; C needs targeted review/retracing; D is unsuitable for the intended anatomical area inference; N has no saved trace. These are not individual-region certification or independent-specimen counts. See the linked report for each map's notes and proposed improvements.

Atlases and guides: see the [project guide](../ReadMe.md). Use same-specimen panels to resolve obscured lines where correspondence is established; use other specimens and atlases for field identity, adjacency and sulcal plausibility only. They do not supply an observed border, justify copying a shape, or establish a missing physical scale.

<!-- project-tracing-review-2026-10-31-pass3 -->
## Project recheck, pass 3

[Current project-wide review](../project_review_2026-10-31_pass3/index.html#Krubitzer_Kaas_1990) · [Scope and methods](../project_review_2026-10-31_pass3/README.md). All inventoried source figures and saved views screened at overview scale; remaining precision/coverage limits are recorded.
