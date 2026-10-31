# Human and naked mole-rat benchmarks for Brecht Figure 3

Search and local source check: 30 October 2026. Compared the principal Brecht workbook entries (human source rows 57–63; naked mole-rat 69–71) with published values. Earlier human alternative entries 327/330/331 retain their unresolved figure/multiple-source provenance and are not pooled with these values. Current tracing values are from `flatmap_measurements/Brecht_Freiwald_2012/data/measurements.csv`. All absolute areas below refer to one hemisphere, not both hemispheres.

## Human

| Structure | Brecht workbook (mm²) | Current Brecht tracing (mm²) | Published benchmark | Assessment |
|---|---:|---:|---|---|
| V1 | 2,771 | 2,850.52 | 2,960 ± 760 mm², Hinds et al. 2008 | Workbook 6.4% below mean; current tracing 3.7% below. Good agreement in magnitude. |
| Cortical outline | 66,231 | 70,517.57 | Mean neocortex 97,300 mm² per hemisphere, Van Essen et al. 2012 | Workbook 31.9% below; tracing 27.5% below. Denominator remains questionable as whole biological neocortex. |
| A1 | 174 | 194.71 | Auditory core rarely exceeds approximately 200 mm²; A1 occupies somewhat more than half of core, Dick et al. 2012 | Useful scale check, but core is not A1. Brecht values are near the size of the larger core; this does not validate their A1 boundary. |
| S1 (workbook S1/3b) | 1,526 | 1,704.30 | No directly matched published numeric benchmark verified in this search | Do not substitute postcentral-gyrus area, whole S1 (3a+3b+1+2), or a hand-only functional map for area 3b. |
| S1-face | 454 | 434.90 | No directly matched published complete face-domain area verified | Need a surface-based definition of face/oral extent in the same somatosensory field. |

**V1:** Hinds et al., *The Intrinsic Shape of Human and Macaque Primary Visual Cortex* (2008), DOI 10.1093/cercor/bhn016, reports ex vivo V1 surface reconstruction based on the stria of Gennari; the results give mean area 2,960 ± 760 mm² and more than twofold variation. [Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC2733317/).

**Neocortex:** Van Essen et al., *Parcellations and Hemispheric Asymmetries of Human Cerebral Cortex Analyzed on Surface-Based Atlases* (2012; online 2011), DOI 10.1093/cercor/bhr291, reports a mean 973 cm² per hemisphere from MRI midthickness surfaces. Conversion is 100 mm² per cm². This supports concern over Brecht's cortical-outline denominator, while allowing method, tissue-scope and individual-size differences. It does not justify scaling all Brecht fields upward: V1 already agrees with its separate benchmark. [Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3432236/) / [abstract](https://pubmed.ncbi.nlm.nih.gov/22047963/).

**Auditory:** Dick et al., *In Vivo Functional and Myeloarchitectonic Mapping of Human Primary Auditory Areas* (2012), DOI 10.1523/JNEUROSCI.1712-12.2012, combines myelin-sensitive MRI and tonotopy. Its approximately 2 cm² statement concerns the auditory core, not a mean A1 measurement. No exact A1 benchmark or percentage discrepancy is manufactured from this qualitative statement. [Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3531973/).

