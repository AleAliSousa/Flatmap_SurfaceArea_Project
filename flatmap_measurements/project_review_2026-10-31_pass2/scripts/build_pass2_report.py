"""Build second-pass review and assert the scope of canonical measurement changes."""
from prepare_precision import *
import csv,io,html,collections
E=lambda s:html.escape(str(s))
PREV=FM/'project_review_2026-10-31'
changes=json.loads((OUT/'applied_changes.json').read_text());changed={(c['paper'],c['map_id']) for c in changes};papers=sorted({c['paper'] for c in changes});baseline=json.loads((OUT/'baseline_inventory.json').read_text());base={(r['paper_id'],r['map_id']):r for r in baseline}
assets=OUT/'views';assets.mkdir(exist_ok=True)
def wc(p,rows):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
areas=[];valid=[]
for paper in papers:
 z=zipfile.ZipFile(OUT/'before'/(paper+'.zip'))
 old={(r['map_id'],r['label']):r for r in csv.DictReader(io.StringIO(z.read('data/measurements.csv').decode()))};new={(r['map_id'],r['label']):r for r in csv.DictReader((FM/paper/'data/measurements.csv').open())}
 expected={(c['map_id'],c['label']) for c in changes if c['paper']==paper}
 # An old unmeasured row can become a measured row under the same key.
 actual={k for k in old if k not in new or old[k]['area_px2']!=new[k]['area_px2']} | (set(new)-set(old))
 assert actual==expected,(paper,actual-expected,expected-actual)
 for k in set(old)&set(new):
  for field in ['scale_length_px','scale_length_mm','specimen','hemisphere','view_type','repeat_of','include_in_whole_hemisphere_summary']:
   assert old[k].get(field)==new[k].get(field),(paper,k,field)
 for c in [c for c in changes if c['paper']==paper]:
  k=(c['map_id'],c['label']);b=old.get(k,{});a=new[k];bp=b.get('area_px2','NA');delta=100*(float(a['area_px2'])/float(bp)-1) if bp not in ['NA','',None] else None
  areas.append(dict(paper_id=paper,map_id=k[0],label=k[1],change_type=c['kind'],before_area_px2=bp,after_area_px2=a['area_px2'],before_area_mm2=b.get('area_mm2','NA'),after_area_mm2=a['area_mm2'],change_percent=round(delta,6) if delta is not None else 'NA',extent=a['extent'],status=a['status'],reason=c['note']))
  c['area_change']=areas[-1]
 v=json.loads((FM/paper/'documentation/validation.json').read_text());assert v['native_imagej_roundtrip']=='passed',(paper,v)
 valid.append(dict(paper_id=paper,changed_regions=len(expected),unaffected_areas_identical=True,scale_identity_repeat_flags_preserved=True,native_imagej_roundtrip=v['native_imagej_roundtrip']))
wc(OUT/'area_changes.csv',areas)
for r in baseline:
 f=FM/r['json'];d=json.loads(f.read_text());key=(r['paper_id'],r['map_id'])
 if key not in changed:assert hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256'],key
 else:
  z=zipfile.ZipFile(OUT/'before'/(r['paper_id']+'.zip'));before=json.loads(z.read('figures/'+r['map_id']+'/rois.json'))
  for k in set(d)|set(before):
   if k not in ['rois','unmeasured']:assert d.get(k)==before.get(k),(key,k)
  old_source=np.asarray(Image.open(io.BytesIO(z.read('figures/'+r['map_id']+'/source.tif'))).convert('RGB'));new_source=np.asarray(Image.open(f.parent/'source.tif').convert('RGB'));assert np.array_equal(old_source,new_source),(key,'source pixels changed')
