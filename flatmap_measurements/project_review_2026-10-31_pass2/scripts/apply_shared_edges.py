from prepare_precision import *
from copy import deepcopy
changes=json.loads((OUT/'applied_changes.json').read_text());extra=json.loads((OUT/'shared_edge_candidates.json').read_text())
for c in extra:
 assert not any((x['paper'],x['map_id'],x['label'])==(c['paper'],c['map_id'],c['label']) for x in changes)
 f=FM/c['paper']/'figures'/c['map_id']/'rois.json';d=json.loads(f.read_text());old=next(r for r in d['rois'] if r['label']==c['label']);assert old==c['old']
 new=deepcopy(c['new']);new['boundary_note']=new.get('boundary_note','')+' Second project review 2026-10-31: '+c['note'];new['tracing_method']='Source-reviewed shared-edge correction, second project pass, 2026-10-31';new['geometry_review']=dict(date='2026-10-31',pass_number=2,status='source_refined_provisional',note=c['note']);c['applied_new']=new
 d['rois'][d['rois'].index(old)]=new;f.write_text(json.dumps(d,indent=2)+'\n');changes.append(c)
(OUT/'applied_changes.json').write_text(json.dumps(changes,indent=2)+'\n');print(len(changes),'changes')
