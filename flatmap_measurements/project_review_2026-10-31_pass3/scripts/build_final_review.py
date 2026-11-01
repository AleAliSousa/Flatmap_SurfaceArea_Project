"""Report actual overview coverage, targeted edits, and unresolved source limits."""
from pass3_helpers import *
import csv,io,hashlib,html,collections
from urllib.parse import quote
E=html.escape
log=json.loads((OUT/'screening_log.json').read_text())
log['Burman_etal_2008']['notes']=log['Burman_etal_2008']['notes'].replace('Fig9 B–D remain additional untraced flatmap candidates','Fig9 B–D are repeated views of the same CJ58R anatomy with different tracers; useful cross-checks, not additional animals')
log['Remple_etal_2006']['notes']=log['Remple_etal_2006']['notes'].replace('Fig8A–C untraced tracer reconstructions have open M1/M2 ends','Fig8A–C tracer reconstructions have additional untraced motor components with open M1/M2 ends')
(OUT/'screening_log.json').write_text(json.dumps(log,indent=2)+'\n')
events=json.loads((OUT/'applied_changes.json').read_text());baseline=json.loads((OUT/'baseline.json').read_text());base={(x['paper_id'],x['map_id']):x for x in baseline};sources=json.loads((OUT/'source_page_inventory.json').read_text())
for r in sources:r['status']='screened_overview'
(OUT/'source_page_inventory.json').write_text(json.dumps(sources,indent=2)+'\n')
manifest=json.loads((OUT/'screening_manifest.json').read_text());assert set(log)=={x['paper_id'] for x in sources};assert all(v['source_overviews_seen'] for v in log.values())
for m in manifest:assert log[m['paper_id']][m['kind']+'_overviews_seen'],m
changedpapers=sorted({x['paper_id'] for x in events});changedmaps={(e['paper_id'],e['map_id']) for e in events}
# Enlarged checks are explicit, separate from the complete overview pass.
enlarged=set(changedmaps)|{('Beck_Kaas_1998',m) for m in ['fig03','fig04','fig06','fig07','fig09','fig10','fig11','fig12']}|{('Krubitzer_Kaas_1990','fig06C')}
# Use actual Beck folder names rather than assuming the eighth figure number.
enlarged={x for x in enlarged if (FM/x[0]/'figures'/x[1]/'rois.json').exists()}
for f in (FM/'Beck_Kaas_1998/figures').glob('*/rois.json'):enlarged.add(('Beck_Kaas_1998',f.parent.name))
current=[]
for paper in sorted(log):
 for f in sorted((FM/paper/'figures').glob('*/rois.json')):
  d=json.loads(f.read_text());mid=f.parent.name;old=base.get((paper,mid));current.append(dict(paper_id=paper,map_id=mid,roi_count=len(d['rois']),source_review='overview_screened',enlarged_check=(paper,mid) in enlarged,geometry_or_metadata_changed=(paper,mid) in changedmaps,baseline_roi_sha256=old['sha256'] if old else '',current_roi_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),review_scope='targeted enlarged check' if (paper,mid) in enlarged else 'overview only; not vertex-by-vertex validation',notes=log[paper]['notes']))
