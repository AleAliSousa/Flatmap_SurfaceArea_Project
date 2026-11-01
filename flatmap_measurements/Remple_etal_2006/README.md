# Remple_etal_2006

Tree shrew: 3b/S1, face/oral and limb subdivisions, S2/PV and its modules, V2, temporal intermediate and auditory fields. V1 is a visibly clipped component because its medial edge is open. Motor maps show open-ended M1/M2 strips; no complete field area is invented. Case320 left/right are paired, and enlarged Fig7B is not a new animal.

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

[View this dataset's quality review](../project_review_2026-10-31/index.html?paper=Remple_etal_2006) · [Review methods and changes](../project_review_2026-10-31/README.md)

View-level screening categories: C=4. A identifies the clearest source/fit examples; B retains caveats; C needs targeted review/retracing; D is unsuitable for the intended anatomical area inference; N has no saved trace. These are not individual-region certification or independent-specimen counts. See the linked report for each map's notes and proposed improvements.

Atlases and guides: see the [project guide](../ReadMe.md). Use same-specimen panels to resolve obscured lines where correspondence is established; use other specimens and atlases for field identity, adjacency and sulcal plausibility only. They do not supply an observed border, justify copying a shape, or establish a missing physical scale.

<!-- project-tracing-review-2026-10-31-pass2 -->
## Second precision pass, 31 October 2026

[Source / before / after review](../project_review_2026-10-31_pass2/index.html?paper=Remple_etal_2006) · [Change log and areas](../project_review_2026-10-31_pass2/area_changes.csv)

8 revised regions; 0 added components. Original datasets are archived in `../project_review_2026-10-31_pass2/before/`.

**Atlases and comparison guides:** Tree-shrew Figs.7A/7B, 8 and the same-case Fig.11 were used to distinguish S1 boundaries, body-part compartments, modules and the medial-wall fold. Lyon et al. 1998 provides same-species orientation only; parcellations are not assumed identical. The medial-wall line does not truncate the closed S1 cap.

Source-based revisions remain provisional. Existing specimen, scale and analysis-eligibility restrictions are preserved. See the review for unresolved fields and source-specific line meanings.

<!-- project-tracing-review-2026-10-31-pass3 -->
## Project recheck, pass 3

[Current project-wide review](../project_review_2026-10-31_pass3/index.html#Remple_etal_2006) · [Scope and methods](../project_review_2026-10-31_pass3/README.md). All inventoried source figures and saved views screened at overview scale; remaining precision/coverage limits are recorded.
