#!/usr/bin/env python3
"""Audit saved geometry overlaps without treating adjacent fields as a partition."""
import itertools
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from measure_flatmaps import coverage

root = Path(__file__).resolve().parents[1]
checks = []
for path in sorted((root / 'figures').glob('*/rois.json')):
    d = json.loads(path.read_text())
    size = (d['crop_xyxy'][2] - d['crop_xyxy'][0], d['crop_xyxy'][3] - d['crop_xyxy'][1])
    outline = coverage(d['outline'], size, d['supersample']) if d.get('outline') else None
    masks = []
    for region in d['rois']:
        c = coverage(region, size, d['supersample'])
        if outline is not None:
            c = np.minimum(c, outline)
        mask = c >= 0.5
        interior = np.asarray(Image.fromarray(mask.astype('uint8') * 255).filter(ImageFilter.MinFilter(5))) > 0
        masks.append((region['label'], mask, interior))
    for a, b in itertools.combinations(masks, 2):
        overlap = int(np.count_nonzero(a[1] & b[1]))
        if overlap:
            interior_overlap = int(np.count_nonzero(a[2] & b[2]))
            checks.append(dict(map_id=d['map_id'], field_a=a[0], field_b=b[0],
                overlap_pixels=overlap, overlap_after_eroding_both_masks_2px=interior_overlap,
                interpretation='documented source overlap' if sorted([a[0],b[0]]) in [sorted(pair) for pair in d.get('permitted_source_overlaps',[])] else 'shared-border raster sliver' if not interior_overlap else 'inspect interior overlap'))
result = dict(overlap_method='Each binary mask eroded by a 5x5 square (two pixels per side); report intersection before and after erosion. This is a geometry diagnostic, not uncertainty estimation.', overlaps=checks,
    new_tracings_source_visually_inspected=True, anatomical_certification=False)
(root / 'documentation/geometry_review.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
if any(x['overlap_after_eroding_both_masks_2px'] and x['interpretation']!='documented source overlap' for x in checks):
    raise SystemExit('Interior overlap needs review')
