#!/usr/bin/env python3
"""Portable contour-audit review from current/prior canonical geometry and source rasters."""
import csv,html,io,json,zipfile
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
root=Path(__file__).resolve().parents[1]
prior=json.loads((root/'documentation/rois_before_precision_audit.json').read_text())
assets=root/'review/precision_audit';assets.mkdir(exist_ok=True)
notes=list(csv.DictReader((root/'documentation/precision_audit.csv').open()))
oldrows={(r['map_id'],r['label']):r for r in csv.DictReader((root/'documentation/measurements_before_precision_audit.csv').open())}
newrows={(r['map_id'],r['label']):r for r in csv.DictReader((root/'data/measurements.csv').open())}
def numeric(r,key):
 try:return float(r.get(key,''))
 except (ValueError,TypeError):return None
changes=[]
for key,r in newrows.items():
 op=numeric(oldrows.get(key,{}),'area_px2');npix=numeric(r,'area_px2')
 if op is None or npix is None:continue
 om=numeric(oldrows[key],'area_mm2');nm=numeric(r,'area_mm2');changes.append(dict(map_id=key[0],label=key[1],previous_mm2=om,current_mm2=nm,previous_pixels=op,current_pixels=npix,change_percent=100*(npix/op-1),previous_percent=numeric(oldrows[key],'percent_of_drawn_neocortex'),current_percent=numeric(r,'percent_of_drawn_neocortex')))
with (root/'documentation/precision_area_changes.csv').open('w',newline='') as out:
 w=csv.DictWriter(out,fieldnames=list(changes[0]));w.writeheader();w.writerows({k:'NA' if v is None else v for k,v in r.items()} for r in changes)

def polygon_mask(polygons,size):
 im=Image.new('L',size);dr=ImageDraw.Draw(im)
 for p in polygons:dr.polygon([tuple(q) for q in p],fill=255)
 return im

def whole(d,mid,size):
 if d.get('outline'):return polygon_mask(d['outline']['polygons'],size)
 if d.get('whole_manual_polygon'):return polygon_mask([d['whole_manual_polygon']],size)
 if 'whole_seeds' in d:
  with zipfile.ZipFile(root/'figures'/mid/'Masks.tif.zip') as z:
   im=Image.open(io.BytesIO(z.read(z.namelist()[0])));im.seek(0);return im.convert('L').copy()
 return Image.new('L',size,255)
def paths(regs,cls,color,mask):
 out=f'<g class="{cls}" fill="none" stroke="{color}" stroke-width="1.5" clip-path="url(#{mask})">'
 for r in regs:
  for p in r['polygons']:out+='<polygon vector-effect="non-scaling-stroke" points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in p)+'"><title>'+html.escape(r['label'])+'</title></polygon>'
 return out+'</g>'
