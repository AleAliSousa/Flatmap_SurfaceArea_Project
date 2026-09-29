# Project context

- Canonical repository: `Flatmap_SurfaceArea_Project`, currently under the user's OneDrive AllenInstitute directory.
- Remote: `https://github.com/AleAliSousa/Flatmap_SurfaceArea_Project.git`.
- Incoming papers: `papers_to_do/Cortical Image References/`.
- One folder per publication: `flatmap_measurements/<Author_Year>/`.
- Shareable skill source: `skills/flatmap-surface-area/`. A personal Codex installation may link to this directory; collaborators can copy it into their own Codex skills directory.

## Existing example: Krubitzer_Kaas_1990

Read its README and `documentation/methods.md` when reusing its design. It has a more specialized rebuild script, a Java native ImageJ exporter, source images, ROI JSON, ROI ZIPs, mask stacks and review gallery. Its original case calibration/segmentation settings are paper-specific and must not be copied into a new dataset.

The 2026-09-28 snapshot has 505 rows for 56 views. Only 13 whole-hemisphere reconstructions are included in its whole-neocortex summary. These are validation observations, not future fixed requirements.

`map_id` denotes a view; partial, contralateral and repeated views are linked by metadata. The 86-25/87-25 label discrepancy is unresolved. `DI` -> `D1` was a user-requested display alias for this paper, not a global renaming rule. The existing comparison R script now includes substantial paper-specific analyses: preserve them when fixing paths, and do not replace it with the generic helper.

## First next paper: Krubitzer_Kaas_1993

*The Dorsomedial Visual Area of Owl Monkeys: Connections, Myeloarchitecture, and Homologies in Other Primates*, J. Comp. Neurol. 334:497–528. Queue file: `krubitzer_kaas_1993.pdf`.

Figure 5 is an individual-case reconstruction (owl monkey 88-32), suitable for a first tracing pass. Figure 3 is described as a representative section, not the same type of reconstruction. Figure 1 and Figure 21 are illustrative organization summaries. Figure 14 uses case 88-16, a specimen label also present in the 1990 dataset: establish source identity and geometry before any cross-paper pooling. Figure 5 is explicitly modified from an earlier publication (Krubitzer and Kaas 1990a); record this provenance without assuming it is new independent tissue.
