# Glasser_etal_2016

Human: 3D/inflated cortex projections cannot provide metric surface areas by tracing the printed page. Matching HCP surface meshes and parcel labels are needed. M1/S1-face also requires appropriate somatotopic labels; a whole area4 or area3b parcel is not a face territory.

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

[View this dataset's quality review](../project_review_2026-10-31/index.html?paper=Glasser_etal_2016) · [Review methods and changes](../project_review_2026-10-31/README.md)

View-level screening categories: N=1. A identifies the clearest source/fit examples; B retains caveats; C needs targeted review/retracing; D is unsuitable for the intended anatomical area inference; N has no saved trace. These are not individual-region certification or independent-specimen counts. See the linked report for each map's notes and proposed improvements.

Atlases and guides: see the [project guide](../ReadMe.md). Use same-specimen panels to resolve obscured lines where correspondence is established; use other specimens and atlases for field identity, adjacency and sulcal plausibility only. They do not supply an observed border, justify copying a shape, or establish a missing physical scale.

<!-- project-tracing-review-2026-10-31-pass3 -->
## Project recheck, pass 3

[Current project-wide review](../project_review_2026-10-31_pass3/index.html#Glasser_etal_2016) · [Scope and methods](../project_review_2026-10-31_pass3/README.md). All inventoried source figures and saved views screened at overview scale; remaining precision/coverage limits are recorded.
