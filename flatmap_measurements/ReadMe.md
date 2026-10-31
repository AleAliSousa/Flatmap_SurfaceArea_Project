# Flatmap measurements

[Workbook PDF batch](review_workbook_batch_2026-10-20.html): ten additional papers assessed, 57 views and 539 provisional field/component measurements. Includes source toggles, editable ImageJ exports and the 35 unresolved anatomical boundaries in Rosa. [Methods and limits](../reports/workbook_batch_2026-10-20/README.md).

The historical [full-dataset recheck](review_full_dataset_audit.html) and its [methods and limits](full_dataset_recheck.md). That historical review covers the earlier 21 papers and shows all traced specimens on shared source pages. Per-case native outputs remain beside each canonical `rois.json`. Earlier batch review counts are historical.

## Atlases and tracing guides

Reference links checked 31 October 2026. These resources are available for consultation; listing them does not mean an atlas has been downloaded, registered or used to generate any saved contour.

| Resource | Intended use | Limits |
|---|---|---|
| [Nencki–Monash histology-based marmoset template](https://www.marmosetbrain.org/nencki_monash_template) | Midthickness surface, flatmap and probabilistic localization of cytoarchitectural areas; useful for checking regional shape, adjacency and anatomical landmarks. | A population template is not the anatomy of an individual case. Its area probabilities do not validate a printed contour or provide figure calibration. |
| [Paxinos et al. (2012), *The Marmoset Brain in Stereotaxic Coordinates*](https://www.marmosetbrain.org/reference) | The official reference page provides the atlas and its volumetric representation; consult it for anatomical identification and area nomenclature. | Reconcile labels with each source paper. Volumetric labels and stereotaxic sections are not directly measurable flatmap surface areas. |
| [Majka et al. (2016), procedure for registering cases to a marmoset template](https://www.marmosetbrain.org/reference) | The official reference page links the registration methods paper; use it to plan case-to-template alignment and document provenance. | Registration needs suitable source data and validation; it does not recover unobserved borders from a schematic. |
| [FSL Multimodal Surface Matching (MSM) guide](https://fsl.fmrib.ox.ac.uk/fsl/docs/registration/msm.html) | Guidance on cortical surface registration and assessment of metric distortion when appropriate surface meshes and features are available. | This is a surface-registration method, not a turnkey tracer for raster figures. Do not infer native cortical area from a deformed atlas image. |

### Applying the guides to tracings

1. Read each figure's caption and methods first. Record areal borders, uncertainty bands, sulci, unfolding cuts, author-estimated borders and crop limits separately.
2. Trace shared regional boundaries once, retaining narrow extensions and correct neighboring regions. Letters, symbols and tracer overlays must not create artificial holes or boundaries.
3. Align repeated views of the same animal before introducing an atlas. Use species-specific references and distinguish dorsal projections from unfolded maps.
4. Store observed, author-estimated and atlas-predicted segments in separate editable layers with provenance. Sulci can guide alignment but do not uniquely determine areal borders. Leave indefensible missing boundaries unmeasured.
5. For broad transition zones, preserve the band edges and document any midpoint convention. Area sensitivity to border placement is not a statistical confidence interval. Measure in the original calibrated geometry; registration does not resolve missing scale or projection distortion.

Local guides: [tracing method](tracing_method.md), [measurement workflow](../skills/flatmap-surface-area/references/measurement-workflow.md), [data contract](../skills/flatmap-surface-area/references/data-contract.md), and [Burman boundary audit with editable shape pilot](Burman_etal_2008/review/boundary_audit.html). The [recommended-paper batch README](recommended_M1_expansion_2026-10-31/README.md) records how these guides relate to that batch.

<!-- project-tracing-review-2026-10-31 -->
## Project-wide tracing review, 31 October 2026

[Open the filterable review](project_review_2026-10-31/index.html) · [Findings, atlas guidance and corrections](project_review_2026-10-31/README.md) · [All area changes](project_review_2026-10-31/area_changes.csv)

448 active views were screened. Nine regional contours in four papers were corrected and rebuilt with prior versions archived. View grades separate clear examples, caveats, retracing priorities and unsuitable inferences; they do not certify every regional boundary.

<!-- project-tracing-review-2026-10-31-pass2 -->
## Second project precision pass

[Open the second-pass review](project_review_2026-10-31_pass2/index.html): all 448 views screened again; 51 contours refined and 11 components added. Includes enlarged source toggles, area changes, atlas/same-species guide notes and remaining priorities. Original datasets archived; no calibration or specimen identities changed.


<!-- beck-dm-symbol-recheck -->
## Beck & Kaas 1998: tracer-overlay and missing-inset correction

[Current DM review](Beck_Kaas_1998/review/dm_recheck_2026-10-31/index.html) covers all eight cortical insets. Figure6 is newly traced; Figure9 follows the smooth anatomical border; Figures4/7 have explicitly inferred envelopes excluded from observed complete-field analysis. Numbered thalamic sections are inventoried separately. This targeted correction supersedes the Beck cards in earlier whole-project snapshots. See [tracing conventions](tracing_method.md) for tracer legends, short occlusion bridges and explicit estimate layers.
