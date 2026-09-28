# Methods and limitations

## Scope

Krubitzer LA & Kaas JH (1990), *Cortical connections of MT in four species of primates: Areal, modular, and retinotopic patterns*, Visual Neuroscience 5:165–204. DOI: 10.1017/S0952523800000213.

Figures 12–24 are 13 individual-case whole-cortex reconstructions: squirrel monkey (12–16), owl monkey (17–19), marmoset (20–21), and galago (22–24). Species names follow the paper. Left/right laterality is unassigned; each map is one hemisphere, without doubling. Additional views from Figures 1, 2, 4, 6, 9–11 and 25–28 are now digitized where boundaries support a measurement. They are not counted as extra whole-hemisphere cases. See data/view_index.csv for each view and documentation/excluded_panels.csv for panels without usable areal geometry.

## Source, calibration and masks

The local source PDF in source/paper.pdf is checked against its recorded SHA-256 before rebuilding. Original Figures 12–24 were rendered at 2.5 pixels per PDF point, then uniformly resized as recorded in source/manifest.json. Added views use direct crops rendered at 2 pixels per PDF point without resizing. Figure 20 retains its original 960 × 910 geometry; the others have width 1,100 pixels. The original Figures 12–24 retain their previous coordinates, calibration and measurements.

Each added panel uses its own printed scale stroke, except Figure 10: the caption explicitly states its 1 mm bar in B applies to all six panels. These unresized crops share that calibration. Reference-bar endpoints may lie outside another Figure 10 crop; they are retained in its JSON with scale_endpoints_external=true and scale_reference_map=fig10B. No bar is borrowed merely because images look similar. Figure 1 has no physical calibration. Pixel area is converted using:

`area_mm2 = area_px2 × (scale_length_mm / scale_length_px)^2`

Saved endpoints reflect manually located scale-stroke extents; red crosses in tracing.png mark those endpoints. The whole-tissue mask uses outside flood filling, saved component seeds, documented contour repairs, a circular inset and saved exclusions for attached annotation artifacts. Labels, tracer dots and injection sites remain inside anatomical regions. Gaps outside flattened pieces are excluded. Figures 12 and 14 include saved short outer-contour repairs. All segmentation parameters are in the same per-figure rois.json as the field polygons.

Fields were manually traced against visible anatomical borders. Small interpretable gaps were interpolated and documented. Shared borders were aligned; proper polygon self-intersections and interior overlaps are checked. Any residual manual boundary overlap is reported in validation.json; fields should not be summed as an exhaustive parcellation. Field areas use 3× fractional pixel coverage, or the saved 4× setting for Figure 20, and are clipped to the whole-tissue mask. These are per-figure parameters of one measurement function. The outline is measured independently: labelled fields do not constitute a complete parcellation and must not be summed to obtain the total.

## Missing information and uncertainty

Figure 19 shows “2 mm” without a recoverable scale line, including at 432 dpi (fig19_scale_detail.png). Its absolute areas remain blank; pixels and percentages are retained. The scale is not borrowed: Figures 17 and 18 have 2 mm lines of approximately 28.012 and 31.049 pixels in equally resized crops. Applied to Figure 19, they would imply approximately 1,831 and 1,490 mm², respectively. Those illustrative assumptions are not entered as measurements. scale_comparison.csv covers all saved views; scale_comparison.png illustrates the original 13 maps only.

In the original 13 reconstructions, forty-eight labels lack complete individual boundaries and are recorded as unavailable, never zero. PP and IT often denote open broad territories. Figure 18's dorsal V2 terminus is approximate. In Figure 22, the compartment labelled M includes UZ's recess; UZ has no separate closed perimeter and is not counted again. PV/IG, MI and C retain the paper's printed labels. Each row retains its detailed boundary note.

CSV sensitivity columns vary field boundaries by ±2 pixels and scale length by ±2 pixels; whole-outline boundaries vary by ±1 pixel. These are sensitivity scenarios, not confidence intervals. They do not capture every uncertainty from anatomy, dashed borders, flattening, missing tissue or processing. No shrinkage correction is applied. Whole-map values describe published reconstructed cortical sheets. New histological-panel measurements describe visible section geometry and may vary with section depth and boundary visibility; they are not interchangeable with reconstructed whole-field areas or in-vivo pial surfaces.

## Added views and their interpretation

