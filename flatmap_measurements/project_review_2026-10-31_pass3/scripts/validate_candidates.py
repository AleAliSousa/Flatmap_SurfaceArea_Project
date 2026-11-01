from pass3_helpers import *
rows=[]
for f in sorted((OUT/'candidates').glob('*.json')):
 d=json.loads(f.read_text())
 if 'after' not in d:continue
 size=Image.open(FM/d['paper_id']/'figures'/d['map_id']/'source.tif').size
 violations=[]
 for k,p in enumerate(d['after']['polygons']):
  clean=[]
  for q in p:
   if not clean or q!=clean[-1]:clean.append(q)
  if clean[-1]==clean[0]:clean.pop()
  d['after']['polygons'][k]=clean;a=np.array(clean);b=np.roll(a,-1,axis=0);v=b-a
  if ((a<0)|(a>=size)).any():violations.append('out_of_bounds')
  for i in range(len(a)):
   j=np.arange(i+2,len(a));j=j[j!=(len(a)-1)] if i==0 else j
   if not len(j):continue
   def cross(x,y):return x[...,0]*y[...,1]-x[...,1]*y[...,0]
   c1=cross(v[i],a[j]-a[i]);c2=cross(v[i],b[j]-a[i]);c3=cross(v[j],a[i]-a[j]);c4=cross(v[j],b[i]-a[j]);ix=j[(c1*c2 < -1e-8)&(c3*c4 < -1e-8)]
   if len(ix):violations.append(dict(segment=i,crossing=ix.tolist()))
 f.write_text(json.dumps(d,indent=2)+'\n');rows.append(dict(paper_id=d['paper_id'],map_id=d['map_id'],label=d['label'],violations=violations))
(OUT/'candidate_geometry_validation.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps([x for x in rows if x['violations']],indent=2));print(len(rows),'candidates checked')