def wc(path,rows):
 if not rows:return
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
wc(OUT/'view_review.csv',current)
area=[];cache={};oldcache={}
for e in events:
 p=e['paper_id'];mid=e['map_id'];lab=e['label'];d=get(p,mid);r=next(r for r in d['rois'] if r['label']==lab);assert r['polygons']==e['after']['polygons']
 if p not in cache:cache[p]=list(csv.DictReader((FM/p/'data/measurements.csv').open()))
 if p not in oldcache:
  with zipfile.ZipFile(OUT/'before'/(p+'.zip')) as z:oldcache[p]=list(csv.DictReader(io.StringIO(z.read('data/measurements.csv').decode())))
 new=next(x for x in cache[p] if x['map_id']==mid and x['label']==lab);old=next((x for x in oldcache[p] if x['map_id']==mid and x['label']==lab and x.get('area_px2') not in ['', 'NA']),None)
 kind='added' if e['before'] is None else ('revised_geometry' if e['before']['polygons']!=r['polygons'] else 'metadata_only')
 area.append(dict(paper_id=p,map_id=mid,label=lab,change=kind,before_px2=old['area_px2'] if old else '',after_px2=new['area_px2'],percent_pixel_area_change=100*(float(new['area_px2'])/float(old['area_px2'])-1) if old and float(old['area_px2']) else '',before_mm2=old['area_mm2'] if old else '',after_mm2=new['area_mm2'],extent=new['extent'],status=new['status'],reason=e['reason']))
 if kind!='metadata_only':
  # Fresh comparison from current canonical geometry; do not deliver obsolete candidate previews.
  im=Image.open(FM/p/'figures'/mid/'source.tif').convert('RGB');pts=np.vstack(r['polygons']+(e['before']['polygons'] if e['before'] else []));lo=np.maximum(0,np.floor(pts.min(0)-18)).astype(int);hi=np.minimum(im.size,np.ceil(pts.max(0)+19)).astype(int);box=tuple(lo)+tuple(hi)
  canvas=Image.new('RGB',(1440,780),'#e6eeeb');draw=ImageDraw.Draw(canvas);draw.text((8,5),p+' / '+mid+' / '+lab,font=FONT,fill='black')
  for i,(title,reg) in enumerate([('Source',None),('Before' if e['before'] else 'Previously untraced',e['before']),('Current',r)]):
   t=im.copy();dr=ImageDraw.Draw(t)
   if reg:
    for poly in reg['polygons']:dr.line([tuple(q) for q in poly]+[tuple(poly[0])],fill='#00a1be',width=max(1,round(max(im.size)/1300)))
   t=t.crop(box);ratio=min(466/t.width,705/t.height);t=t.resize((round(t.width*ratio),round(t.height*ratio)),Image.Resampling.LANCZOS);canvas.paste(t,(i*480+(480-t.width)//2,65));draw.text((i*480+10,35),title,font=FONT,fill='black')
  canvas.save(OUT/'changes'/f'{p}__{mid}__{lab.replace("/","_")}.jpg',quality=94)
wc(OUT/'area_changes.csv',area)
counts=collections.Counter(x['change'] for x in area)
stats=dict(processed_publications=len(log),baseline_views=len(baseline),current_views=len(current),current_regional_rois=sum(x['roi_count'] for x in current),source_pages_screened=len(sources),overview_screening_complete=True,all_boundaries_validated=False,enlarged_views=len(enlarged),changes=dict(counts),changed_publications=changedpapers,source_figure_numbering_gaps='none within inventoried 1..maximum figure ranges; Felleman Fig5 found on page31',scope_limit='All processed publication inventories and current canonical views; not every PDF elsewhere in the project queue, every supplementary figure, or every boundary at full resolution.')
(OUT/'review_summary.json').write_text(json.dumps(stats,indent=2)+'\n')
queue=[
 ('Krubitzer_Dooley_2013','Fig7D S1_other_body','unsuitable_for_anatomical_area','Hand/body pictogram perimeter, not independent S1 boundary. Canonical status changed; retained only for drawing audit.'),
 ('Burman_etal_2008','21 older outlines; Fig6 M1 and remaining Fig9 fields','retrace_priority','Seven CJ58R outlines improved; other outlines still rejected. Use gray uncertainty bands, dashed borders and repeated A–D anatomy. Physical scale unresolved.'),
 ('Lyon_etal_1998','Fig09_D auditory border; Fig11A sulcal junction','precision_priority','Possible inset/drift at overview scale. Requires enlarged source border placement, not adjustment toward a desired area.'),
 ('Luethke_etal_1988','Fig12 M/S-I corner; Fig1/2 whole maps','precision_and_coverage','Residual corner rounding/line drift; additional whole-map panels not yet digitized. Establish repeated case identity first.'),
 ('Rosa_etal_1993','V2/MT junctions and frontal islands','precision_and_coverage','Crowded tracer overlays and faint field borders; additional closed frontal components may be possible.'),
 ('Krubitzer_Kaas_1990','Fig6C DM/DI; Fig9A–F strips','source_limited_partial','DM is already partial; separator extrapolation explicit. Additional strips only partial, not whole fields.'),
 ('Krubitzer_Kaas_1993','Fig12B/C DM/VPP and Fig13 motor/3a','not_yet_digitized','Histological envelopes need uncertainty-qualified source interpretation.'),
 ('Krubitzer_etal_1993','Fig15 3b; Fig12/14/18 motor; Fig21 summary','not_yet_digitized','Do not confuse injection with border. Some open components; summary drawing-only.'),
 ('Krubitzer_etal_1995','Fig23 E2 and Fig3 P4 SI islands','not_yet_digitized','Closed components may add partial coverage; body drawings are not cortex.'),
 ('Slutsky_etal_2000','Fig7–10/12/13 body-part subdomains','not_yet_digitized','Some closed local domains remain; whole SI/PM open. Repeated cases must stay linked.'),
 ('Barton_etal_2012','hR/hRT/belt fields','not_yet_digitized','Larger full-panel crops and field-specific tracing needed; no invented border across response gaps.'),
 ('Mayer_etal_2019','PMd/PMv/1/2/5 sampled components','not_yet_digitized','Response/sampled territories only, not complete fields.'),
 ('Halley_etal_2025','Additional 1/2/PPC components','not_yet_digitized','Sampled windows; pooled maps not independent animals.'),
 ('Ghosh_1997','Remaining medial/parietal components; case9 scale','not_yet_digitized_or_uncalibrated','Bank components must remain separate; visible case9 bar or explicit common-scale evidence required.'),
 ('Remple_etal_2006','Fig8–11 additional motor/response components','partial_open','Partial motor strips and sampled colored domains cannot become whole M1.'),
 ('Krubitzer_1995','Summary primary-field silhouettes including echidna Fig1','drawing_only_candidates','Drawable omitted fields, not new calibrated animal observations.'),
 ('VanEssen_Drury_1997','Fig13C atlas and other flatmap displays','native_surface_required','Drawing-only tracing possible; intrinsic metric areas require matching native mesh.'),
 ('Zilles_1985','Fig46–49 and73–76 surface reconstructions','projection_assessment_required','Not just sections: drawable reconstructions exist, but metric surface interpretation must be established.'),
 ('SanchezPanchuelo_etal_2018','Additional Fig3 participants and Fig6 SII','native_surface_required','Thresholded response domains need native vertices and comparable definitions.'),
 ('Neafsey_etal_1986','All physical areas','local_calibration_required','Curved coordinate grid has spatially varying image scale; integrate local cells.'),
 ('Brecht_Freiwald_2012','All schematic measurements','schematic_only','No independent calibration establishes metric fidelity. Keep flagged; do not borrow a locator scale.')]
wc(OUT/'remaining_review_queue.csv',[dict(paper_id=p,figure_or_region=f,status=s,next_step=n) for p,f,s,n in queue])
style='body{font:16px system-ui;line-height:1.5;max-width:1450px;margin:32px auto;padding:0 24px;background:#f4f7f5;color:#203630}a{color:#006878}h1{font-size:34px}h2{margin-top:38px}.notice{padding:18px;background:#fff0ce;border-left:5px solid #b27600}.stats{display:flex;gap:12px;flex-wrap:wrap}.stats div{padding:15px;background:white;border:1px solid #ccd9d3}.paper,.change{background:white;padding:20px;margin:18px 0;border:1px solid #ccd9d3}img{max-width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #ccd9d3;padding:9px}input{font:inherit;padding:10px;width:min(600px,90%)}small{color:#4b625a}'
p=[f'<!doctype html><html><head><meta charset="utf-8"><title>Project tracing recheck — pass 3</title><style>{style}</style></head><body><h1>Project tracing recheck — pass 3</h1><p>31 October 2026 · All 47 processed publication inventories reviewed, including source-only figures.</p>',f'<div class="stats"><div><b>{len(current)}</b> current views</div><div><b>{len(sources)}</b> source pages screened</div><div><b>{counts["revised_geometry"]}</b> revised outlines</div><div><b>{counts["added"]}</b> added outlines</div><div><b>{counts["metadata_only"]}</b> metadata corrections</div></div>','<p class="notice"><b>Complete overview coverage is not complete anatomical validation.</b> All 448 pre-existing views were screened against source images; one additional Beck et al. view now contains four outlines. Selected suspicious borders were checked enlarged. Remaining precision problems, untraced components and source limitations are listed below. Burman and Brecht remain unsuitable for accepted physical-area comparisons.</p>','<p><a href="view_review.csv">Every current view</a> · <a href="area_changes.csv">Area changes</a> · <a href="remaining_review_queue.csv">Remaining work</a> · <a href="source_page_inventory.json">Source-page inventory</a> · <a href="README.md">Methods and scope</a> · <a href="../Beck_Kaas_1998/review/dm_recheck_2026-10-31/index.html">Focused Beck &amp; Kaas review</a></p>','<h2>Clearest examples and unresolved examples</h2><p>The simple closed S1/PV/S2 envelopes in Krubitzer et al. (1997), Fig4/6, and Slutsky et al. (2000), Fig2, were among the clearer examples at overview scale. Beck et al. (1996), Fig11, has clear drawn sensory outlines but uncertain projection. The revised Luethke (1989) Fig6 envelopes now bridge internal tracer marks explicitly. Clear line placement alone does not establish whole-field completeness or metric validity.</p><p>Burman’s remaining older outlines, crowded Rosa V2/MT junctions, Lyon auditory/sulcal edges, and Luethke (1988) Fig12 need further precision work. Krubitzer &amp; Dooley’s naked mole-rat S1-other-body outline is a pictogram footprint; it is now explicitly flagged in canonical measurements.</p>','<details><summary>Enlarged naked mole-rat warning</summary><img src="enlarged/Krubitzer_Dooley_2013__fig07D_pictogram_warning.png" alt="Source body pictogram and its previous S1 contour"><p>No independent anatomical envelope is visible. Geometry retained for audit; status changed to pictorial_footprint_not_anatomical_area.</p></details>','<h2>Applied changes</h2><p>Before versions are archived. Shared borders use the same path. Short obscured segments remain explicitly interpolated. New outlines do not represent additional animals. Comparison images below use the final saved geometry.</p>']
for e,a in zip(events,area):
 key=f'{a["paper_id"]}__{a["map_id"]}__{a["label"].replace("/","_")}.jpg';delta='' if a['percent_pixel_area_change']=='' else f' ({a["percent_pixel_area_change"]:+.2f}%)'
 p.append(f'<article class="change"><h3>{E(a["paper_id"])} / {E(a["map_id"])} / {E(a["label"])}</h3><p><b>{E(a["change"])}</b> · {E(str(a["before_px2"]) or "untraced")} → {E(a["after_px2"])} px²{delta}</p><p>{E(a["reason"])}</p><p><b>Current status:</b> {E(a["status"])} · {E(a["extent"])}</p>')
 if (OUT/'changes'/key).exists():p.append(f'<a href="changes/{quote(key)}"><img loading="lazy" src="changes/{quote(key)}" alt="Source, previous and current {E(a["label"])} outline"></a>')
 p.append(f'<p><a href="../{a["paper_id"]}/review/gallery.html">Current gallery</a> · <a href="../{a["paper_id"]}/figures/{a["map_id"]}/rois.json">Editable geometry</a></p></article>')
p.append('<h2>Remaining precision and coverage queue</h2><table><tr><th>Paper / region</th><th>Status</th><th>Next step</th></tr>')
for paper,f,s,n in queue:p.append(f'<tr><td>{E(paper)}<br>{E(f)}</td><td>{E(s)}</td><td>{E(n)}</td></tr>')
p.append('</table><h2>All 47 publication reviews</h2><p>Overview panels preserve the pre-edit screening state. Use each current gallery or the changes above for revised geometry. Source pages are separately linked, including figures with no saved ROI.</p><input id="filter" placeholder="Filter paper or notes" aria-label="Filter publication reviews">')
for paper,n in sorted(log.items()):
 views=[x for x in current if x['paper_id']==paper];sp=[x for x in sources if x['paper_id']==paper];panels=[x for x in manifest if x['paper_id']==paper]
 p.append(f'<section class="paper" id="{paper}"><h3>{E(paper)}</h3><p>{len(views)} current views · {sum(x["roi_count"] for x in views)} regional outlines · {len(sp)} inventoried source pages</p><p>{E(n["notes"])}</p><p><a href="../{paper}/review/gallery.html">Current gallery</a> · <a href="../{paper}/source/paper.pdf">Source PDF</a></p><details><summary>Screened overviews and source pages</summary>')
 for m in panels:p.append(f'<p><a href="screening/{m["file"]}">{E(m["kind"])} overview: {E(m["file"])}</a></p>')
 p.append('<p>'+' · '.join(f'<a href="../{quote(x["source_image"])}">PDF p{x["pdf_page"]} (Fig {E(x["figures"])})</a>' for x in sp)+'</p></details></section>')
p.append('<script>document.querySelector("#filter").addEventListener("input",e=>{const q=e.target.value.toLowerCase();document.querySelectorAll(".paper").forEach(x=>x.hidden=!x.textContent.toLowerCase().includes(q));});</script></body></html>')
(OUT/'index.html').write_text(''.join(p))
readme=f'''# Project tracing recheck — pass 3

31 October 2026. [Open report](index.html).

Overview screening covered all **{len(log)} processed publications**, **{len(baseline)} pre-existing canonical views**, and **{len(sources)} inventoried source pages**. One new repeated view brings the current count to **{len(current)} views / {stats['current_regional_rois']} regional ROIs**. This is not a claim that every boundary has been checked vertex by vertex, every omitted region has now been traced, or every supplementary figure/PDF in the unprocessed queue was reviewed.

This pass made **{counts['revised_geometry']} contour revisions**, **{counts['added']} additions**, and **{counts['metadata_only']} metadata corrections** in {len(changedpapers)} publications. [Changes](area_changes.csv), [every current view](view_review.csv), [remaining work](remaining_review_queue.csv), [actual screening notes](screening_log.json).

## Interpretation

- Beck & Kaas (1998): all eight saved envelopes checked enlarged. Figs3/11 geometry improved; Fig9 interpolation display clarified. Figs4/7 remain inferred, Fig11 partial.
- Luethke et al. (1989): eight A-I/R contours in four Fig6 panels corrected across internal tracer symbols. These repeat the same tamarin case87-44.
- Burman et al. (2008): CJ58R M1 dorsal component, 3a and 3b revised; 6Dc, 6Dr, 8Ad and 8Av added. Seven provisional gray-band-center estimates, 21 older outlines still rejected. No physical calibration resolved. Fig9A–D repeat the same anatomy.
- Beck et al. (1996): Fig11 case92-78 S1/S2/PV/Aud added; repeated tissue, own printed 1-mm bar. Projection uncertain: scaled drawing areas only, excluded from accepted intrinsic complete-field summaries. Aud/PV overlap is documented in the source, not silently erased.
- Krubitzer & Dooley (2013): naked mole-rat S1_other_body is a pictogram footprint, not an independently bounded cortical field. Geometry retained for audit and canonical status changed to exclude anatomical interpretation.

## Methods and guides

Source captions govern solid/dashed boundaries, broad uncertainty bands, sulci, cuts and internal tracer/body-part symbols. Compare repeated views of the same animal first; similar maps guide interpretation, not vertex copying. Shared borders use identical paths where revised. Interpolations remain provisional; missing borders are not inferred merely to close a polygon. No scale was transferred between figures.

See the [project atlas/guide directory](../ReadMe.md#atlases-and-tracing-guides), [tracing method](../tracing_method.md), and [Burman caption/atlas guidance](../Burman_etal_2008/README.md#atlases-and-tracing-guides). Marmoset references include the Nencki–Monash template, Paxinos atlas and Majka registration guidance; the project also lists the FSL surface-registration guide. They are guidance resources, not sources of these revised coordinates. No atlas registration or predicted sulcal layer was applied.

## Audit and validation

`before/` preserves prior publication outputs; `baseline.json` preserves the original 448-view inventory. `applied_changes.json` contains before/after geometry; `changes/` is rendered from final canonical coordinates. Overview panels are pre-edit screening snapshots. Current galleries contain rebuilt editable ImageJ ROI sets, masks and measurements. Native ImageJ checks verify saved geometry/calibration, not anatomical correctness.

`source_page_inventory.json` includes continuation pages and a manually recovered Felleman Fig5 page31 (a graph). Figure numbers have no gaps within the inventoried ranges after that recovery; this is not proof of supplement completeness. Source-only studies are included in screening, with no invented ROIs.

The project-wide downstream M1 merge was not regenerated: repeated views, partial maps, drawings and rejected contours require explicit inclusion rules. The recommended-paper batch was refreshed from canonical measurements. Remaining uncertainty is recorded rather than treated as a pass.
'''
(OUT/'README.md').write_text(readme)
for paper in changedpapers:
 es=[a for a in area if a['paper_id']==paper];root=FM/paper;doc=root/'documentation/pass3_tracing_review.md'
 text=f'# Pass 3 tracing review — {paper}\n\n31 October 2026. [Project review](../../project_review_2026-10-31_pass3/index.html#{paper}).\n\n{log[paper]["notes"]}\n\n'
 text+='\n'.join('- '+e['map_id']+' / '+e['label']+': '+e['change']+'. '+e['reason'] for e in es)
 text+='\n\nNative ImageJ read-back and measurement verification check file integrity, not anatomical certification. Prior outputs are archived in the project pass3 review. See [all area changes](../../project_review_2026-10-31_pass3/area_changes.csv).\n\n## Atlases and guides\n\nUse the [project atlas and tracing-guide directory](../../ReadMe.md#atlases-and-tracing-guides) and [tracing method](../../tracing_method.md). Source captions and repeated same-case views guided this pass. Atlases can guide identity/adjacency but were not registered or copied into these contours, and supplied no calibration.\n'
 doc.write_text(text)
# README links outside checksum-scoped generated directories; preserve atlas sections.
marker='<!-- project-tracing-review-2026-10-31-pass3 -->'
for paper in sorted(log):
 path=FM/paper/'README.md'
 if not path.exists():path=FM/paper/'ReadMe.md'
 old=path.read_text() if path.exists() else '# '+paper+'\n'
 old=old.split(marker)[0].rstrip()
 if paper=='Burman_etal_2008':old=old.replace('The original 24 ROIs remain rejected pending retracing.', 'Pass3 supersedes three original outlines and adds four: seven provisional gray-band-center estimates, with 21 older outlines still rejected.')
 path.write_text(old+f'\n\n{marker}\n## Project recheck, pass 3\n\n[Current project-wide review](../project_review_2026-10-31_pass3/index.html#{paper}) · [Scope and methods](../project_review_2026-10-31_pass3/README.md). All inventoried source figures and saved views screened at overview scale; remaining precision/coverage limits are recorded.\n'+ ('\n[This paper’s changes and limitations](documentation/pass3_tracing_review.md).\n' if paper in changedpapers else ''))
path=FM/'ReadMe.md';s=path.read_text().split(marker)[0].rstrip();path.write_text(s+f'\n\n{marker}\n## Project recheck, pass 3\n\n[Open the latest review](project_review_2026-10-31_pass3/index.html): {len(log)} publications, {len(current)} current views, {len(sources)} source pages screened; {counts["revised_geometry"]} contours revised, {counts["added"]} added. [Remaining precision and coverage queue](project_review_2026-10-31_pass3/remaining_review_queue.csv). Overview completion does not certify every boundary.\n')
print(json.dumps(stats,indent=2))
