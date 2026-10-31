"""Source-guided interior masks, NOT estimates of complete architectural fields.

The selected Fig9A interiors are enclosed by printed gray transition bands and
the solid line across the dorsal/medial map boundary. No atlas is fitted here.
Canonical inputs are the source crop and the explicit seeds/threshold below.
"""
from collections import deque
from pathlib import Path
import csv
import hashlib
import json
import subprocess
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MID = 'fig09A_CJ58R_flatmap'
OUT = ROOT / 'review/boundary_pilot'
FIG = OUT / 'figures' / MID
FIG.mkdir(parents=True, exist_ok=True)
(OUT / 'documentation').mkdir(exist_ok=True)

def flood(allowed, seeds):
    h, w = allowed.shape
    seen = np.zeros((h, w), dtype=bool)
    q = deque()
    for x, y in seeds:
        if allowed[y, x] and not seen[y, x]:
            seen[y, x] = True
            q.append((x, y))
    while q:
        x, y = q.popleft()
        for xx, yy in ((x-1,y), (x+1,y), (x,y-1), (x,y+1)):
            if 0 <= xx < w and 0 <= yy < h and allowed[yy,xx] and not seen[yy,xx]:
                seen[yy,xx] = True
                q.append((xx,yy))
    return seen

source = ROOT / 'figures' / MID / 'source_preview.png'
im = Image.open(source).convert('RGB')
a = np.asarray(im).astype(int)
h, w = a.shape[:2]
# Neutral gray/black printed strokes block connectivity; colored tracer dots
# are not interpreted as architectural boundaries. Threshold is figure-specific.
barrier = (a.max(2)-a.min(2) < 16) & (a.mean(2) < 237)
specs = [('3a_printed_interior', (790,375), '#e56b30'),
         ('3b_printed_interior', (741,390), '#3984eb'),
         ('M1_dorsal_printed_interior', (781,320), '#23b573')]
boundary = [(x,0) for x in range(w)] + [(x,h-1) for x in range(w)]
boundary += [(0,y) for y in range(h)] + [(w-1,y) for y in range(h)]
overlay = np.asarray(im).copy()
im.save(FIG / 'source.tif')
jobs = [['map_id','roi_index','label','source','mask','pixel_size','unit','fractional_pixels','color']]
entries = []
masks = []
for i, (label, seed, color) in enumerate(specs):
    mask = flood(~barrier, [seed])
    # Fill enclosed typography/dot holes; retain the connected outer perimeter.
    mask = ~flood(~mask, boundary)
    if not 2000 < mask.sum() < 10000 or mask[0].any() or mask[-1].any():
        raise ValueError('Seed leaked or failed: ' + label)
    if any((mask & previous).any() for previous in masks):
        raise ValueError('Pilot interiors overlap')
    masks.append(mask)
    mp = FIG / (label + '_mask.tif')
    Image.fromarray(mask.astype('uint8')*255).save(mp)
    rgb = np.array([int(color[j:j+2],16) for j in (1,3,5)])
    overlay[mask] = np.round(.55*overlay[mask]+.45*rgb).astype('uint8')
    jobs.append([MID, str(i), label, str(FIG/'source.tif'), str(mp), '1', 'pixel', str(mask.sum()), color])
    entries.append(dict(label=label, seed_px=seed, mask_file=mp.name, area_px2=int(mask.sum()),
                        area_mm2=None, analysis_eligible=False,
                        status='shape_review_pilot; printed_interior_only; excludes_uncertain_boundary_band'))
Image.fromarray(overlay).save(FIG / 'interior_overlay.png')
Image.fromarray(overlay).crop((640,240,870,450)).resize((920,840)).save(OUT / 'CJ58R_interiors_zoom.png')
im.crop((640,240,870,450)).resize((920,840)).save(OUT / 'CJ58R_source_zoom.png')
Image.open(ROOT/'figures'/MID/'tracing.png').crop((640,240,870,450)).resize((920,840)).save(OUT/'CJ58R_previous_zoom.png')
config = dict(source_map=MID, source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    coordinate_system='pixels of saved source crop; 3 px per PDF point',
    source_pdf_page=11, gray_channel_range_lt=16, gray_mean_lt=237, connectivity=4,
    hole_policy='Fill enclosed text/dot holes; no smoothing or atlas deformation',
    interpretation='Printed interiors excluding gray transition bands, not full field estimates or statistical lower confidence limits. Solid dorsal/medial map line limits these components. No calibration borrowed.',
    limitation='Figure-specific masks. Thresholding fails on CJ61 because colored overlays and open borders permit leakage. Does not recover hidden boundary geometry.',
    rois=entries)
(FIG/'interior_definitions.json').write_text(json.dumps(config,indent=2)+'\n')
jobfile = OUT/'documentation/imagej_jobs.tsv'
with jobfile.open('w',newline='') as f:
    csv.writer(f,delimiter='\t').writerows(jobs)
subprocess.run(['/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home/bin/java',
    '-Djava.awt.headless=true', '--class-path','/Applications/Fiji.app/jars/ij-1.54p.jar',
    str(ROOT/'scripts/ImageJIO.java'),str(jobfile),str(OUT/'figures'),str(OUT/'documentation')],check=True)
# Jobs contain transient absolute execution paths; canonical definitions are portable.
jobfile.unlink()
print(json.dumps(entries,indent=2))
