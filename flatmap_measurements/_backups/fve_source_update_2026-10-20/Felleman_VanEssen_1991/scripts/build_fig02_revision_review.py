#!/usr/bin/env python3
"""Review the 20 October figure-2 revision against its immutable pre-revision snapshot."""
from pathlib import Path
import csv,json,html,shutil
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
backup=root.parent/'_backups/fve_fig02_revision_2026-10-20/Felleman_VanEssen_1991'
rev=root/'review/fig02_revision';rev.mkdir(exist_ok=True)
prior=rev/'previous_rois.json'
if not prior.exists():shutil.copy2(backup/'figures/fig02/rois.json',prior)
prior_measurements=rev/'previous_measurements.csv'
if not prior_measurements.exists():shutil.copy2(backup/'data/measurements.csv',prior_measurements)
old=json.loads(prior.read_text());new=json.loads((root/'figures/fig02/rois.json').read_text())
oldrois={r['label']:r for r in old['rois']};newrois={r['label']:r for r in new['rois']}
oldrows={r['label']:r for r in csv.DictReader(prior_measurements.open()) if r['map_id']=='fig02'}
newrows={r['label']:r for r in csv.DictReader((root/'data/measurements.csv').open()) if r['map_id']=='fig02'}
source=Image.open(root/'figures/fig02/source_preview.png').convert('RGB');w,h=source.size
import pypdfium2 as pdfium
pg=pdfium.PdfDocument(root/'source/color_reference.pdf')[0]
for obj in pg.get_objects():
 if isinstance(obj,pdfium.PdfImage):obj.get_bitmap().to_pil().save(rev/'color_reference.png')
E=html.escape
rows=[];regions=[]
for r in new['rois']:
 name=r['label'];before=oldrows.get(name,{}).get('area_mm2','NA');after=newrows[name]['area_mm2'];previous=oldrois.get(name)
 change='added' if previous is None else 'revised' if r['polygons']!=previous['polygons'] else 'reviewed; geometry retained'
 q=[p for poly in r['polygons'] for p in poly];pad=85
 x=max(0,min(p[0] for p in q)-pad);y=max(0,min(p[1] for p in q)-pad)
 xx=min(w,max(p[0] for p in q)+pad);yy=min(h,max(p[1] for p in q)+pad)
 regions.append(dict(label=name,box=[x,y,xx-x,yy-y],note=r['boundary_note'],before=before,after=after,change=change))
 rows.append(dict(label=name,change=change,previous_area_mm2=before,current_area_mm2=after,previous_area_px2=oldrows.get(name,{}).get('area_px2','NA'),current_area_px2=newrows[name]['area_px2']))
