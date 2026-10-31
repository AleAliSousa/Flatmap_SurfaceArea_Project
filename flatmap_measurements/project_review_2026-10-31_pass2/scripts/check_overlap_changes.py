from prepare_precision import *
import io,itertools,csv
changes=json.loads((OUT/'applied_changes.json').read_text());rows=[]
def read_masks(blob,labels):
 z=zipfile.ZipFile(io.BytesIO(blob));im=Image.open(io.BytesIO(z.read('Masks.tif')));assert im.n_frames==len(labels),(im.n_frames,labels)
 out={}
 for i,label in enumerate(labels):
  im.seek(i);im2=im.copy().convert('L');a=np.asarray(im2)>0;b=np.asarray(im2.filter(ImageFilter.MinFilter(5)))>0;out[label]=(a,b)
 return out
for paper,mid in sorted({(c['paper'],c['map_id']) for c in changes}):
 z=zipfile.ZipFile(OUT/'before'/(paper+'.zip'));old=json.loads(z.read('figures/'+mid+'/rois.json'));new=json.loads((FM/paper/'figures'/mid/'rois.json').read_text())
 lab=lambda d:([d['outline']['label']] if d.get('outline') else [])+[r['label'] for r in d['rois']]
 before=read_masks(z.read('figures/'+mid+'/Masks.tif.zip'),lab(old));after=read_masks((FM/paper/'figures'/mid/'Masks.tif.zip').read_bytes(),lab(new))
 for a,b in itertools.combinations([r['label'] for r in new['rois']],2):
  now=int((after[a][1]&after[b][1]).sum());was=int((before[a][1]&before[b][1]).sum()) if a in before and b in before else 0
  if now or was:rows.append(dict(paper_id=paper,map_id=mid,field_a=a,field_b=b,before_interior_overlap_px=was,after_interior_overlap_px=now,change_px=now-was))
with (OUT/'validation/overlap_changes.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(rows,indent=2))
