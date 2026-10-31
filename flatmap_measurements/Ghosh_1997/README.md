# Ghosh_1997

Cat: 4gamma, 4delta, 4sfu, premotor and somatosensory components in exposed cortex and unfolded sulcal banks. Reconstructed at upper layer V. Components are retained separately; no validated whole-M1 sum. Case9 remains pixels: caption specifies 2 mm but no unambiguous bar is visible on the supplied page.

## Results

- [Source-versus-tracing gallery](review/gallery.html)
- [Measurements](data/measurements.csv)
- [Figure inventory](documentation/figure_inventory.csv)
- [Validation](documentation/validation.json)

Canonical editable geometry is in `figures/<map_id>/rois.json`. Every traced view has a calibrated or pixel-unit `source.tif`, editable ImageJ `RoiSet.zip`, masks and `tracing.png`. Source-only views intentionally contain no ROI.

All measurements remain provisional manual digitizations. Source review and native ImageJ read-back do not certify anatomical accuracy. No field sum was used to invent a whole-neocortex denominator. A view is not an animal.

Rebuild from this folder with `python scripts/measure_flatmaps.py --rebuild`, then `python scripts/measure_flatmaps.py --verify`. Batch tables/report can be regenerated with the batch report script.

<!-- project-tracing-review-2026-10-31 -->
## Project-wide tracing review, 31 October 2026

[View this dataset's quality review](../project_review_2026-10-31/index.html?paper=Ghosh_1997) · [Review methods and changes](../project_review_2026-10-31/README.md)

View-level screening categories: C=6. A identifies the clearest source/fit examples; B retains caveats; C needs targeted review/retracing; D is unsuitable for the intended anatomical area inference; N has no saved trace. These are not individual-region certification or independent-specimen counts. See the linked report for each map's notes and proposed improvements.

Atlases and guides: see the [project guide](../ReadMe.md). Use same-specimen panels to resolve obscured lines where correspondence is established; use other specimens and atlases for field identity, adjacency and sulcal plausibility only. They do not supply an observed border, justify copying a shape, or establish a missing physical scale.

<!-- project-tracing-review-2026-10-31-pass2 -->
## Second precision pass, 31 October 2026

[Source / before / after review](../project_review_2026-10-31_pass2/index.html?paper=Ghosh_1997) · [Change log and areas](../project_review_2026-10-31_pass2/area_changes.csv)

39 revised regions; 10 added components. Original datasets are archived in `../project_review_2026-10-31_pass2/before/`.

**Atlases and comparison guides:** Same-paper cat case maps in Figs.9, 10, 14, 15 and 16 were compared for field identity, adjacency and exposed-versus-bank components. Source labels and each panel’s own lines govern the tracing. The fSCor fundus divides bank components, not cortical areas; the new 3a/3b ventral-bank ROIs are only components. No case geometry or scale was transferred.

Source-based revisions remain provisional. Existing specimen, scale and analysis-eligibility restrictions are preserved. See the review for unresolved fields and source-specific line meanings.
