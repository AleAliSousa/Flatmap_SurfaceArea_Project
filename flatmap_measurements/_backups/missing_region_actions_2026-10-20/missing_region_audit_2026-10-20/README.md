# Missing-region audit — 20 October 2026

This pass records the improved tracing method and checks other files for omissions. No measurement geometry or area tables were changed.

## Scope

- Machine inventory: all 21 paper folders, 304 saved view definitions and 1,088 ROI records.
- Targeted visual inspection: 22 views across 18 papers besides Felleman & Van Essen. The queue below records every inspected view and the result. Source captions were additionally consulted for the Krubitzer (1995) comparative maps, Krubitzer et al. (1995) fig19, Lyon et al. (1998) fig04 and Beck & Kaas (1998) fig04.
- Kaas (2011) and Zilles (1985): existing exclusion documentation read; no new source-figure inspection. Felleman (1991): the preceding correction is the worked example.
- The 1,178 saved unmeasured entries are neither unique fields nor confirmed omissions. The 18 explicit `not_yet_digitized` entries consist of 17 pilot fields in Krubitzer & Kaas (1993) fig05 and one grouped hippocampal/subicular entry in Felleman fig02. Legacy entries without a status remain explicitly marked `status_not_recorded` in this audit.

## Main findings

Five views contain clear missing tracings: Krubitzer & Kaas (1993) fig05; Krubitzer (1995) fig01 macaque and marmoset; Krubitzer et al. (1995) fig19; and Krubitzer (1998) fig14F. Start with area 17, the FST/FEF/FV/R leader targets, the enclosed V region and the dark M field. Other fields listed on the same rows still require their own boundary decisions.

Lyon (1998) fig04A also has a second S component absent from both the ROIs and the missing-region list. Enlarged inspection shows its border interrupted at the tissue cut: this is an inventory omission, not a claim that a complete field can already be measured. This illustrates why missing-region assessment must distinguish an unrecorded component from a recoverable total area.

The old generic “small print,” “dark fill” and “overprinted lettering” reasons were too broad for several comparative figures. Their compartments must be reviewed individually. Conversely, open borders, projection lines, recording windows and diffuse histological staining remain real limits.

## Review and reproducibility

[Open the image review and prioritized queue](index.html). [Reusable tracing method](../tracing_method.md).

`visual_findings.json` is the human-authored assessment ledger. `visual_findings.csv` is its tabular copy. `view_inventory.csv` and `saved_unmeasured_entries.csv` retain the saved state, including old reasons that this audit disputes. They do not silently relabel canonical inputs. `canonical_input_sha256.json` records all inventoried definitions.

Run `python3 flatmap_measurements/scripts/audit_missing_regions.py` from the project to regenerate inventories and the review from the current definitions and the saved assessment ledger. The script does not discover anatomical borders. If geometry changes later, reassess the findings rather than assuming this dated ledger still describes the new traces.

Before retracing, preserve the affected paper, then update canonical JSON, areas, native ImageJ outputs, summaries and visual review together. Do not merely change an NA status without rebuilding the associated measurement records. No claim of complete anatomical review of the entire dataset is made here.
