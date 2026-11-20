"""Screen saved ROI edges for distance to dark source pixels.

This is only a mechanical triage signal. Printed boundaries can be gray, colored,
dashed, obscured by symbols, or intentionally interpolated; nearby dark labels
can also produce misleadingly small distances. Visual source review is required.
"""
import csv
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

review_dir = Path(__file__).resolve().parents[1]
root = review_dir.parent
rows = []
for paper in root.iterdir():
    if not paper.is_dir() or not (paper / 'data/measurements.csv').exists():
        continue
    for path in (paper / 'figures').glob('*/rois.json'):
        try:
            data = json.loads(path.read_text())
            source = path.parent / 'source_preview.png'
            if not source.exists():
                source = path.parent / 'source.tif'
            if not source.exists():
                continue
            im = Image.open(source).convert('RGB')
            W, H = im.size
            factor = min(1.0, 1400 / max(W, H))
            if factor < 1:
                im = im.resize((round(W * factor), round(H * factor)), Image.Resampling.BOX)
            arr = np.asarray(im, dtype=np.uint8)
            # Black printed line; color scans are still supported by gray mean.
            ink = arr.mean(axis=2) < 155
            dist = distance_transform_edt(~ink)
            color_fraction = float((arr.max(axis=2).astype(float) - arr.min(axis=2).astype(float) > 35).mean())
            for roi in data.get('rois', []):
                points = []
                for polygon in roi.get('polygons') or []:
                    a = np.asarray(polygon, dtype=float)
                    if a.ndim != 2 or len(a) < 3:
                        continue
                    b = np.roll(a, -1, axis=0)
                    for p, q in zip(a, b):
                        n = max(1, round(np.linalg.norm(q-p) / 2))
                        points.append(p + np.arange(n)[:, None] / n * (q-p))
                if not points:
                    continue
                points = np.concatenate(points)
                x = np.clip(np.rint(points[:, 0] * factor).astype(int), 0, dist.shape[1]-1)
                y = np.clip(np.rint(points[:, 1] * factor).astype(int), 0, dist.shape[0]-1)
                d = dist[y, x] / factor
                bad = d > 8
                starts = np.flatnonzero(bad & ~np.roll(bad, 1))
                run = (0, 0, 0)
                for st in starts:
                    en = int(st)
                    while bad[en]:
                        en = (en+1) % len(bad)
                        if en == st:
                            break
                    length = (en-int(st)) % len(bad) or len(bad)
                    if length > run[0]:
                        run = (length, int(st), (en-1) % len(bad))
                rows.append({
                    'paper': paper.name, 'view': data.get('map_id') or path.parent.name,
                    'roi': roi.get('label'), 'extent': roi.get('extent', ''),
                    'geometry_model': ('mask_clipped_polygon' if 'whole_seeds' in data else 'direct_polygon'),
                    'source_color_fraction': round(color_fraction, 3),
                    'n_samples': len(d), 'frac_gt8': round(float(bad.mean()), 3),
                    'frac_gt15': round(float((d>15).mean()), 3),
                    'median_dist': round(float(np.median(d)), 1),
                    'max_dist': round(float(d.max()), 1),
                    'longest_offline_px': 2*run[0],
                    'run_start': points[run[1]].round(1).tolist(),
                    'run_end': points[run[2]].round(1).tolist(),
                    'path': str(path.relative_to(root)),
                })
        except Exception as exc:
            print('ERROR', path, exc, flush=True)
    print(paper.name, flush=True)
rows.sort(key=lambda r: (r['longest_offline_px'], r['frac_gt15']), reverse=True)
for r in rows:
    r['source_type'] = 'color or tinted' if r['source_color_fraction'] > 0.02 else 'mostly monochrome'
    r['visual_review_flag'] = ('enlarged review'
                               if r['geometry_model'] == 'direct_polygon'
                               and r['source_color_fraction'] <= 0.02
                               and r['longest_offline_px'] >= 80
                               and r['frac_gt15'] >= 0.05 else '')
    r['manual_review_status'] = ''
known = {
    ('Catania_Remple_2002', 'fig04A_rat', 'V1'): 'color-filled figure; dark-ink score not diagnostic',
    ('Catania_Remple_2002', 'fig04A_rat', 'A1'): 'color-filled figure; dark-ink score not diagnostic',
    ('Felleman_VanEssen_1991', 'fig02', 'SMA'): 'gray source stroke; dark-ink score overstates drift',
    ('Felleman_VanEssen_1991', 'fig02', 'ER posterior'): 'gray source stroke; dark-ink score overstates drift',
}
for review_csv in ['flagged_review_burman_felleman.csv', 'flagged_review_other.csv']:
    with (review_dir / review_csv).open(newline='') as f:
        for reviewed in csv.DictReader(f):
            key = (reviewed['paper'], reviewed['view'], reviewed['roi'])
            known[key] = reviewed['classification'].replace('_', ' ') + '; ' + reviewed['action']
with (review_dir / 'area_changes.csv').open(newline='') as f:
    for change in csv.DictReader(f):
        known[(change['paper_id'], change['map_id'], change['label'])] = 'confirmed and corrected in this review'
for r in rows:
    r['manual_review_status'] = known.get((r['paper'], r['view'], r['roi']), '')
fields = list(rows[0])
with (review_dir / 'line_proximity_all_rois.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
flagged = [r for r in rows if r['visual_review_flag'] or r['manual_review_status']]
with (review_dir / 'line_proximity_flagged.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(flagged)
print(f'{len(rows)} regional ROIs across {len({(r["paper"],r["view"]) for r in rows})} ROI-bearing views; '
      f'{len(flagged)} flagged or manually reviewed')
