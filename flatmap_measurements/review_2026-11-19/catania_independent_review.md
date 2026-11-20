# Independent review: Catania et al. 1999

Reviewed 2026-11-19. This was a read-only visual audit of the ten traced source/tracing pairs in `flatmap_measurements/Catania_etal_1999`, all at view scale, with enlarged border checks for Figs. 3A, 6A, 7A, 11B, and 13. I also checked the paper's figure captions against the field names and the source-only rationale for Figs. 11A and 12.

## Confirmed correction needed

| View | ROI | Finding |
| --- | --- | --- |
| `fig06A_97_79` | `V1` | Along the lower edge near source x ≈ 715–728, y ≈ 202–221, the outline makes a narrow upward notch around the black microlesion mark. The surrounding gray V1 outer edge runs smoothly through this interval. The notch traces the mark rather than the field boundary; redraw this short segment to the gray edge. The nearby S1 border is distinct and should remain separate. |

This finding was sent to the lead agent immediately. The enlarged comparison was saved at `/tmp/catania_fig06_v1_notch.png` for the current session; the canonical geometry is `flatmap_measurements/Catania_etal_1999/figures/fig06A_97_79/rois.json`.

## View and caption audit

| Traced view | Result |
| --- | --- |
| `fig03A_97_81` | The sampled gray CO field envelopes and labels agree with the source and caption. Some stain edges are diffuse; no other clear line error. |
| `fig04A_97_47` | Named fields and traced envelopes agree at view scale. |
| `fig05A_97_75` | Named fields and traced envelopes agree at view scale. |
| `fig06A_97_79` | One local V1 error above; remaining field envelopes agree at view scale. |
| `fig07A_97_80` | Enlarged S1/A1 border samples agree with the printed boundary within the scan's edge uncertainty. |
| `fig08_97_77` | The measured visual oval is supported by the caption's visual-response map. |
| `fig09A_97_44` | V1 stripe and A1 crescent agree with the CO section; Fig. 9C is the same case and is not a separate measurement. |
| `fig10A_97_42` | Shaded field envelopes agree at view scale. The caption distinguishes the recording map from V1/A1 borders inferred from CO, as documented in the dataset. |
| `fig11B_scinereus_V1` | The V1 outline follows the dark CO-dense oval at enlarged scale. Its edge is diffuse, so this is a provisional stain-based outline. |
| `fig13_slongirostris_reconstruction` | Traces follow the drawing's field shapes at view and enlarged scale. The A1 lower-left tip and upper border are slightly inset from parts of the black drawing line (roughly a few source pixels); this is below the confidence needed to prescribe a correction in the reconstructed figure. The dataset documents the multi-section reconstruction. |

The Fig. 3–7 and 9–10 captions describe CO-stained sensory fields and a dashed *rough* S1/S2 division, which supports measuring the combined somatosensory territory without claiming separately closed S1 and S2 borders. Fig. 11A and 11B are adjacent sections of one hemisphere: 11B has the CO-dense V1 oval, while 11A shows diffuse S1/S2/A1 staining and has no separate printed scale. The source-only/NA treatment of 11A is supported. Fig. 12 shows a presumptive dashed S1/S2 division and broad dark V1/A1 staining that merges into surrounding tissue without reliably closed borders in this scan; its source-only/NA treatment is also supported despite the visible 500 µm scale bar. Neither should be silently converted to an area estimate from an invented closing edge.

This audit checks the published raster and captions, not microscopic ground truth. Diffuse stain boundaries remain measurement uncertainty, and agreement at view scale does not certify every contour point.

## Resolution

The Fig. 6A V1 notch was removed after this independent audit. The replacement segment follows the gray outer field edge under the microlesion symbol. The source, old red contour, and corrected green contour are preserved in `evidence/Catania_etal_1999__fig06A_97_79_V1_old_red_new_green.png`; the prior JSON is in `before/`. The rebuilt dataset passed native ImageJ read-back and `scripts/measure_flatmaps.py --verify` (82 saved file hashes and 88 rows). The correction changed V1 from 5,194.3125 to 5,351.9375 source pixel² (+3.03%).
