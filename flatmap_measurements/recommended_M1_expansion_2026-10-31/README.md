# Recommended M1 and sensory papers: tracing batch

Open the [batch report](index.html) for the paper inventory, saved tracings, published values and comparison tables. Canonical geometry lives in each publication's folder. Saved ROI counts include partial regions, repeated views and rejected tracings; they are not counts of validated whole-field estimates or independent animals.

## Atlases and tracing guides

The [project atlas and guide directory](../ReadMe.md#atlases-and-tracing-guides) links the Nencki–Monash marmoset template, Paxinos et al. (2012) atlas, Majka et al. (2016) registration methods and FSL MSM surface-registration documentation, with their intended uses and limits. The [measurement workflow](../../skills/flatmap-surface-area/references/measurement-workflow.md) and [data contract](../../skills/flatmap-surface-area/references/data-contract.md) describe source inspection, calibration, editable geometry and measurement provenance.

For Burman, use the [paper-specific atlas guidance](../Burman_etal_2008/README.md#atlases-and-tracing-guides) and [boundary audit](../Burman_etal_2008/review/boundary_audit.html). All 24 original Burman outlines are rejected for analysis pending retracing. The separate CJ58R printed-interior pilot demonstrates shape capture; it does not supply complete-field measurements or physical calibration.

Atlas guidance must match the species and map type. Keep observed borders, source-author estimates and atlas predictions distinguishable; use shared borders between adjacent regions and retain uncertainty bands. Measure in the original calibrated geometry. The marmoset resources are not substitutes for species-appropriate references for the other mammals, and no batch-wide atlas registration has been performed.

## Regeneration

Run `scripts/build_report.py` from the project root after rebuilding publication measurements. It regenerates the batch tables/report and per-paper README introductions while preserving appended sections marked `<!-- atlas-guidance -->`. This batch README is maintained separately. Numerical file checks do not establish anatomical validity.
