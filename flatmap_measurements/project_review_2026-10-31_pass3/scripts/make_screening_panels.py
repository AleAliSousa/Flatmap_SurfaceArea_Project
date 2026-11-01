from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
O=Path(__file__).resolve().parents[1]; D=O/'screening';D.mkdir(exist_ok=True)
f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',18)
manifest=[]
for typ,fn,key in [('trace','sheets.json','file'),('source','source_sheets.json','sheet')]:
 rows=json.loads((O/fn).read_text());papers=sorted(set(r['paper_id'] for r in rows))
 for paper in papers:
  rr=[r for r in rows if r['paper_id']==paper]
  for j in range(0,len(rr),4):
   group=rr[j:j+4];ims=[]
   for r in group:
    im=Image.open(O/('sheets' if typ=='trace' else 'source_sheets')/r[key]);im.thumbnail((1000,1100));ims.append(im)
   width=max(im.width for im in ims);height=sum(im.height for im in ims)+len(ims)*28
   out=Image.new('RGB',(width,height),'#e4eeeb');d=ImageDraw.Draw(out);y=0
   for r,im in zip(group,ims):
    d.text((3,y),r[key],font=f,fill='black');y+=28;out.paste(im,(0,y));y+=im.height
   name=f'{paper}__{typ}_{j//4+1}.jpg';out.save(D/name,quality=91);manifest.append(dict(file=name,paper_id=paper,kind=typ,sheets=[r[key] for r in group]))
(O/'screening_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(len(manifest))
