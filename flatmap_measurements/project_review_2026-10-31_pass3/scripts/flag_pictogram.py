from pass3_helpers import *
paper='Krubitzer_Dooley_2013';mid='fig07D_naked_mole_rat';root=FM/paper
archive(paper)
f=root/'figures'/mid/'rois.json';d=get(paper,mid);r=next(r for r in d['rois'] if r['label']=='S1_other_body')
if r.get('status')!='pictorial_footprint_not_anatomical_area':
 before=copy.deepcopy(r)
 r.update(extent='pictorial_footprint',status='pictorial_footprint_not_anatomical_area',analysis_eligible=False,boundary_note='Enlarged source recheck 2026-10-31: this silhouette follows the hand/body pictogram superimposed on S1, including finger edges. The source supplies no independent anatomical perimeter here. Retained only as a published drawing footprint for audit; not a valid S1 field area. No anatomical contour was invented by smoothing the pictogram.')
 d['precision_review_pass3']='../../documentation/pass3_tracing_review.md';f.write_text(json.dumps(d,indent=2)+'\n')
 events=json.loads((OUT/'applied_changes.json').read_text());events.append(dict(paper_id=paper,map_id=mid,label=r['label'],before=before,after=copy.deepcopy(r),reason=r['boundary_note'],status='applied_metadata_only_geometry_unchanged'));(OUT/'applied_changes.json').write_text(json.dumps(events,indent=2)+'\n')
script=root/'scripts/measure_flatmaps.py';s=script.read_text();s=s.replace("status='provisional; anatomical review required', boundary_note=region.get('boundary_note')", "status=region.get('status','provisional; anatomical review required'), boundary_note=region.get('boundary_note')");script.write_text(s)
