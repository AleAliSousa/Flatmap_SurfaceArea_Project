from pass3_helpers import *
checks=json.loads((OUT/'candidate_geometry_validation.json').read_text());assert not any(x['violations'] for x in checks)
log=OUT/'applied_changes.json';applied=json.loads(log.read_text()) if log.exists() else [];known={(d['paper_id'],d['map_id'],d['label']) for d in applied}
for f in sorted((OUT/'candidates').glob('*.json')):
 e=json.loads(f.read_text())
 if 'after' not in e:continue
 key=(e['paper_id'],e['map_id'],e['label'])
 if key in known:continue
 archive(e['paper_id']);p=FM/e['paper_id']/'figures'/e['map_id']/'rois.json';d=json.loads(p.read_text());old=next((r for r in d['rois'] if r['label']==e['label']),None);assert old==e['before'],key
 if old:d['rois'][d['rois'].index(old)]=e['after']
 else:d['rois'].append(e['after'])
 d['unmeasured']=[r for r in d.get('unmeasured',[]) if r['label']!=e['label']]
 d['precision_review_pass3']='Source and before/after inspected; see ../../documentation/pass3_tracing_review.md. Native file verification separate from anatomical accuracy.'
 if e['paper_id']=='Burman_etal_2008':d['review_note']='Seven CJ58R fields retraced/added using approximate gray-band centers in pass3; these remain provisional pixel-only estimates excluded from analysis. Other existing fields remain rejected pending retracing.'
 p.write_text(json.dumps(d,indent=2)+'\n');e['status']='applied_after_visual_review';applied.append(e);log.write_text(json.dumps(applied,indent=2)+'\n')
print(len(applied),'applied changes')
