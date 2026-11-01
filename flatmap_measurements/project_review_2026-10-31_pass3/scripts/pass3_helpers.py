from pathlib import Path
import json,zipfile,math,copy
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3]; FM=ROOT/'flatmap_measurements'; OUT=Path(__file__).resolve().parents[1]
for x in ['before','candidates','changes','enlarged']:(OUT/x).mkdir(exist_ok=True)
FONT=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',16)
def archive(paper):
 dst=OUT/'before'/(paper+'.zip')
 if not dst.exists():
  with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as z:
   for f in (FM/paper).rglob('*'):
    if f.is_file() and not any(x in f.parts for x in ['revisions','__pycache__']):z.write(f,f.relative_to(FM/paper))
def curve(points,closed=False,step=2):
 a=np.array(points,float);out=[];n=len(a)
 for i in range(n if closed else n-1):
  p1=a[i];p2=a[(i+1)%n];p0=a[(i-1)%n] if closed or i else 2*p1-p2;p3=a[(i+2)%n] if closed or i+2<n else 2*p2-p1
  for t in np.linspace(0,1,max(2,int(np.linalg.norm(p2-p1)/step)),endpoint=False):out.append((.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)).round(3).tolist())
 if not closed:out.append(a[-1].tolist())
 return out
def get(paper,mid):return json.loads((FM/paper/'figures'/mid/'rois.json').read_text())
def preview(paper,mid,old,new,name=None):
 im=Image.open(FM/paper/'figures'/mid/'source.tif').convert('RGB');pts=np.vstack((old or new)['polygons']+new['polygons']);lo=np.maximum(0,np.floor(pts.min(axis=0)-20)).astype(int);hi=np.minimum(im.size,np.ceil(pts.max(axis=0)+21)).astype(int);bbox=tuple(lo)+tuple(hi)
 cards=[]
 for title,r in [('Source',None),('Before',old),('Proposed' if name else 'Current',new)]:
  t=im.copy();dr=ImageDraw.Draw(t)
  if r:
   for poly in r['polygons']:dr.line([tuple(p) for p in poly]+[tuple(poly[0])],fill='#00a7c8',width=max(1,round(max(im.size)/1200)))
  t=t.crop(bbox);ratio=min(440/t.width,650/t.height);t=t.resize((round(t.width*ratio),round(t.height*ratio)));c=Image.new('RGB',(450,700),'white');c.paste(t,((450-t.width)//2,35));ImageDraw.Draw(c).text((5,5),title,fill='black',font=FONT);cards.append(c)
 result=Image.new('RGB',(1350,730),'#dce6e2');ImageDraw.Draw(result).text((5,4),paper+' / '+mid+' / '+new['label'],font=FONT,fill='black')
 for i,c in enumerate(cards):result.paste(c,(i*450,30))
 dest=OUT/'candidates'/((name or paper+'__'+mid+'__'+new['label'].replace('/','_'))+'.jpg');result.save(dest,quality=94);return str(dest)
def candidate(paper,mid,label,polygons,note,extent=None,**extra):
 d=get(paper,mid);old=next((r for r in d['rois'] if r['label']==label),None);new=copy.deepcopy(old) if old else dict(label=label,extent=extent or 'complete')
 new.update(polygons=polygons,boundary_note=note,tracing_method='Source-guided manual envelope; shared boundary paths reused');new.update(extra)
 if extent:new['extent']=extent
 event=dict(paper_id=paper,map_id=mid,label=label,before=old,after=new,reason=note,status='candidate_pending_visual_review')
 name=paper+'__'+mid+'__'+label.replace('/','_');(OUT/'candidates'/(name+'.json')).write_text(json.dumps(event,indent=2)+'\n');preview(paper,mid,old,new,name)
def record(paper,notes,trace=True,source=True,extra=None):
 p=OUT/'screening_log.json';a=json.loads(p.read_text()) if p.exists() else {};a[paper]=dict(notes=notes,trace_overviews_seen=trace,source_overviews_seen=source,scope='Overview screening; enlarged checks separately recorded. Not every boundary validated.',**(extra or {}));p.write_text(json.dumps(a,indent=2)+'\n')
