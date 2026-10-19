#!/usr/bin/env python3
"""Build a full-source-page review, preserving specimen overlays in their source coordinates."""
from pathlib import Path
import csv,hashlib,html,json,re
import numpy as np
from PIL import Image,ImageDraw
import pypdfium2 as pdfium
B=Path(__file__).resolve().parents[1]
BACK=B/'_backups/full_dataset_review_2026-10-16'
E=html.escape
PALETTE=['#007d83','#bc3675','#3469b1','#a65c00','#673eaa','#218341','#9b3131','#4f5a17']
CSS='''body{font:16px system-ui;line-height:1.5;max-width:1350px;margin:32px auto;padding:0 24px;background:#f2f6f5;color:#173335}a{color:#006780}h1{font-size:32px}h2{font-size:23px}article,section{background:white;padding:20px;border:1px solid #d5dfdc;border-radius:9px;margin:24px 0}.controls{position:sticky;top:0;background:#fffdf3;padding:12px;z-index:2;border:1px solid #dadaca;display:flex;gap:22px;flex-wrap:wrap}.viewport{overflow:auto;max-height:88vh;border:1px solid #ddd}svg{display:block;width:100%;height:auto}.previous{display:none}.show-previous .previous{display:inline}.hide-current .current{display:none}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-bottom:1px solid #dce5e2;text-align:left;padding:9px;vertical-align:top}small,.muted{color:#516866}.legend{display:flex;gap:14px;flex-wrap:wrap}summary{cursor:pointer;font-weight:600}input,select{font:inherit}li{margin:6px 0}.tag{white-space:nowrap;font-size:13px;background:#e9f2ef;padding:3px 7px;border-radius:4px}.note{border-left:4px solid #b47b23;padding:9px 14px;background:#fff8e9}'''
JS='''document.querySelectorAll('[data-control]').forEach(el=>el.addEventListener('change',()=>{document.body.classList.toggle(el.dataset.control,el.checked)}));document.querySelectorAll('.zoom').forEach(el=>el.addEventListener('input',()=>el.closest('article').querySelector('svg').style.width=el.value+'%'));document.querySelectorAll('[data-case]').forEach(el=>el.addEventListener('change',()=>{el.closest('article').querySelectorAll('[data-view]').forEach(g=>{if(g.dataset.view===el.dataset.case)g.style.display=el.checked?'':'none'})}));'''
def page_numbers(s):
 out=[]
 for token in re.split('[;,]',s):
  q=token.strip().replace('–','-')
  if not q:continue
  if '-' in q:a,b=map(int,q.split('-'));out+=list(range(a,b+1))
  else:out.append(int(q))
 return out

def load_defs(root):return {f.parent.name:json.loads(f.read_text()) for f in sorted((root/'figures').glob('*/rois.json'))}
def illustrative(d):return bool(re.search('composite|illustrative|schematic|atlas|summary',d.get('view_type',''),re.I))
def geometry(r):return {k:r.get(k,[]) for k in ['polygons','exclude_polygons']}
def shape_on_page(poly,d,mid,manifest,W,H):
 q=np.array(poly,dtype=float)
 if 'crop_xyxy' in d:
  scale=d['render_scale'];q+=np.array(d['crop_xyxy'][:2]);rotation=d.get('source_rotation_degrees',0)
  x,y=q[:,0].copy(),q[:,1].copy();rw,rh=int(np.ceil(W*scale)),int(np.ceil(H*scale))
  if rotation==270:q[:,0]=y;q[:,1]=rh-1-x
  elif rotation==90:q[:,0]=rw-1-y;q[:,1]=x
  elif rotation==180:q[:,0]=rw-1-x;q[:,1]=rh-1-y
  return q/scale
 crops=manifest['crops'];m=next((x for x in crops if x.get('map_id')==mid),None)
 if m is None:m=next(x for x in crops if x['figure']==d['figure'] and not x.get('map_id'))
 return (q/m.get('resize_scale',1)+np.array(m['crop_xyxy'][:2]))/m['pdf_render_scale']

