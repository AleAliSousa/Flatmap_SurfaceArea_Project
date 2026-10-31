#!/usr/bin/env python3
"""Rebuild measurements from rois.json WITHOUT the native ImageJ export step.

Used on 2026-10-30 in an environment with no ImageJ/Fiji jar and Java 11. It runs the
unchanged measure_flatmaps.rebuild() (same rendering, coverage and CSV code) but skips
the ImageJIO.java call, then marks validation.json so nobody mistakes the result for a
verified native round trip.

Stale until the full rebuild is rerun locally:
  figures/<map_id>/RoiSet.zip, Masks.tif.zip, documentation/imagej_measurements.tsv,
  documentation/imagej_runtime.txt
Rerun:  python scripts/rebuild_all.py --java /path/to/java17 --ij-jar /path/to/ij.jar
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import measure_flatmaps as mf  # noqa: E402

root = Path(__file__).resolve().parents[1]
_real_run = subprocess.run


def _skip_imagej(cmd, *a, **k):
    if any(str(c).endswith('ImageJIO.java') for c in cmd):
        print('skipped native ImageJ export (not available here)')
        return subprocess.CompletedProcess(cmd, 0)
    return _real_run(cmd, *a, **k)


mf.resolve_imagej = lambda java, jar: ('java', 'ij.jar-not-available')
mf.subprocess.run = _skip_imagej
mf.rebuild(root)
vp = root / 'documentation' / 'validation.json'
v = json.loads(vp.read_text())
v['native_imagej_roundtrip'] = ('PENDING: 2026-10-30 Python-only rebuild; RoiSet.zip, Masks.tif.zip and '
                                'imagej_measurements.tsv predate the current rois.json. Rerun rebuild_all.py with ImageJ.')
vp.write_text(json.dumps(v, indent=2) + '\n')
for s in ['audit_vertices.py', 'audit_geometry.py']:
    _real_run([sys.executable, '-B', str(root / 'scripts' / s)], check=True, stdout=subprocess.DEVNULL)
print('python-only rebuild done; native ImageJ export pending')
