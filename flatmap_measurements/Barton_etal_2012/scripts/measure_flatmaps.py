#!/usr/bin/env python3
"""Render and measure saved flatmap polygons; no reference dataset is required."""
import argparse
import csv
import hashlib
import html
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import numpy as np
from PIL import Image, ImageDraw
import pypdfium2 as pdfium

PALETTE = ['#009e73', '#0072b2', '#d55e00', '#cc79a7', '#e69f00', '#56b4e9']
METADATA = ['map_id', 'figure', 'panel', 'pdf_page', 'printed_page', 'species',
            'specimen', 'hemisphere', 'view_type', 'hemisphere_relation',
            'linked_main_map', 'repeat_of', 'relationship_note', 'specimen_link_status',
            'include_in_whole_hemisphere_summary', 'outline_scope', 'scale_note',
            'scale_reference_map']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, rows, empty_fields=()):
    fields = list(dict.fromkeys(k for row in rows for k in row)) if rows else list(empty_fields)
    if not fields:
        raise ValueError("CSV schema is required for an empty table")
    with path.open('w', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k: 'NA' if v is None else v for k, v in row.items()} for row in rows)


def check_polygon(points, size):
    p = np.asarray(points, dtype=float)
    w, h = size
    if p.ndim != 2 or p.shape[1] != 2 or len(p) < 3 or not np.isfinite(p).all():
        raise ValueError('Polygon needs at least three finite x/y vertices')
    if (p < 0).any() or (p[:, 0] >= w).any() or (p[:, 1] >= h).any():
        raise ValueError('Polygon vertices must lie inside the source crop')
    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    for i in range(len(p)):
        a, b = p[i], p[(i+1) % len(p)]
        for j in range(i+2, len(p)):
            if i == 0 and j == len(p)-1:
                continue
            c, d = p[j], p[(j+1) % len(p)]
            if cross(a,b,c)*cross(a,b,d) < 0 and cross(c,d,a)*cross(c,d,b) < 0:
                raise ValueError('Self-intersecting polygon')


def coverage(region, size, supersample):
    w, h = size
    canvas = Image.new('L', (w*supersample, h*supersample), 0)
    draw = ImageDraw.Draw(canvas)
    for key, fill in [('polygons', 255), ('exclude_polygons', 0)]:
        for points in region.get(key, []):
            check_polygon(points, size)
            draw.polygon([(round((x+.5)*supersample), round((y+.5)*supersample))
                          for x, y in points], fill=fill)
    return np.asarray(canvas, dtype=np.float32).reshape(h, supersample, w, supersample).mean((1,3))/255


def resolve_imagej(java, ij_jar):
    java = java or shutil.which('java')
    if not ij_jar:
        jars = list(Path('/Applications/Fiji.app/jars').glob('ij-1*.jar'))
        jars += [p for p in [Path('/Applications/ImageJ.app/Contents/Java/ij.jar')] if p.is_file()]
        ij_jar = str(jars[0]) if jars else None
    if not java or not ij_jar or not Path(ij_jar).is_file():
        raise RuntimeError('Native ImageJ export needs Java 17+ and an ij.jar; pass --java and --ij-jar, '
                           'or --skip-imagej to write ImageJ-compatible files with Python (roifile/tifffile)')
    return java, ij_jar


# ---- Python fallback for environments without Java/ImageJ ---------------------------------
# Writes the same files as ImageJIO.java (calibrated TIFF with overlay, RoiSet.zip, Masks.tif.zip)
# using roifile and tifffile. ROIs are pixel-edge traced polygons of the binary masks, like
# ImageJ's ThresholdToSelection. Pixel equality is checked with a centre-sampling even-odd
# rasterizer; the native ImageJ read-back itself is recorded as not run.