with (root/'data/fig02_revision_changes.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
def paths(d,color,dashed=False):
 s=''
 for r in d['rois']:
  for poly in r['polygons']:
   points=' '.join(f'{x:.3f},{y:.3f}' for x,y in poly)
   dash=' stroke-dasharray="5 4"' if dashed else ''
   s+=f'<polygon data-label="{E(r["label"])}" points="{points}" fill="none" stroke="{color}" stroke-width="1.4" vector-effect="non-scaling-stroke"{dash}><title>{E(r["label"])}</title></polygon>'
 return s
opts='<option value="">Whole figure</option>'+''.join('<option value="'+E(r['label'])+'"'+(' selected' if r['label']=='TF' else '')+'>'+E(r['label'])+'</option>' for r in regions)
trs=''.join('<tr>'+''.join('<td>'+E(str(row[k]))+'</td>' for k in ['label','change','previous_area_mm2','current_area_mm2'])+'</tr>' for row in rows)
style='''body{font:16px/1.5 system-ui;color:#21393e;background:#f1f5f4;margin:0}main{max-width:1420px;padding:26px;margin:auto}a{color:#006a77}h1{margin-bottom:8px}.controls{position:sticky;top:0;background:#fff;padding:14px;display:flex;gap:20px;align-items:center;flex-wrap:wrap;z-index:2;border:1px solid #ccd8d8}select,button{font:inherit;padding:6px}.layout{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:22px}.viewport{background:white;border:1px solid #ccd8d8;overflow:auto;max-height:82vh}svg{width:100%;display:block}aside img{width:100%}.note{background:#fff;padding:14px}table{border-collapse:collapse;background:white;width:100%;font-size:14px}th,td{text-align:left;padding:8px;border-bottom:1px solid #ddd}.previous{display:none}.muted{color:#52676b;font-size:14px}@media(max-width:850px){.layout{grid-template-columns:1fr}aside{max-width:450px}}'''
js='''const regions=JSON.parse(document.getElementById('regions').textContent), select=document.getElementById('region'), svg=document.querySelector('svg');function update(){const label=select.value,r=regions.find(x=>x.label===label);svg.setAttribute('viewBox',r?r.box.join(' '):'0 0 WIDTH HEIGHT');svg.querySelectorAll('polygon').forEach(p=>p.style.opacity=!r||p.dataset.label===label?'1':'.14');document.getElementById('note').textContent=r?r.label+' — '+r.change+'. Before: '+r.before+' mm²; current: '+Number(r.after).toFixed(2)+' mm². '+r.note:'Select a region to inspect its anatomical perimeter. Both overlays are aligned to the unchanged original PDF crop.';}select.addEventListener('change',update);document.getElementById('current').addEventListener('change',e=>document.querySelector('.current').style.display=e.target.checked?'':'none');document.getElementById('previous').addEventListener('change',e=>document.querySelector('.previous').style.display=e.target.checked?'inline':'none');document.getElementById('zoom').addEventListener('input',e=>svg.style.width=e.target.value+'%');document.querySelectorAll('[data-select]').forEach(b=>b.addEventListener('click',()=>{select.value=b.dataset.select;update()}));update();'''.replace('WIDTH',str(w)).replace('HEIGHT',str(h))
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Felleman &amp; Van Essen 1991 · Figure 2 correction</title><style>{style}</style><main><h1>Figure 2 · leader lines and anatomical borders</h1><p>Revised 20 October 2026: 74 field/component observations, including 12 previously missing fields. The color reference identifies regions; measurements use the original calibrated monochrome figure. Internal labels remain included tissue.</p><p><a href="../figures/fig02/tracing.png">Full tracing</a> · <a href="../figures/fig02/RoiSet.zip">ImageJ ROIs</a> · <a href="../figures/fig02/source.tif">Calibrated TIFF</a> · <a href="../data/fig02_revision_changes.csv">Area changes</a> · <a href="../documentation/fig02_revision_2026-10-20.md">Methods and limitations</a></p><div class="controls"><label>Region <select id="region">{opts}</select></label><label><input id="current" type="checkbox" checked> Current (teal)</label><label><input id="previous" type="checkbox"> Previous (orange dashed)</label><label>Zoom <input id="zoom" type="range" min="100" max="250" step="25" value="100"></label><button data-select="ER anterior">Anterior ER</button><button data-select="TF">TF</button></div><p id="note" class="note"></p><div class="layout"><div class="viewport"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><image href="../figures/fig02/source_preview.png" width="{w}" height="{h}"/><g class="previous">{paths(old,'#df7620',True)}</g><g class="current">{paths(new,'#008498')}</g></svg></div><aside><h2>Color reference</h2><a href="fig02_revision/color_reference.png"><img src="fig02_revision/color_reference.png" alt="Color flat map attributed to Felleman and Van Essen 1991"></a><p class="muted">User-supplied PDF of the <a href="https://www.hms.harvard.edu/bss/neuro/bornlab/lab/figures/FVE_map.html">Harvard page</a>. This 432 × 444 pixel reference clarifies leader endpoints and colored compartments. It is displayed separately, not stretched onto measurement coordinates.</p><p class="muted">Atlas/composite observations are excluded from animal means. PSv's thin merged border remains unresolved; hippocampal/subicular subdivisions remain untraced in this revision.</p></aside></div><h2>Measurements</h2><p>Original 1 cm scale retained. Areas are provisional digitizations, not certified anatomical boundaries. TF and other dark fields include their internal labels.</p><table><thead><tr><th>Region</th><th>Revision</th><th>Previous mm²</th><th>Current mm²</th></tr></thead><tbody>{trs}</tbody></table><p><a href="precision_review.html">Standard precision review</a> · <a href="gallery.html">All-figure assessment</a></p></main><script id="regions" type="application/json">{json.dumps(regions).replace('<','&lt;')}</script><script>{js}</script></html>'''
(root/'review/fig02_revision.html').write_text(page)
# Source / prior / current panels use exactly the same source pixels and crop.
for name,box,labels in [('TF',(900,1270,1210,1510),['TF']),('ER_anterior',(1360,960,1630,1235),['ER anterior','PAC','35']),('visual_ribbons',(600,340,1200,1550),['V2','V3','V3A','VP','V4','V4t','VOT','MT','TH'])]:
 panels=[]
 for title,dct,col in [('Source',{},'#008498'),('Previous',oldrois,'#e27320'),('Current',newrois,'#008498')]:
  im=source.copy();dr=ImageDraw.Draw(im)
  for label in labels:
   if label in dct:
    for p in dct[label]['polygons']:dr.line([tuple(x) for x in p]+[tuple(p[0])],fill=col,width=2)
  crop=im.crop(box);panel=Image.new('RGB',(crop.width,crop.height+34),'white');panel.paste(crop,(0,34));ImageDraw.Draw(panel).text((10,9),title,fill='#183439');panels.append(panel)
 combined=Image.new('RGB',(sum(p.width for p in panels),panels[0].height),'white');offset=0
 for panel in panels:combined.paste(panel,(offset,0));offset+=panel.width
 combined.save(rev/(name+'_comparison.png'))
print('Figure 2 revision review:',len(new['rois']),'current contours;',sum(x['change']=='added' for x in rows),'added;',sum(x['change']=='revised' for x in rows),'revised')