# Actual guide use, explicitly distinguished from recommended atlases/registration.
guides={
 'Ghosh_1997':'Same-paper cat case maps in Figs.9, 10, 14, 15 and 16 were compared for field identity, adjacency and exposed-versus-bank components. Source labels and each panel’s own lines govern the tracing. The fSCor fundus divides bank components, not cortical areas; the new 3a/3b ventral-bank ROIs are only components. No case geometry or scale was transferred.',
 'Remple_etal_2006':'Tree-shrew Figs.7A/7B, 8 and the same-case Fig.11 were used to distinguish S1 boundaries, body-part compartments, modules and the medial-wall fold. Lyon et al. 1998 provides same-species orientation only; parcellations are not assumed identical. The medial-wall line does not truncate the closed S1 cap.',
 'Burman_etal_2008':'Fig.9A–D anatomical insets identify V1ca and V1op within the detached occipital lobe; both belong to V1. Gray architectural bands, estimated dashed borders and solid folds/cuts require separate interpretations, as documented in this dataset’s atlas guide. Krubitzer & Kaas 1990 marmoset maps supplied orientation only. Nencki–Monash and the Marmoset Brain Connectivity Atlas remain proposed guides; no atlas registration was applied. V2 remains partial; all 24 Burman ROIs remain rejected for analysis.',
 'Beck_Kaas_1998':'The source Fig.9 DM fragment was enlarged, and the same-paper Fig.10 map was used as an identity/topology guide. The revised contour follows the visible perimeter across lettering interruptions. The fragment and uncertain source borders remain provisional.',
 'Krubitzer_2009':'The macaque map in Krubitzer & Dooley 2013 was compared for orientation/adjacency only. In the 2009 source itself, M/POd lies between PIP, V3d and V2; the former tiny outline followed lettering instead of the field. These summary maps use different parcellations and are not independent animals.',
 'Krubitzer_1998':'Luethke et al. 1988 squirrel maps corroborate the M/SI arrangement. The new M outline follows the black silhouette in the 1998 Fig.14D summary itself, preserving the internal M lettering. It remains an illustrative summary, not an additional specimen or a whole-neocortex denominator.'}
remaining=[
 ('Burman_etal_2008','CJ61 and CJ58R M1/3a/3b; remaining architectural parcels','Gray uncertainty bands, narrow extensions and estimated borders need a dedicated joint retrace. V2’s ventral continuation remains unresolved. All 24 ROIs remain excluded; missing calibration is unchanged. A 15-pixel eroded overlap between revised V1 and the retained provisional V2 strip is explicitly unresolved.'),
 ('Ghosh_1997','Unrevised physiology-heavy boundaries and missing parietal/medial compartments','Some outer edges still deviate at lettering/tracer marks. Only visually reviewed candidates were adopted. Components are not a validated whole-M1 sum. Case9 has no defensible visible scale.'),
 ('Remple_etal_2006','Face/oral partitions, some S1 margins and open motor strips','Automatic fills can stop at the medial-wall line or cross an internal subdivision. Rejected candidates were not applied. Remaining open-ended M1/M2 drawings do not establish whole-field areas.'),
 ('Rosa_etal_1993','V2 and crowded MT/parietal contours','Sulcal landmarks can be mistaken for areal boundaries. Same-paper schematic maps can guide field identity but cannot supply a case-specific border.'),
 ('Luethke_etal_1988','Fig.12 shared M/SI edge','Local border displacement remains; compare the squirrel case series while preserving each case’s own geometry.'),
 ('Luethke_etal_1989','Fig.6 panels1/2 A1/R','Use clearer repeated panels3/4 to interpret source lines after establishing tissue correspondence; no copied border was applied here.'),
 ('Lyon_etal_1998','Fig.9D auditory and Fig.11A sensory/V1 margins','These still merit enlarged joint-border review; Remple maps help topology, not metric calibration or geometry.'),
 ('Hinds_etal_2008','V1 near star annotations','Symbol-shaped notches require local source review; an atlas average would not establish the missing individual perimeter.'),
 ('Brecht_Freiwald_2012','All schematic fields','Close tracing cannot recover a metric area from schematic proportions. Existing D grades and calibration cautions remain.'),
 ('Neafsey_etal_1986','Curved sampling-grid maps','Physical areas require local cell calibration; a single borrowed scale is not valid. Pixel geometry is retained.')]
