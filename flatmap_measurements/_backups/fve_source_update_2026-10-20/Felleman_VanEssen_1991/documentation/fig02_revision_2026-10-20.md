# Figure 2 correction — 20 October 2026

The figure now has **74 field/component observations: 12 added, 50 existing contours revised, and 12 existing contours retained after inspection**. All measurements remain atlas/composite observations, excluded from biological animal means.

[Interactive before/after review](../review/fig02_revision.html) · [Area-change table](../data/fig02_revision_changes.csv) · [TF comparison](../review/fig02_revision/TF_comparison.png) · [Anterior ER comparison](../review/fig02_revision/ER_anterior_comparison.png)

## Source and coordinates

The user supplied `Flat Map of Macaque Visual Cortex.pdf`, a print of the [Harvard Born Lab page](https://www.hms.harvard.edu/bss/neuro/bornlab/lab/figures/FVE_map.html). The page explicitly attributes the map to Felleman and Van Essen (1991), *Cerebral Cortex* 1:1–47. A preserved copy and SHA-256 manifest are in `source/color_reference.pdf` and `source/color_reference_manifest.json`. The embedded map is 432 × 444 pixels. It provides supporting evidence for field identity and colored boundaries.

Measurement geometry remains on the original paper PDF page 4, rendered at four pixels per PDF point, crop `[520,250,2370,1990]`. The original 1 cm scale endpoints `[1514,1644]` and `[1635,1644]` are retained. No calibration is transferred from the color image, and no extra shrinkage correction is applied.

## Corrections

- **External leaders:** trace the field at the leader endpoint, not the area containing its letters. Added anterior ER, PAC, 35 and 36. Both ER components are retained separately, without treating them as separate animals.
- **Visual ribbons:** V3 points to the pale ribbon (two drawn components), VP to the outer ventral ribbon, V4t to the narrow strip beside MT, and VOT to the strip beside PITv. These are now identified and measured. V2, V4, MT and TH were also recovered.
- **TF and dark fields:** TF's complete continuous dark envelope is traced, including its upper-left extension. Its white label remains included tissue. PITd/v, CITd/v, AITd/v, MSTd/l, STPp/a, FEF and 46 were rechecked against their actual compartment edges.
- **Overprinted borders:** removed glyph-shaped detours around MDP, SOMATO-SENSORY, PIR, PA and other labels. The 9/10 border no longer follows letters in DORSAL PREFRONTAL. Pro, MIP, PIP and V3A were corrected. Shared boundaries use the same inspected path where necessary.

TF changed from **73.2242 to 106.8579 mm²**. Anterior ER is **42.0928 mm²**. These are digitized areas of the published composite drawing, not new biological specimen observations.

## Method and verification

Source compartments were inspected individually with the color map as a guide. External white-compartment perimeters were extracted without internal label holes, smoothed at the source-stroke scale, and corrected manually where labels touch boundaries. Dark fields and obscured joins use manually placed anatomical junctions and dense interpolating curves. A smooth curve is not evidence of anatomical certainty: every accepted envelope was checked on enlarged source overlays. All editable geometry is in `figures/fig02/rois.json`.

Prior files are preserved under `flatmap_measurements/_backups/fve_fig02_revision_2026-10-20/Felleman_VanEssen_1991/`. The interactive review's previous polygons are an immutable local copy of that snapshot. Rebuild native outputs with `scripts/rebuild_all.py`, then regenerate this comparison with `scripts/build_fig02_revision_review.py`.

Vertex validation passed for all 74 contours. Native ImageJ TIFF/ROI/mask read-back passed. The source-coordinate overlap audit found no interior overlap after eroding each mask by two pixels. This erosion is a diagnostic for source-stroke slivers, not a measurement correction or confidence interval. Full-source tracing and enlarged TF, anterior ER and visual-ribbon comparisons were inspected.

## Remaining limits

The very thin PSv border merges with cut/subicular strokes in the monochrome scan; its full envelope remains unresolved. Hippocampal and subicular subdivisions were not added in this field revision. Unspecified compartments remain unnamed. No complete-neocortex denominator is inferred from a field sum. Anatomical certification remains pending user review.
