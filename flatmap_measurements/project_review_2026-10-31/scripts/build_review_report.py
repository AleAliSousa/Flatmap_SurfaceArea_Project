"""Build an offline, filterable audit without modifying measurement geometry."""
from pathlib import Path
from collections import Counter
import csv,json,html,hashlib,zipfile,io
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parents[1];FM=OUT.parent
E=html.escape
def writecsv(path,rows):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
inv=list(csv.DictReader((OUT/'inventory.csv').open()));ass=json.loads((OUT/'assessments.json').read_text());changes=json.loads((OUT/'applied_changes.json').read_text())
changed={(c['paper'],c['map_id']) for c in changes};assets=OUT/'views';assets.mkdir(exist_ok=True);comparisons=OUT/'before_after';comparisons.mkdir(exist_ok=True)
for c in changes:
 k=c['paper']+'/'+c['map_id'];a=ass[k]
 if 'baseline_assessment' not in a:a['baseline_assessment']={x:a[x] for x in ['grade','fit','notes','improvement']}
 a['grade']='A' if c['paper'] in ['Beck_etal_1996','Frost_etal_2000'] else 'B'
 a['fit']='source_refined_and_enlargement_reviewed'
 a['notes']=' '.join(x['note'] for x in changes if x['paper']==c['paper'] and x['map_id']==c['map_id'])
 a['improvement']='Applied source-supported correction. Review before/after geometry and measured area change. Preserve existing calibration, specimen relationships and source limitations.'
for k,a in ass.items():
 if k.startswith('Ghosh_1997/'):
  a['notes']+=' Enlarged review confirms coarse corners on thin areal borders, especially exposed 4gamma and bank edges. Fig16CD case8 has substantial ventral bank-edge displacement.'
  a['improvement']='Retrace shared thin field boundaries and outer bank edges jointly on enlarged source; use the paired exposed/bank panel and caption to distinguish sulci. Do not sum exposed and bank components without proving nonoverlap and coverage.'
 if k.startswith('Rosa_etal_1993/'):
  a['notes']+=' Enlarged review: several V2 outer guides and crowded parietal/MT-complex contours depart from source; some large black paths are sulcal landmarks, not areal borders. V1 generally clearer, with local edge deviations.'
  a['improvement']='Use schematic Figures 3C/11 for label adjacency only; resolve each specimen border against its own source and caption. Preserve tracer deposits inside tissue. Review exclusions used for overlap resolution separately from real tissue cuts.'
 if k=='Krubitzer_2009/fig07_macaque':
  a.update(grade='C',fit='mostly_close_with_annotation_artifacts',notes='Enlarged source shows mostly close field envelopes but letter-shaped contour detours in crowded MIP/VIP/auditory labels. This is a comparative summary drawing, not an independent macaque specimen.',improvement='Resolve label-obscured short edges against the source stroke and original cited maps; preserve field adjacency. Avoid copying contours from a different summary or treating its scale as independent calibration.')
 if k.startswith('Krubitzer_Kaas_1990/') and k.split('/')[1] in ['fig'+str(i) for i in range(12,25)]:
  a['notes']+=' Final tissue-clipped filled overlays were also inspected; protruding construction polygons are not measured outside the tissue mask.'
 if k=='Felleman_VanEssen_1991/fig02':a['notes']+=' Enlarged inspection supports generally close envelopes; composite and historical calibration limitations remain separate from line fit.'
 # Do not append the same enlargement note on a rerun.
 for field in ['notes']:
  for phrase in [' Enlarged review confirms',' Enlarged review:',' Final tissue-clipped',' Enlarged inspection supports']:
   if a[field].count(phrase)>1:
    first=a[field].index(phrase);second=a[field].index(phrase,first+1);a[field]=a[field][:second]
(OUT/'assessments.json').write_text(json.dumps(ass,indent=2)+'\n')

