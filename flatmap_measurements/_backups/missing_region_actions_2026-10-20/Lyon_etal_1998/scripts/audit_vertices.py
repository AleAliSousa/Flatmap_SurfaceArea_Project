#!/usr/bin/env python3
"""Check proper crossings, crop bounds, unique labels and document dense tracing."""
import json,csv
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1];issues=[];rows=[]
def cross(a,b,c):return (b[...,0]-a[...,0])*(c[...,1]-a[...,1])-(b[...,1]-a[...,1])*(c[...,0]-a[...,0])
for f in sorted((root/'figures').glob('*/rois.json')):
 d=json.loads(f.read_text());size=np.array(d['crop_xyxy'][2:])-d['crop_xyxy'][:2];labels=[r['label'] for r in d['rois']+d['unmeasured']]
 if len(labels)!=len(set(labels)):issues.append([d['map_id'],'duplicate label'])
 for r in d['rois']:
  vertices=0
  for k,poly in enumerate(r['polygons']):
   p=np.array(poly,float);q=np.roll(p,-1,0);vertices+=len(p)
   if not np.isfinite(p).all() or (p<0).any() or (p>=size).any():issues.append([d['map_id'],r['label'],k,'bounds/nonfinite'])
   for i in range(len(p)):
    js=np.arange(i+2,len(p));js=js[~((i==0)&(js==len(p)-1))]
    hit=(cross(p[i],q[i],p[js])*cross(p[i],q[i],q[js])<0)&(cross(p[js],q[js],p[i])*cross(p[js],q[js],q[i])<0)
    for j in js[hit]:issues.append([d['map_id'],r['label'],k,i,int(j)])
  rows.append(dict(map_id=d['map_id'],label=r['label'],extent=r.get('extent','complete'),vertices=vertices,source_render_pixels_per_pdf_point=d['render_scale'],source_visual_check='enlarged perimeter reviewed; short symbol continuations documented',tracing_method=r.get('tracing_method','source-guided dense tracing'),anatomical_certification='pending'))
with (root/'documentation/contour_precision.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['map_id','label','extent','vertices','source_render_pixels_per_pdf_point','source_visual_check','tracing_method','anatomical_certification']);w.writeheader();w.writerows(rows)
(root/'documentation/vertex_validation.json').write_text(json.dumps(dict(fields_checked=len(rows),proper_crossings_or_invalid_bounds=issues),indent=2)+'\n')
if issues:raise ValueError(issues)
print(root.name,len(rows),'contours: vertex/label checks passed')