opts=[];cards=[]
for file in sorted((root/'figures').glob('*/rois.json')):
 mid=file.parent.name;d=json.loads(file.read_text());old=prior.get(mid,{'rois':[]});im=Image.open(file.parent/'source.tif').convert('RGB');size=im.size;W,H=size;im.save(assets/(mid+'.png'));wm=whole(d,mid,size);wo=whole(old,mid,size);clip='c'+mid;clipold='o'+mid
 defs='<defs>'
 for name,definition in [(clip,d),(clipold,old)]:
  if definition.get('outline'):poly=definition['outline']['polygons']
  elif definition.get('whole_manual_polygon'):poly=[definition['whole_manual_polygon']]
  else:poly=[[[0,0],[W,0],[W,H],[0,H]]]
  defs+=f'<clipPath id="{name}">'+''.join('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+'"/>' for p in poly)+'</clipPath>'
 defs+='</defs>'
 # Independently segmented 1990 tissue mask is pixel-exact; use it to clip intentional outside-tissue guide segments.
 if 'whole_seeds' in d:
  for name,mask in [(clip,wm),(clipold,wo)]:
   mask.save(assets/f'{mid}_{name}.png');defs+=f'<defs><mask id="m{name}"><image href="precision_audit/{mid}_{name}.png" width="{W}" height="{H}"/></mask></defs>'
  curr=paths(d['rois'],'current','#008eac',clip).replace(f'clip-path="url(#{clip})"',f'mask="url(#m{clip})"')
  prev=paths(old['rois'],'previous','#dc7528',clipold).replace(f'clip-path="url(#{clipold})"',f'mask="url(#m{clipold})"')
 else:curr=paths(d['rois'],'current','#008eac',clip);prev=paths(old['rois'],'previous','#dc7528',clipold)
 if d.get('outline'):curr+=paths([d['outline']],'current','#008eac',clip)
 if old.get('outline'):prev+=paths([old['outline']],'previous','#dc7528',clipold)
 if d.get('whole_manual_polygon'):curr+=paths([{'label':'Schematic outline','polygons':[d['whole_manual_polygon']]}],'current','#008eac',clip)
 if old.get('whole_manual_polygon'):prev+=paths([{'label':'Schematic outline','polygons':[old['whole_manual_polygon']]}],'previous','#dc7528',clipold)
 if 'whole_seeds' in d:
  for cls,col,mask in [('current',(0,142,172),wm),('previous',(220,117,40),wo)]:
   edge=np.array(mask)>0;edge &= np.array(mask.filter(ImageFilter.MinFilter(3)))==0;rgba=np.zeros((H,W,4),np.uint8);rgba[edge]=(*col,255);Image.fromarray(rgba).save(assets/f'{mid}_{cls}_outline.png');curr_or_prev=f'<image class="{cls}" href="precision_audit/{mid}_{cls}_outline.png" width="{W}" height="{H}"/>'
   if cls=='current':curr+=curr_or_prev
   else:prev+=curr_or_prev
 boxes={'all':[0,0,W,H]}
 for r in d['rois']:
  field=polygon_mask(r['polygons'],size);field=Image.fromarray(np.minimum(np.array(field),np.array(wm)));bb=field.getbbox()
  if bb:
   x0,y0,x1,y1=bb;pad=max(12,.08*max(x1-x0,y1-y0));x0=max(0,x0-pad);y0=max(0,y0-pad);x1=min(W,x1+pad);y1=min(H,y1+pad);boxes[r['label']]=[x0,y0,x1-x0,y1-y0]
 options='<option value="all">Entire view</option>'+''.join('<option value="'+html.escape(k,quote=True)+'">'+html.escape(k)+'</option>' for k in boxes if k!='all')
 fieldcontrol='<select data-boxes="'+html.escape(json.dumps(boxes),quote=True)+'" onchange="this.closest(\'article\').querySelector(\'svg\').setAttribute(\'viewBox\',JSON.parse(this.dataset.boxes)[this.value].join(\' \'))">'+options+'</select>'
 nn=[n for n in notes if n['map_id']==mid];table=''.join('<tr><td>'+html.escape(n['label'])+'</td><td>'+html.escape(n['status'].replace('_',' '))+'</td><td>'+html.escape(n['source_limits'])+'</td></tr>' for n in nn)
 audit=d.get('precision_audit',{});title=mid+' · '+str(d.get('specimen',''))
 opts.append('<option value="'+mid+'">'+html.escape(title)+'</option>')
 controls='<label><input type="checkbox" checked onchange="this.closest(\'article\').classList.toggle(\'hide-current\',!this.checked)"> Current (teal)</label><label><input type="checkbox" onchange="this.closest(\'article\').classList.toggle(\'show-previous\',this.checked)"> Previous (orange)</label>'
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{defs}<image href="precision_audit/{mid}.png" width="{W}" height="{H}"/>{prev}{curr}</svg>'
 cards.append(f'<article data-map="{mid}" style="display:{"block" if len(cards)==0 else "none"}"><h2>{html.escape(title)}</h2><p>{len(d["rois"])} measured fields · {audit.get("changed_regions",0)} region definitions updated. '+('No defensible field ROI in this source view.' if not d['rois'] else '')+f'</p><div class="controls">{controls}<label>Enlarge field {fieldcontrol}</label><label>Zoom <input type="range" min="70" max="240" value="100" oninput="this.closest(\'article\').querySelector(\'svg\').style.width=this.value+\'%\'"></label></div><div class="viewport">{svg}</div><details><summary>Per-region audit and source limits</summary><table><tr><th>Region</th><th>Outcome</th><th>Source limits</th></tr>{table}</table></details></article>')
summary=json.loads((root/'documentation/precision_audit_summary.json').read_text())
style='body{font:16px/1.5 system-ui;max-width:1250px;padding:0 24px;margin:36px auto;background:#f1f6f4;color:#1a3238}a{color:#006c83}h1{font-size:32px}article{background:white;border:1px solid #ceded7;border-radius:9px;padding:20px;margin:24px 0}select{font:inherit;max-width:95%;padding:5px}.controls{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:15px}.viewport{max-height:80vh;overflow:auto;border:1px solid #dce5e1}svg{display:block;width:100%;height:auto}.previous{display:none}.show-previous .previous{display:inline}.hide-current .current{display:none}td,th{padding:8px;border-bottom:1px solid #dce5e1;text-align:left}table{font-size:14px;border-collapse:collapse}details{margin-top:15px}'
s=f'<!doctype html><html><head><meta charset="utf-8"><title>Earlier contour precision review</title><style>{style}</style></head><body><h1>{html.escape(root.name.replace("_"," "))} · contour precision review</h1><p>15 October 2026 · All {summary["saved_views_reviewed"]} saved views reviewed. Current tracings are teal; previous tracings are orange. Select a view, then enlarge a field. Hide the contours to examine the source stroke.</p><p><a href="../documentation/precision_audit.md">Methods and source limits</a> · <a href="../documentation/precision_audit.csv">Per-region audit</a> · <a href="../documentation/precision_area_changes.csv">Area changes</a> · <a href="../data/measurements.csv">Current measurements</a> · <a href="gallery.html">Full gallery</a></p><p>Visible curves were refined; existing dense traces and source-limited dotted/schematic boundaries were retained where a new contour was not justified. Obscured/dashed intervals remain approximate. This review does not certify anatomical interpretation.</p><label>View <select onchange="document.querySelectorAll(\'article[data-map]\').forEach(e=&gt;e.style.display=e.dataset.map===this.value?\'block\':\'none\')">'+''.join(opts)+'</select></label>'+''.join(cards)+'</body></html>'
(root/'review/precision_audit.html').write_text(s)
print(root.name,'review generated:',len(cards),'saved views;',len(changes),'area comparisons')

gallery=root/'review/gallery.html'
if gallery.exists() and 'precision_audit.html' not in gallery.read_text():
 gallery.write_text(gallery.read_text().replace('<h1>', '<p><a href="precision_audit.html">Contour precision audit: source toggles and field enlargement</a></p><h1>',1))
