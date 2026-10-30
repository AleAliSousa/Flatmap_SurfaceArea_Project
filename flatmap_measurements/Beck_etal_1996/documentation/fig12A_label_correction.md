# Figure 12A: labels are annotations, not anatomy

16 October 2026. The SR contour previously bent toward the `78 / El,S` label and the lower `38 / T` label. These segments were replaced by smooth continuations between the visible anatomical line ends. Image-intensity fitting is disabled across these text interruptions so the fit cannot reattach to letters or numbers. S1/SC geometry, the source crop and calibration are unchanged.

Interior letters, numbers and stimulation symbols do not remove tissue, add tissue, create holes or define boundaries. The polygon integrator counts every pixel inside the anatomical envelope independently of source-image ink. This rule applies to all project tracings. A label crossing a border is handled by continuing the anatomical curve across the overprint.

The immediately preceding JSON, ImageJ selections, masks, TIFF, tracing and measurement tables are preserved in `_backups/internal_label_correction_2026-10-16/Beck_etal_1996/`. The view remains pixel-only: the orientation-axis annotation does not supply a separate accepted calibration stroke.