area_changes=[];validation=[]
for paper in sorted({c['paper'] for c in changes}):
 z=zipfile.ZipFile(OUT/'before'/f'{paper}.zip')
 old={(r['map_id'],r['label']):r for r in csv.DictReader(io.StringIO(z.read('data/measurements.csv').decode()))}
 new={(r['map_id'],r['label']):r for r in csv.DictReader((FM/paper/'data/measurements.csv').open())}
 expected={(c['map_id'],c['label']) for c in changes if c['paper']==paper}
 actual={k for k in old if old[k]['area_px2']!=new[k]['area_px2']}
 assert actual==expected,(paper,actual,expected)
 for k in old:
  for field in ['scale_length_px','scale_length_mm','specimen','hemisphere','view_type','extent']:
   assert old[k].get(field)==new[k].get(field),(paper,k,field)
 for c in [c for c in changes if c['paper']==paper]:
  k=(c['map_id'],c['label']);b=old[k];a=new[k];change=100*(float(a['area_px2'])/float(b['area_px2'])-1)
  area_changes.append(dict(paper_id=paper,map_id=k[0],label=k[1],before_area_px2=b['area_px2'],after_area_px2=a['area_px2'],before_area_mm2=b['area_mm2'],after_area_mm2=a['area_mm2'],change_percent=round(change,6),extent=a['extent'],reason=c['note']))
  im=Image.open(FM/paper/'figures'/k[0]/'source.tif').convert('RGB');before=im.copy();after=im.copy()
  for image,polys in [(before,c['old_polygons']),(after,c['polygons'])]:
   draw=ImageDraw.Draw(image)
   for p in polys:draw.line([tuple(x) for x in p]+[tuple(p[0])],fill='#00a3cc',width=max(1,round(im.width/700)))
  pane_w=650;pane_h=round(im.height*pane_w/im.width);sheet=Image.new('RGB',(pane_w*3,pane_h+45),'white');dr=ImageDraw.Draw(sheet)
  for i,(name,image) in enumerate([('Source',im),('Before',before),('After',after)]):
   sheet.paste(image.resize((pane_w,pane_h)),(i*pane_w,45));dr.text((i*pane_w+12,12),name+' — '+k[1],fill='black')
  stem=paper+'__'+k[0]+'__'+k[1].replace(' ','_');sheet.save(comparisons/(stem+'.png'))
  c['comparison_path']='before_after/'+stem+'.png';c['change_percent']=change
 validation.append(dict(paper_id=paper,changed_ROIs=len(expected),unaffected_areas_identical=True,calibration_and_identity_preserved=True,native_imagej_roundtrip=json.loads((FM/paper/'documentation/validation.json').read_text())['native_imagej_roundtrip']))
writecsv(OUT/'area_changes.csv',area_changes)

rows=[];roi_rows=[]
for r in inv:
 paper,mid=r['paper_id'],r['map_id'];key=paper+'/'+mid;a=ass[key];f=FM/r['roi_path'];d=json.loads(f.read_text());row=dict(r)
 row.update({k:v for k,v in a.items() if k!='baseline_assessment'});row['baseline_roi_sha256']=r['source_roi_sha256'];row['current_roi_sha256']=hashlib.sha256(f.read_bytes()).hexdigest();row['changed_this_review']=(paper,mid) in changed
 row['review_scope']='view-level source/contour screening; selected enlargements; not independent certification of every region'
 row['measurement_scope']=str(d.get('view_type',''))+'; '+('physical calibration recorded' if r['has_calibration']=='True' else 'pixel only')+'; '+('eligible whole-neocortex denominator recorded' if d.get('include_in_whole_hemisphere_summary') else 'no eligible whole-neocortex denominator')
 if not row['changed_this_review']:assert row['current_roi_sha256']==row['baseline_roi_sha256'],key
 im=Image.open(FM/r['source_path']).convert('RGB');tr=im.copy();draw=ImageDraw.Draw(tr);regions=([d['outline']] if d.get('outline') else [])+d.get('rois',[])
 for reg in regions:
  for name,color in [('polygons','#009bbb'),('exclude_polygons','#d34b19')]:
   for p in reg.get(name,[]):
    if len(p)>2:draw.line([tuple(x) for x in p]+[tuple(p[0])],fill=color,width=max(1,round(max(im.size)/950)))
  roi_rows.append(dict(paper_id=paper,map_id=mid,label=reg['label'],view_grade=a['grade'],grade_basis='inherited view-level screening, not an individual-region certification',source_clarity=a['clarity'],contour_fit=a['fit'],extent=reg.get('extent','outline'),status=reg.get('status','provisional'),changed_this_review=any(c['paper']==paper and c['map_id']==mid and c['label']==reg['label'] for c in changes),boundary_note=reg.get('boundary_note',''),view_notes=a['notes'],improvement=a['improvement']))
 if paper=='Krubitzer_Kaas_1990' and 'whole_seeds' in d:tr=Image.open(f.parent/'tracing.png').convert('RGB')
 stem=paper+'__'+mid
 for name,img in [('source',im),('trace',tr)]:
  img.thumbnail((1200,1400));img.save(assets/(stem+'_'+name+'.jpg'),quality=92)
 row['source_preview']='views/'+stem+'_source.jpg';row['trace_preview']='views/'+stem+'_trace.jpg';rows.append(row)
