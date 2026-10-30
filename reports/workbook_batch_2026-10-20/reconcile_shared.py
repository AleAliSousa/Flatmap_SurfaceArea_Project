"""Reconcile narrow overlaps of adjacent manually guided contours; reject broad conflicts."""
from pathlib import Path
import json,cv2,numpy as np,itertools,sys
ROOT=Path('flatmap_measurements');cfg=json.load(open('/tmp/m1_new_papers/views.json'));reports=[];bad=[]
for v in cfg:
 if v['paper'] not in ['Rosa_etal_1993','Krubitzer_2009','VanEssen_2005']:continue
 if len(sys.argv)>1 and v['paper'] not in sys.argv[1:] and v['map_id'] not in sys.argv[1:]:continue
 p=ROOT/v['paper']/'figures'/v['map_id']/'rois.json'
 if not p.exists():continue
 d=json.loads(p.read_text());w,h=np.array(d['crop_xyxy'][2:])-d['crop_xyxy'][:2];masks=[]
 for r in d['rois']:
  m=np.zeros((h,w),np.uint8)
  for pts in r['polygons']:cv2.fillPoly(m,[np.round(pts).astype(np.int32)],1)
  for pts in r.get('exclude_polygons',[]):cv2.fillPoly(m,[np.round(pts).astype(np.int32)],0)
  masks.append(m)
 orig=[m.copy() for m in masks];dist=[cv2.distanceTransform(m,cv2.DIST_L2,5) for m in masks];changed=set();allowed={tuple(sorted(x)) for x in d.get('allowed_overlap_pairs',[])}
 for i,j in itertools.combinations(range(len(masks)),2):
  labels=[d['rois'][i]['label'],d['rois'][j]['label']]
  if tuple(sorted(labels)) in allowed:continue
  both=masks[i]&masks[j];count=int(both.sum())
  if not count:continue
  radius=float(cv2.distanceTransform(both,cv2.DIST_L2,5).max());frac=count/min(orig[i].sum(),orig[j].sum())
  record=dict(paper=v['paper'],map_id=v['map_id'],fields=labels,overlap_pixels=count,overlap_fraction_smaller=float(frac),max_overlap_radius_source_pixels=radius)
  if radius>6 or frac>.12:
   bad.append(record);continue
  take_i=dist[i]>=dist[j];masks[i][(both>0)&(~take_i)]=0;masks[j][(both>0)&take_i]=0;changed|={i,j};reports.append(record)
 # Do not partially modify any view with a broad unresolved conflict.
 if any(x['paper']==v['paper'] and x['map_id']==v['map_id'] for x in bad):continue
 for i in changed:
  cs,hier=cv2.findContours(masks[i],cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE);r=d['rois'][i]
  poly=[];holes=[]
  for k,c in enumerate(cs):
   if cv2.contourArea(c)<3:continue
   pts=cv2.approxPolyDP(c,.35,True).reshape(-1,2).astype(float).tolist()
   if len(pts)<3:continue
   (poly if hier[0,k,3]<0 else holes).append(pts)
  r['polygons']=poly;r['exclude_polygons']=holes;r['shared_boundary_note']='Narrow adjacent-guide overlap reconciled at equidistance from the two interiors; maximum overlap half-width <=6 rendered pixels. No broad conflict accepted. Shared raster edge exported to both ROIs.'
 if changed:
  backup=ROOT/v['paper']/'documentation/pre_reconciliation';backup.mkdir(exist_ok=True)
  q=backup/(v['map_id']+'.json')
  if not q.exists():q.write_text(p.read_text())
  p.write_text(json.dumps(d,indent=2)+'\n')
Path('/tmp/m1_new_papers/reconciliation.json').write_text(json.dumps(dict(reconciled=reports,unresolved=bad),indent=2))
print('Reconciled narrow pairs:',len(reports),'Unresolved:',len(bad))
for x in bad:print(x)
