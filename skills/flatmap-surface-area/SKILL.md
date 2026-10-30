---
name: flatmap-surface-area
description: Measure cortical fields from published or unpublished flatmap images and PDFs, preserve editable ImageJ tracings, and build species/case surface-area summaries in Flatmap_SurfaceArea_Project. Use for a new paper, continuing digitization, rebuilding measurements, or optionally comparing them with reference data. Reference measurements are not required.
---

# Flatmap surface area

Create reproducible, reviewable measurements from the actual image geometry, one dataset folder per source publication. Work in the user's current repository; default local project is `/Users/crossmodal/Library/CloudStorage/OneDrive-AllenInstitute/Flatmap_SurfaceArea_Project`. The paper queue is `papers_to_do/Cortical Image References`. Use relative paths within datasets so collaborators can relocate the repository.

## Choose the work

- **New paper:** inspect its PDF, captions and methods; inventory individual panels and select views whose geometry supports the requested measurements. Use [the measurement workflow](references/measurement-workflow.md). Start with a representative calibrated view, validate it, then continue to remaining eligible views within the user's requested scope.
- **Existing paper:** read its methods, saved ROI definitions and scripts first. Preserve prior geometry and user edits. Rebuild from canonical inputs only when necessary.
- **Summary only:** read `data/measurements.csv`, use `scripts/summarize_flatmaps.R`, and adapt field/species display order to this paper. Do not digitize images again.
- **Reference comparison:** perform this only when usable reference measurements are available and it is in scope. See [optional comparison](references/comparison.md). Missing reference data never blocks measurement, ImageJ review or summary creation.

Read [the data contract](references/data-contract.md) before creating or changing measurement tables. For the migrated Krubitzer & Kaas example and the paper queue, see [project context](references/project-context.md).

## Essential decisions

- Inspect source images before placing vertices. Saved polygons must follow visible anatomical borders; document short interpolations. Missing or indefensible boundaries remain `NA`. `not_yet_digitized` is different from `not_measurable`.
- Preserve scale-bar endpoints, printed length, source page, crop and rendering scale. Without physical calibration, retain pixel areas and defensible proportions; absolute areas are `NA`. Borrow calibration only with explicit source evidence.
- A view is not an animal. Record specimen, hemisphere, partial extent, repeated tissue and links to other views. Species alone does not establish specimen identity. Keep unresolved cross-paper overlap visible before pooling.
- Determine whole-neocortex area independently. Never sum the named fields to invent a cortex denominator. Partial sections and illustrative summaries cannot become additional whole-hemisphere cases.
- Summary statistics use nonmissing observations and sample SD; SD is `NA` for fewer than two values. New eligible cases enter automatically on rerun. Preserve zeros only when they are actual measured zeros.
- `review/` contains source-versus-tracing checks and remains part of the core workflow. `comparison/` is optional and contains external reference comparisons, not the required tracing review.

## Reusable helpers

Run helpers with the skill folder's actual path; `SKILL_DIR` below denotes that folder.

```sh
python "$SKILL_DIR/scripts/prepare_paper.py" --project /path/to/Flatmap_SurfaceArea_Project --paper-id Author_Year --pdf /path/to/paper.pdf
```

This creates a new dataset under `flatmap_measurements/`, copies portable processing helpers, and records the PDF checksum. It never overwrites an existing paper folder. Omit `--comparison-data` when there is no reference dataset; then no `comparison/` directory is created. A provided file is preserved as reference input, not assumed to be schema-compatible or already compared.

After inspecting the images, save per-view `figures/<map_id>/rois.json` using the contract. The helper renders crops from the PDF and measures saved polygons:

```sh
python scripts/measure_flatmaps.py --rebuild
python scripts/measure_flatmaps.py --verify
Rscript scripts/summarize_flatmaps.R data/measurements.csv
```

Run from the paper folder. Python needs numpy, Pillow and pypdfium2; native ImageJ exports additionally use Java 17+ and ImageJ/Fiji. Use available workspace runtimes; do not install unrelated software. Pass `--java` and `--ij-jar` for nonstandard installations. The generic helper supports polygon outlines, multiple polygon components and explicit exclusions; adapt it for a paper requiring a different documented geometry model rather than forcing unsuitable polygons.

The helpers do not discover anatomical boundaries or certify scientific accuracy. Inspect every exported tracing, inspect suspicious overlaps and verify native ImageJ ROI/mask read-back. Report the measured subset, missing calibration/boundaries and remaining views accurately. Save results locally; a GitHub remote does not itself request a commit, push or publication.