A search also located cortical maps and cytoarchitectonic work relevant to human S1 (Geyer et al. 1999, *Areas 3a, 3b, and 1 of human primary somatosensory cortex*, [PubMed](https://pubmed.ncbi.nlm.nih.gov/10385582/)), but no directly comparable whole-field or whole-face surface-area number was verified here. These gaps remain explicit rather than being filled with anatomical volume or functional activation-cluster size.

## Naked mole-rat

**Catania & Remple (2002), Table 1 supplies actual case measurements.** It was checked in the local PDF, including visual verification of printed p.5695 (PDF p.4). Four adult cases were mapped and related to flattened cortical histology. Mean ± SD below are the authors' reported rounded values. [Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC122833/), DOI 10.1073/pnas.072097999.

| Measure | Brecht workbook | Current tracing | Published comparator |
|---|---:|---:|---:|
| S1, mm² | 8.209 | 8.191 | 10.5 ± 1.8; case range 7.9–12.0 |
| Neocortex / drawn outline, mm² | 26.682 | 26.254 | 33.7 ± 6.4; case range 25.3–39.8 |
| S1 / cortex | 30.77% | 31.20% | Approximately 31% of neocortex |
| S1-face / S1 | 64.58% | 61.87% | Candidate broad orofacial comparator: 68.5%, derived as described below |

Both Brecht absolute estimates lie within the four published case ranges, near their lower end. The workbook's S1 and cortex are respectively 21.8% and 20.8% below the published means, so their ratio is closely preserved. This is compatible with the scale of a smaller specimen/illustrative map; it is not evidence that Brecht depicts a particular case. In particular, the numerical proximity to Case 2 does not establish specimen identity.

The publication's approximately **47%** refers to the fraction of *possible sensory cortex* occupied by S1, whereas approximately **31%** refers to *total neocortex*. They must not be interchanged. Another approximately 31% in the same paper refers to *incisor representations as a fraction of S1*, which is a third quantity.

### Face definition

The original table separates incisors, head/vibrissae, buccal cavity and chin. Summing their published mean percentages gives **30.8 + 18.7 + 11.5 + 7.5 = 68.5% of S1**. This is a candidate broad orofacial comparison; it is not proven identical to Brecht's S1-face. Incisors alone are only 30.8% and are not an appropriate substitute for the complete face domain.

Summing the corresponding rounded absolute areas *within each case* gives **7.1, 5.8, 8.5 and 7.3 mm²**, with a calculated mean **7.175 mm²** and sample SD **1.106 mm²**. These are derived, not separately reported face totals. Brecht's 5.301 mm² is 8.6% below the smallest candidate total and approximately 26% below their mean; the current tracing is 5.068 mm². Anatomical definition, specimen size and redraw differences remain possible explanations. No uncertainty interval was invented from independent sums of category SDs.

### Source independence and Henry 2006

Henry et al. (2006), the reference cited by Brecht, is already present locally at `papers_to_do/cortical_flatmap_bibliography/Henry_etal_2006.pdf`. Its text attributes the approximately 30% incisor proportion and comparative S1 enlargement to Catania & Remple (2002). The earlier primary table is therefore a strong provenance and magnitude check, **not necessarily independent replication of Brecht's evidence**. No additional numerical whole-S1/neocortex table was found in the inspected Henry PDF text. The original figures may still clarify which case or reconstruction was redrawn.

Our existing Catania tracing of Figure 2 case 4 gives S1 = 11.584 mm², versus the published case-4 11.4 mm². That is a separate check on the project's tracing procedure, not a replacement for the published case values.

## Implication for the flag

The naked mole-rat results do not show the gross scale discrepancy observed in the macaque workbook rows. Its S1 and cortex areas have primary empirical support in magnitude, and its S1 fraction agrees closely. Keep it as provisional schematic/source-derived evidence while resolving redraw lineage and the face definition. Human V1 is also supported in magnitude; the human cortical denominator and A1 definition need more caution, and S1/S1-face still lack a verified matched numerical benchmark. Retain the per-row flags rather than treating all species and fields as equally uncertain.

## Files and reproducibility

- `Catania_Remple_2002_published_cases.csv`: four visually verified published case records plus explicitly derived quantities.
- `Brecht_human_molerat_benchmarks.csv`: ten comparisons, including unresolved fields, definitions, units, source URLs and numerical differences where appropriate.
- `build_brecht_benchmarks.py`: reproduces both CSV files.
- `Catania_2002_Table1_page.png`: local source-page rendering used for transcription verification.

These comparison files do not replace any workbook or canonical measurements. Numerical differences use 100 × (Brecht/reference − 1); they describe agreement in magnitude, not matched-case error or statistical significance.

## Existing tracings added alongside Brecht

See [side-by-side table](Brecht_alongside_existing_tracings.html) and [CSV](Brecht_alongside_existing_tracings.csv). These contain 11 source/view rows, with human and naked mole-rat records grouped by species.

| Naked mole-rat source/view | S1 mm² | Face / candidate oral-head sum mm² | Face / S1 | Cortex mm² |
|---|---:|---:|---:|---:|
| Brecht workbook, Fig 3d | 8.209 | 5.301 | 64.58% | 26.682 |
| Brecht current tracing, Fig 3d | 8.191 | 5.068 | 61.87% | 26.254 |
| Catania current tracing, Fig 2 case 4 | 11.584 | 7.226 | 62.38% | unavailable |
| Catania current tracing, Fig 4B summary | 10.982 | unavailable | unavailable | unavailable |
| Catania published Table 1, case 4 | 11.400 | 7.300 (derived) | 64.04% (derived) | 32.500 |

Catania's traced candidate oral/head sum comprises lower and upper incisors, buccal cavity/tongue, chin, and vibrissae/head. It is not automatically equivalent to Brecht's S1-face. Its 62.38% of S1 is close to Brecht's traced 61.87%, despite different absolute sizes. Catania Fig 2 S1 tracing is 1.62% above the same case's published value, and the candidate oral/head sum is 1.01% below the corresponding published sum. These check tracing agreement for case 4, not biological differences between independent samples.

The figure-2 tracing does not establish a whole-neocortex perimeter. Its published case-4 cortex value is shown on a distinct published-data row; it is not presented as a traced cortex measurement. Figure 4B is an unidentified summary, not an additional animal or a known second view of case 4.

Human tracings from Van Essen 2005 Fig 9A/B and Wilkinson 2021 Fig 4 are included as unavailable-mm² rows: their pixel geometry exists, but no accepted physical calibration is available. Krubitzer & Dooley 2013 Fig 7D likewise has unscaled mole-rat teeth/body tracings. Van Essen & Drury 1997 has unavailable measurement records, not an additional usable calibrated tracing. Henry 2006 has a local source PDF but no existing canonical tracing dataset. No new digitization or calibration was performed for this addition.

## Caption clarification and contribution audit

On rechecking Brecht printed p.262 / Figure 3, the caption explicitly states that human and macaque S1 outlines represent **putative areas 3a and 3b**, and that the four species' maps have been normalized to the same displayed area. The earlier warnings about ambiguous S1/3b equivalence can now be made more specific: a human benchmark should target 3a+3b, not isolated 3b or all of 3a+3b+1+2. This does not establish exact anatomical fidelity of the outlines.

The surrounding text reports approximate S1-face fractions of cortical surface: macaque 0.5%, human 0.7%, mouse 10%, naked mole-rat 20%. These are author-reported approximations from the same review and source lineage, not independent validation of our tracings. Mouse contributes no row to this reanalysis workbook. No Brecht-linked workbook row measures M1.

For naked mole-rat, Catania 2002 supplies four cases with reported S1 and neocortex areas and individual somatotopic components; its existing case-4 tracing also supplies a candidate broad orofacial sum. Brecht adds a directly outlined S1-face compartment and a convenient comparative redraw, rather than a clearly unique primary case or a necessary source of total S1/neocortex area. Equating its face compartment to the Catania oral/head sum still requires verification. For humans and macaques, Brecht supplies face compartments that Catania's mole-rat study cannot supply. The original reason the workbook author selected Brecht is undocumented; convenience and cross-species face comparison are inferences, not established history.
