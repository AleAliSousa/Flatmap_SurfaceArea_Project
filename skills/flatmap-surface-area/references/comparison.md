# Optional reference comparison

Default: no reference comparison and no `comparison/` folder. Still perform internal numerical checks and source/tracing visual review in `documentation/` and `review/`.

When reference measurements are available and comparison is requested or part of the chosen paper workflow:

1. Preserve the reference input and its citation, page/table, units, denominator and transcription provenance under `comparison/`. A published table can be transcribed from the supplied PDF; verify against the actual table, not OCR alone.
2. Establish correspondence before comparing: field definitions, taxa, case/specimen IDs, hemisphere, reconstructed surface versus section, and tissue/shrinkage treatment. Mark unmatched identities. Display case numbers and closest numerical matches do not prove specimen matches.
3. Recompute reference means, sample SDs and totals when case data allow it. Retain documented discrepancies rather than altering source values to force agreement.
4. Use matched-case differences only for supported matches. Otherwise compare species/field summaries or ranges and label that scope. Keep n per field and state when totals use complete cases. Reference absence remains NA, never zero.
5. Store the comparison script and results within `comparison/`; it reads core `data/measurements.csv`. Core rendering, measurements, ImageJ exports and summaries must run successfully with `comparison/` absent.

Do not carry Krubitzer & Kaas (1990)'s species, eight visual fields, Table 1 values, published case counts, significance tests or known discrepancies into another paper. Do not adjust tracings to match expected values. Skip unavailable comparisons, recording the reason in the paper methods.
