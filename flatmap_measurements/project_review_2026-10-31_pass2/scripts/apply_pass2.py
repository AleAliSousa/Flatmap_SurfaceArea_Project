"""Apply reviewed proposals once, preserving complete pre-pass datasets."""
from prepare_precision import *
from collections import defaultdict
from copy import deepcopy
changes=json.loads((OUT/'proposed_changes.json').read_text())
if (OUT/'applied_changes.json').exists():raise RuntimeError('Already applied; inspect provenance instead of reapplying')
baseline=json.loads((OUT/'baseline_inventory.json').read_text())
for row in baseline:
 assert hashlib.sha256((FM/row['json']).read_bytes()).hexdigest()==row['sha256'],row['json']
groups=defaultdict(list)
for c in changes:groups[(c['paper'],c['map_id'])].append(c)
updated={}
def cross(a,b,c):return (b[...,0]-a[...,0])*(c[...,1]-a[...,1])-(b[...,1]-a[...,1])*(c[...,0]-a[...,0])
for (paper,mid),cs in groups.items():
 f=FM/paper/'figures'/mid/'rois.json';d=json.loads(f.read_text());size=np.array(Image.open(f.parent/'source.tif').size)
 for c in cs:
  old=next((r for r in d['rois'] if r['label']==c['label']),None)
  assert old==c['old'],(paper,mid,c['label'],'old mismatch')
  new=deepcopy(c['new'])
  for poly in new['polygons']:
   p=np.array(poly,float);q=np.roll(p,-1,axis=0)
   assert np.isfinite(p).all() and (p>=0).all() and (p<size).all(),(paper,mid,c['label'],'bounds')
   for i in range(len(p)):
    js=np.arange(i+2,len(p));js=js[~((i==0)&(js==len(p)-1))]
    hit=(cross(p[i],q[i],p[js])*cross(p[i],q[i],q[js])<0)&(cross(p[js],q[js],p[i])*cross(p[js],q[js],q[i])<0)
    assert not hit.any(),(paper,mid,c['label'],'crossing',i,js[hit])
  new['boundary_note']=new.get('boundary_note','')+' Second project review 2026-10-31: '+c['note']
  new['tracing_method']='Source-reviewed second-pass refinement, 2026-10-31; see project_review_2026-10-31_pass2'
  new['geometry_review']=dict(date='2026-10-31',pass_number=2,status='source_refined_provisional',note=c['note'])
  if old is None:d['rois'].append(new)
  else:d['rois'][d['rois'].index(old)]=new
  d['unmeasured']=[r for r in d.get('unmeasured',[]) if r['label']!=c['label']]
  c['applied_new']=new
 assert len({r['label'] for r in d['rois']+d.get('unmeasured',[])})==len(d['rois'])+len(d.get('unmeasured',[]))
 updated[f]=d
print('Validated',len(changes),'changes in',len(updated),'views',flush=True)
for paper in sorted({c['paper'] for c in changes}):
 archive(paper);print('Archived',paper,flush=True)
for f,d in updated.items():f.write_text(json.dumps(d,indent=2)+'\n')
(OUT/'applied_changes.json').write_text(json.dumps(changes,indent=2)+'\n')
print('Applied',len(changes),'changes',flush=True)
