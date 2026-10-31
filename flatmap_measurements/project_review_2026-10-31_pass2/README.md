# Second project tracing pass — 31 October 2026

[Open review](index.html) · [Area changes](area_changes.csv) · [All views](view_review.csv) · [Remaining priorities](remaining_priorities.csv)

All 448 active source/overlay views in 44 datasets were screened again on 128 overview sheets. The 62 changed regions were additionally reviewed enlarged: 51 existing contours revised and 11 previously omitted components added, across 14 views in six papers. There are now 1871 regional ROIs. This is not individual anatomical certification of every unchanged field. Source-only views, schematic limits and unresolved borders remain explicit.

## Applied work

- **Ghosh 1997:** 39 existing cat contours revised; 10 medial/coronal-bank components added. Four corrections were prompted by joint-edge overlap checks. Medial components in cases6/9 and case9 bank components are not whole fields. The ventral 3a/3b bank components stop at fSCor; a fundus is not an areal limit. No validated whole-M1 sum is claimed.
- **Remple 2006:** eight tree-shrew contours improved, including S1’s medial cap and seven sensory/module outlines. The medial-wall fold does not truncate the closed S1 field.
- **Burman 2008:** the Fig.9 inset resolves V1ca/V1op as parts of V1. Removed their mistaken inclusion in V2; retained V2 strip is explicitly partial. All 24 Burman ROIs remain rejected for analysis. Neither this correction nor an atlas supplies calibration.
- **Beck & Kaas 1998:** enlarged DM-fragment boundary corrected across lettering artifacts; remains a partial uncertain fragment.
- **Krubitzer 2009:** M/POd corrected from a letter-shaped contour to the source field envelope. Large percentage change reflects the earlier wrong object, not a biological difference.
- **Krubitzer 1998:** squirrel summary M silhouette added. Illustrative/repeated geometry is not another animal.

## How precision was improved

Source crops were inspected before geometry changes. Closed printed interiors were extracted only when the resulting outline followed the correct anatomical compartment. Internal lettering and recording marks were retained by filling interior holes. Short pixel gaps were closed in working masks, then candidate perimeters were compared enlarged against the unchanged source. Manual revisions addressed folds, label interruptions and erroneous field identity. Region extraction used a half-pixel coordinate correction and 0.5-pixel simplification; these are numerical conventions, not anatomical precision claims. Shared-edge checks prompted four additional cat revisions, including a complete retrace of the case8 4sfu wedge.

Some automatic candidates were rejected because they stopped at a fold, crossed a body-part subdivision, or followed tracer/letter artifacts. They remain only in `candidates/` for provenance; **only `applied_changes.json` describes saved canonical changes**. `proposed_changes.json` contains the initial 58 proposals and `shared_edge_candidates.json` the later 4 reviewed proposals. Do not rerun candidate generation against the updated canonical inputs to reproduce the old baseline; use the archived inputs.

## Atlases, same-species maps and guides actually used

### Beck_Kaas_1998

The source Fig.9 DM fragment was enlarged, and the same-paper Fig.10 map was used as an identity/topology guide. The revised contour follows the visible perimeter across lettering interruptions. The fragment and uncertain source borders remain provisional.

### Burman_etal_2008

Fig.9A–D anatomical insets identify V1ca and V1op within the detached occipital lobe; both belong to V1. Gray architectural bands, estimated dashed borders and solid folds/cuts require separate interpretations, as documented in this dataset’s atlas guide. Krubitzer & Kaas 1990 marmoset maps supplied orientation only. Nencki–Monash and the Marmoset Brain Connectivity Atlas remain proposed guides; no atlas registration was applied. V2 remains partial; all 24 Burman ROIs remain rejected for analysis.

### Ghosh_1997

Same-paper cat case maps in Figs.9, 10, 14, 15 and 16 were compared for field identity, adjacency and exposed-versus-bank components. Source labels and each panel’s own lines govern the tracing. The fSCor fundus divides bank components, not cortical areas; the new 3a/3b ventral-bank ROIs are only components. No case geometry or scale was transferred.

### Krubitzer_1998

Luethke et al. 1988 squirrel maps corroborate the M/SI arrangement. The new M outline follows the black silhouette in the 1998 Fig.14D summary itself, preserving the internal M lettering. It remains an illustrative summary, not an additional specimen or a whole-neocortex denominator.

### Krubitzer_2009

The macaque map in Krubitzer & Dooley 2013 was compared for orientation/adjacency only. In the 2009 source itself, M/POd lies between PIP, V3d and V2; the former tiny outline followed lettering instead of the field. These summary maps use different parcellations and are not independent animals.

### Remple_etal_2006

Tree-shrew Figs.7A/7B, 8 and the same-case Fig.11 were used to distinguish S1 boundaries, body-part compartments, modules and the medial-wall fold. Lyon et al. 1998 provides same-species orientation only; parcellations are not assumed identical. The medial-wall line does not truncate the closed S1 cap.

The [project atlas directory](../ReadMe.md#atlases-and-tracing-guides) and existing paper README atlas sections remain available. Source figures/captions establish line meanings. Same-species topology helps distinguish fields and folds; it does not justify transplanting shapes, predicting unobserved sulci as measured borders, or borrowing scales. No atlas registration or predicted sulcal layer was applied.

## What remains unclear

See [remaining priorities](remaining_priorities.csv). All previous view grades are retained and explicitly described as screening categories. Selected corrected contours can be more accurate while the encompassing map still merits grade C. Brecht stays grade D for intended metric inference. Native ImageJ read-back verifies file/mask agreement, not anatomical truth.

The final overlap audit reports expected parent/subregion overlap in Remple Fig.8A/C a 4-pixel residual S1/S2-PV edge overlap in Remple Fig.7A, and a 15-pixel unresolved V1/V2 strip overlap in Burman, which remains excluded. Cat shared-edge interior overlaps introduced during refinement were corrected. Eroding by two source pixels is a diagnostic, not a calibrated uncertainty envelope. No regions are summed across uncertain overlaps.

## Reproducibility and verification

`before/<paper>.zip` preserves each affected dataset before this pass (including canonical polygons, ImageJ ROIs, images, measurements and documentation). `applied_changes.json` preserves complete old/new region objects and reasons. Each changed source crop has identical RGB pixels before/after; scale endpoints, crop, render scale, specimen, hemisphere, repeat relationships and denominator eligibility remain unchanged. Unchanged view JSON hashes and unaffected regional area values were checked. The V2 extent change to partial is deliberate.

All six publications were rebuilt with native ImageJ; ROI/mask read-back passed. Updated measurements, editable ROI archives, masks and native tracing galleries are in the publication folders. The recommended-paper aggregate is regenerated after publication rebuilds. Validation logs and overlap diagnostics are in `validation/`; final verification results are in `summary.json` and `validation/final_checks.json`.

The new HTML source toggles use identical image and polygon coordinates, so display rescaling cannot shift the overlay relative to the source. Region before/after comparisons and exact area differences are supplied for review. The first-pass report remains a historical record and links here. Cross-project `surface_area_analysis` snapshots and workbook comparison tables were not recomputed in this tracing pass; use the publication measurement tables and this report for current contour-derived values.
