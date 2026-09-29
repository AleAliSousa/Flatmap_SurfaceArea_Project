# Pilot methods and limitations

Source: Krubitzer LA and Kaas JH (1993), *The Dorsomedial Visual Area of Owl Monkeys: Connections, Myeloarchitecture, and Homologies in Other Primates*, Journal of Comparative Neurology 334:497–528. Source checksum is in `source/manifest.json`.

The paper has 32 PDF pages and 21 numbered figures. Captions were screened into `figure_inventory.csv`; individual panels still require image-by-image assessment. This pass measures Figure 5 only (PDF page 10, printed p.506), an individual-case reconstruction labelled owl monkey 88-32. The methods identify the owl monkeys as Aotus trivirgatus. Laterality is not assigned.

Figure 5 is explicitly modified from Krubitzer and Kaas (1990a). Its Figure 4 photomicrograph and other views of 88-32 are not independent additional animals. Figure 14 identifies 88-16, also a label in the existing 1990 dataset; do not pool across papers without checking identity and source reuse.

## Geometry

The source is rendered at two pixels per PDF point and cropped at `[140,145,1080,990]`, without resizing, to 940 × 845 pixels. All saved vertices are in crop coordinates. The external closed tissue contour was segmented at grayscale <170, selected as the largest outer contour and simplified with 0.65-pixel tolerance, then visually inspected and saved as a polygon. Rebuild uses this polygon, not a second segmentation step. The whole outline is measured independently of cortical fields.

The visible 2 mm scale stroke spans 36 pixels between crop positions `(716,610)` and `(752,610)`. Thus area conversion is `area_px2 × (2/36)^2`. The red crosses in the tracing mark the actual measured endpoints. Calibration is local to Figure 5; it is not borrowed from another figure.

MT, FST and the compound region AI + R were traced against visible outlines. Shared MT/FST boundary vertices are identical in reverse order. The 21 binary overlap pixels reported in validation are on that shared boundary, not a second region to add to cortex area. Internal tracer marks and labels remain part of the anatomical envelope. AI and R are not split without a visible divider. MST's rostral boundary stops without meeting MT; no long artificial closure was drawn. All other fields in this pilot remain `not_yet_digitized`, rather than being asserted unmeasurable.

Fourfold raster supersampling estimates fractional pixel coverage. Fields are clipped to the whole-tissue outline. CSV area uses fractional pixels; ImageJ selections use >=50% coverage. Native ImageJ reads back the TIFF calibration, ROI ZIP, overlay and mask-stack pixels and checks equality. Small binary/fractional differences are reported in `imagej_measurements.tsv`.

## Interpretation

These are provisional image-derived areas of the drawn flattened cortex. No shrinkage correction or anatomical certification is claimed. Pixel-perturbation sensitivity bounds have not been calculated and remain NA. Short scale bars and uncertain boundaries limit precision. Species summaries use observed values only; one measured case provides a mean but not a sample SD. Totals spanning unfinished fields remain NA.

Source/tracing images were visually inspected. Scientific anatomical review remains pending. No external reference measurements were supplied for this paper, and the reference-comparison step was skipped. The core pipeline and ImageJ validation run with no `comparison/` directory.
