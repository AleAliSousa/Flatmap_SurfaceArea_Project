<!-- full-dataset-recheck-2026-10-16 -->
# VanEssen_Drury_1997 · current recheck

**0 field/component observations.** No new metric cortical areas: the digital flatmaps have explicitly nonuniform local distortion and the supplied raster lacks the mesh/Jacobian needed to recover true surface. Color activation boundaries are not anatomical field borders. Published table areas from 3-D reconstruction are not raster-derived measurements.

[Latest source review](review/full_dataset_audit.html) · [Recheck findings and limits](documentation/full_dataset_recheck.md) · [Current measurements](data/measurements.csv). Earlier notes below describe the previous processing state; their counts are superseded.

<!-- earlier-processing-notes -->
## Earlier processing notes

# VanEssen_Drury_1997

Van Essen, D. C., & Drury, H. A. (1997). Structural and functional analyses of human cerebral cortex using a surface-based atlas. Journal of Neuroscience, 17(18), 7079–7102. https://doi.org/10.1523/JNEUROSCI.17-18-07079.1997

All **13 numbered figures assessed**. **0 provisional contours**, 27 explicit unavailable-field entries. Status: `assessed_no_defensible_field_contours`.

[Enlarged contour review](review/precision_review.html) · [All-figure assessment](review/gallery.html) · [Measurements](data/measurements.csv) · [Complete-field summary](data/field_area_summary.csv) · [Case selection](data/summary_case_selection.csv) · [Methods and limits](documentation/methods.md)

All 13 figures are assessed. PDF pp.5–7 (printed pp.7083–7085), figure 4 and Table 1 distinguish area in the flattened image from 3-D cortical surface area. Table 1 explicitly calculates lobar areas by summing 3-D mesh tiles, not flatmap pixels. Mean areal distortion differs between hemispheres and varies spatially; a grid/scale bar cannot supply the missing tilewise 3-D metric. Therefore no true field area or field/cortex proportion is derived from the raster flatmaps. No 3-D mesh/metric data accompanies this local PDF. Source crops and explicit NA rows are retained for figures 3, 9D, 10D and 13C. The latter reprojects the Felleman & Van Essen (1991) macaque parcellation already represented in this project; it is not a new functional specimen observation. Figures 8, 11 and 12 show activation/uncertainty domains, not anatomical areal boundaries. Published Table 1 areas are source-reported context, not newly traced measurements and are not inserted into the new measurement table. No ROI is fabricated solely to complete the queue.

Canonical geometry and editable ImageJ outputs are under `figures/`. Tracings remain provisional. Missing source boundaries/calibration are NA, never zero; all figures assessed does not imply that every field can be measured.

<!-- project-tracing-review-2026-10-31 -->
## Project-wide tracing review, 31 October 2026

[View this dataset's quality review](../project_review_2026-10-31/index.html?paper=VanEssen_Drury_1997) · [Review methods and changes](../project_review_2026-10-31/README.md)

View-level screening categories: N=5. A identifies the clearest source/fit examples; B retains caveats; C needs targeted review/retracing; D is unsuitable for the intended anatomical area inference; N has no saved trace. These are not individual-region certification or independent-specimen counts. See the linked report for each map's notes and proposed improvements.

Atlases and guides: see the [project guide](../ReadMe.md). Use same-specimen panels to resolve obscured lines where correspondence is established; use other specimens and atlases for field identity, adjacency and sulcal plausibility only. They do not supply an observed border, justify copying a shape, or establish a missing physical scale.