writecsv(OUT/'view_review.csv',rows);writecsv(OUT/'roi_review.csv',roi_rows)
counts=Counter(r['grade'] for r in rows);papers=sorted({r['paper_id'] for r in rows})
summary=dict(active_datasets=len(papers),active_views=len(rows),traced_views=sum(int(r['ROI_count'])+int(r['outline_count'])>0 for r in rows),regional_ROIs=sum(int(r['ROI_count']) for r in rows),explicit_outlines=sum(int(r['outline_count']) for r in rows),grades=dict(counts),corrected_regions=len(changes),corrected_views=len(changed),corrected_papers=len(validation),rebuild_validation=validation,scope='Active canonical figures only. Historical revisions and archived alternatives excluded; Burman interior pilot is noncanonical and not a full-field estimate.')
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')

legend='A: clearest source/closest fit; B: usable drawing fit with caveats; C: unclear, displaced or requires targeted retracing; D: unsuitable for the intended anatomical area inference despite possible close image fit; N: no saved trace. These are screening categories, not a precision score or permission to pool observations.'
guide='''Use same-specimen panels first: verify case, hemisphere, crop, cuts and scale, then align several distributed anatomical landmarks. A second panel can disambiguate a hidden edge only if tissue identity and correspondence are established. Between animals, use field adjacency, sulcal relationships and expected shape as checks; never transplant a border or force all brains to one shape. Treat areal borders, sulci, flattening cuts, uncertainty bands, recording symbols and annotation leaders as separate features. Dashed and gray lines have paper-specific meanings, established from captions. For uncertain borders retain an inner/outer envelope or mark the field unmeasurable; do not count an interior-only mask as a complete area. Atlas registration may guide review, but predicted sulci and inferred borders must remain explicitly inferred and separate from observed measurements.'''
readme=f'''# Project tracing review — 31 October 2026

[Open the filterable review](index.html) · [Every view](view_review.csv) · [Region index](roi_review.csv) · [Area changes](area_changes.csv)

Reviewed {len(rows)} active views across {len(papers)} datasets: {summary['traced_views']} traced views containing {summary['regional_ROIs']} regional ROIs, plus {summary['explicit_outlines']} explicit outlines; {counts['N']} source-only views. All were inspected at contact-sheet scale, with enlargements for problem cases and dense maps. This is a view-level screening pass, not individual anatomical certification of every ROI. Archived revisions are excluded. The separate Burman interior pilot is not a whole-field tracing.

{legend}

Current counts: {', '.join(f'{k} = {counts[k]}' for k in ['A','B','C','D','N'])}. Use the review filters to find specific views, notes and proposed improvements. Region rows inherit the view grade and say so explicitly.

## Applied corrections

Nine regional contours in eight views across four datasets were changed. Beck 1996: PV in Fig10A/10B and S2 in Fig7A. Frost 2000: the three closed Fig4 distal-forelimb envelopes, preserving the case9213 arm exclusion. Manger 2002 Fig6right: restored the ventral-trunk compartment inside the partial PPr envelope. Krubitzer 1998 Fig11B: Vc/Vr now include both upper/lower visual-field compartments instead of following internal retinotopy lines.

Prior complete dataset files are in `before/*.zip` (excluding nested historical archives). Canonical polygons, native ImageJ selections/masks, tracing previews, measurements and affected summaries were rebuilt. Native ImageJ read-back passed for all four datasets. Other area values, scales, identity metadata and extent classifications were checked against the archives and preserved. The new-batch combined tables were refreshed. These technical checks do not establish anatomical validity.

The largest change is illustrative Vc in Krubitzer Fig11B (+49.29% pixels); Vr changes +8.47%. These remain pixel-only illustrative geometry. Manger partial PPr changes +5.85%. Other revised regions change between −4.29% and +1.64%. Beck Fig10A changes only +0.08%, demonstrating that a similar area can conceal a different boundary shape. No scale was fitted to a published number.

## Best examples and priorities

Catania & Remple Fig2 case4, many Beck 1996 local sensory envelopes, and selected Huffman 1999 maps are among the clearest source-to-trace examples (filter A for the exact maps). A good silhouette fit does not turn a summary into an independent animal.

Burman's 24 ROIs remain rejected pending anatomical retracing; the gray bands, dashed estimates, sulcal lines and flattening cuts need separate treatment. Brecht remains flagged as schematic, with unresolved metric calibration. Other priority groups include Remple's coarse subregions, Ghosh's exposed/bank boundaries, Hinds' symbol-obscured V1 edges, Rosa's crowded parietal/MT complexes and selected thin-line maps. Every C view has a specific improvement note. Source ambiguity is not repaired by making the curve smoother.

## Atlases, guides and information from other images

{guide}

The project's [atlas and tracing guide](../ReadMe.md#atlases-and-tracing-guides) links the Marmoset Brain Connectivity Atlas, Nencki–Monash template, published marmoset parcellation guides and surface-registration documentation. For Burman, use these for regional identity, fingerlike extensions and sulcal plausibility, then return to the individual printed map. No atlas-derived coordinates or borrowed scales were applied in this pass. For Rosa, Figures3C/11 help label adjacency but cannot replace a case-specific boundary. For Luethke1989, the repeated same-case panels can clarify line identity after registration.

## Reproducibility

`inventory.csv` and `sheets/` preserve the pre-correction inventory and contact sheets. `assessments.json` stores screening judgments; changed views also retain their earlier assessment. `view_review.csv` includes baseline/current ROI hashes. `area_changes.csv` records all numerical changes. `before_after/` shows source, old contour and new contour. `scripts/refine_contours.py` documents source-coordinate decisions; its apply mode refuses to overwrite an existing baseline archive. Run `scripts/build_review_report.py` to refresh this report after a deliberate review. Do not regenerate the baseline inventory over the saved before state.
'''
(OUT/'README.md').write_text(readme)