wc(OUT/'remaining_priorities.csv',[dict(paper_id=p,regions=r,next_step=n) for p,r,n in remaining])
rows=[]
for oldrow in csv.DictReader((PREV/'view_review.csv').open()):
 r=dict(oldrow);paper,mid=r['paper_id'],r['map_id'];f=FM/r['roi_path'];d=json.loads(f.read_text());cs=[c for c in changes if (c['paper'],c['map_id'])==(paper,mid)]
 r['prior_grade']=r['grade'];r['grade_basis']='Retained view-level screening category; individual corrected fields do not certify the whole map.';r['ROI_count']=len(d['rois']);r['labels']='; '.join(x['label'] for x in d['rois']);r['changed_this_review']=bool(cs);r['pass2_corrected_regions']=len(cs);r['pass2_new_regions']=sum(c['kind']=='addition' for c in cs);r['current_roi_sha256']=hashlib.sha256(f.read_bytes()).hexdigest();r['baseline_roi_sha256']=base[(paper,mid)]['sha256'];r['review_scope']='Second whole-project overview screening; changed regions additionally reviewed enlarged. No independent anatomical certification.'
 r['pass2_note']=('Applied '+str(len(cs))+' region changes. '+guides[paper]) if cs else ('Overview revisited; no canonical geometry change in this pass. '+next((n for p,_,n in remaining if p==paper),'No additional source-supported correction selected at overview resolution.'))
 if cs:
  stem=paper+'__'+mid;im=Image.open(f.parent/'source.tif').convert('RGB');im.save(assets/(stem+'_source.png'));trace=im.copy();dr=ImageDraw.Draw(trace)
  for reg in d['rois']:
   for p in reg['polygons']:dr.line([tuple(v) for v in p]+[tuple(p[0])],fill='#008fa8',width=1)
  for name,x in [('source',im.copy()),('trace',trace)]:x.thumbnail((1200,1400));x.save(assets/(stem+'_'+name+'.jpg'),quality=95)
  r['source_preview']='views/'+stem+'_source.jpg';r['trace_preview']='views/'+stem+'_trace.jpg';r['precision_view']='views/'+stem+'.html'
  def layer(items,mode):
   out=[]
   for reg in items:
    c=next((c for c in cs if c['label']==reg['label']),None);color=('#c36d12' if c['kind']=='addition' else '#008ca6') if c else '#6b7e87';cl='changed' if c else 'unchanged'
    for poly in reg['polygons']:out.append('<polygon class="'+cl+'" points="'+' '.join(str(x)+','+str(y) for x,y in poly)+'" fill="none" stroke="'+color+'" stroke-width="1.2" vector-effect="non-scaling-stroke"><title>'+E(reg['label'])+'</title></polygon>')
   return '<g id="'+mode+'">'+''.join(out)+'</g>'
  z=zipfile.ZipFile(OUT/'before'/(paper+'.zip'));before=json.loads(z.read('figures/'+mid+'/rois.json'))
  h='<!doctype html><meta charset="utf-8"><title>'+E(paper+' '+mid)+'</title><style>body{font:16px system-ui;margin:24px;color:#18312f}button,input{font:inherit;margin:5px}#frame{overflow:auto;border:1px solid #ddd}svg{display:block;width:100%;height:auto}#before{display:none}.unchanged{display:none}.bar{position:sticky;top:0;background:white;padding:8px;z-index:1}li{margin:8px 0}</style><p><a href="../index.html">← Second-pass review</a></p><h1>'+E(paper+' / '+mid)+'</h1><p>'+E(guides[paper])+'</p><div class="bar"><button onclick="mode(0)">Source</button><button onclick="mode(1)">Before</button><button onclick="mode(2)">After</button><label><input type="checkbox" onchange="document.querySelectorAll(\'.unchanged\').forEach(x=>x.style.display=this.checked?\'\':\'none\'); if(this.checked) document.querySelectorAll(\'.unchanged\').forEach(x=>x.style.display=\'inline\')">Show unchanged regions</label><label>Zoom <input type="range" min="60" max="350" value="100" oninput="document.querySelector(\'svg\').style.width=this.value+\'%\'"></label><span id="state">After: teal revised; orange added</span></div><div id="frame"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+str(im.width)+' '+str(im.height)+'"><image href="'+stem+'_source.png" width="'+str(im.width)+'" height="'+str(im.height)+'"/>'+layer(before['rois'],'before')+layer(d['rois'],'after')+'</svg></div><ul>'+''.join('<li><b>'+E(c['label'])+'</b>: '+E(c['note'])+'</li>' for c in cs)+'</ul><script>function mode(n){document.getElementById("before").style.display=n===1?"inline":"none";document.getElementById("after").style.display=n===2?"inline":"none";document.getElementById("state").textContent=["Source only","Before","After: teal revised; orange added"][n]}</script>'
  (assets/(stem+'.html')).write_text(h)
 else:
  r['source_preview']='../project_review_2026-10-31/'+oldrow['source_preview'];r['trace_preview']='../project_review_2026-10-31/'+oldrow['trace_preview'];r['precision_view']='../'+paper+'/review/gallery.html'
 rows.append(r)
