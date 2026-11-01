# Burman_etal_2008

NOT READY FOR ANALYSIS: 28 saved ROIs comprise seven provisional gray-band-center outlines in CJ58R (three revised and four added in pass3), plus 21 older outlines still rejected pending retracing. See the pass3 review and original boundary audit. The earlier printed-interior pilot is not a whole-field estimate. Marmoset: dorsal M1 components, M1-face component and core visual/sensory/auditory fields from Fig9A. Pixel areas only: Fig6 caption prints 1 μm, inconsistent with a whole-brain image; Fig9 bar length is not specified. No silent correction to 1 mm. Additional atlas labels are listed as not yet digitized, not falsely classified as impossible.

## Results

- [Source-versus-tracing gallery](review/gallery.html)
- [Measurements](data/measurements.csv)
- [Figure inventory](documentation/figure_inventory.csv)
- [Validation](documentation/validation.json)

Canonical editable geometry is in `figures/<map_id>/rois.json`. Every traced view has a calibrated or pixel-unit `source.tif`, editable ImageJ `RoiSet.zip`, masks and `tracing.png`. Source-only views intentionally contain no ROI.

All measurements remain provisional manual digitizations. Source review and native ImageJ read-back do not certify anatomical accuracy. No field sum was used to invent a whole-neocortex denominator. A view is not an animal.

Rebuild from this folder with `python scripts/measure_flatmaps.py --rebuild`, then `python scripts/measure_flatmaps.py --verify`. Batch tables/report can be regenerated with the batch report script.

<!-- atlas-guidance -->
## Atlases and tracing guides

For anatomical review, consult the [Nencki–Monash marmoset template](https://www.marmosetbrain.org/nencki_monash_template), which supplies a flatmap, midthickness surface and probabilistic cytoarchitectural labels. The [Marmoset Brain Connectivity Atlas reference page](https://www.marmosetbrain.org/reference) provides the Paxinos et al. (2012) stereotaxic atlas and Majka et al. (2016) registration methods. See the [project atlas and guide directory](../ReadMe.md#atlases-and-tracing-guides) for uses, limitations and the surface-registration guide.

These atlases are proposed anatomical references, not sources of the current contours or calibration. No atlas registration or predicted sulcal layer has been applied. Group-average atlas shapes must not replace the observed anatomy of CJ58R or CJ61.

The source captions govern the interpretation:

- **Fig. 6, including CJ61:** gray bands represent uncertainty in architectural borders; the dashed line is the authors' best estimate of the M1 outer boundary. LS identifies the lateral sulcus. The colored stimulation territories are not complete architectural fields. Caption: PDF page 9, printed page 868.
- **Fig. 9, CJ58R:** gray bands are architectural boundary regions; dashed gray lines are borders estimated from other animals. Solid lines include map boundaries and major cortical folds. Use the insets to distinguish folds and unfolding cuts. A–D repeat one animal with different tracer overlays. Caption: PDF page 13, printed page 872; panel A: PDF page 11.

Follow the [boundary audit and shape-review pilot](review/boundary_audit.html): reuse shared borders, preserve the narrow extensions of 3a/3b, retain uncertainty bands, and keep any atlas predictions separate. The pilot captures only printed interiors of dorsal M1, 3a and 3b, excluding gray bands; it is not a complete-field area estimate. Pass3 supersedes three original outlines and adds four: seven provisional gray-band-center estimates, with 21 older outlines still rejected. Improved shape guidance does not resolve the missing or ambiguous physical scales.

<!-- project-tracing-review-2026-10-31 -->
## Project-wide tracing review, 31 October 2026

[View this dataset's quality review](../project_review_2026-10-31/index.html?paper=Burman_etal_2008) · [Review methods and changes](../project_review_2026-10-31/README.md)

View-level screening categories: C=4. A identifies the clearest source/fit examples; B retains caveats; C needs targeted review/retracing; D is unsuitable for the intended anatomical area inference; N has no saved trace. These are not individual-region certification or independent-specimen counts. See the linked report for each map's notes and proposed improvements.

Atlases and guides: see the [project guide](../ReadMe.md). Use same-specimen panels to resolve obscured lines where correspondence is established; use other specimens and atlases for field identity, adjacency and sulcal plausibility only. They do not supply an observed border, justify copying a shape, or establish a missing physical scale.

<!-- project-tracing-review-2026-10-31-pass2 -->
## Second precision pass, 31 October 2026

[Source / before / after review](../project_review_2026-10-31_pass2/index.html?paper=Burman_etal_2008) · [Change log and areas](../project_review_2026-10-31_pass2/area_changes.csv)

2 revised regions; 0 added components. Original datasets are archived in `../project_review_2026-10-31_pass2/before/`.

**Atlases and comparison guides:** Fig.9A–D anatomical insets identify V1ca and V1op within the detached occipital lobe; both belong to V1. Gray architectural bands, estimated dashed borders and solid folds/cuts require separate interpretations, as documented in this dataset’s atlas guide. Krubitzer & Kaas 1990 marmoset maps supplied orientation only. Nencki–Monash and the Marmoset Brain Connectivity Atlas remain proposed guides; no atlas registration was applied. V2 remains partial; all 24 Burman ROIs remain rejected for analysis.

Source-based revisions remain provisional. Existing specimen, scale and analysis-eligibility restrictions are preserved. See the review for unresolved fields and source-specific line meanings.

<!-- project-tracing-review-2026-10-31-pass3 -->
## Project recheck, pass 3

[Current project-wide review](../project_review_2026-10-31_pass3/index.html#Burman_etal_2008) · [Scope and methods](../project_review_2026-10-31_pass3/README.md). All inventoried source figures and saved views screened at overview scale; remaining precision/coverage limits are recorded.

[This paper’s changes and limitations](documentation/pass3_tracing_review.md).
