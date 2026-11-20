"""Recheck saved per-paper measurements and file hashes without rebuilding them.

Run with the framework Python 3.9 interpreter used by paper rebuilds. The older
Krubitzer and Kaas 1990 script requires reportlab at import time, so its geometry
check is called separately without that unused-for-verification import. Its
historical checksum ledger is reported, not rewritten.
"""

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


REVIEW = Path(__file__).resolve().parents[1]
ROOT = REVIEW.parent


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def verify_1990(paper):
    script = paper / 'scripts/rebuild.py'
    source = '\n'.join(line for line in script.read_text().splitlines()
                       if not line.startswith('from reportlab.'))
    namespace = {'__file__': str(script), '__name__': 'read_only_verify'}
    exec(compile(source, str(script), 'exec'), namespace)
    namespace['verify']()
    ledger = json.loads((paper / 'documentation/checksums.json').read_text())
    missing = [name for name in ledger if not (paper / name).is_file()]
    changed = [name for name, expected in ledger.items()
               if (paper / name).is_file() and digest(paper / name) != expected]
    status = 'geometry_pass_hash_incomplete' if missing or changed else 'passed'
    message = ('56 views and 373 selections: geometry, calibration, scope and ROI archives passed; '
               f'{len(ledger)} ledger entries, {len(missing)} missing, {len(changed)} changed; '
               'missing=' + ';'.join(missing) + '; changed=' + ';'.join(changed))
    return status, 0, message


def main():
    rows = []
    for paper in sorted(ROOT.iterdir()):
        if not paper.is_dir() or not (paper / 'data/measurements.csv').is_file():
            continue
        if paper.name == 'Krubitzer_Kaas_1990':
            try:
                status, code, message = verify_1990(paper)
            except Exception as exc:
                status, code, message = 'failed', 1, repr(exc)
        else:
            script = paper / 'scripts/measure_flatmaps.py'
            proc = subprocess.run([sys.executable, '-B', str(script), '--verify'],
                                  cwd=paper, text=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, timeout=180)
            status = 'passed' if proc.returncode == 0 else 'failed'
            code = proc.returncode
            message = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ''
        rows.append({'paper_id': paper.name, 'verify_status': status,
                     'exit_code': code, 'last_output': message})
        print(paper.name, status, flush=True)
    target = REVIEW / 'technical_verification.csv'
    with target.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['paper_id', 'verify_status',
                                                     'exit_code', 'last_output'])
        writer.writeheader()
        writer.writerows(rows)
    print(f'{len(rows)} papers; {sum(r["verify_status"] == "passed" for r in rows)} fully passed')


if __name__ == '__main__':
    main()