wc(OUT/'view_review.csv',rows)
# Explicit review ledger, including pitfalls discovered in the enlarged pass.
log=json.loads((OUT/'screening_log.json').read_text());log['notes'].update(guides);log['notes'].update({p:log['notes'].get(p,'')+' Remaining: '+n for p,_,n in remaining});log['notes']['Krubitzer_Kaas_1990']='Area17 construction polygons in Figs.12–24 can protrude beyond tissue, but clip_to_tissue is true and the final masks are tissue-clipped; those construction paths were not mistaken for measured exterior cortex.';log['applied_regions']=len(changes);log['changed_views']=len(changed);(OUT/'screening_log.json').write_text(json.dumps(log,indent=2)+'\n')
summary=dict(active_datasets=len({r['paper_id'] for r in rows}),active_views=len(rows),overview_sheets_reviewed=len(log['sheets_reviewed']),traced_views=sum(int(r['ROI_count'])>0 for r in rows),regional_ROIs=sum(int(r['ROI_count']) for r in rows),revised_regions=sum(c['kind']=='revision' for c in changes),added_regions=sum(c['kind']=='addition' for c in changes),changed_regions=len(changes),changed_views=len(changed),changed_papers=len(papers),grades=dict(collections.Counter(r['grade'] for r in rows)),rebuild_validation=valid,unchanged_view_hashes_verified=True,source_pixels_scale_and_metadata_preserved=True,anatomical_certification=False)
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
style='body{font:16px system-ui;max-width:1380px;margin:32px auto;padding:0 24px;background:#f4f7f5;color:#193733}h1{font-size:34px}h2{margin-top:36px}a{color:#006f81}p{line-height:1.5}.notice{padding:18px;background:#fff0cc;border-left:5px solid #b57812}.card{background:white;padding:20px;border:1px solid #ccdcd6;margin:14px 0;border-radius:8px}img{max-width:100%;height:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}.bar{position:sticky;top:0;background:#e4efea;padding:14px;z-index:1}input,select,button{font:inherit;padding:7px;margin:4px}summary{cursor:pointer;line-height:1.6}small{color:#526d65}.pill{display:inline-block;background:#dcece7;padding:4px 10px;border-radius:16px}td,th{text-align:left;padding:8px;border-bottom:1px solid #ccdcd6}table{border-collapse:collapse;width:100%}.hidden{display:none}'
parts=['<!doctype html><html><head><meta charset="utf-8"><title>Flatmap review — second precision pass</title><style>'+style+'</style></head><body><h1>Flatmap review · second precision pass</h1><p>31 October 2026 · All <b>448 views across 44 datasets</b> revisited on 128 overview sheets. Changed regions also inspected enlarged.</p><p><span class="pill">'+str(summary['revised_regions'])+' revised contours</span> <span class="pill">11 added components</span> <span class="pill">14 views · 6 papers</span> <span class="pill">'+str(summary['regional_ROIs'])+' regional ROIs now saved</span></p><p><a href="area_changes.csv">Area changes</a> · <a href="view_review.csv">All-view review table</a> · <a href="remaining_priorities.csv">Remaining priorities</a> · <a href="README.md">Methods, guides and verification</a> · <a href="../project_review_2026-10-31/index.html">First-pass record</a></p><div class="notice"><b>Improved line fit does not establish calibration or anatomical certainty.</b> Burman remains rejected for analysis; Brecht remains schematic. Added cat bank/medial regions are components, and the squirrel M is an illustrative summary. No scales or contours were borrowed, no atlas registration was applied, and no new whole-M1 or whole-neocortex total was manufactured.</div><h2>What changed</h2><p>The main gains are smoother cat motor/sensory borders and previously omitted medial/bank components; tree-shrew sensory modules and the complete drawn S1 cap; marmoset V1/V2 identity; a macaque M/POd field previously traced around lettering; a clearer DM fragment; and the squirrel summary M silhouette. Four further cat contours were corrected after checking neighboring borders together. Small residual edge overlaps remain documented for Remple Fig.7A (4 pixels after erosion) and Burman V1/V2 (15 pixels).</p><h2>Enlarged source toggles</h2><p>Open a map to toggle source / before / after at identical coordinates and zoom in. Changed regions are shown first; unchanged contours can be enabled.</p><div class="grid">']
for r in rows:
 if r['changed_this_review']:parts.append('<div class="card"><a href="'+r['precision_view']+'"><b>'+E(r['paper_id'])+' / '+E(r['map_id'])+'</b></a><p>'+str(r['pass2_corrected_regions'])+' changes; '+str(r['pass2_new_regions'])+' additions. View grade '+r['grade']+' retained.</p></div>')