- `extent=complete` means a closed printed field boundary was traced. `approximate_complete` means the field envelope required conspicuous interpolation. `partial` measures only the visible fragment, sometimes closed at crop edges or between drawn strip endpoints; these straight closures are stated in each boundary note. None of these statuses guarantees anatomical accuracy.
- The program never assigns a partial panel's rectangle as a neocortex outline. `percent_of_drawn_neocortex` is populated only for the original 13 hemispheres. `percent_of_drawn_outline` also covers the separately named schematic outlines. No denominator is used for partial views.
- Figures 25A–D link to Figures 12–15 respectively, in the opposite injected hemisphere. Figure 25E is printed **86-25**, unlike **87-25** in Figure 16; its identity is unresolved and no automatic link is made. Figure 8E also prints 86-25.
- Figures 26A/B/C link to Figures 18/22/21 in the opposite hemisphere. Figure 26D repeats MT from 26C at higher magnification. Its envelope bridges pale myelin-light notches; it is not a measurement of only the heavily myelinated compartment. The two MT estimates must not be added or averaged automatically.
- Figure 10 depicts the V2 patch from marmoset 87-53 (Figure 20) in registered/adjacent sections and reconstructions. It is a repeated tissue view. Figures 11A/B/C are fragments from 88-5/88-11/88-10 (Figures 22/24/23). Figure 11D is **87-62**, a DL-injection case without a whole-map entry here.
- Figures 2, 4 and 6 do not supply specimen IDs in their captions. Species alone does not establish a link to a numbered whole-map specimen. Figure 9G's dual MT/DL injections suggest a possible relationship to Figure 19 but do not supply an explicit specimen ID in that panel, so the link remains unassigned.
- Figures 27 and 28 **do have 5 mm bars**. They are scaled summaries; Figure 28 is adapted from external literature. Their geometric areas and proportions describe drawings, not new observations of animals. Macaque species is not assigned beyond what the figure reports. Figure 1 is an unscaled explanatory flattening drawing. Black sulcal cortex remains inside its cortical fields; white connection arrows remain inside the summary fields.
- Small scale bars (especially Figures 27/28) and obscured/dotted borders make absolute values sensitive to endpoint and boundary choices. CSV sensitivity intervals are pixel-perturbation scenarios only, not confidence intervals or estimates of all anatomical uncertainty. The manual tracings are a starting point for the user's ImageJ review.

## Comparison with Table 1

The printed species ranges on p.175 were used for 101 screening comparisons; 25 estimates fall outside those ranges. These flags remain visible in table1_range_check.csv. Numbered Table 1 cases have not been securely matched to figure specimen IDs, so these are not specimen-matched validation. Traces were not changed to force agreement.

## ImageJ representation

Native ImageJ ROI ZIPs and calibrated TIFFs are generated and read back by ImageJ's own library. Each exported selection matches its binary mask exactly, including disconnected components and clipped outer borders. Binary field selections use at least 50% pixel coverage; consequently their areas differ slightly from fractional CSV areas. The current maximum binary/fractional difference is reported in validation.json; original whole-cortex counts are exact. imagej_measurements.tsv records both baselines and their differences. TIFF resolution tags add small numeric rounding; read-back calibration is checked to a relative tolerance of one part per million (or absolute 1e-8).

Masks.tif.zip contains one named mask per slice, with 255 included and 0 excluded. The first slice is a whole-tissue denominator only in whole-hemisphere or schematic-outline views. In partial panels it is simply the first named cortical field; no whole-neocortex mask exists. Figure 4B has no defensible closed ROI and retains its calibrated source/tracing/JSON without ROI or mask archives. Native ImageJ edits are saved in the user's revised ROI ZIP and Results table; they do not automatically update the baseline JSON or CSV. Rebuilding from JSON regenerates the baseline, so keep user edits under separate names.

## Verification and recovery provenance

validation.json records scientific checks, counts, scale status, overlap audits and native ImageJ read-back validation. checksums.json verifies the current package files. provenance.json preserves recovery evidence and the cleanup equivalence check. The PDF and selected image comparisons were visually inspected; gallery script syntax was checked. Browser interaction was not tested because the app's browser blocked local-file URLs.

The previous working folder disappeared. Its coordinates and source code were recovered from this chat's saved edit history, then outputs were regenerated from the unchanged paper. Before this reorganization, the complete measurement CSV matched the original SHA-256 exactly: c9b8bb30ab662a3507cfb5277562605adbc3af2af58bb658e4cdb32bfe7a1511. Cleanup changes file paths and organization; all scientific values and tracing geometry are checked against that recovered dataset. Figure 20 is fully included in the common workflow. No project-wide surface-area tables were changed.

Official ImageJ references: [ROI Manager](https://imagej.net/ij/docs/menus/analyze.html#manager), [selection tools](https://imagej.net/ij/docs/guide/146-19.html), [creating selections from masks](https://imagej.net/ij/docs/menus/edit.html).
