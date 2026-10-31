from pathlib import Path
import csv,json,html,hashlib,zipfile,io,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review/dm_recheck_2026-10-31';FM=ROOT.parent
E=lambda x:html.escape(str(x));cs=json.loads((OUT/'applied_changes.json').read_text());change={c['map_id']:c for c in cs};z=zipfile.ZipFile(FM/'_backups/Beck_Kaas_1998_DM_symbols_2026-10-31.zip')
oldrows=list(csv.DictReader(io.StringIO(z.read('data/measurements.csv').decode())));newrows=list(csv.DictReader((ROOT/'data/measurements.csv').open()));bynew={(r['map_id'],r['label']):r for r in newrows}
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',18)
def wc(path,rows):
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
notes={
 'fig03':'Existing closed DM envelope retained. Tracer deposits are internal; visible field boundary controls the outline.',
 'fig04':'New estimated envelope. A long left-border interval is hidden by the large injection. Orange dashes are a hypothesis constrained by endpoints/tangents, not an observed boundary; analysis_eligible=False.',
 'fig06':'New DM outline. Short continuation through the Fluororuby injection oval; the large smooth DM perimeter is otherwise visible. Same-species Fig7 and cross-species Fig9 used only to interpret conventions.',
 'fig07':'New estimated envelope. The injection conceals a long left-border interval. Orange dashes are inferred; the large ellipse extends into VPP and must not define DM. analysis_eligible=False.',
 'fig09':'Corrected the smooth gray DM perimeter, ignoring tracer symbols/injection ovals. Both DM endpoints meet V2 inside the frame, so this is the complete published drawn DM envelope, not a cropped fragment.',
 'fig10':'Existing geometry retained; corrected the fragment label/extent. The shared V2 line continues beyond the closed DM endpoints, which does not make DM incomplete.',
 'fig11':'Existing partial geometry retained. Upper DM contour is clipped by the frame; lower legend-obscured continuation remains provisional.',
 'fig12':'Existing geometry retained; corrected the fragment label/extent after checking the closed DM endpoints inside the inset.'}
