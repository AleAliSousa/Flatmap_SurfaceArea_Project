# Brecht calibration flag — 30 October 2026

All 18 workbook rows citing Brecht & Freiwald are flagged in new Calibration review and Use restriction columns, with comments on the Area cells. Original cell values, notes and comparisons are preserved. A pre-edit workbook is saved beside this note. The five macaque rows (source rows 64–68) are on hold for biological absolute-area pooling pending calibration reconstruction. Other Brecht rows are flagged as provisional schematic measurements; this does not assert that their scales are wrong.

## What can be calibrated?

The published Figure 3 caption explicitly says the same scale applies to the side view and flatmap in panels a and b. Thus panel b has a documented local **10 mm bar**, and the current tracing uses its measured **58 pixels** in the canonical rendered crop. That is a reproducible calibration of the published drawing. It yields 6,632.326 mm² for the drawn cortical outline. It does not establish that the simplified outline preserves whole cortical biological area. The discrepancy with typical published hemisphere totals motivates checking the redraw/source chain; it does not prove the printed bar itself is incorrect.

Physical measurements, MRI surface estimates, and atlas normalization commonly give approximately 10,000–10,500 mm² per hemisphere. The workbook total of 67,253 mm² is approximately 6.4–6.7 times those values. The workbook's sixfold hypothesis gives 11,208.833 mm² and is biologically plausible in magnitude, although it is not a demonstrated correction. The current printed-bar drawing estimate is smaller than the published averages. Neither value should be promoted to a validated whole-neocortex estimate solely by resemblance to a population mean.

Primary sources checked:

- Sincich, Adams & Horton (2003), *Complete flatmounting of the macaque cerebral cortex*: 10,430 ± 1,859 mm² cortical area per hemisphere, excluding hippocampus. https://www.uab.edu/vsrc/images/Labs/SincichLab/Sincich.Adams.Horton.2003.VN.pdf
- Van Essen et al. (2012), *Cortical parcellations of the macaque monkey analyzed on surface-based atlases*: normalized F99 average 105 cm² = 10,500 mm² per hemisphere; native atlas 122 cm². https://pmc.ncbi.nlm.nih.gov/articles/PMC3500860/
- *Towards HCP-Style Macaque Connectomes*: 10,052 ± 1,584 mm², 24 hemispheres, excluding the non-cortical medial wall. https://pmc.ncbi.nlm.nih.gov/articles/PMC7116593/
- Young, Collins & Kaas (2013): one macaque flattened hemisphere 15,200 mm². https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2013.00030/full

## Could a Felleman & Van Essen reference explain it?

Yes, an incorrectly transferred calibration could explain a large discrepancy. Correct use of that source alone does not imply a 67,253 mm² hemisphere.

1. **Copying a pixel scale across images:** mm/pixel depends on image resolution and resizing. If the target drawing is enlarged by a factor s without updating calibration, its computed area is inflated by s². A sixfold area error corresponds to a length factor of sqrt(6), about 2.45; the approximately tenfold workbook-versus-current difference corresponds to about 3.2. These are possible mechanisms, not evidence of what happened.
2. **Using a known area as an anchor:** target area = target pixel area / anchor pixel area × anchor known area. This creates an explicit reference-normalized estimate. It is defensible only to the extent that the anchor and target geometry are comparable; it does not become an independently observed animal area.
3. **Choosing a different anchor changes the answer:** the workbook macaque V1/outline ratio is 10492/67253 = 0.156008. Using the workbook's Felleman Fig 2 cortex entry, 9,885.852 mm² (row 105), as an assumed outline anchor predicts V1 = **1,542.271 mm²**. Using its V1 entry, 1,121.117 mm² (row 86), as the anchor predicts cortex = **7,186.283 mm²**. These are illustrative scenarios using workbook values, not validated calibrations or accepted neocortex denominators. Both anchors cannot be matched by one uniform rescaling because the drawings have different V1/outline proportions.
4. **Mislabeled anchors are another possibility:** a whole-cortex area assigned to V1 could produce an inflated total of this order. The workbook V1 value 10,492 mm² is itself close to published whole-hemisphere areas. This resemblance is only a diagnostic lead; it is not proof of such a mistake.

The canonical Felleman Fig 2 calibration is 10 mm / 121 rendered pixels and includes the source's shrinkage handling. Its pixel scale cannot be pasted into a different image. Those current renderings also do not reveal what resolution or crop the original workbook used.

## Evidence required to resolve the flag

Recover the original workbook image/crop, ROI files or ImageJ Results, Set Scale distance and units, and the exact source value/field used as an anchor. Trace Brecht's macaque drawing through the cited references (97–100) to identify whether it is a resized map, a redraw or a composite. Multiple homologous landmarks are needed to test whether one uniform transformation fits. If the original geometry cannot be recovered, retain the local-bar result as a schematic measurement and, if useful, report separately labeled normalization scenarios or within-drawing proportions. Do not silently replace the original values or treat reference-normalized estimates as independent data.
