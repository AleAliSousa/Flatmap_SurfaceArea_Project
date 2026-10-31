from pathlib import Path
import sys,json,subprocess,hashlib,zipfile
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageFont
ROOT=Path(__file__).resolve().parents[3];FM=ROOT/'flatmap_measurements';OUT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(FM/'project_review_2026-10-31/scripts'))
from prepare_candidates import flood
JAVA='/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home/bin/java';IJ='/Applications/Fiji.app/jars/ij-1.54p.jar'
for sub in ['candidates','components','before','sheets','enlarged']:(OUT/sub).mkdir(exist_ok=True)
FONT=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',16)
def archive(paper):
 path=OUT/'before'/(paper+'.zip')
 if path.exists():return
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
  for f in (FM/paper).rglob('*'):
   if f.is_file() and not any(x in f.parts for x in ['revisions','__pycache__']):z.write(f,f.relative_to(FM/paper))
def labels(paper,mid,threshold=190):
 src=FM/paper/'figures'/mid/'source.tif';dest=OUT/'components'/f'{paper}__{mid}_{threshold}.bin'
 if not dest.exists():subprocess.run([JAVA,'-Djava.awt.headless=true','--class-path',IJ,str(OUT/'scripts/Components.java'),str(src),str(dest),str(threshold)],check=True)
 a=np.fromfile(dest,dtype='>i4');w,h,n=a[:3];return a[3:].reshape(h,w)
def mask_region(r,size):
 im=Image.new('1',size);dr=ImageDraw.Draw(im)
 for p in r['polygons']:dr.polygon([tuple(x) for x in p],fill=1)
 for p in r.get('exclude_polygons',[]):dr.polygon([tuple(x) for x in p],fill=0)
 return np.array(im)
def rdp(p,eps=.5):
 p=np.array(p,float)
 if len(p)<3:return p.tolist()
 v=p[-1]-p[0];dd=np.dot(v,v);t=np.clip(((p-p[0])@v)/dd,0,1) if dd else np.zeros(len(p));dist=np.linalg.norm(p-(p[0]+t[:,None]*v),axis=1);i=int(dist.argmax())
 return rdp(p[:i+1],eps)[:-1]+rdp(p[i:],eps) if dist[i]>eps else [p[0].tolist(),p[-1].tolist()]
def mask_outline(mask,name,expand=1,close=0):
 yy,xx=np.where(mask);x0=max(0,int(xx.min())-20);y0=max(0,int(yy.min())-20);x1=min(mask.shape[1],int(xx.max())+21);y1=min(mask.shape[0],int(yy.max())+21)
 im=Image.fromarray(mask[y0:y1,x0:x1].astype('uint8')*255)
 if expand:im=im.filter(ImageFilter.MaxFilter(2*expand+1))
 if close:im=im.filter(ImageFilter.MaxFilter(2*close+1)).filter(ImageFilter.MinFilter(2*close+1))
 a=np.asarray(im)>0;mask=~flood(~np.pad(a,1),(0,0))[1:-1,1:-1]
 im=Image.fromarray(mask.astype('uint8')*255)
 dest=OUT/'candidates'/name;im.save(str(dest)+'.tif')
 subprocess.run([JAVA,'-Djava.awt.headless=true','--class-path',IJ,str(OUT/'scripts/MaskOutline.java'),str(dest)+'.tif',str(dest)+'.json'],check=True,stdout=subprocess.DEVNULL)
 p=np.array(json.loads(Path(str(dest)+'.json').read_text()),float)-.5+np.array([x0,y0]);k=len(p)//2
 return rdp(p[:k+1])+rdp(np.vstack([p[k:],p[:1]]))[1:-1]
def preview(paper,mid,old,new,name,after_title='Candidate'):
 im=Image.open(FM/paper/'figures'/mid/'source.tif').convert('RGB');pts=np.vstack(old['polygons']+new['polygons']);x0,y0=np.floor(pts.min(axis=0)-20).astype(int);x1,y1=np.ceil(pts.max(axis=0)+21).astype(int);bbox=(max(0,x0),max(0,y0),min(im.width,x1),min(im.height,y1));cards=[]
 for title,r in [('Source',None),('Before',old),(after_title,new)]:
  t=im.copy();dr=ImageDraw.Draw(t)
  if r:
   for poly in r['polygons']:dr.line([tuple(p) for p in poly]+[tuple(poly[0])],fill='#00a7c8',width=1)
  t=t.crop(bbox);ratio=min(420/t.width,700/t.height);t=t.resize((round(t.width*ratio),round(t.height*ratio)));c=Image.new('RGB',(430,740),'white');c.paste(t,((430-t.width)//2,40));ImageDraw.Draw(c).text((10,10),title,fill='black',font=FONT);cards.append(c)
 result=Image.new('RGB',(1290,770),'#e2e7e5');dr=ImageDraw.Draw(result);dr.text((10,5),paper+' / '+mid+' / '+new['label'],font=FONT,fill='black')
 for i,c in enumerate(cards):result.paste(c,(i*430,30))
 result.save(OUT/'candidates'/(name+'.jpg'),quality=95)
def suggest(paper):
 result=[]
 for f in sorted((FM/paper/'figures').glob('*/rois.json')):
  d=json.loads(f.read_text());mid=f.parent.name;a=labels(paper,mid);counts=np.bincount(a[a>=0]);size=(a.shape[1],a.shape[0])
  for index,r in enumerate(d['rois']):
   if len(r['polygons'])!=1:continue
   old=mask_region(r,size);inter=np.bincount(a[old&a.__ge__(0)],minlength=len(counts));iou=inter/(old.sum()+counts-inter+1e-9);iou[0]=0;cid=int(iou.argmax());score=float(iou[cid]);name=paper+'__'+mid+'__'+str(index)
   if score<.55:result.append(dict(paper=paper,map_id=mid,label=r['label'],index=index,iou=score,status='no_candidate'));continue
   poly=mask_outline(a==cid,name,expand=1,close=3 if paper=='Ghosh_1997' else 0);new=dict(r,polygons=[poly]);preview(paper,mid,r,new,name)
   result.append(dict(paper=paper,map_id=mid,label=r['label'],index=index,iou=score,status='candidate_pending_visual_review',polygons=[poly],name=name))
 (OUT/(paper+'_candidates.json')).write_text(json.dumps(result,indent=2)+'\n');print(paper,len(result),'candidates',sum(r['status'].startswith('candidate') for r in result),flush=True)
if __name__=='__main__':
 for paper in sys.argv[1:]:suggest(paper)