def trace_mask_edges(binary):
    """Return closed loops of integer pixel-corner vertices bounding a binary mask."""
    b = np.pad(np.asarray(binary, dtype=bool), 1)
    h, w = b.shape
    edges = {}  # start vertex -> list of end vertices (directed, region on the right)
    def add(a, c):
        edges.setdefault(a, []).append(c)
    ys, xs = np.nonzero(b)
    for y, x in zip(ys.tolist(), xs.tolist()):
        if not b[y-1, x]: add((x, y), (x+1, y))          # top edge, moving right
        if not b[y, x+1]: add((x+1, y), (x+1, y+1))      # right edge, moving down
        if not b[y+1, x]: add((x+1, y+1), (x, y+1))      # bottom edge, moving left
        if not b[y, x-1]: add((x, y+1), (x, y))          # left edge, moving up
    loops = []
    for start in list(edges):
        while edges.get(start):
            loop = [start]
            current = edges[start].pop()
            while current != start:
                loop.append(current)
                current = edges[current].pop()
            simplified = []
            n = len(loop)
            for i in range(n):
                p, q, r = loop[i-1], loop[i], loop[(i+1) % n]
                if (q[0]-p[0])*(r[1]-q[1]) != (q[1]-p[1])*(r[0]-q[0]):
                    simplified.append((q[0]-1, q[1]-1))  # remove padding offset
            loops.append(simplified)
    return loops


def keyhole_polygon(loops):
    """Join several loops into one even-odd polygon with zero-width grid-aligned bridges."""
    loops = sorted(loops, key=len, reverse=True)
    poly = list(loops[0])
    for loop in loops[1:]:
        a, u = poly[0], loop[0]
        corner = (u[0], a[1])
        bridge = [corner] if corner not in (a, u) else []
        poly = [a] + bridge + list(loop) + [u] + bridge[::-1] + [a] + poly[1:]
    return poly


def rasterize_even_odd(points, size):
    """Fill pixels whose centres are inside the polygon (even-odd rule)."""
    w, h = size
    p = np.asarray(points, dtype=np.float64)
    q = np.roll(p, -1, axis=0)
    mask = np.zeros((h, w), dtype=bool)
    rows = {}
    for (x0, y0), (x1, y1) in zip(p, q):
        if y0 == y1:
            continue
        lo, hi = (y0, y1) if y0 < y1 else (y1, y0)
        j0, j1 = math.ceil(lo - .5), math.ceil(hi - .5)
        for j in range(max(j0, 0), min(j1, h)):
            yc = j + .5
            rows.setdefault(j, []).append(x0 + (yc - y0) * (x1 - x0) / (y1 - y0))
    for j, xs in rows.items():
        xs.sort()
        for xa, xb in zip(xs[0::2], xs[1::2]):
            i0, i1 = math.ceil(xa - .5), math.ceil(xb - .5)
            if i1 > i0:
                mask[j, max(i0, 0):min(i1, w)] = True
    return mask


