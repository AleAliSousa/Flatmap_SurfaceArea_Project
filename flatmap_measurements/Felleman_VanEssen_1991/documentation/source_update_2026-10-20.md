# Source PDF replacement — 20 October 2026

The user-supplied `Felleman-1991-Distributed hierarchical process.pdf` replaces the main reading/reference copy, [source/paper.pdf](../source/paper.pdf). It is copied without recompression or alteration.

| Check | Previous copy | Replacement |
|---|---:|---:|
| File size, bytes | 2,944,698 | 15,103,460 |
| File size, MiB | 2.81 | 14.40 |
| PDF pages | 47 | 47 |
| Pages rendering entirely white | 20–47 (28 pages) | None |
| Figure 2 page size, PDF points | 626.159973 × 808.080017 | 626 × 808 |
| Main embedded image on figure 2 page, pixels | 2609 × 3367 | 2611 × 3368 |

All 47 pages were rendered and checked for blank output at 0.3 pixels/PDF point. Figure 2 was rendered at the established measurement scale for visual side-by-side comparison. Its anatomical content and visible detail are comparable; the primary demonstrated benefit is restoration of missing later pages, including tables, connection diagrams and references. This is not evidence of higher anatomical resolution. The page-by-page results are in `source_pdf_page_checks_2026-10-20.json`.

The replacement is 14.40 MiB, below GitHub's 25 MiB browser-upload limit and 50 MiB regular-Git warning threshold: [GitHub file-size documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github). No lossy compression, Git LFS configuration, commit or push is needed for this local replacement.

## Exact measurement reproducibility

The original scan is retained as [source/paper_measurement_original.pdf](../source/paper_measurement_original.pdf). Both source checksums and roles are explicit in `source/manifest.json`. The measurement renderer now selects and checks the manifest's `measurement_pdf` and `measurement_sha256`; it also verifies the primary PDF. Existing figures 1 and 2 continue to use the original scan, crop, render scale and scale-bar coordinates. No contour, calibration or area has been changed or reprojected onto the replacement scan.

The full pre-update dataset is backed up at `_backups/fve_source_update_2026-10-20/Felleman_VanEssen_1991/` relative to `flatmap_measurements`. Source-page reading previews in the gallery use the replacement; traced-image overlays continue to use the original measurement crop.

## Assessment scope

The existing inventory covers figures 1–3, available in the original copy. Restored pages 20–47 have not received a new measurement-eligibility inventory. For example, figure 4 is now visibly accessible on page 30 and is a connectivity hierarchy diagram. Existing records of blank pages describe the superseded source only. The validation report explicitly marks the full replacement paper's figure assessment incomplete, without discarding prior tracing checks.

## Validation result

Full native ImageJ rebuild and geometry checks passed for all 74 selections. Both canonical ROI JSON files are byte-identical to the backup. Both measurement source TIFFs are pixel-identical, and every data CSV is byte-identical. The installed primary PDF matches the user file SHA-256 exactly. See `source_update_validation_2026-10-20.json`.