parts.append('</div><h2>Each applied region change</h2><p>Source, previous outline and saved second-pass outline. Expand each row for the enlarged comparison. Area changes compare saved measurements before and after this pass; they are not accuracy scores.</p>')
for i,c in enumerate(changes):
 name='applied_'+str(i).zfill(2);preview(c['paper'],c['map_id'],c['old'] or dict(polygons=[]),c['applied_new'],name,after_title='After');a=c['area_change'];val='added' if a['change_percent']=='NA' else f"{a['change_percent']:+.1f}%";parts.append('<details class="card"><summary><b>'+E(c['paper']+' / '+c['map_id']+' / '+c['label'])+'</b> · '+val+'</summary><p>'+E(c['note'])+'</p><p>Extent: '+E(a['extent'])+'; '+E(a['status'])+'</p><img loading="lazy" src="candidates/'+name+'.jpg" alt="Source, before and after '+E(c['label'])+'"></details>')
parts.append('<h2>Clearer examples and remaining uncertainty</h2><p>Examples retaining the strongest source/fit grade include Catania & Remple 2002 and selected Beck 1996, Huffman 1999 and Frost 2000 maps. Dense annotations, faint borders, gray uncertainty bands and low-resolution dotted lines remain harder. A close schematic outline can still be unsuitable for a metric comparison. Grades are view-level screening judgments, not certification of every region.</p><table><tr><th>Dataset / region</th><th>Remaining work</th></tr>')
for p,r,n in remaining:parts.append('<tr><td>'+E(p)+'<br><small>'+E(r)+'</small></td><td>'+E(n)+'</td></tr>')
parts.append('</table><h2>All 448 views</h2><p>A: clearest source/fit; B: drawing fit with caveats; C: targeted retracing needed; D: unsuitable for intended area inference; N: source-only. Prior grades are retained so fixing a few fields does not imply that the whole map is now reliable. All were screened again; only the 62 listed regions changed.</p><div class="bar"><input id="query" type="search" placeholder="Find paper, species or map"><select id="grade"><option value="">All grades</option>'+''.join('<option>'+x+'</option>' for x in 'ABCDN')+'</select><select id="action"><option value="">All views</option><option value="changed">Changed this pass</option></select><span id="count"></span></div><div id="allviews">')
for r in rows:
 search=' '.join(str(r.get(x,'')) for x in ['paper_id','map_id','species','labels']).lower();parts.append('<details class="card view" data-search="'+E(search)+'" data-grade="'+r['grade']+'" data-action="'+('changed' if r['changed_this_review'] else '')+'"><summary><b>'+E(r['paper_id']+' / '+r['map_id'])+'</b> · '+E(r['species'])+' · grade '+r['grade']+' · '+str(r['ROI_count'])+' regions'+(' · UPDATED' if r['changed_this_review'] else '')+'</summary><p>'+E(r['pass2_note'])+'</p><p><small>Previous screening notes: '+E(r['notes'])+'</small></p><p><a href="'+r['precision_view']+'">Open map review</a> · <a href="../'+r['paper_id']+'/figures/'+r['map_id']+'/rois.json">Canonical geometry</a></p><div class="grid"><div>Source<img loading="lazy" src="'+r['source_preview']+'" alt="Source"></div><div>Current tracing<img loading="lazy" src="'+r['trace_preview']+'" alt="Current tracing"></div></div></details>')
