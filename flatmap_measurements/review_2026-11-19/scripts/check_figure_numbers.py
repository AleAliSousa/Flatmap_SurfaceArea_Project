"""List gaps in the numbered figure inventories of active paper datasets."""

import csv
import re
from pathlib import Path


REVIEW = Path(__file__).resolve().parents[1]
ROOT = REVIEW.parent
rows = []
for paper in sorted(ROOT.iterdir()):
    if not paper.is_dir() or not (paper / 'data/measurements.csv').is_file():
        continue
    path = paper / 'documentation/figure_inventory.csv'
    if path.is_file():
        inventory = list(csv.DictReader(path.open(newline='')))
        numbered = set()
        for item in inventory:
            match = re.search(r'(?i)(?:fig(?:ure)?[ ._-]*)?(\d+)',
                              str(item.get('figure', '')))
            if match:
                numbered.add(int(match.group(1)))
        gap = sorted(set(range(1, max(numbered)+1))-numbered) if numbered else []
        status = 'contiguous' if numbered and not gap else 'gap_or_unparsed'
    else:
        inventory, numbered, gap, status = [], set(), [], 'no_inventory'
    rows.append({'paper_id': paper.name, 'status': status,
                 'inventory_rows': len(inventory), 'numbered_figures': len(numbered),
                 'first_number': min(numbered) if numbered else '',
                 'last_number': max(numbered) if numbered else '',
                 'missing_numbers': ';'.join(map(str, gap))})
target = REVIEW / 'figure_number_coverage.csv'
with target.open('w', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(f'{len(rows)} paper inventories; '
      f'{sum(r["status"] == "contiguous" for r in rows)} contiguous')
