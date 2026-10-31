# Tracing anatomical regions across labels and dark fills

Recorded 20 October 2026 after the Felleman & Van Essen (1991), figure 2 correction. This is the reusable method for subsequent corrections and missing-region checks.

## What improved the Felleman tracing

1. **Resolve the label before drawing its region.** Follow every external leader to its anatomical endpoint. ER's letters lie outside cortex; its anterior tissue strip lies between PAC and area 35. V3, VP, V4t, VOT and TH also required endpoint-based identification. Neither the letters nor the leader's path are an anatomical border.
2. **Use the color reference to distinguish compartments.** The supplied color map helped identify adjoining fields that merge into similar gray or black tones in the scan. Its low resolution does not replace the original measurement image. Coordinates, crop and scale remained on the original monochrome PDF.
3. **Trace the entire field envelope.** TF is a continuous dark-filled field, including its upper-left extension. The white TF lettering is tissue, not a hole. Do not threshold only the pale interior of a dark field, or mistake a label-sized white patch for the field.
4. **Combine image-assisted contours with inspected manual corrections.** For suitable white compartments, extract the external perimeter and fill annotation holes. Where labels touch the perimeter, replace glyph-shaped detours with the anatomical continuation supported by visible edges on both sides. For dark fields and difficult junctions, place anatomical guide points manually and interpolate densely along the visible curve.
5. **Smooth at the printed-stroke scale.** Use enough vertices to follow curvature without following scan speckle. Smooth locally, retaining tips, junctions and narrow ribbons. The previous implementation used approximately 1.5-pixel smoothing and 2-pixel curve sampling in some source-coordinate steps; these are settings for that rendering, not universal anatomical tolerances. More vertices or a smoother curve alone does not improve accuracy.
6. **Use one boundary for adjoining regions.** Reuse the same inspected path on both sides of a shared border. Check joins for loops, slivers and interior overlap; smoothing neighbors independently can change both areas.
7. **Review source, old trace and new trace at enlargement.** Remove the overlay periodically to see the underlying ink. Rebuild editable ImageJ ROIs and masks from the canonical JSON and verify read-back, geometry and calibration. These checks verify saved geometry, not anatomical certainty.

The result was 74 field/component observations: 12 added, 50 revised and 12 retained. TF changed from 73.2242 to 106.8579 mm². These are areas of a published composite drawing, not new animal observations. See the [specific correction record](Felleman_VanEssen_1991/documentation/fig02_revision_2026-10-20.md) and [before/after review](Felleman_VanEssen_1991/review/fig02_revision.html).

## Missing-region check for every figure

- Inventory all named regions and all depicted components, including peripheral strips, small dark fields, externally labeled regions, insets and additional specimens. Compare that inventory with **both** saved ROIs and the unmeasured list. A label absent from both lists is an inventory gap.
- Check each repeated component independently. One traced S component does not account for another S component elsewhere on the map. A partial component must not be presented as a complete field.
- Revisit generic rejection reasons such as “dark fill,” “label overprint,” or “small print.” None by itself proves that the anatomical envelope is unavailable. Inspect the actual border and identify the specific unresolved segment.
- Distinguish anatomical boundaries from label leaders, recording sites, tracer deposits, body-part subdivisions, exposed-surface projection lines, cuts, sulci and the image frame. Identify ambiguous conventions using captions and methods.
- Treat labels and recording symbols inside tissue as included tissue. Bridge a short overprinted segment only when both visible continuations support it; record the interpolation. Do not invent a long missing boundary or transfer another animal's shape.
- Preserve uncertainty: `not_yet_digitized` means work remains; `not_measurable` requires a specific source limitation. A candidate in an audit is not yet an accepted measurement. Missing entries remain NA, never zero.
- Verify calibration on the same image. Color references, illustrative summaries and repeated views do not create additional independent specimens. An independent whole-neocortex outline is required for its denominator.

Before modifying a paper, preserve the current geometry and user edits. Update canonical ROIs, measurement tables, native outputs, review images and provenance together when a correction is accepted. Keep an explicit review queue when the task is inspection only.

## Current audit

The [20 October missing-region audit](missing_region_audit_2026-10-20/index.html) inventories every saved definition and records a targeted visual review of high-risk figures. It distinguishes clear missing tracings, candidates, inventory gaps and source limitations. It is not a certification that every figure in every paper is complete.

## Tracer overlays and coverage — Beck & Kaas 1998 correction, 31 October 2026

Read the tracer legend before identifying boundaries. Triangles, squares, crosses and circles can mark tracer identity; enclosing ovals can mark injection spread. Neither is automatically an areal compartment. Follow the larger continuous anatomical envelope across these marks using visible tangents; retain injected tissue within the region. Compare same-case panels first, then same-species cases; a similar map from another species can explain conventions but cannot supply metric geometry.

Do not reject an entire inset because one short border interval is overprinted. Record and display each interpolated segment. For long hidden intervals, retain the observed-complete boundary as unavailable; any proposed envelope must be explicitly identified as an inferred estimate, excluded from observed complete-field analysis, and drawn with a separate uncertainty style. It must not silently become an observed contour.

A shared V2 border continuing beyond the two DM junctions does not by itself mean that DM is clipped. Inspect the actual field endpoints. Inventory every panel by measurement type: cortical flatmap, anatomical section, schematic or locator. An excluded thalamic section is not an untraced cortical area. Link old review snapshots prominently to the current dataset review.
