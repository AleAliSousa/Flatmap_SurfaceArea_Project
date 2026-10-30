import json,cv2,itertools
import numpy as np
from pathlib import Path
vs=json.load(open('/tmp/m1_new_papers/views.json'));out=[]
for v in vs:
 p=Path('flatmap_measurements')/v['paper']/'figures'/v['map_id']/'rois.json'
 if not p.exists():continue
 d=json.loads(p.read_text());w,h=np.array(d['crop_xyxy'][2:])-d['crop_xyxy'][:2];ms=[]
 for r in d['rois']:
  m=np.zeros((h,w),np.uint8)
  for pts in r['polygons']:cv2.fillPoly(m,[np.round(pts).astype(np.int32)],1)
  for pts in r.get('exclude_polygons',[]):cv2.fillPoly(m,[np.round(pts).astype(np.int32)],0)
  m=cv2.erode(m,np.ones((5,5),np.uint8));ms.append((r['label'],m,int(m.sum())))
 for a,b in itertools.combinations(ms,2):
  n=int((a[1]&b[1]).sum())
  if sorted([a[0],b[0]]) in [sorted(x) for x in d.get('allowed_overlap_pairs',[])]:continue
  if n:out.append(dict(paper=v['paper'],map_id=v['map_id'],a=a[0],b=b[0],pixels=n,fraction=round(n/min(a[2],b[2]),3)))
Path('/tmp/m1_new_papers/fast_overlaps.json').write_text(json.dumps(out,indent=2))
for x in out:print(x)
