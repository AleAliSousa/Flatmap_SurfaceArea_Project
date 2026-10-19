#!/usr/bin/env python3
"""Build portable source-toggle review and physical-area revision table."""
import csv,html,json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
prior=json.loads((root/'documentation/rois_before_line_refinement.json').read_text())
old=list(csv.DictReader((root/'documentation/measurements_before_line_refinement.csv').open()))
new=list(csv.DictReader((root/'data/measurements.csv').open()))
key=lambda r:(r['map_id'],r['label'])
a={key(r):r for r in old};b={key(r):r for r in new};rows=[]
def number(r):
 try:return float(r['area_mm2'])
 except (TypeError,ValueError,KeyError):return None
for k in sorted(set(a)|set(b)):
 av=number(a.get(k,{}));bv=number(b.get(k,{}))
 if av is None and bv is None:continue
 change=(bv/av-1)*100 if av and bv is not None else None
 rows.append(dict(map_id=k[0],label=k[1],previous_mm2=av,current_mm2=bv,change_percent=change,revision='refined contour' if av is not None and bv is not None else 'withdrawn: unsupported separate closure' if bv is None else 'combined envelope'))
f=root/'documentation/line_refinement_changes.csv'
with f.open('w',newline='') as out:
 w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows({k:'NA' if v is None else v for k,v in r.items()} for r in rows)
asset=root/'review/line_refinement';asset.mkdir(exist_ok=True)
def regions(d):return ([d['outline']] if d.get('outline') else [])+d['rois']
def paths(d,ratio,color,cls):
 s='<g class="'+cls+'" fill="none" stroke="'+color+'" stroke-width="1.6" stroke-linejoin="round">'
 for r in regions(d):
  for p in r['polygons']:
   s+='<polygon vector-effect="non-scaling-stroke" points="'+' '.join(f'{x*ratio:.3f},{y*ratio:.3f}' for x,y in p)+'"><title>'+html.escape(r['label'])+'</title></polygon>'
 return s+'</g>'
cards=[];focus=[]
for file in sorted((root/'figures').glob('*/rois.json')):
 d=json.loads(file.read_text());mid=d['map_id']
 if not regions(d):continue
 im=Image.open(file.parent/'source.tif').convert('RGB');im.save(asset/(mid+'.png'));w,h=im.size
 oldpaths=paths(prior[mid],d['render_scale']/prior[mid]['render_scale'],'#dd7029','previous') if mid in prior else ''
 newpaths=paths(d,1,'#008eac','current')
 def svg(viewbox):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-label="{mid} source with switchable contours"><image href="line_refinement/{mid}.png" width="{w}" height="{h}"/>{oldpaths}{newpaths}</svg>'
 labels=', '.join(r['label'] for r in regions(d))
 controls='<label><input type="checkbox" checked onchange="this.closest(\'article\').classList.toggle(\'hide-current\',!this.checked)"> Current contour</label> <label><input type="checkbox" onchange="this.closest(\'article\').classList.toggle(\'show-previous\',this.checked)"> Previous contour</label>'
 cards.append(f'<article id="{mid}"><h2>{mid} · {html.escape(d["specimen"])}</h2><p>{html.escape(labels)}</p><div class="controls">{controls} <label>Zoom <input type="range" min="60" max="240" value="100" oninput="this.closest(\'article\').querySelector(\'svg\').style.width=this.value+\'%\'"></label></div><div class="viewport">{svg(f"0 0 {w} {h}")}</div></article>')
 boxes={('Huffman_etal_1999','fig02'):[(365,910,745,1125,'Inferior SII/PV scallops')],('Huffman_etal_1999','fig03'):[(405,455,545,610,'C caudal tip')],('Huffman_etal_1999','fig05'):[(490,310,705,570,'Curved C border'),(330,800,660,1155,'SII/PV compound envelope')],('Beck_Kaas_1998','fig09'):[(835,990,946,1158,'Fine gray DM boundary')],('Beck_Kaas_1998','fig11'):[(800,835,983,1118,'DM border and obscured legend')]} 
 for x0,y0,x1,y1,title in boxes.get((root.name,mid),[]):
  scale=d['render_scale']/2;bx=x0*scale-d['crop_xyxy'][0];by=y0*scale-d['crop_xyxy'][1];bw=(x1-x0)*scale;bh=(y1-y0)*scale;v=f'{bx} {by} {bw} {bh}';focus.append(f'<article><h2>{mid} · {title}</h2><div class="pair"><div class="before"><h3>Previous</h3>{svg(v)}</div><div class="after"><h3>Revised</h3>{svg(v)}</div></div></article>')
def fmt(x):return 'NA' if x is None else f'{x:.4f}'
trs=''.join('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [r['map_id'],r['label'],fmt(r['previous_mm2']),fmt(r['current_mm2']),('NA' if r['change_percent'] is None else f'{r["change_percent"]:+.2f}%'),r['revision']])+'</tr>' for r in rows)
s='''<!doctype html><html><head><meta charset="utf-8"><title>Refined tracing review</title><style>
body{font:16px system-ui;line-height:1.5;max-width:1200px;margin:36px auto;padding:0 24px;color:#183237;background:#f3f7f6}h1{font-size:34px}h2{font-size:22px}h3{margin:0 0 8px}article{background:white;border:1px solid #d4e0dd;border-radius:10px;padding:20px;margin:24px 0}a{color:#006a83}.controls{display:flex;gap:22px;flex-wrap:wrap;margin:14px 0}.viewport{max-height:85vh;overflow:auto;background:white;border:1px solid #d9e1df}svg{display:block;width:100%;height:auto}.previous{display:none}.show-previous .previous{display:inline}.hide-current .current{display:none}.pair{display:grid;grid-template-columns:1fr 1fr;gap:22px}.before .previous{display:inline}.before .current{display:none}.after .previous{display:none}td,th{text-align:left;border-bottom:1px solid #d4dfdc;padding:8px}table{width:100%;font-size:14px;border-collapse:collapse}.tablewrap{overflow:auto}@media(max-width:700px){.pair{grid-template-columns:1fr}}details{margin:20px 0}
</style></head><body>'''
s+='<h1>'+html.escape(root.name.replace('_',' '))+' · refined tracings</h1><p>Revised 15 October 2026. <b>Teal = current; orange = previous.</b> Enlarged views below show the source stroke beneath each contour. Use the controls on each full view to hide either contour; use Zoom to examine it closely. Source pixels and physical calibration are preserved.</p><p><a href="gallery.html">All-figure gallery</a> · <a href="../documentation/line_refinement.md">Revision methods and limitations</a> · <a href="../documentation/line_refinement_changes.csv">Area changes (CSV)</a> · <a href="../data/measurements.csv">Current measurements</a></p>'
if root.name=='Huffman_etal_1999':s+='<p><b>Figure 5 correction:</b> separate SII and PV areas were withdrawn because the drawn divider stops short of the outer border. Their combined external envelope is measured; individual values are NA.</p>'
s+='<p>Short interpolations remain where a printed border is obscured by symbols or a legend. The review records the fit to this scan; anatomical interpretation remains provisional.</p><h2>Focused before-and-after checks</h2>'+''.join(focus)+'<h2>All measured views · source toggles</h2>'+''.join(cards)+'<details><summary>Changes in physical areas</summary><div class="tablewrap"><table><tr><th>View</th><th>Field</th><th>Previous mm²</th><th>Current mm²</th><th>Change</th><th>Revision</th></tr>'+trs+'</table></div></details></body></html>'
(root/'review/line_refinement.html').write_text(s)
print(root.name,'line refinement review saved;',len(rows),'area comparisons')