style='''body{font:16px system-ui;max-width:1500px;margin:32px auto;padding:0 24px;color:#18332f;background:#f5f7f6}a{color:#006c80}h1{font-size:32px}p{max-width:1100px;line-height:1.5}.bar{position:sticky;top:0;background:#e5ede8;padding:14px;z-index:2;display:flex;gap:12px;flex-wrap:wrap}input,select{font:inherit;padding:8px}input{min-width:330px}.badge{padding:4px 10px;border-radius:5px;background:#dde9e2}.C,.D{background:#ffdfb3}.A{background:#c8ecd5}details{background:white;border:1px solid #cbd8d0;margin:12px 0;padding:15px}summary{cursor:pointer;font-weight:650}.images{display:grid;grid-template-columns:1fr 1fr;gap:12px}.images img{width:100%;height:auto}.change img{width:100%;height:auto}small{color:#52655c}.note{padding:16px;background:#fff1d4}table{border-collapse:collapse}td,th{border:1px solid #cbd8d0;padding:8px;text-align:left}button{font:inherit;padding:8px}#count{align-self:center}'''
parts=[f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Project tracing review</title><style>{style}</style><h1>Project tracing review</h1><p><b>{len(rows)} views · {len(papers)} datasets · {summary["regional_ROIs"]:,} regional ROIs</b><br>31 October 2026 — whole-project screening with selected enlarged reviews. Nine regional corrections applied; originals archived.</p><p class="note">{E(legend)}</p><p>Grades describe this review, not biological precision. All 448 views were screened; individual certification of every field remains outstanding. Source-only views and partial/schematic maps are explicitly retained in the inventory.</p><p><a href="README.md">Methods and findings</a> · <a href="view_review.csv">View review CSV</a> · <a href="roi_review.csv">Region index CSV</a> · <a href="area_changes.csv">Area changes CSV</a> · <a href="#corrections">Before/after corrections</a></p><p><b>Current categories:</b> '+E(', '.join(k+': '+str(counts[k]) for k in ['A','B','C','D','N']))+'</p>']
parts.append('<details><summary>How other maps and atlases can help</summary><p>'+E(guide)+'</p><p><a href="../ReadMe.md">Project atlases and guides</a>. No atlas coordinates or borrowed calibration were applied.</p></details>')
parts.append('<div class="bar"><input id="search" aria-label="Search" placeholder="Search paper, species, case, region or note"><select id="grade" aria-label="Review category"><option value="">All categories</option>'+''.join(f'<option>{k}</option>' for k in ['A','B','C','D','N'])+'<option value="changed">Corrected this review</option></select><select id="paper" aria-label="Dataset"><option value="">All datasets</option>'+''.join('<option>'+E(p)+'</option>' for p in papers)+'</select><span id="count"></span></div><main id="views">')
for r in rows:
 paper,mid=r['paper_id'],r['map_id'];key=paper+'/'+mid;folder='../'+paper+'/figures/'+mid
 search=' '.join(str(r.get(k,'')) for k in ['paper_id','map_id','species','specimen','labels','notes','improvement']).lower()
 parts.append(f'<details class="view" data-grade="{r["grade"]}" data-paper="{E(paper)}" data-changed="{str(r["changed_this_review"]).lower()}" data-search="{E(search,quote=True)}"><summary><span class="badge {r["grade"]}">{r["grade"]}</span> {E(key)}'+(' · corrected' if r['changed_this_review'] else '')+f' · {r["ROI_count"]} regions</summary><p>{E(r["species"])} · {E(r["specimen"])}<br>{E(r["measurement_scope"])}</p><p><b>Clarity:</b> {E(r["clarity"])} · <b>Fit:</b> {E(r["fit"])}</p><p>{E(r["notes"])}</p><p><b>Improvement:</b> {E(r["improvement"])}</p><p><small>Labels: {E(r["labels"])}</small></p><div class="images"><div>Source<a href="{folder}/source.tif"><img loading="lazy" src="{r["source_preview"]}" alt="Source {E(mid)}"></a></div><div>Current tracing<a href="{folder}/tracing.png"><img loading="lazy" src="{r["trace_preview"]}" alt="Current tracing {E(mid)}"></a></div></div><p><a href="{folder}/rois.json">Canonical geometry</a> · <a href="../{paper}/review/gallery.html">Paper gallery</a> · <a href="{r["sheet"]}">Baseline contact sheet</a></p></details>')
parts.append('</main><section id="corrections"><h2>Applied corrections</h2><p>Cyan shows the regional contour. Scale and field identity are unchanged. Click each comparison to enlarge.</p>')
for c in changes:
 parts.append(f'<article class="change"><h3>{E(c["paper"]+" / "+c["map_id"]+" / "+c["label"])}</h3><p><b>Area change {c["change_percent"]:+.2f}%</b>. {E(c["note"])}</p><a href="{c["comparison_path"]}"><img loading="lazy" src="{c["comparison_path"]}" alt="Source, old contour, revised contour"></a></article>')
parts.append('''</section><script>
const search=document.getElementById('search'),grade=document.getElementById('grade'),paper=document.getElementById('paper');
const cards=[...document.querySelectorAll('.view')];
function filter(){const q=search.value.toLowerCase().trim();let n=0;for(const c of cards){const show=(!q||c.dataset.search.includes(q))&&(!paper.value||paper.value===c.dataset.paper)&&(!grade.value||(grade.value==='changed'?c.dataset.changed==='true':grade.value===c.dataset.grade));c.hidden=!show;if(show)n++;}document.getElementById('count').textContent=n+' / '+cards.length+' views';}
for(const el of [search,grade,paper])el.addEventListener('input',filter);
paper.value=new URLSearchParams(location.search).get('paper')||'';filter();
</script></html>''')
(OUT/'index.html').write_text(''.join(parts))

marker='<!-- project-tracing-review-2026-10-31 -->'
for paper in papers:
 candidates=[FM/paper/'README.md',FM/paper/'ReadMe.md'];p=next((p for p in candidates if p.exists()),candidates[0]);previous=p.read_text() if p.exists() else '# '+paper+'\n';previous=previous.split(marker)[0].rstrip()
 c=Counter(r['grade'] for r in rows if r['paper_id']==paper)
 section=f'''\n\n{marker}
## Project-wide tracing review, 31 October 2026

[View this dataset's quality review](../project_review_2026-10-31/index.html?paper={paper}) · [Review methods and changes](../project_review_2026-10-31/README.md)

View-level screening categories: {', '.join(k+'='+str(c[k]) for k in ['A','B','C','D','N'] if c[k])}. A identifies the clearest source/fit examples; B retains caveats; C needs targeted review/retracing; D is unsuitable for the intended anatomical area inference; N has no saved trace. These are not individual-region certification or independent-specimen counts. See the linked report for each map's notes and proposed improvements.

Atlases and guides: see the [project guide](../ReadMe.md). Use same-specimen panels to resolve obscured lines where correspondence is established; use other specimens and atlases for field identity, adjacency and sulcal plausibility only. They do not supply an observed border, justify copying a shape, or establish a missing physical scale.
'''
 p.write_text(previous+section)
for p,rel in [(FM/'ReadMe.md','project_review_2026-10-31/'),(FM.parent/'README.md','flatmap_measurements/project_review_2026-10-31/')]:
 previous=p.read_text().split(marker)[0].rstrip();p.write_text(previous+f'\n\n{marker}\n## Project-wide tracing review, 31 October 2026\n\n[Open the filterable review]({rel}index.html) · [Findings, atlas guidance and corrections]({rel}README.md) · [All area changes]({rel}area_changes.csv)\n\n448 active views were screened. Nine regional contours in four papers were corrected and rebuilt with prior versions archived. View grades separate clear examples, caveats, retracing priorities and unsuitable inferences; they do not certify every regional boundary.\n')
print(json.dumps(summary,indent=2))
