#!/usr/bin/env python3
"""Create a new portable paper folder; reference comparison is optional."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil


def prepare(project, paper_id, pdf, comparison_data=None):
    project, pdf = Path(project).resolve(), Path(pdf).resolve()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", paper_id):
        raise ValueError("paper-id must be a simple folder name, e.g. Krubitzer_Kaas_1993")
    if not pdf.is_file() or pdf.suffix.lower() != '.pdf':
        raise ValueError("An existing source PDF is required")
    reference = Path(comparison_data).resolve() if comparison_data else None
    if reference and not reference.is_file():
        raise ValueError("Comparison data file does not exist")
    target = project / 'flatmap_measurements' / paper_id
    if target.exists():
        raise FileExistsError(f"Continue the existing dataset instead of replacing it: {target}")
    here = Path(__file__).resolve().parent
    helpers = ['measure_flatmaps.py', 'summarize_flatmaps.R', 'ImageJIO.java']
    for name in helpers:
        if not (here / name).is_file():
            raise FileNotFoundError(here / name)
    for name in ['source', 'figures', 'data', 'scripts', 'review', 'documentation']:
        (target / name).mkdir(parents=True, exist_ok=True)
    shutil.copy2(pdf, target / 'source' / 'paper.pdf')
    manifest = dict(paper_id=paper_id, source_pdf='paper.pdf',
                    original_filename=pdf.name,
                    source_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
                    processing_status='initialized; no views digitized',
                    comparison_status='not_requested_or_unavailable')
    if reference:
        (target / 'comparison').mkdir()
        shutil.copy2(reference, target / 'comparison' / reference.name)
        manifest['comparison_status'] = 'reference_available; not_yet_compared'
        manifest['comparison_source'] = 'comparison/' + reference.name
    (target / 'source' / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    for name in helpers:
        shutil.copy2(here / name, target / 'scripts' / name)
    (target / 'README.md').write_text(
        f'# {paper_id}\n\nInitialized from `{pdf.name}`. No views digitized yet.\n\n'
        'Inspect the source and captions, then save each view as `figures/<map_id>/rois.json`.\n'
        'Run `python scripts/measure_flatmaps.py --rebuild`, then `--verify`.\n'
        'Run `Rscript scripts/summarize_flatmaps.R data/measurements.csv` for summaries.\n'
        'Python needs numpy, Pillow and pypdfium2. Native exports use Java 17+ and ImageJ/Fiji.\n'
        'Source-versus-tracing review belongs in `review/`. Reference comparison is optional.\n')
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--paper-id', required=True)
    parser.add_argument('--pdf', required=True, type=Path)
    parser.add_argument('--comparison-data', type=Path)
    args = parser.parse_args()
    print(prepare(args.project, args.paper_id, args.pdf, args.comparison_data))
