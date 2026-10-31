from pathlib import Path
from collections import deque
import json,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parents[1]; C=OUT/'candidates';C.mkdir(exist_ok=True)
def flood(a,seed):
 h,w=a.shape;out=np.zeros_like(a);x,y=seed
 if not a[y,x]:return out
 q=deque([(x,y)]);out[y,x]=1
 while q:
  x,y=q.popleft()
  for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=xx<w and 0<=yy<h and a[yy,xx] and not out[yy,xx]:out[yy,xx]=1;q.append((xx,yy))
 return out
def largest(a):
 work=a.copy();best=np.zeros_like(a)
 while work.any():
  y,x=np.argwhere(work)[0];comp=flood(work,(x,y));work[comp]=0
  if comp.sum()>best.sum():best=comp
 return best

def candidate(paper,mid,ink_threshold=150,inset=2):
 folder=ROOT/'flatmap_measurements'/paper/'figures'/mid;im=Image.open(folder/'source.tif').convert('RGB');a=np.asarray(im.convert('L'))<ink_threshold
 comp=largest(a);pad=np.pad(comp,1);outside=flood(~pad,(0,0))[1:-1,1:-1];mask=Image.fromarray((~outside).astype('uint8')*255)
 if inset:mask=mask.filter(ImageFilter.MinFilter(2*inset+1))
 name=paper+'__'+mid;mask.save(C/(name+'.tif'))
 subprocess.run(['/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home/bin/java','-Djava.awt.headless=true','--class-path','/Applications/Fiji.app/jars/ij-1.54p.jar',str(OUT/'scripts/MaskOutline.java'),str(C/(name+'.tif')),str(C/(name+'.json'))],check=True,stdout=subprocess.DEVNULL)
 poly=json.loads((C/(name+'.json')).read_text());trace=im.copy();d=ImageDraw.Draw(trace);d.line([tuple(p) for p in poly]+[tuple(poly[0])],fill='#00b6e0',width=2)
 trace.save(C/(name+'.png'));print(name,im.size,len(poly),int(np.asarray(mask).sum()/255))
if __name__=='__main__':
 for mid in ['fig10A','fig10B','fig07A']:candidate('Beck_etal_1996',mid)
 for mid in ['fig04_9213_distal_forelimb','fig04_9321_distal_forelimb','fig04_9324_distal_forelimb']:candidate('Frost_etal_2000',mid,150,1)
