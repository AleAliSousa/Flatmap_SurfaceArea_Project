from pass3_helpers import *
import csv,io,hashlib,re
root=FM/'Beck_Kaas_1998';out=root/'review/dm_recheck_2026-10-31';z=zipfile.ZipFile(OUT/'before/Beck_Kaas_1998.zip');old=list(csv.DictReader(io.StringIO(z.read('data/measurements.csv').decode())));new=list(csv.DictReader((root/'data/measurements.csv').open()));changes=[]
for a in new:
 b=next(x for x in old if x['map_id']==a['map_id'] and x['label']==a['label'])
 if a['area_px2']!=b['area_px2']:changes.append(dict(map_id=a['map_id'],label=a['label'],before_mm2=b['area_mm2'],after_mm2=a['area_mm2'],percent_change=100*(float(a['area_mm2'])/float(b['area_mm2'])-1)))
for f in (root/'figures').glob('*/rois.json'):
 d=json.loads(f.read_text());prior=json.loads(z.read(str(f.relative_to(root))))
 for k in ['crop_xyxy','render_scale','scale_endpoints_px','scale_length_mm','species','specimen','hemisphere']:assert d.get(k)==prior.get(k),(f,k)
 im=Image.open(f.parent/'source.tif').convert('RGB');oi=Image.open(io.BytesIO(z.read(str((f.parent/'source.tif').relative_to(root))))).convert('RGB');assert np.array_equal(im,oi)
 for r in d['rois']:
  for poly in r['polygons']:
   a=np.array(poly);assert ((a>=0)&(a<im.size)).all(),f
   b=np.roll(a,-1,axis=0);v=b-a
   def cross(x,y):return x[...,0]*y[...,1]-x[...,1]*y[...,0]
   for i in range(len(a)):
    j=np.arange(i+2,len(a));j=j[j!=len(a)-1] if i==0 else j
    c1=cross(v[i],a[j]-a[i]);c2=cross(v[i],b[j]-a[i]);c3=cross(v[j],a[i]-a[j]);c4=cross(v[j],b[i]-a[j]);assert not ((c1*c2 < -1e-8)&(c3*c4 < -1e-8)).any(),(f,i)
assert sorted(c['map_id'] for c in changes)==['fig03','fig11'],changes
summary=list(csv.DictReader((root/'data/field_area_summary.csv').open()));assert sum(int(r['n']) for r in summary if r['field']=='DM')==5
assert all(int(r['n'])==0 for r in summary if r['field'] in ['DM estimated envelope','DM visible fragment'])
v=json.loads((root/'documentation/validation.json').read_text());assert v['native_imagej_roundtrip']=='passed'
f=out/'followup_recheck.json';r=json.loads(f.read_text());r.update(native_verification='passed',source_pixels_scale_identity_preserved=True,polygon_bounds_and_self_intersections='passed for all eight contours',unchanged_area_values='6/8 unchanged; only Figs3/11 revised',area_changes=changes,summary_exclusions='passed; Figs4/7 estimates and Fig11 partial excluded; five complete published-envelope observations remain',anatomical_certification=False);f.write_text(json.dumps(r,indent=2)+'\n')
p=out/'validation.json';r=json.loads(p.read_text());r.update(geometry_revised_existing=3,additional_recheck='followup_recheck.json');p.write_text(json.dumps(r,indent=2)+'\n')
files=[p for name in ['source','figures','data','scripts','review','documentation'] for p in (root/name).rglob('*') if p.is_file() and p.name!='checksums.json' and p.suffix!='.log' and '__pycache__' not in p.parts];(root/'documentation/checksums.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n');print(json.dumps(changes,indent=2))
