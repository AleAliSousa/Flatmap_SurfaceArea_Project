from pass3_helpers import *
import hashlib,csv,io,collections
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
es=json.loads((OUT/'applied_changes.json').read_text());rows=[];seen=set();archives={}
for e in es:
 p=e['paper_id'];mid=e['map_id'];d=get(p,mid);r=next(x for x in d['rois'] if x['label']==e['label']);assert r['polygons']==e['after']['polygons']
 size=Image.open(FM/p/'figures'/mid/'source.tif').size
 for poly in r['polygons']:
  a=np.array(poly);b=np.roll(a,-1,axis=0);v=b-a;assert ((a>=0)&(a<size)).all(),(p,mid,'bounds')
  def cross(x,y):return x[...,0]*y[...,1]-x[...,1]*y[...,0]
  for i in range(len(a)):
   j=np.arange(i+2,len(a));j=j[j!=len(a)-1] if i==0 else j
   c1=cross(v[i],a[j]-a[i]);c2=cross(v[i],b[j]-a[i]);c3=cross(v[j],a[i]-a[j]);c4=cross(v[j],b[i]-a[j]);assert not ((c1*c2<-1e-8)&(c3*c4<-1e-8)).any(),(p,mid,e['label'],'crossing')
 if (p,mid) not in seen:
  seen.add((p,mid));z=archives.setdefault(p,zipfile.ZipFile(OUT/'before'/(p+'.zip')));name='figures/'+mid+'/rois.json'
  if name in z.namelist():
   old=json.loads(z.read(name))
   for k in ['crop_xyxy','render_scale','scale_endpoints_px','scale_length_mm','species','specimen','hemisphere']:assert old.get(k)==d.get(k),(p,mid,k)
   im=Image.open(FM/p/'figures'/mid/'source.tif').convert('RGB');oldim=Image.open(io.BytesIO(z.read('figures/'+mid+'/source.tif'))).convert('RGB');assert np.array_equal(im,oldim),(p,mid,'source pixels')
 rows.append(dict(paper_id=p,map_id=mid,label=e['label'],canonical_matches_event=True,bounds='passed',proper_self_crossings='none'))
for p in {e['paper_id'] for e in es}:assert json.loads((FM/p/'documentation/validation.json').read_text())['native_imagej_roundtrip']=='passed',p
for row in csv.DictReader((FM/'Beck_etal_1996/data/measurements.csv').open()):
 if row['map_id']=='fig11_92_78' and row['area_px2']!='NA':assert row['status']=='projection_uncertain_drawing_area_only',row
rowsn=list(csv.DictReader((FM/'Krubitzer_Dooley_2013/data/measurements.csv').open()));r=next(x for x in rowsn if x['map_id']=='fig07D_naked_mole_rat' and x['label']=='S1_other_body');assert r['status']=='pictorial_footprint_not_anatomical_area';assert r['extent']=='pictorial_footprint'
bur=list(csv.DictReader((FM/'Burman_etal_2008/data/measurements.csv').open()));c=collections.Counter(r['status'] for r in bur if r['area_px2']!='NA');assert c['rejected_pending_retrace']==21 and c['provisional_gray_band_center_estimate']==7,c
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,a):
  self.links.extend(v for k,v in a if k in ['href','src'] and v)
h=Parser();h.feed((OUT/'index.html').read_text())
for link in h.links:
 u=urlparse(link)
 if not u.scheme and u.path:assert (OUT/unquote(u.path)).exists(),link
result=dict(changed_region_checks=rows,native_imagej_roundtrip='passed for all five changed publications',existing_changed_view_source_pixels_and_calibration='unchanged',burman_status_counts=dict(c),naked_mole_rat_pictogram_flag='propagated to canonical measurement table',beck1996_new_view='projection_uncertain_drawing_area_only; repeated case',local_review_links_checked=len(h.links),local_review_links='passed',anatomical_certification=False)
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
# Refresh manifests after documented metadata/report additions and batch regeneration.
changed={e['paper_id'] for e in es}|set(json.loads((FM/'recommended_M1_expansion_2026-10-31/papers.json').read_text()).values())
for p in changed:
 root=FM/p;files=[f for name in ['source','figures','data','scripts','review','documentation'] for f in (root/name).rglob('*') if f.is_file() and f.name!='checksums.json' and '__pycache__' not in f.parts and 'revisions' not in f.parts]
 (root/'documentation/checksums.json').write_text(json.dumps({str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},indent=2)+'\n')
print('Validated',len(es),'changed region records,',len(seen),'changed views;',len(h.links),'local links. Refreshed',len(changed),'manifests.')
print('VERIFY_PAPERS='+json.dumps(sorted(changed)))
