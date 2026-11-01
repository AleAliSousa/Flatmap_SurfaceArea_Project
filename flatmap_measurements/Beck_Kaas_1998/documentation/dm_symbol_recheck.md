# DM tracer/occlusion recheck — 31 October 2026

[Current source toggles](../review/dm_recheck_2026-10-31/index.html) · [Coverage audit](../review/dm_recheck_2026-10-31/coverage_audit.csv) · [Panel inventory](../review/dm_recheck_2026-10-31/panel_inventory_fig06_fig09.csv)

All eight cortical insets were compared. This corrects two errors: tracer/injection contours influencing the anatomical outline, and blanket exclusion/partial classification without checking the actual DM endpoints. Figure6 had enough source boundary to trace with a short injection-obscured continuation. Figure9 was retraced on the faint gray line. Figures9/10/12 close inside the inset; the V2 line continuing beyond DM does not make DM a fragment. Figure11 remains partial.

Figures4/7 receive **explicit inferred envelopes**, not observed complete-field measurements. The hidden left border is constrained by visible endpoints/tangents, but cannot be uniquely recovered. These rows have extent `approximate_complete`, status `inferred_boundary_estimate_not_observed`, and `analysis_eligible=False`; observed-complete DM remains unavailable. They do not enter the default complete-field summary. Orange dashed paths in the review and `interpolated_border_segments` in JSON show the hidden intervals. No confidence interval is claimed.

The thirteen main panels in Figure9 and seven in Figure6 are thalamic cross-sections, not cortical surface maps. They remain excluded from this dataset’s surface-area measurements. Complete V2 and VPP boundaries are not supplied. Their missing areas remain NA, not zero.

## Source and guides

Use the source PDF p.3 Results discussion of DM architecture and boundary uncertainty; p.5 Fig3 caption for the distinction between injection-site inset and numbered subcortical sections; p.8 Fig6 caption; p.11 Fig9 caption/legend. Figure6 is Aotus trivirgatus94-3 and Figure9 Saimiri sciureus94-71. Same-species Fig7 and Fig10, respectively, help interpret topology and injection overlays; no geometry or calibration is transferred. No external atlas was registered. General resemblance does not establish a shared specimen or permit copying a contour.

Canonical geometry, source crops and all scales remain in each `figures/<map_id>/` folder. Prior state is archived at `../../_backups/Beck_Kaas_1998_DM_symbols_2026-10-31.zip` relative to this documentation folder. The exact old/new view definitions are in `../review/dm_recheck_2026-10-31/applied_changes.json`. Manual source anchors and smooth local interpolation replace annotation-driven segmentation in the four new/refined contours. Source pixel equality, unchanged calibration/identity and native ImageJ read-back are verified; this is not independent anatomical certification.

## Additional recheck

All eight insets were re-inspected at enlargement. Figure3 still had injection-driven bends on its right edge; these were replaced by a continuous local DM/V2 arc and marked as interpolated. Figure11’s lower legend-driven notches were also replaced by a smooth local continuation. Figure9’s short upper-right gap and Figure11’s legend-hidden/frame-closure segments are explicitly shown in orange. Figures4/7 remain inferred estimates excluded from observed complete-field analysis, and Figure11 remains partial. Original state for this follow-up is archived in `../../project_review_2026-10-31_pass3/before/Beck_Kaas_1998.zip`.
