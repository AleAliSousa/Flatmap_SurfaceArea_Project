# Project tracing review — 31 October 2026

[Open the filterable review](index.html) · [Every view](view_review.csv) · [Region index](roi_review.csv) · [Area changes](area_changes.csv)

Reviewed 448 active views across 44 datasets: 385 traced views containing 1860 regional ROIs, plus 17 explicit outlines; 63 source-only views. All were inspected at contact-sheet scale, with enlargements for problem cases and dense maps. This is a view-level screening pass, not individual anatomical certification of every ROI. Archived revisions are excluded. The separate Burman interior pilot is not a whole-field tracing.

A: clearest source/closest fit; B: usable drawing fit with caveats; C: unclear, displaced or requires targeted retracing; D: unsuitable for the intended anatomical area inference despite possible close image fit; N: no saved trace. These are screening categories, not a precision score or permission to pool observations.

Current counts: A = 60, B = 262, C = 58, D = 5, N = 63. Use the review filters to find specific views, notes and proposed improvements. Region rows inherit the view grade and say so explicitly.

## Applied corrections

Nine regional contours in eight views across four datasets were changed. Beck 1996: PV in Fig10A/10B and S2 in Fig7A. Frost 2000: the three closed Fig4 distal-forelimb envelopes, preserving the case9213 arm exclusion. Manger 2002 Fig6right: restored the ventral-trunk compartment inside the partial PPr envelope. Krubitzer 1998 Fig11B: Vc/Vr now include both upper/lower visual-field compartments instead of following internal retinotopy lines.

Prior complete dataset files are in `before/*.zip` (excluding nested historical archives). Canonical polygons, native ImageJ selections/masks, tracing previews, measurements and affected summaries were rebuilt. Native ImageJ read-back passed for all four datasets. Other area values, scales, identity metadata and extent classifications were checked against the archives and preserved. The new-batch combined tables were refreshed. These technical checks do not establish anatomical validity.

The largest change is illustrative Vc in Krubitzer Fig11B (+49.29% pixels); Vr changes +8.47%. These remain pixel-only illustrative geometry. Manger partial PPr changes +5.85%. Other revised regions change between −4.29% and +1.64%. Beck Fig10A changes only +0.08%, demonstrating that a similar area can conceal a different boundary shape. No scale was fitted to a published number.

## Best examples and priorities

Catania & Remple Fig2 case4, many Beck 1996 local sensory envelopes, and selected Huffman 1999 maps are among the clearest source-to-trace examples (filter A for the exact maps). A good silhouette fit does not turn a summary into an independent animal.

Burman's 24 ROIs remain rejected pending anatomical retracing; the gray bands, dashed estimates, sulcal lines and flattening cuts need separate treatment. Brecht remains flagged as schematic, with unresolved metric calibration. Other priority groups include Remple's coarse subregions, Ghosh's exposed/bank boundaries, Hinds' symbol-obscured V1 edges, Rosa's crowded parietal/MT complexes and selected thin-line maps. Every C view has a specific improvement note. Source ambiguity is not repaired by making the curve smoother.

## Atlases, guides and information from other images

Use same-specimen panels first: verify case, hemisphere, crop, cuts and scale, then align several distributed anatomical landmarks. A second panel can disambiguate a hidden edge only if tissue identity and correspondence are established. Between animals, use field adjacency, sulcal relationships and expected shape as checks; never transplant a border or force all brains to one shape. Treat areal borders, sulci, flattening cuts, uncertainty bands, recording symbols and annotation leaders as separate features. Dashed and gray lines have paper-specific meanings, established from captions. For uncertain borders retain an inner/outer envelope or mark the field unmeasurable; do not count an interior-only mask as a complete area. Atlas registration may guide review, but predicted sulci and inferred borders must remain explicitly inferred and separate from observed measurements.

The project's [atlas and tracing guide](../ReadMe.md#atlases-and-tracing-guides) links the Marmoset Brain Connectivity Atlas, Nencki–Monash template, published marmoset parcellation guides and surface-registration documentation. For Burman, use these for regional identity, fingerlike extensions and sulcal plausibility, then return to the individual printed map. No atlas-derived coordinates or borrowed scales were applied in this pass. For Rosa, Figures3C/11 help label adjacency but cannot replace a case-specific boundary. For Luethke1989, the repeated same-case panels can clarify line identity after registration.

## Reproducibility

`inventory.csv` and `sheets/` preserve the pre-correction inventory and contact sheets. `assessments.json` stores screening judgments; changed views also retain their earlier assessment. `view_review.csv` includes baseline/current ROI hashes. `area_changes.csv` records all numerical changes. `before_after/` shows source, old contour and new contour. `scripts/refine_contours.py` documents source-coordinate decisions; its apply mode refuses to overwrite an existing baseline archive. Run `scripts/build_review_report.py` to refresh this report after a deliberate review. Do not regenerate the baseline inventory over the saved before state.
