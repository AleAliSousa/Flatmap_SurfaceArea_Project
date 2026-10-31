#!/usr/bin/env python3
"""Image-assisted contour for a white, line-bounded compartment of a monochrome flatmap.

Used for the 30 October 2026 Felleman fig02 corrections (PaI, AUDITORY remainder). It
implements tracing_method.md items 4 and 6 for a white compartment:

  * the compartment is the white connected component(s) at the given seed(s);
  * thin internal boundary strokes are split at their centre line: every dark pixel is
    assigned to its nearest white component (Euclidean Voronoi), so labels, letters and
    dangling leader tips inside the compartment become tissue, not holes;
  * thick outer-cortex strokes are excluded, so the contour follows their inner edge
    (the convention used by the existing fig02 ROIs, e.g. 13 and Pro);
  * every already-saved ROI is subtracted, so a shared border reuses the neighbour's
    inspected path instead of a second, independently smoothed one;
  * the outline is extracted at 4x, smoothed at ~1.5 px and resampled every ~2 px.

It proposes geometry only. Every result must be inspected over the source before it is
saved, and anatomical identity comes from leader endpoints, not from this script.
"""
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

WHITE = 200        # grey level above which a pixel is paper/tissue interior
THICK_CORE = 2.5   # dark-pixel EDT (px) marking the core of a thick outer stroke
UP = 4             # contour extraction supersampling


def roi_mask(polygons, size):
    """Binary pixel mask with the same (x+.5) convention as measure_flatmaps.coverage."""
    w, h = size
    im = Image.new('L', (w * UP, h * UP), 0)
    dr = ImageDraw.Draw(im)
    for P in polygons:
        dr.polygon([(round((x + .5) * UP), round((y + .5) * UP)) for x, y in P], fill=255)
    a = np.asarray(im).reshape(h, UP, w, UP).mean((1, 3))
    return a >= 127.5


def propose(source_tif, rois, seeds, min_component_px=50):
    g = np.asarray(Image.open(source_tif).convert('L')).astype(int)
    h, w = g.shape
    white = g > WHITE
    lab, _ = ndi.label(white)
    targets = {int(lab[y, x]) for x, y in seeds}
    if 0 in targets:
        raise ValueError('A seed lies on a stroke, not in a white compartment')
    dark = ~white
    core = ndi.distance_transform_edt(dark) >= THICK_CORE
    thick = ndi.binary_dilation(core, iterations=1) & dark
    _, (iy, ix) = ndi.distance_transform_edt(~white, return_indices=True)
    nearest = lab[iy, ix]
    region = np.isin(nearest, list(targets)) & ~thick
    occupied = np.zeros_like(region)
    for r in rois:
        occupied |= roi_mask(r['polygons'], (w, h))
    region &= ~occupied
    region = ndi.binary_opening(region, iterations=1)
    cl, n = ndi.label(region)
    if n == 0:
        raise ValueError('Empty proposal')
    sizes = ndi.sum(region, cl, range(1, n + 1))
    keep = np.isin(cl, [i + 1 for i, s in enumerate(sizes) if s >= min_component_px])
    keep = ndi.binary_fill_holes(keep)
    up = np.kron(keep.astype(np.uint8), np.ones((UP, UP), np.uint8))
    contours, _ = cv2.findContours(up, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    polys = []
    for c in contours:
        c = c[:, 0, :].astype(float)
        if len(c) < 40:
            continue
        # circular smoothing over ~1.5 source px, then resample every ~2 source px
        k = int(1.5 * UP) | 1
        pad = np.vstack([c[-k:], c, c[:k]])
        ker = np.ones(k) / k
        sm = np.column_stack([np.convolve(pad[:, j], ker, 'same') for j in (0, 1)])[k:-k]
        seg = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([sm, sm[:1]]), axis=0).T))]
        t = np.arange(0, seg[-1], 2 * UP)
        xs = np.interp(t, seg, np.r_[sm[:, 0], sm[0, 0]])
        ys = np.interp(t, seg, np.r_[sm[:, 1], sm[0, 1]])
        polys.append([[round((x + .5) / UP - .5, 2), round((y + .5) / UP - .5, 2)] for x, y in zip(xs, ys)])
    return polys, int(keep.sum())


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('map_id')
    ap.add_argument('seed', nargs='+', help='x,y in crop coordinates')
    a = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    d = json.loads((root / 'figures' / a.map_id / 'rois.json').read_text())
    seeds = [tuple(int(v) for v in s.split(',')) for s in a.seed]
    polys, px = propose(root / 'figures' / a.map_id / 'source.tif', d['rois'], seeds)
    print(json.dumps(dict(n_polygons=len(polys), n_vertices=[len(p) for p in polys], mask_px=px)))
