from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,csv,hashlib,math
ROOT=Path(__file__).resolve().parents[3];FM=ROOT/'flatmap_measurements';OUT=Path(__file__).resolve().parents[1];S=OUT/'sheets';S.mkdir(exist_ok=True)
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',18);small=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',14)
rows=[];sheets=[]
for paper in sorted(FM.iterdir()):
 fs=sorted((paper/'figures').glob('*/rois.json'))
 if not fs:continue
 cards=[]
 for f in fs:
  d=json.loads(f.read_text());d.setdefault('map_id',f.parent.name);regs=([d['outline']] if d.get('outline') else [])+d.get('rois',[])
  src=f.parent/'source.tif'
  if not src.exists():src=f.parent/'source_preview.png'
  im=Image.open(src).convert('RGB');trace=im.copy();draw=ImageDraw.Draw(trace)
  line=max(1,round(max(im.size)/800))
  for r in regs:
   for poly in r.get('polygons',[]):
    if len(poly)>2:draw.line([tuple(p) for p in poly]+[tuple(poly[0])],fill='#0095b6',width=line)
   for poly in r.get('exclude_polygons',[]):
    if len(poly)>2:draw.line([tuple(p) for p in poly]+[tuple(poly[0])],fill='#e14c2d',width=line)
  card=Image.new('RGB',(1000,560),'white');cd=ImageDraw.Draw(card)
  title=f'{d["map_id"]} | {len(regs)} outlines | {d.get("species",d.get("species_as_reported",""))}'
  cd.text((10,8),title[:113],font=font,fill='black')
  cd.text((10,34),str(d.get('view_type',''))+' | '+str(d.get('specimen',''))[:65],font=small,fill='#333333')
  for j,v in enumerate([im,trace]):
   v=v.copy();ratio=min(490/v.width,465/v.height);v=v.resize((round(v.width*ratio),round(v.height*ratio)));card.paste(v,(j*500+(500-v.width)//2,60+(465-v.height)//2))
  labels=', '.join(r['label'] for r in regs)
  cd.text((10,532),labels[:130] or 'SOURCE ONLY — no saved outline',font=small,fill='#114d5d')
  cards.append(card)
  r=dict(paper_id=paper.name,map_id=d['map_id'],species=d.get('species',d.get('species_as_reported','')),specimen=d.get('specimen',''),view_type=d.get('view_type',''),source_size=f'{im.width}x{im.height}',ROI_count=len(d.get('rois',[])),outline_count=int(bool(d.get('outline'))),labels=labels,has_calibration=bool(d.get('scale_length_mm') and d.get('scale_endpoints_px')),source_roi_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),source_path=str(src.relative_to(FM)),roi_path=str(f.relative_to(FM)),review_status='pending_visual_review' if regs else 'source_only_no_tracing',clarity='',fit='',notes='',improvement='',sheet='')
  rows.append(r)
 for start in range(0,len(cards),4):
  batch=cards[start:start+4];sheet=Image.new('RGB',(2000,560*math.ceil(len(batch)/2)+35),'#d8e0e0');dr=ImageDraw.Draw(sheet);dr.text((10,8),paper.name+f' | views {start+1}–{start+len(batch)}',font=font,fill='black')
  for i,c in enumerate(batch):sheet.paste(c,((i%2)*1000,35+(i//2)*560))
  name=f'{paper.name}_{start//4+1:02d}.jpg';sheet.save(S/name,quality=92)
  selected=[r for r in rows if r['paper_id']==paper.name][start:start+4]
  for r in selected:r['sheet']='sheets/'+name
  sheets.append(dict(file=name,views=[r['map_id'] for r in selected],paper_id=paper.name))
with (OUT/'inventory.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'sheets.json').write_text(json.dumps(sheets,indent=2)+'\n')
if not (OUT/'assessments.json').exists():(OUT/'assessments.json').write_text('{}\n')
print(json.dumps(dict(papers=len(set(r['paper_id'] for r in rows)),views=len(rows),traced_views=sum(r['ROI_count']+r['outline_count']>0 for r in rows),ROIs=sum(r['ROI_count'] for r in rows),sheets=len(sheets)),indent=2))
