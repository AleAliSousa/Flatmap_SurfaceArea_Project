# Project tracing recheck — pass 3

31 October 2026. [Open report](index.html).

Overview screening covered all **47 processed publications**, **448 pre-existing canonical views**, and **621 inventoried source pages**. One new repeated view brings the current count to **449 views / 1882 regional ROIs**. This is not a claim that every boundary has been checked vertex by vertex, every omitted region has now been traced, or every supplementary figure/PDF in the unprocessed queue was reviewed.

This pass made **13 contour revisions**, **8 additions**, and **2 metadata corrections** in 5 publications. [Changes](area_changes.csv), [every current view](view_review.csv), [remaining work](remaining_review_queue.csv), [actual screening notes](screening_log.json).

## Interpretation

- Beck & Kaas (1998): all eight saved envelopes checked enlarged. Figs3/11 geometry improved; Fig9 interpolation display clarified. Figs4/7 remain inferred, Fig11 partial.
- Luethke et al. (1989): eight A-I/R contours in four Fig6 panels corrected across internal tracer symbols. These repeat the same tamarin case87-44.
- Burman et al. (2008): CJ58R M1 dorsal component, 3a and 3b revised; 6Dc, 6Dr, 8Ad and 8Av added. Seven provisional gray-band-center estimates, 21 older outlines still rejected. No physical calibration resolved. Fig9A–D repeat the same anatomy.
- Beck et al. (1996): Fig11 case92-78 S1/S2/PV/Aud added; repeated tissue, own printed 1-mm bar. Projection uncertain: scaled drawing areas only, excluded from accepted intrinsic complete-field summaries. Aud/PV overlap is documented in the source, not silently erased.
- Krubitzer & Dooley (2013): naked mole-rat S1_other_body is a pictogram footprint, not an independently bounded cortical field. Geometry retained for audit and canonical status changed to exclude anatomical interpretation.

## Methods and guides

Source captions govern solid/dashed boundaries, broad uncertainty bands, sulci, cuts and internal tracer/body-part symbols. Compare repeated views of the same animal first; similar maps guide interpretation, not vertex copying. Shared borders use identical paths where revised. Interpolations remain provisional; missing borders are not inferred merely to close a polygon. No scale was transferred between figures.

See the [project atlas/guide directory](../ReadMe.md#atlases-and-tracing-guides), [tracing method](../tracing_method.md), and [Burman caption/atlas guidance](../Burman_etal_2008/README.md#atlases-and-tracing-guides). Marmoset references include the Nencki–Monash template, Paxinos atlas and Majka registration guidance; the project also lists the FSL surface-registration guide. They are guidance resources, not sources of these revised coordinates. No atlas registration or predicted sulcal layer was applied.

## Audit and validation

`before/` preserves prior publication outputs; `baseline.json` preserves the original 448-view inventory. `applied_changes.json` contains before/after geometry; `changes/` is rendered from final canonical coordinates. Overview panels are pre-edit screening snapshots. Current galleries contain rebuilt editable ImageJ ROI sets, masks and measurements. Native ImageJ checks verify saved geometry/calibration, not anatomical correctness.

`source_page_inventory.json` includes continuation pages and a manually recovered Felleman Fig5 page31 (a graph). Figure numbers have no gaps within the inventoried ranges after that recovery; this is not proof of supplement completeness. Source-only studies are included in screening, with no invented ROIs.

The project-wide downstream M1 merge was not regenerated: repeated views, partial maps, drawings and rejected contours require explicit inclusion rules. The recommended-paper batch was refreshed from canonical measurements. Remaining uncertainty is recorded rather than treated as a pass.