parts.append('</div><script>const q=document.getElementById("query"),g=document.getElementById("grade"),a=document.getElementById("action");function filter(){let n=0;document.querySelectorAll(".view").forEach(x=>{let ok=x.dataset.search.includes(q.value.toLowerCase())&&(!g.value||x.dataset.grade===g.value)&&(!a.value||x.dataset.action===a.value);x.classList.toggle("hidden",!ok);n+=ok});document.getElementById("count").textContent=n+" views"}for(const e of [q,g,a])e.addEventListener("input",filter);q.value=new URLSearchParams(location.search).get("paper")||"";filter();</script></body></html>');(OUT/'index.html').write_text(''.join(parts))
readme=f'''# Second project tracing pass — 31 October 2026

[Open review](index.html) · [Area changes](area_changes.csv) · [All views](view_review.csv) · [Remaining priorities](remaining_priorities.csv)

All 448 active source/overlay views in 44 datasets were screened again on 128 overview sheets. The 62 changed regions were additionally reviewed enlarged: 51 existing contours revised and 11 previously omitted components added, across 14 views in six papers. There are now {summary['regional_ROIs']} regional ROIs. This is not individual anatomical certification of every unchanged field. Source-only views, schematic limits and unresolved borders remain explicit.

## Applied work

- **Ghosh 1997:** 39 existing cat contours revised; 10 medial/coronal-bank components added. Four corrections were prompted by joint-edge overlap checks. Medial components in cases6/9 and case9 bank components are not whole fields. The ventral 3a/3b bank components stop at fSCor; a fundus is not an areal limit. No validated whole-M1 sum is claimed.
- **Remple 2006:** eight tree-shrew contours improved, including S1’s medial cap and seven sensory/module outlines. The medial-wall fold does not truncate the closed S1 field.
- **Burman 2008:** the Fig.9 inset resolves V1ca/V1op as parts of V1. Removed their mistaken inclusion in V2; retained V2 strip is explicitly partial. All 24 Burman ROIs remain rejected for analysis. Neither this correction nor an atlas supplies calibration.
- **Beck & Kaas 1998:** enlarged DM-fragment boundary corrected across lettering artifacts; remains a partial uncertain fragment.
- **Krubitzer 2009:** M/POd corrected from a letter-shaped contour to the source field envelope. Large percentage change reflects the earlier wrong object, not a biological difference.
- **Krubitzer 1998:** squirrel summary M silhouette added. Illustrative/repeated geometry is not another animal.

## How precision was improved

Source crops were inspected before geometry changes. Closed printed interiors were extracted only when the resulting outline followed the correct anatomical compartment. Internal lettering and recording marks were retained by filling interior holes. Short pixel gaps were closed in working masks, then candidate perimeters were compared enlarged against the unchanged source. Manual revisions addressed folds, label interruptions and erroneous field identity. Region extraction used a half-pixel coordinate correction and 0.5-pixel simplification; these are numerical conventions, not anatomical precision claims. Shared-edge checks prompted four additional cat revisions, including a complete retrace of the case8 4sfu wedge.

Some automatic candidates were rejected because they stopped at a fold, crossed a body-part subdivision, or followed tracer/letter artifacts. They remain only in `candidates/` for provenance; **only `applied_changes.json` describes saved canonical changes**. `proposed_changes.json` contains the initial 58 proposals and `shared_edge_candidates.json` the later 4 reviewed proposals. Do not rerun candidate generation against the updated canonical inputs to reproduce the old baseline; use the archived inputs.

## Atlases, same-species maps and guides actually used

'''+''.join('### '+p+'\n\n'+guides[p]+'\n\n' for p in papers)+'''The [project atlas directory](../ReadMe.md#atlases-and-tracing-guides) and existing paper README atlas sections remain available. Source figures/captions establish line meanings. Same-species topology helps distinguish fields and folds; it does not justify transplanting shapes, predicting unobserved sulci as measured borders, or borrowing scales. No atlas registration or predicted sulcal layer was applied.

## What remains unclear

See [remaining priorities](remaining_priorities.csv). All previous view grades are retained and explicitly described as screening categories. Selected corrected contours can be more accurate while the encompassing map still merits grade C. Brecht stays grade D for intended metric inference. Native ImageJ read-back verifies file/mask agreement, not anatomical truth.

The final overlap audit reports expected parent/subregion overlap in Remple Fig.8A/C a 4-pixel residual S1/S2-PV edge overlap in Remple Fig.7A, and a 15-pixel unresolved V1/V2 strip overlap in Burman, which remains excluded. Cat shared-edge interior overlaps introduced during refinement were corrected. Eroding by two source pixels is a diagnostic, not a calibrated uncertainty envelope. No regions are summed across uncertain overlaps.

## Reproducibility and verification

`before/<paper>.zip` preserves each affected dataset before this pass (including canonical polygons, ImageJ ROIs, images, measurements and documentation). `applied_changes.json` preserves complete old/new region objects and reasons. Each changed source crop has identical RGB pixels before/after; scale endpoints, crop, render scale, specimen, hemisphere, repeat relationships and denominator eligibility remain unchanged. Unchanged view JSON hashes and unaffected regional area values were checked. The V2 extent change to partial is deliberate.

All six publications were rebuilt with native ImageJ; ROI/mask read-back passed. Updated measurements, editable ROI archives, masks and native tracing galleries are in the publication folders. The recommended-paper aggregate is regenerated after publication rebuilds. Validation logs and overlap diagnostics are in `validation/`; final verification results are in `summary.json` and `validation/final_checks.json`.

The new HTML source toggles use identical image and polygon coordinates, so display rescaling cannot shift the overlay relative to the source. Region before/after comparisons and exact area differences are supplied for review. The first-pass report remains a historical record and links here. Cross-project `surface_area_analysis` snapshots and workbook comparison tables were not recomputed in this tracing pass; use the publication measurement tables and this report for current contour-derived values.
'''
(OUT/'README.md').write_text(readme)
# Persistent README links, preserving prior atlas guidance.
marker='<!-- project-tracing-review-2026-10-31-pass2 -->'
for paper in papers:
 path=FM/paper/'README.md';s=path.read_text().split(marker)[0].rstrip();cs=[c for c in changes if c['paper']==paper]
 path.write_text(s+'\n\n'+marker+'\n## Second precision pass, 31 October 2026\n\n[Source / before / after review](../project_review_2026-10-31_pass2/index.html?paper='+paper+') · [Change log and areas](../project_review_2026-10-31_pass2/area_changes.csv)\n\n'+str(sum(c['kind']=='revision' for c in cs))+' revised regions; '+str(sum(c['kind']=='addition' for c in cs))+' added components. Original datasets are archived in `../project_review_2026-10-31_pass2/before/`.\n\n**Atlases and comparison guides:** '+guides[paper]+'\n\nSource-based revisions remain provisional. Existing specimen, scale and analysis-eligibility restrictions are preserved. See the review for unresolved fields and source-specific line meanings.\n')
path=FM/'ReadMe.md';s=path.read_text().split(marker)[0].rstrip();path.write_text(s+'\n\n'+marker+'\n## Second project precision pass\n\n[Open the second-pass review](project_review_2026-10-31_pass2/index.html): all 448 views screened again; 51 contours refined and 11 components added. Includes enlarged source toggles, area changes, atlas/same-species guide notes and remaining priorities. Original datasets archived; no calibration or specimen identities changed.\n')
# Keep the old review navigable as a historical baseline.
import re
p=PREV/'index.html';s=p.read_text();banner='<!-- pass2-link -->';endmark='<!-- /pass2-link -->'
if banner in s:
 if endmark in s:s=re.sub(re.escape(banner)+'.*?'+re.escape(endmark),'',s,flags=re.S)
 else:s=s.split(banner)[0]
notice=banner+'<p style="padding:18px;background:#fff0cc"><b>A newer precision pass is available:</b> <a href="../project_review_2026-10-31_pass2/index.html">62 region changes and updated source toggles</a>. This page preserves the first-pass review.</p>'+endmark
s=s.replace('<body>','<body>'+notice,1);p.write_text(s)

print(json.dumps(summary,indent=2))