def python_exports(jobs, figures, documentation):
    import roifile
    import tifffile
    import zipfile
    import io
    header, rows_all = jobs[0], jobs[1:]
    groups = {}
    for r in rows_all:
        groups.setdefault(r[0], []).append(r)
    report = ['map_id\troi_index\tlabel\tarea_pixels\tarea_calibrated\tunit\toriginal_fractional_pixels\tpixel_difference_percent\troi_roundtrip_pixels_equal']
    total = 0
    for fig, rows in groups.items():
        folder = figures / fig
        pixel_size, unit = float(rows[0][5]), rows[0][6]
        source = np.asarray(Image.open(rows[0][3]).convert('RGB'))
        h, w = source.shape[:2]
        info = ('Cortical flatmap view ' + fig + '. Provisional manual traces. '
                + ('No scale line: pixel units only.' if unit == 'pixel' else 'Calibration provenance is in rois.json. No shrinkage correction.')
                + ' Overlay and RoiSet.zip contain the same editable selections; do not import both.'
                + ' Files written by the Python fallback exporter (roifile/tifffile); native ImageJ read-back pending.')
        resolution = (1/pixel_size, 1/pixel_size)
        metadata = {'unit': unit if unit != 'pixel' else 'pixel', 'Info': info}
        if int(rows[0][1]) < 0:
            tifffile.imwrite(folder/'source.tif', source, imagej=True, resolution=resolution, metadata=metadata, photometric='rgb')
            print('View ' + fig + ': calibrated source retained; no defensible field ROI (python exporter)')
            continue
        rois, mask_stack, labels = [], [], []
        for row in rows:
            index, label = int(row[1]), row[2]
            mask = np.asarray(Image.open(row[4]).convert('L')) == 255
            loops = trace_mask_edges(mask)
            if not loops:
                raise ValueError('Empty mask: ' + fig + ' ' + label)
            points = keyhole_polygon(loops)
            name = f'{index:02d} {label}'
            roi = roifile.ImagejRoi.frompoints(np.asarray(points, dtype=np.int32), name=name)
            roi.right, roi.bottom = roi.right - 1, roi.bottom - 1  # ImageJ bounds convention (right = max x)
            roi.roitype = roifile.ROI_TYPE.TRACED
            roi.options = roifile.ROI_OPTIONS(8192)  # SCALE_STROKE_WIDTH, as written by ImageJ 1.54
            roi.stroke_width = 1
            rgb = bytes.fromhex(row[8].lstrip('#'))
            roi.stroke_color = b'\xff' + rgb
            roi.position = 0
            decoded = roifile.ImagejRoi.frombytes(roi.tobytes())
            coords = decoded.coordinates()
            refill = rasterize_even_odd(coords, (w, h))
            equal = bool(np.array_equal(refill, mask))
            if not equal:
                raise ValueError('Traced ROI does not reproduce its mask: ' + fig + ' ' + name)
            pixels = int(mask.sum())
            area = pixels * pixel_size * pixel_size
            original = float(row[7])
            report.append('\t'.join([fig, row[1], label, str(pixels), repr(area), 'mm^2' if unit == 'mm' else 'pixel^2',
                                     repr(original), repr(100*(pixels-original)/original), 'true']))
            rois.append(roi)
            mask_stack.append((mask.astype(np.uint8) * 255))
            labels.append(name)
            total += 1
        roifile.roiwrite(folder/'RoiSet.zip', rois, mode='w')
        overlay_bytes = [r.tobytes() for r in rois]
        tifffile.imwrite(folder/'source.tif', source, imagej=True, resolution=resolution,
                         metadata=dict(metadata, Overlays=overlay_bytes), photometric='rgb')
        buffer = io.BytesIO()
        tifffile.imwrite(buffer, np.stack(mask_stack), imagej=True, resolution=resolution,
                         metadata={'unit': metadata['unit'], 'Labels': labels, 'axes': 'ZYX'})
        with zipfile.ZipFile(folder/'Masks.tif.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('Masks.tif', buffer.getvalue())
        # read back
        reread = roifile.roiread(folder/'RoiSet.zip')
        if len(reread) != len(rois) or any(a.name != b.name for a, b in zip(reread, rois)):
            raise ValueError('RoiSet.zip read-back mismatch: ' + fig)
        with tifffile.TiffFile(folder/'source.tif') as t:
            page = t.pages[0]
            if not np.array_equal(page.asarray(), source):
                raise ValueError('Source TIFF pixels changed: ' + fig)
            xres = page.tags['XResolution'].value
            if abs(xres[0]/xres[1] - 1/pixel_size) > 1e-6 * (1/pixel_size):
                raise ValueError('TIFF calibration mismatch: ' + fig)
            if (t.imagej_metadata or {}).get('unit') != metadata['unit'] or len((t.imagej_metadata or {}).get('Overlays', [])) != len(rois):
                raise ValueError('TIFF ImageJ metadata mismatch: ' + fig)
        with zipfile.ZipFile(folder/'Masks.tif.zip') as zf:
            with tifffile.TiffFile(io.BytesIO(zf.read('Masks.tif'))) as t:
                stack = t.asarray()
                if stack.shape[0] != len(rois) or not np.array_equal(stack, np.stack(mask_stack)):
                    raise ValueError('Mask stack read-back mismatch: ' + fig)
        print('Figure ' + fig + ': ' + str(len(rows)) + ' selections written by Python exporter; traced ROIs reproduce masks')
    (documentation/'imagej_measurements.tsv').write_text('\n'.join(report) + '\n')
    (documentation/'imagej_runtime.txt').write_text(
        'Python fallback exporter (roifile ' + roifile.__version__ + '; tifffile ' + tifffile.__version__ +
        '); native ImageJ read-back not run; ' + str(total) + ' traced ROIs reproduce their masks in Python\n')


def rebuild(root, java=None, ij_jar=None, skip_imagej=False):
    manifest = json.loads((root/'source/manifest.json').read_text())
    pdf_path = root/'source/paper.pdf'
    if digest(pdf_path) != manifest['source_sha256']:
        raise ValueError('Source PDF checksum changed; inspect provenance before rebuilding')
    definitions = sorted((root/'figures').glob('*/rois.json'))
    if not definitions:
        raise ValueError('No saved rois.json definitions; inspect and digitize a view first')
    if not skip_imagej:
        java, ij_jar = resolve_imagej(java, ij_jar)
    for name in ['data', 'documentation', 'review']:
        (root/name).mkdir(exist_ok=True)
    pdf = pdfium.PdfDocument(pdf_path)
    rows, views, hemispheres, overlaps, cards = [], [], [], [], []
    seen = set()
    with tempfile.TemporaryDirectory(prefix='flatmap_masks_') as tmpdir:
        tmp = Path(tmpdir)
        jobs = [['map_id','roi_index','label','source','mask','pixel_size','unit','fractional_pixels','color']]
        for definition in definitions:
            d = json.loads(definition.read_text())
            mid, folder = d['map_id'], definition.parent
            if mid != folder.name or mid in seen:
                raise ValueError('map_id must be unique and equal its figure folder name')
            seen.add(mid)
            if not isinstance(d['include_in_whole_hemisphere_summary'], bool):
                raise ValueError('JSON inclusion flag must be boolean')
            included = d['include_in_whole_hemisphere_summary']
            if included and (d['view_type'] != 'whole_hemisphere' or d['outline_scope'] != 'whole_drawn_neocortex'
                             or not d.get('outline') or d.get('repeat_of')):
                raise ValueError('Included maps need independent whole-neocortex reconstruction/outline')
            scale = float(d['render_scale'])
            if not math.isfinite(scale) or scale <= 0:
                raise ValueError('render_scale must be positive')
            page = pdf[int(d['pdf_page'])-1]
            rendered = page.render(scale=scale).to_pil().convert('RGB')
            crop = d['crop_xyxy']
            if len(crop) != 4 or any(int(x) != x for x in crop) or not (
                0 <= crop[0] < crop[2] <= rendered.width and 0 <= crop[1] < crop[3] <= rendered.height):
                raise ValueError('Invalid crop coordinates')
            im = rendered.crop(crop)
            im.save(folder/'source.tif')
            ss = d.get('supersample', 4)
            if not isinstance(ss, int) or not 1 <= ss <= 16:
                raise ValueError('supersample must be an integer from 1 to 16')
            endpoints = d.get('scale_endpoints_px', [])
            length_mm = d.get('scale_length_mm')
            bar = None
            factor = None
            if endpoints:
                if len(endpoints) != 2 or any(len(p) != 2 for p in endpoints):
                    raise ValueError('Scale needs two x/y endpoints')
                bar = math.dist(*endpoints)
                if not math.isfinite(bar) or bar <= 0 or length_mm is None or not math.isfinite(length_mm) or length_mm <= 0:
                    raise ValueError('Invalid calibration')
                if not d.get('scale_reference_map') and any(
                    x < 0 or y < 0 or x >= im.width or y >= im.height for x, y in endpoints):
                    raise ValueError('Local scale endpoints must lie in crop')
                factor = (length_mm/bar)**2
            outline = coverage(d['outline'], im.size, ss) if d.get('outline') else None
            denominator = float(outline.sum(dtype=np.float64)) if outline is not None else None
            if denominator is not None and denominator <= 0:
                raise ValueError('Empty outline')
            regions = ([dict(d['outline'], is_outline=True, extent='complete')] if outline is not None else [])
            regions += [dict(r, is_outline=False) for r in d['rois']]
            labels = [r['label'] for r in regions] + [r['label'] for r in d.get('unmeasured', [])]
            if len(set(labels)) != len(labels) or any('\t' in x or '\n' in x for x in labels):
                raise ValueError('Labels must be unique and cannot contain tabs/newlines')
            trace = im.copy()
            draw = ImageDraw.Draw(trace)
            masks = []
            base = {k: d.get(k) for k in METADATA}
            base.update(scale_length_mm=length_mm, scale_length_px=bar,
                        source_roi_file='../figures/'+mid+'/rois.json')
            map_rows = []
            for index, region in enumerate(regions):
                cov = outline if region['is_outline'] else coverage(region, im.size, ss)
                if outline is not None and not region['is_outline']:
                    cov = np.minimum(cov, outline)
                area = float(cov.sum(dtype=np.float64))
                if area <= 0:
                    raise ValueError('Empty ROI: '+mid+' '+region['label'])
                pct = 100*area/denominator if denominator else None
                row = dict(base, label=region['label'], is_outline=region['is_outline'],
                           extent=region.get('extent', 'complete'), area_px2=area,
                           area_mm2=area*factor if factor else None,
                           percent_of_drawn_neocortex=pct if included else None,
                           percent_of_drawn_outline=pct, sensitivity_low_mm2=None, sensitivity_high_mm2=None,
                           status='provisional; anatomical review required', boundary_note=region.get('boundary_note'))
                map_rows.append(row)
                color = PALETTE[index % len(PALETTE)]
                for polygon in region.get('polygons', []) + region.get('exclude_polygons', []):
                    draw.line([tuple(p) for p in polygon]+[tuple(polygon[0])], fill=color, width=2)
                binary = cov >= .5
                mask_path = tmp/f'{mid}_{index}.tif'
                Image.fromarray(binary.astype('uint8')*255).save(mask_path)
                jobs.append([mid, str(index), region['label'], str(folder/'source.tif'), str(mask_path),
                             str(math.sqrt(factor) if factor else 1), 'mm' if factor else 'pixel', str(area), color])
                if not region['is_outline']:
                    masks.append((region['label'], binary))
            for region in d.get('unmeasured', []):
                map_rows.append(dict(base, label=region['label'], is_outline=False, extent=None,
                    area_px2=None, area_mm2=None, percent_of_drawn_neocortex=None, percent_of_drawn_outline=None,
                    sensitivity_low_mm2=None, sensitivity_high_mm2=None,
                    status=region['status'], boundary_note=region['reason']))
            for a, (label_a, mask_a) in enumerate(masks):
                for label_b, mask_b in masks[a+1:]:
                    n = int((mask_a & mask_b).sum())
                    if n:
                        overlaps.append(dict(map_id=mid, field_a=label_a, field_b=label_b, overlap_pixels=n))
            for x, y in endpoints:
                draw.line([(x-5,y),(x+5,y)],fill='red',width=2)
                draw.line([(x,y-5),(x,y+5)],fill='red',width=2)
            trace.save(folder/'tracing.png')
            if not regions:
                jobs.append([mid, '-1', '', str(folder/'source.tif'), '',
                             str(math.sqrt(factor) if factor else 1), 'mm' if factor else 'pixel', '0', '#000000'])
            rows.extend(map_rows)
            views.append(dict(base, measured_fields=len(d['rois']), unmeasured_fields=len(d.get('unmeasured', []))))
            if included:
                hemispheres.append(dict(map_id=mid, species=d['species'], specimen=d['specimen'],
                    figure=d['figure'], neocortex_pixels=denominator, neocortex_mm2=denominator*factor if factor else None))
            table = ''.join('<tr><td>'+html.escape(r['label'])+'</td><td>'+('NA' if r['area_mm2'] is None else f"{r['area_mm2']:.3f}")+
                '</td><td>'+('NA' if r['percent_of_drawn_neocortex'] is None else f"{r['percent_of_drawn_neocortex']:.3f}")+
                '</td><td>'+html.escape(r['status'])+'</td></tr>' for r in map_rows)
            cards.append(f'<section><h2>{html.escape(mid)} — {html.escape(d["specimen"])}</h2>'
                f'<p>{html.escape(d.get("review_note", "Provisional digitization; inspect anatomical boundaries."))}</p>'
                f'<div class="images"><img src="../figures/{mid}/source.tif" alt="Source (TIFF)">'
                f'<img src="../figures/{mid}/tracing.png" alt="Saved tracing"></div>'
                f'<p><a href="../figures/{mid}/RoiSet.zip">ImageJ ROIs</a> · '
                f'<a href="../figures/{mid}/source.tif">Calibrated TIFF</a></p>'
                f'<table><tr><th>Field</th><th>mm²</th><th>% neocortex</th><th>Status</th></tr>{table}</table></section>')
            # PNG preview avoids browsers that cannot display TIFF; original TIFF stays canonical.
            im.save(folder/'source_preview.png')
        job_path = tmp/'jobs.tsv'
        with job_path.open('w', newline='') as out:
            csv.writer(out, delimiter='\t').writerows(jobs)
        if skip_imagej:
            python_exports(jobs, root/'figures', root/'documentation')
        else:
            subprocess.run([str(java), '-Djava.awt.headless=true', '--class-path', str(ij_jar),
                            str(root/'scripts/ImageJIO.java'), str(job_path), str(root/'figures'),
                            str(root/'documentation')], check=True)
    write_csv(root/'data/measurements.csv', rows)
    write_csv(root/'data/view_index.csv', views)
    write_csv(root/'data/hemisphere_summary.csv', hemispheres,
              ['map_id','species','specimen','figure','neocortex_pixels','neocortex_mm2'])
    validation = dict(processed_views=len(views), measured_fields=sum(v['measured_fields'] for v in views),
        unmeasured_fields=sum(v['unmeasured_fields'] for v in views), overlaps=overlaps,
        native_imagej_roundtrip=('not_run: ImageJ-compatible files written by the Python fallback exporter '
                                 '(roifile/tifffile); rerun --rebuild with Java 17+ and ImageJ/Fiji for native verification'
                                 if skip_imagej else 'passed'),
        anatomical_review='provisional; pending user review',
        reference_comparison='not_run; core workflow does not require reference data')
    (root/'documentation/validation.json').write_text(json.dumps(validation, indent=2)+'\n')
    page = '<!doctype html><meta charset="utf-8"><title>Flatmap tracing review</title><style>body{font:16px Arial;max-width:1400px;margin:32px auto;padding:20px;color:#18302e} .images{display:flex;gap:16px}.images img{width:49%;object-fit:contain}table{border-collapse:collapse}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}section{margin-bottom:50px}</style><h1>Flatmap tracing review</h1><p>Source image, saved anatomical outlines and scale endpoints. Unfinished fields are NA.</p>' + ''.join(cards)
    (root/'review/gallery.html').write_text(page.replace('/source.tif" alt="Source (TIFF)"', '/source_preview.png" alt="Source"'))
    outputs = [p for name in ['source','figures','data','scripts','review','documentation']
               for p in (root/name).rglob('*') if p.is_file() and p.name != 'checksums.json' and '__pycache__' not in p.parts]
    (root/'documentation/checksums.json').write_text(json.dumps({str(p.relative_to(root)):digest(p) for p in outputs},indent=2)+'\n')
    print(json.dumps(validation))


def verify(root):
    checks = json.loads((root/'documentation/checksums.json').read_text())
    for rel, expected in checks.items():
        if digest(root/rel) != expected:
            raise ValueError('Changed file: '+rel)
    with (root/'data/measurements.csv').open() as source:
        rows = list(csv.DictReader(source))
    keys = [(r['map_id'], r['label']) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate measurements')
    denominators = {r['map_id']:float(r['area_px2']) for r in rows
                    if r.get('is_outline') == 'True' and r['area_px2'] != 'NA'}
    for row in rows:
        if row['area_px2'] == 'NA':
            if any(row[k] != 'NA' for k in ['area_mm2','percent_of_drawn_neocortex','percent_of_drawn_outline']):
                raise ValueError('A missing field has a derived measurement')
            continue
        area = float(row['area_px2'])
        if row['area_mm2'] != 'NA':
            expected = area * (float(row['scale_length_mm'])/float(row['scale_length_px']))**2
            if not math.isclose(float(row['area_mm2']), expected, rel_tol=1e-10):
                raise ValueError('Area calibration mismatch')
        for column in ['percent_of_drawn_neocortex','percent_of_drawn_outline']:
            if row[column] != 'NA':
                expected = 100*area/denominators[row['map_id']]
                if not math.isclose(float(row[column]), expected, rel_tol=1e-10):
                    raise ValueError('Percentage denominator mismatch')
        if row['include_in_whole_hemisphere_summary'] != 'True' and row['percent_of_drawn_neocortex'] != 'NA':
            raise ValueError('Excluded view has a whole-neocortex percentage')
    print(f'Verified {len(checks)} saved file hashes, {len(rows)} unique rows, areas and percentages.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paper-dir', type=Path, default=Path(__file__).resolve().parent.parent)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--rebuild', action='store_true')
    action.add_argument('--verify', action='store_true')
    parser.add_argument('--java')
    parser.add_argument('--ij-jar')
    parser.add_argument('--skip-imagej', action='store_true',
                        help='no Java/ImageJ available: write ImageJ-compatible TIFF/ROI/mask files with '
                             'roifile and tifffile and record the native read-back as not run')
    args = parser.parse_args()
    if args.verify:
        verify(args.paper_dir.resolve())
    else:
        rebuild(args.paper_dir.resolve(), args.java, args.ij_jar, args.skip_imagej)