rows=[];area=[];cards=[];all_images=[]
for f in sorted((ROOT/'figures').glob('*/rois.json')):
 d=json.loads(f.read_text());mid=d['map_id'];r=d['rois'][0];a=bynew[(mid,r['label'])];old=change[mid]['old'] if mid in change else d;before=next((x for x in oldrows if x['map_id']==mid and x['area_px2']!='NA'),None)
 row=dict(map_id=mid,species=d['species'],specimen=d['specimen'],saved_label=r['label'],extent=r['extent'],area_mm2=a['area_mm2'],boundary_type='long_hidden_interval_inferred' if mid in ['fig04','fig07'] else 'partial_source_extent' if mid=='fig11' else 'closed_published_envelope_with_provisional_borders',previous_roi_count=len(old['rois']),current_roi_count=len(d['rois']),decision=notes[mid]);rows.append(row)
 if mid in change:area.append(dict(map_id=mid,old_label=before['label'] if before else 'NA',new_label=r['label'],old_extent=before['extent'] if before else 'NA',new_extent=r['extent'],before_mm2=before['area_mm2'] if before else 'NA',after_mm2=a['area_mm2'],change_percent=100*(float(a['area_mm2'])/float(before['area_mm2'])-1) if before else 'NA',geometry_changed=[x['polygons'] for x in old['rois']]!=[x['polygons'] for x in d['rois']],note=change[mid]['note']))
 before_d=json.loads(z.read('figures/'+mid+'/rois.json'))
 for k in d:
  if k not in ['rois','unmeasured','review_note']:assert d[k]==before_d[k],(mid,k)
 im=Image.open(f.parent/'source.tif').convert('RGB');oldim=Image.open(io.BytesIO(z.read('figures/'+mid+'/source.tif'))).convert('RGB');assert np.array_equal(np.asarray(im),np.asarray(oldim)),mid
 im.save(OUT/(mid+'_source.png'));w,h=im.size
 def layer(d,ident,color):
  s='<g class="'+ident+'" fill="none" stroke="'+color+'" stroke-width="1.3">'
  for r in d['rois']:
   for p in r['polygons']:s+='<polygon vector-effect="non-scaling-stroke" points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in p)+'"/>'
   for p in r.get('interpolated_border_segments',[]):s+='<polyline stroke="#d77100" stroke-width="2.2" stroke-dasharray="5 3" vector-effect="non-scaling-stroke" points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in p)+'"/>'
  return s+'</g>'
 svg=f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><image href="{mid}_source.png" width="{w}" height="{h}"/>'+layer(old,'before','#a33aa0')+layer(d,'after','#008aa1')+'</svg>'
 controls='<label><input type="checkbox" checked onchange="this.closest(\'article\').classList.toggle(\'hideafter\',!this.checked)">Current</label> <label><input type="checkbox" onchange="this.closest(\'article\').classList.toggle(\'showbefore\',this.checked)">Before this correction</label> <label>Zoom <input type="range" min="60" max="220" value="100" oninput="this.closest(\'article\').querySelector(\'svg\').style.width=this.value+\'%\'"></label>'
 cards.append('<article id="'+mid+'"><h2>'+mid+' · '+E(d['species'])+' · case '+E(d['specimen'])+'</h2><p>'+E(notes[mid])+'</p><p><b>'+E(r['label'])+' · '+E(r['extent'])+' · '+f"{float(a['area_mm2']):.3f} mm²"+'</b>'+(' (inferred estimate; not observed complete-field area)' if mid in ['fig04','fig07'] else ' (provisional figure-derived area)')+'</p><div class="controls">'+controls+'</div><div class="viewport">'+svg+'</div><p><a href="../../figures/'+mid+'/RoiSet.zip">ImageJ ROI</a> · <a href="../../figures/'+mid+'/rois.json">Geometry and interpolation notes</a></p></article>')
 # A source/current comparison for direct inspection outside the browser.
 panes=[]
 for name,geom in [('Source',None),('Current; orange = inferred',d)]:
  t=im.copy();dr=ImageDraw.Draw(t)
  if geom:
   for rr in geom['rois']:
    for p in rr['polygons']:dr.line([tuple(v) for v in p]+[tuple(p[0])],fill='#008aa1',width=1)
    for p in rr.get('interpolated_border_segments',[]):dr.line([tuple(v) for v in p],fill='#d77100',width=2)
  ratio=min(500/t.width,1000/t.height);t=t.resize((round(t.width*ratio),round(t.height*ratio)));can=Image.new('RGB',(520,1040),'white');can.paste(t,((520-t.width)//2,40));ImageDraw.Draw(can).text((10,10),name,font=font,fill='black');panes.append(can)
 sheet=Image.new('RGB',(1040,1080),'#e2ede9');ImageDraw.Draw(sheet).text((10,10),mid+' / '+r['label'],font=font,fill='black')
 for i,t in enumerate(panes):sheet.paste(t,(520*i,40))
 sheet.save(OUT/(mid+'_current.png'))
wc(OUT/'coverage_audit.csv',rows);wc(OUT/'area_changes.csv',area)
panelrows=[]
for fig,sections in [(6,[111,116,121,126,131,136,141]),(9,list(range(64,113,4)))]:
 for sec in sections:panelrows.append(dict(figure=fig,panel='section '+str(sec),geometry='thalamic cross-section',decision='excluded_from_cortical_surface_area',reason='Planar area of a coronal subcortical section; not an unfolded cortical field. Tracer symbols show labeling and are not areal parcels.'))
 panelrows.append(dict(figure=fig,panel='boxed cortical inset',geometry='cortical DM map',decision='traced',reason='Own local scale retained; smooth DM envelope traced across superimposed tracer annotations.'))
wc(OUT/'panel_inventory_fig06_fig09.csv',panelrows)
style='body{font:17px system-ui;line-height:1.5;max-width:1200px;margin:32px auto;padding:0 24px;color:#173630;background:#f4f7f5}a{color:#00697f}article{background:white;border:1px solid #c9d9d3;padding:20px;margin:24px 0;border-radius:8px}.note{background:#fff0cc;padding:18px;border-left:5px solid #b87900}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:10px;border-bottom:1px solid #c9d9d3}.controls{position:sticky;top:0;background:white;padding:12px;z-index:1}label{margin-right:20px}.viewport{max-height:950px;overflow:auto;border:1px solid #ddd}svg{display:block;width:100%;height:auto}.before{display:none}.showbefore .before{display:inline}.hideafter .after{display:none}img{max-width:100%;height:auto}h2{margin-top:30px}'
s='<!doctype html><html><head><meta charset="utf-8"><title>Beck & Kaas DM: tracers are not borders</title><style>'+style+'</style></head><body><h1>DM contours across tracer overlays</h1><p>Beck & Kaas 1998 · correction and coverage recheck, 31 October 2026</p><p><b>Eight cortical insets now have saved outlines:</b> five closed published DM envelopes, one partial contour and two explicitly inferred estimates. Figure6 is newly traced; Figure9 follows the faint smooth anatomical envelope. Figures4/7 have long hidden intervals, shown in orange and excluded from observed complete-field analysis.</p><p><a href="#fig09">Figure9</a> · <a href="#fig06">Figure6</a> · <a href="coverage_audit.csv">All eight insets</a> · <a href="area_changes.csv">Area/extent changes</a> · <a href="panel_inventory_fig06_fig09.csv">Every panel in Figs6/9</a> · <a href="../../data/measurements.csv">Current measurements</a></p><div class="note"><b>The symbols are a separate annotation layer.</b> Triangles, squares, crosses and circles encode tracers; enclosing ovals indicate injection sites/spread. They do not divide DM. Short border continuations are interpolated only where the visible edges support them. Orange dashed segments identify interpolation; long hidden segments in Figs4/7 remain hypotheses, not recovered observations.</div><h2>Why the other drawings were not traced as cortex</h2><p>Figure9 contains thirteen thalamic cross-sections plus one cortical inset; Figure6 contains seven thalamic cross-sections plus one cortical inset. The main panels show PL, PM, inferior pulvinar divisions, LGN and related structures. Their 2-D sectional areas are a different measurement from cortical surface area. The panel inventory records this explicitly. Complete V2/VPP extents are also absent from the cortical insets.</p><p>Figure6 is owl monkey94-3; Figure9 is squirrel monkey94-71. They share drawing conventions but are different species/cases. Figure7 is the stronger same-species comparison for Fig6, and Fig10 for Fig9. Each contour uses its own source coordinates and scale. The source text (PDF p.3) identifies the V2 border as clearest and other DM borders as less certain.</p><details><summary>Full source pages: see the cortical inset and thalamic sections together</summary><h3>Figure6 · PDF page8</h3><img loading="lazy" src="page08.png"><h3>Figure9 · PDF page11</h3><img loading="lazy" src="page11.png"></details><h2>Coverage and decisions</h2><table><tr><th>Figure</th><th>Saved outline</th><th>Extent</th><th>Decision</th></tr>'
for r in rows:s+='<tr><td><a href="#'+r['map_id']+'">'+r['map_id']+'</a></td><td>'+E(r['saved_label'])+'</td><td>'+E(r['extent'])+'</td><td>'+E(r['decision'])+'</td></tr>'
s+='</table><p>Use Current to hide the outline and inspect the source beneath it. The older whole-project galleries are dated snapshots; this page and the dataset gallery are current. All scales, crops, species and specimen identities are preserved.</p>'+''.join(sorted(cards,key=lambda x:0 if 'id="fig09"' in x else 1 if 'id="fig06"' in x else 2))+'</body></html>'
(OUT/'index.html').write_text(s)
md='''# DM tracer/occlusion recheck — 31 October 2026

[Current source toggles](../review/dm_recheck_2026-10-31/index.html) · [Coverage audit](../review/dm_recheck_2026-10-31/coverage_audit.csv) · [Panel inventory](../review/dm_recheck_2026-10-31/panel_inventory_fig06_fig09.csv)

All eight cortical insets were compared. This corrects two errors: tracer/injection contours influencing the anatomical outline, and blanket exclusion/partial classification without checking the actual DM endpoints. Figure6 had enough source boundary to trace with a short injection-obscured continuation. Figure9 was retraced on the faint gray line. Figures9/10/12 close inside the inset; the V2 line continuing beyond DM does not make DM a fragment. Figure11 remains partial.

Figures4/7 receive **explicit inferred envelopes**, not observed complete-field measurements. The hidden left border is constrained by visible endpoints/tangents, but cannot be uniquely recovered. These rows have extent `approximate_complete`, status `inferred_boundary_estimate_not_observed`, and `analysis_eligible=False`; observed-complete DM remains unavailable. They do not enter the default complete-field summary. Orange dashed paths in the review and `interpolated_border_segments` in JSON show the hidden intervals. No confidence interval is claimed.

The thirteen main panels in Figure9 and seven in Figure6 are thalamic cross-sections, not cortical surface maps. They remain excluded from this dataset’s surface-area measurements. Complete V2 and VPP boundaries are not supplied. Their missing areas remain NA, not zero.

## Source and guides

Use the source PDF p.3 Results discussion of DM architecture and boundary uncertainty; p.5 Fig3 caption for the distinction between injection-site inset and numbered subcortical sections; p.8 Fig6 caption; p.11 Fig9 caption/legend. Figure6 is Aotus trivirgatus94-3 and Figure9 Saimiri sciureus94-71. Same-species Fig7 and Fig10, respectively, help interpret topology and injection overlays; no geometry or calibration is transferred. No external atlas was registered. General resemblance does not establish a shared specimen or permit copying a contour.

Canonical geometry, source crops and all scales remain in each `figures/<map_id>/` folder. Prior state is archived at `../../_backups/Beck_Kaas_1998_DM_symbols_2026-10-31.zip` relative to this documentation folder. The exact old/new view definitions are in `../review/dm_recheck_2026-10-31/applied_changes.json`. Manual source anchors and smooth local interpolation replace annotation-driven segmentation in the four new/refined contours. Source pixel equality, unchanged calibration/identity and native ImageJ read-back are verified; this is not independent anatomical certification.
'''
(ROOT/'documentation/dm_symbol_recheck.md').write_text(md)
# Make stale report snapshots unmistakable without rewriting their historical measurements.
marker='<!-- latest-beck-dm-recheck -->';end='<!-- /latest-beck-dm-recheck -->'
for folder in ['project_review_2026-10-31','project_review_2026-10-31_pass2']:
 p=FM/folder/'index.html';old=p.read_text();old=re.sub(re.escape(marker)+'.*?'+re.escape(end),'',old,flags=re.S);link=marker+'<div style="padding:20px;background:#fff0cc;border:3px solid #b87900"><b>Beck &amp; Kaas 1998 has a newer correction:</b> <a href="../Beck_Kaas_1998/review/dm_recheck_2026-10-31/index.html">Open current DM contours and all eight cortical insets</a>. Figures6/4/7 now have outlines; tracer symbols are not borders. The Beck cards below are an earlier snapshot.</div>'+end;old=old.replace('<body>','<body>'+link,1);p.write_text(old)
for p in [ROOT/'review/gallery.html',ROOT/'review/line_refinement.html']:
 old=p.read_text();old=re.sub(re.escape(marker)+'.*?'+re.escape(end),'',old,flags=re.S);link=marker+'<p style="padding:18px;background:#fff0cc"><a href="dm_recheck_2026-10-31/index.html">Latest DM source/overlay review: tracer symbols, inferred segments and all eight insets</a></p>'+end;p.write_text(old.replace('<body>','<body>'+link,1) if '<body>' in old else old+link)
print('DM review built: 8 insets, 3 added outlines; 2 explicitly inferred; 6 view definitions updated.')
