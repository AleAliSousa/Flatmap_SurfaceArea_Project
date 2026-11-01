from pass3_helpers import *
p='Beck_Kaas_1998';out=FM/p/'review/dm_recheck_2026-10-31';dst=out/'followup_recheck.json'
if dst.exists():raise SystemExit('Already applied')
archive(p);events=[];olddefs={}
for m in ['fig03','fig09','fig11']:olddefs[m]=get(p,m)
d=copy.deepcopy(olddefs['fig03']);r=d['rois'][0];poly=r['polygons'][0];a=np.array(poly[58]);b=np.array(poly[72]);delta=b[1]-a[1];seg=[]
for t in np.linspace(0,1,43):
 x=(2*t**3-3*t**2+1)*a[0]+(t**3-2*t**2+t)*(.02*delta)+(-2*t**3+3*t**2)*b[0]+(t**3-t**2)*(-.33*delta);seg.append([round(x,4),round(a[1]+t*delta,4)])
r['polygons']=[poly[:58]+seg+poly[73:]];r['interpolated_border_segments']=[[q for q in seg if 106<=q[1]<=172]]
r['boundary_note']='Follow-up 31 October: residual right-border detours around the clustered injection ovals removed. A continuous DM/V2 arc is interpolated between visible source tangents above and below the cluster (roughly y106–172 in the original crop). Injection outlines are not anatomical borders. All other vertices and the local 4-mm calibration are retained. Complete denotes the published envelope with a locally obscured, provisional boundary.'
r['tracing_method']='Local cubic Hermite continuation across tracer occlusion; unchanged visible-boundary geometry elsewhere'
events.append(dict(paper_id=p,map_id='fig03',label='DM',before=olddefs['fig03']['rois'][0],after=copy.deepcopy(r),reason=r['boundary_note'],status='applied_after_visual_review'))
# Only stage until the before/after has been inspected.
(OUT/'candidates'/'Beck_Kaas_1998__fig03__DM.json').write_text(json.dumps(events[0],indent=2)+'\n');preview(p,'fig03',events[0]['before'],events[0]['after'],'Beck_Kaas_1998__fig03__DM')
(OUT/'candidates'/'beck_followup_definition.json').write_text(json.dumps(d,indent=2)+'\n')
