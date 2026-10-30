#!/usr/bin/env python3
"""Portable source/contour comparison from canonical ROI definitions."""
from pathlib import Path
import json,html,csv
from PIL import Image
root=Path(__file__).resolve().parents[1];dest=root/'review/precision';dest.mkdir(exist_ok=True)
esc=html.escape
measure=list(csv.DictReader((root/'data/measurements.csv').open()));cards=[]
for f in sorted((root/'figures').glob('*/rois.json')):
 d=json.loads(f.read_text());mid=d['map_id'];im=Image.open(f.parent/'source.tif');im.convert('RGB').save(dest/(mid+'.png'));w,h=im.size
 regions=[]
 for r in d['rois']:
  p=[pt for poly in r['polygons'] for pt in poly];xs=[x[0] for x in p];ys=[x[1] for x in p];pad=25;box=[max(0,min(xs)-pad),max(0,min(ys)-pad),min(w,max(xs)+pad),min(h,max(ys)+pad)];box[2]-=box[0];box[3]-=box[1]
  regions.append({'label':r['label'],'box':box,'extent':r.get('extent','complete'),'note':r.get('boundary_note','')})
 opts='<option value="-1">Whole source crop</option>'+''.join('<option value="'+str(i)+'">'+esc(r['label'])+' · '+esc(r['extent'])+'</option>' for i,r in enumerate(regions))
 paths=''
 for i,r in enumerate(d['rois']):
  color='#b66a00' if 'approx' in r.get('extent','') else '#9443c7' if r.get('extent')=='partial' else '#00859a'
  for poly in r['polygons']:
   points=' '.join(f'{x:.2f},{y:.2f}' for x,y in poly);paths+=f'<polygon data-region="{i}" points="{points}" fill="none" stroke="{color}" stroke-width="1.7" vector-effect="non-scaling-stroke"><title>{esc(r["label"])}</title></polygon>'
  for poly in r.get('exclude_polygons',[]):
   points=' '.join(f'{x:.2f},{y:.2f}' for x,y in poly);paths+=f'<polygon data-region="{i}" points="{points}" fill="none" stroke="{color}" stroke-dasharray="4 2" stroke-width="1.7" vector-effect="non-scaling-stroke"><title>{esc(r["label"])} excluded/shared boundary</title></polygon>'
 e=d.get('scale_endpoints_px',[])
 if e:
  (x,y),(xx,yy)=e;paths+=f'<path d="M{x},{y-7}V{y+7} M{xx},{yy-7}V{yy+7}" stroke="#d83838" stroke-width="1" vector-effect="non-scaling-stroke"/>'
 links=f'<a href="../figures/{mid}/rois.json">Editable coordinates</a> · <a href="../figures/{mid}/source.tif">ImageJ TIFF</a>'
 for filename,label in [('RoiSet.zip','ImageJ ROIs'),('Masks.tif.zip','Masks')]:
  if (f.parent/filename).exists():links+=f' · <a href="../figures/{mid}/{filename}">{label}</a>'
 rows=[]
 for x in measure:
  if x['map_id']!=mid:continue
  rows.append('<tr>'+''.join('<td>'+esc(str(v))+'</td>' for v in [x['label'],x['extent'],x['area_px2'],x['area_mm2'],x['status'],x['boundary_note']])+'</tr>')
 payload=json.dumps(regions).replace('<','\\u003c')
 cards.append(f'''<article id="{mid}"><h2>{esc(mid)} <small>{esc(d['species'])} · case {esc(d['specimen'])}</small></h2>
<p>PDF page {d['pdf_page']}; figure {d['figure']}. {esc(d['view_type'])}. Repeat of: {esc(str(d.get('repeat_of') or 'none assigned'))}.</p>
<p>{esc(d['scale_note'])}</p><p>{links}</p>
<div class="controls"><label>Region <select class="region">{opts}</select></label><label><input type="checkbox" class="overlay" checked> Show contours</label><label>Zoom <input class="zoom" type="range" min="100" max="300" value="100" step="25"></label></div>
<p class="note">Teal: complete envelope · Purple: partial patch · Amber: approximate. Hide contours to inspect source ink. Red ticks mark scale endpoints.</p>
<div class="viewport"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" data-full="0 0 {w} {h}" role="img" aria-label="Source and contours for {mid}"><image href="precision/{mid}.png" x="0" y="0" width="{w}" height="{h}"/><g class="paths">{paths}</g></svg></div>
<div class="tablewrap"><table><thead><tr><th>Field / patch</th><th>Extent</th><th>Pixel area</th><th>mm²</th><th>Status</th><th>Boundary / NA reason</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div><script type="application/json" class="regions">{payload}</script></article>''')
style='''body{font:16px/1.5 system-ui,sans-serif;color:#20343a;background:#f3f6f5;margin:0}main{max-width:1350px;margin:auto;padding:32px}h1{font-size:32px}h2 small{font-size:15px;font-weight:400;display:block}article{background:white;padding:22px;margin:30px 0;border:1px solid #d5dfdf;border-radius:12px}a{color:#006b80}.controls{display:flex;gap:25px;flex-wrap:wrap;padding:12px;background:#edf5f4;position:sticky;top:0;z-index:1}.controls label{display:flex;align-items:center;gap:8px}select{max-width:500px;padding:6px}.viewport{overflow:auto;max-height:85vh;border:1px solid #ddd;background:white}svg{display:block;width:100%;height:auto;max-width:none}.note{font-size:14px;color:#546369}.tablewrap{overflow:auto}table{border-collapse:collapse;font-size:13px;min-width:950px}td,th{padding:9px;border-bottom:1px solid #ddd;text-align:left;vertical-align:top}td:last-child{min-width:380px}nav a{display:inline-block;margin:5px 12px 5px 0}'''
js='''document.querySelectorAll('article').forEach(card=>{const svg=card.querySelector('svg'), regions=JSON.parse(card.querySelector('script.regions').textContent), select=card.querySelector('select.region'), group=card.querySelector('g.paths'), note=card.querySelector('.note');card.querySelector('.overlay').addEventListener('change',e=>{group.style.display=e.target.checked?'':'none'});card.querySelector('.zoom').addEventListener('input',e=>{svg.style.width=e.target.value+'%'});select.addEventListener('change',()=>{const i=Number(select.value);svg.setAttribute('viewBox',i<0?svg.dataset.full:regions[i].box.join(' '));group.querySelectorAll('polygon').forEach(p=>{p.style.opacity=i<0||Number(p.dataset.region)===i?'1':'.15'});note.textContent=i<0?'Teal: complete envelope · Purple: partial patch · Amber: approximate. Hide contours to inspect source ink. Red ticks mark scale endpoints.':regions[i].extent+': '+regions[i].note;});});'''
nav=''.join(f'<a href="#{json.loads(f.read_text())["map_id"]}">{f.parent.name}</a>' for f in sorted((root/'figures').glob('*/rois.json')))
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(root.name)} — precision review</title><style>{style}</style><main><h1>{esc(root.name)} · contour precision review</h1><p>Each source crop uses the saved 4-pixels/PDF-point rendering. Select a field to enlarge its boundary; toggle contours to inspect the original. Dense vertices describe the printed drawing, with source limitations retained.</p><p>All tracings provisional. No complete-neocortex denominator; repeated views are not additional animals. Open boundaries are NA. Physical areas are NA without a labeled scale.</p><p><a href="gallery.html">All-figure source assessment</a> · <a href="../documentation/methods.md">Methods and limits</a> · <a href="../data/measurements.csv">Measurements</a> · <a href="../documentation/figure_inventory.csv">Figure inventory</a></p><nav>{nav}</nav>{''.join(cards)}</main><script>{js}</script></html>'''
(root/'review/precision_review.html').write_text(page)
print(root.name,'source-toggle precision review built',len(cards),'views')
