# Flatmap Surface Area Project

Reproducible measurements of cortical flatmaps from published or unpublished source material. Each publication has its own folder under `flatmap_measurements/`, with original source provenance, editable ImageJ tracings, measurement tables and visual review.

## Reusable skill

[Read the flatmap-surface-area skill](skills/flatmap-surface-area/SKILL.md). It covers paper inventory, calibration, tracing, measurement, ImageJ exports, missing values, species/case summaries and optional comparison with reference measurements.

For Codex, invoke `$flatmap-surface-area`. Collaborators can copy `skills/flatmap-surface-area/` into their personal Codex skills directory. On macOS/Linux, link this checkout instead to keep the installed skill aligned with the repository. From the repository root, if no installation with this name already exists:

```sh
mkdir -p "$HOME/.codex/skills"
ln -s "$PWD/skills/flatmap-surface-area" "$HOME/.codex/skills/flatmap-surface-area"
```

The instructions and Python/R helpers are also usable without Codex. The [skill's data contract](skills/flatmap-surface-area/references/data-contract.md) documents the inputs. Python helpers need numpy, Pillow and pypdfium2; native ImageJ export uses Java 17+ and ImageJ/Fiji. The summary helper uses base R.

## Optional comparison

Core measurements, ImageJ editing and source-versus-tracing review work without reference values. Create `comparison/` only when reference data are available and comparison is part of the task. Always retain `review/` for checking the actual traces. No reference match is required to process a paper.

## Datasets and queue

- [Krubitzer & Kaas (1990)](flatmap_measurements/Krubitzer_Kaas_1990/README.md): existing dataset; specialized comparisons retained.
- [Krubitzer & Kaas (1993)](flatmap_measurements/Krubitzer_Kaas_1993/README.md): first run started; Figure 5 outline and three fields traced, remaining work recorded.
- [Paper inventory](papers_to_do/paper_inventory.csv): 21 source PDFs, one existing dataset and one new pilot. Sources are in `papers_to_do/Cortical Image References/`.

Saved geometry and calibration are canonical inputs. Rebuilding generated files can replace ImageJ edits that have not been reconciled into those inputs. Review each paper's methods before combining data: different panels or publications may represent the same specimen or tissue.