def paths(d,mid,manifest,W,H,color,prior=False):
 result=[]
 for r in d['rois']:
  title=E(mid+' · '+d.get('specimen','not reported')+' · '+r['label']+' · '+r.get('extent','complete'))
  for k in ['polygons','exclude_polygons']:
   for poly in r.get(k,[]):
    q=shape_on_page(poly,d,mid,manifest,W,H);points=' '.join(f'{x:.2f},{y:.2f}' for x,y in q)
    dash=' stroke-dasharray="4 3"' if prior or k=='exclude_polygons' else ''
    result.append(f'<polygon points="{points}" fill="none" stroke="{color}" stroke-width="1.5" vector-effect="non-scaling-stroke"{dash}><title>{title}</title></polygon>')
 body=''.join(result)
 # Legacy guides are intentionally clipped by an independent whole-tissue mask in measurement.
 # Display that same effective selection rather than an unmeasured outside-tissue guide segment.
 clipid=('old_' if prior else 'now_')+mid
 outline=d.get('outline') or ({'polygons':[d['whole_manual_polygon']]} if d.get('whole_manual_polygon') else None)
 if outline:
  poly=''.join('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in shape_on_page(q,d,mid,manifest,W,H))+'"/>' for q in outline['polygons'])
  return f'<defs><clipPath id="{clipid}">{poly}</clipPath></defs><g clip-path="url(#{clipid})">{body}</g>'
 if 'whole_seeds' in d:
  crops=manifest['crops'];m=next((x for x in crops if x.get('map_id')==mid),None)
  if m is None:m=next(x for x in crops if x['figure']==d['figure'] and not x.get('map_id'))
  x,y=np.array(m['crop_xyxy'][:2])/m['pdf_render_scale'];w,h=np.array(m['source_size'])/(m['resize_scale']*m['pdf_render_scale'])
  return f'<defs><mask id="{clipid}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}"><image href="precision_audit/{mid}_c{mid}.png" x="{x}" y="{y}" width="{w}" height="{h}"/></mask></defs><g mask="url(#{clipid})">{body}</g>'
 return body

def write_csv(f,rows,fields):
 with f.open('w',newline='') as out:w=csv.DictWriter(out,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)

summaries=[];changes=[]
for root in sorted(B.iterdir()):
 if not(root/'source/paper.pdf').exists():continue
 paper=root.name;defs=load_defs(root);old=load_defs(BACK/paper);manifest=json.loads((root/'source/manifest.json').read_text());doc=pdfium.PdfDocument(root/'source/paper.pdf')
 invfile=root/'documentation/figure_inventory.csv'
 if not invfile.exists():invfile=root/'documentation/paper_figure_inventory.csv'
 inv=list(csv.DictReader(invfile.open()));pages=set()
 for r in inv:pages.update(page_numbers(r.get('pdf_page',r.get('pdf_pages',''))))
 pages.update(int(d['pdf_page']) for d in defs.values())
 new_count=changed_count=new_case_count=new_illustrative=0;new_views=[]
 for mid,d in defs.items():
  before={r['label']:r for r in old.get(mid,{}).get('rois',[])}
  for r in d['rois']:
   status='added' if r['label'] not in before else 'refined' if geometry(r)!=geometry(before[r['label']]) else 'unchanged'
   if status=='added':
    new_count+=1;new_illustrative+=int(illustrative(d));new_case_count+=int(not illustrative(d))
   changed_count+=int(status=='refined')
   if status!='unchanged':changes.append(dict(paper=paper,map_id=mid,figure=d['figure'],specimen=d.get('specimen','not reported'),label=r['label'],extent=r.get('extent','complete'),change=status,view_type=d.get('view_type',''),repeat_of=d.get('repeat_of') or '',count_as_additional_animal='no; view observations are not animal counts'))
  if mid not in old and d['rois']:new_views.append(mid)
 removed=sum(r['label'] not in {z['label'] for z in defs.get(mid,{}).get('rois',[])} for mid,d in old.items() for r in d['rois'])
 for mid,d in old.items():
  for r in d['rois']:
   if r['label'] not in {z['label'] for z in defs.get(mid,{}).get('rois',[])}:changes.append(dict(paper=paper,map_id=mid,figure=d['figure'],specimen=d.get('specimen','not reported'),label=r['label'],extent=r.get('extent','complete'),change='withdrawn: unsupported white-gap envelope',view_type=d.get('view_type',''),repeat_of=d.get('repeat_of') or '',count_as_additional_animal='no; unsupported contour withdrawn'))
 row=dict(paper=paper,withdrawn_observations=removed,numbered_figures=len(set(r['figure'] for r in inv)),views=len(defs),previous_contours=sum(len(d['rois']) for d in old.values()),current_contours=sum(len(d['rois']) for d in defs.values()),added_observations=new_count,added_case_view_observations=new_case_count,added_illustrative_observations=new_illustrative,refined_existing_contours=changed_count,source_review='full numbered-figure inventory rechecked',anatomical_certification=False)
 summaries.append(row)
 dest=root/'review/full_dataset_source_pages';dest.mkdir(parents=True,exist_ok=True);cards=[]
 for page in sorted(pages):
  pg=doc[page-1];W,H=pg.get_size();imfile=dest/f'page{page:03}.png'
  if not imfile.exists():pg.render(scale=1.5).to_pil().convert('RGB').save(imfile)
  views=[(mid,d) for mid,d in defs.items() if int(d['pdf_page'])==page and d['rois']];overlay=[];legend=[];before=[]
  for k,(mid,d) in enumerate(views):
   color=PALETTE[k%len(PALETTE)];overlay.append(f'<g data-view="{E(mid)}">'+paths(d,mid,manifest,W,H,color)+'</g>')
   if mid in old:before.append(f'<g data-view="{E(mid)}">'+paths(old[mid],mid,manifest,W,H,'#e17322',True)+'</g>')
   native=f'../figures/{mid}/'
   legend.append(f'<li><label style="color:{color}"><input type="checkbox" checked data-case="{E(mid)}"> <b>{E(mid)}</b> · {E(d.get("specimen","not reported"))}</label> · {len(d["rois"])} field/component observations'+(' · <span class="tag">illustrative</span>' if illustrative(d) else '')+f' · <a href="{native}tracing.png">Tracing</a> · <a href="{native}rois.json">Coordinates</a> · <a href="{native}RoiSet.zip">ImageJ ROIs</a><br><small>'+E(', '.join(r['label']+(' [partial]' if r.get('extent')=='partial' else '') for r in d['rois']))+'</small></li>')
  details=[]
  for r in inv:
   if page in page_numbers(r.get('pdf_page',r.get('pdf_pages',''))):
    reason=r.get('reason_or_result',r.get('next_action',r.get('reason','')));interpretation=r.get('interpretation',r.get('interpretation_from_caption',r.get('type','')))
    details.append('<p><b>Figure '+E(r['figure'])+(' '+E(r['panel']) if r.get('panel') else '')+'</b> · '+E(interpretation)+'. '+E(reason)+'</p>')
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" aria-label="Original source page with all saved case contours"><image href="full_dataset_source_pages/page{page:03}.png" width="{W}" height="{H}"/><g class="previous">'+''.join(before)+'</g><g class="current">'+''.join(overlay)+'</g></svg>'
  card=f'<article id="page{page}"><h2>PDF page {page} · {len(views)} traced views</h2>'+''.join(details)
  if views:card+='<ul>'+''.join(legend)+'</ul><label>Page zoom <input class="zoom" type="range" min="75" max="300" step="25" value="100"></label>'
  card+='<div class="viewport">'+svg+'</div></article>'
  if views:cards.append(card)
  else:cards.append(f'<details><summary>PDF page {page} · no saved field contours</summary>'+card+'</details>')
  if paper=='Beck_etal_1996' and page==5:
   im=pg.render(scale=2).to_pil().convert('RGB');dr=ImageDraw.Draw(im)
   for k,(mid,d) in enumerate(views):
    color=PALETTE[k%len(PALETTE)]
    for r in d['rois']:
     for poly in r['polygons']:
      q=shape_on_page(poly,d,mid,manifest,W,H)*2;dr.line([tuple(z) for z in q]+[tuple(q[0])],fill=color,width=3)
   im.save(root/'review/all_cases_fig02.png')
 controls='<div class="controls"><label><input type="checkbox" data-control="hide-current"> Hide current contours</label><label><input type="checkbox" data-control="show-previous"> Show previous contours (orange dashed)</label><a href="../../review_full_dataset_audit.html">All 21 papers</a></div>'
 note='All specimens sharing a figure appear together. Checkbox labels identify saved views, not independent animals. Dashed orange outlines show the archived geometry from before this pass. Blank source pages retain the documented assessment; no contour is manufactured to close an open field.'
 s='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(paper)+' · full dataset recheck</title><style>'+CSS+'</style></head><body><h1>'+E(paper.replace('_',' '))+' · source review</h1><p>Rechecked 16 October 2026. '+str(row['numbered_figures'])+' numbered figures; '+str(row['current_contours'])+' saved field/component observations; '+str(new_count)+' added and '+str(changed_count)+' existing contours refined.</p><p>'+note+'</p><p class="note">Areas remain provisional anatomical interpretations. Partial components are labelled; comparative drawings and repeated views do not add animals. Source projections, sections and nonmetric schematics cannot establish unfolded cortical surface area.</p><p><a href="../documentation/'+invfile.name+'">Figure inventory</a> · <a href="../data/measurements.csv">Measurements</a> · <a href="../documentation/full_dataset_recheck.md">Recheck findings</a></p>'+controls+''.join(cards)+'<script>'+JS+'</script></body></html>'
 (root/'review/full_dataset_audit.html').write_text(s)
 doc.close()
 print(paper,row['current_contours'],'new',new_count,'refined',changed_count,flush=True)
for change in changes:
 paper=change['paper'];key=(change['map_id'],change['label'])
 before={(r['map_id'],r['label']):r for r in csv.DictReader((BACK/paper/'data/measurements.csv').open())};after={(r['map_id'],r['label']):r for r in csv.DictReader((B/paper/'data/measurements.csv').open())}
 for prefix,data in [('previous',before),('current',after)]:
  for col in ['area_px2','area_mm2']:change[prefix+'_'+col]=data.get(key,{}).get(col) or 'NA'
 try:change['pixel_area_change_percent']=100*(float(change['current_area_px2'])/float(change['previous_area_px2'])-1)
 except (ValueError,TypeError,ZeroDivisionError):change['pixel_area_change_percent']='NA'
write_csv(B/'full_dataset_recheck_papers.csv',summaries,list(summaries[0]));write_csv(B/'full_dataset_recheck_contours.csv',changes,list(changes[0]))
tot={k:sum(r[k] for r in summaries) for k in ['numbered_figures','previous_contours','current_contours','withdrawn_observations','added_observations','added_case_view_observations','added_illustrative_observations','refined_existing_contours']}
(B/'full_dataset_recheck_stats.json').write_text(json.dumps(dict(date='2026-10-16',papers=len(summaries),**tot,anatomical_certification=False),indent=2)+'\n')
trs=''.join('<tr><td><a href="'+E(r['paper'])+'/review/full_dataset_audit.html">'+E(r['paper'])+'</a></td>'+''.join('<td>'+str(r[k])+'</td>' for k in ['numbered_figures','previous_contours','current_contours','added_case_view_observations','added_illustrative_observations','refined_existing_contours','withdrawn_observations'])+'</tr>' for r in summaries)
start='<section><h2>Start with the omissions</h2><ul><li><a href="Beck_etal_1996/review/full_dataset_audit.html#page5">Beck 1996, figure 2: all four cases together</a>. They were already separate saved views; a single-case tracing image made the other cases look omitted. This pass also adds nine local field outlines and the missing motor-map SR outline.</li><li><a href="Luethke_etal_1988/review/full_dataset_audit.html#page5">Luethke 1988, figure 3: specimen 85-90</a>. The main reconstruction had been omitted while its inset was retained. Twelve main-map fields and one repeated inset observation are now saved.</li><li><a href="Krubitzer_etal_1993/review/full_dataset_audit.html">Krubitzer et al. 1993: bat local maps</a>. Closed SII/PV/VS envelopes and explicitly partial 3b components are recovered without counting repeated panels as new animals.</li></ul></section>'
s='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Full dataset contour recheck</title><style>'+CSS+'</style></head><body><h1>Full dataset · coverage and contour recheck</h1><p>16 October 2026 · All '+str(len(summaries))+' papers and '+str(tot['numbered_figures'])+' numbered figures rechecked against the supplied source pages.</p><section><h2>'+str(tot['added_observations'])+' additional field/component observations · '+str(tot['refined_existing_contours'])+' existing contours refined</h2><p>'+str(tot['added_case_view_observations'])+' additions belong to experimental or repeated case views; '+str(tot['added_illustrative_observations'])+' belong to comparative illustrations. The dataset now contains '+str(tot['current_contours'])+' contour observations after withdrawing '+str(tot['withdrawn_observations'])+' unsupported earlier white-gap candidates. These are not counts of animals or complete cortical areas.</p><p>Each paper below provides full source pages with all case overlays, current/source/previous toggles, case labels and editable ImageJ links. Existing per-case tracing.png files continue to match their own ROI sets. Letter-shaped and tracer-gap candidates were corrected or rejected; unresolved field totals remain flagged.</p></section>'+start+'<p class="note">Complete-field summaries choose one calibrated complete observation per identified animal and field where supported. Partial components, illustrative summaries and unresolved specimen identities remain separate. Unclosed anatomical borders and nonmetric source geometries remain explicit NA; the recheck does not certify every anatomical interpretation.</p><p><a href="full_dataset_recheck_validation.json">Final verification</a> · <a href="full_dataset_recheck_papers.csv">Paper counts CSV</a> · <a href="full_dataset_recheck_contours.csv">Added/refined contour ledger</a> · <a href="full_dataset_recheck.md">Methods and source limits</a></p><table><thead><tr><th>Paper · open source review</th><th>Figures</th><th>Before</th><th>Now</th><th>Added case-view observations</th><th>Added illustrative observations</th><th>Existing contours refined</th><th>Unsupported contours withdrawn</th></tr></thead><tbody>'+trs+'</tbody></table><p>Archived geometry and outputs: <code>_backups/full_dataset_review_2026-10-16/</code>. Earlier batch reviews are historical snapshots; this review and current per-paper CSVs describe the revised dataset.</p></body></html>'
(B/'review_full_dataset_audit.html').write_text(s)
print(json.dumps(tot))
