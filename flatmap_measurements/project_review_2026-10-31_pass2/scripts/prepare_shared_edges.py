from prepare_precision import *
from copy import deepcopy
jobs=[('Ghosh_1997','fig09_case1_motor_fields','4gamma_dorsolateral_component','3a_dorsolateral_component'),('Ghosh_1997','fig09_case1_motor_fields','6aalpha_rostral_cruciate_bank','4gamma_rostral_cruciate_bank'),('Ghosh_1997','fig16AB_case7','4gamma_caudal_cruciate_bank','4delta_caudal_cruciate_bank'),('Ghosh_1997','fig16CD_case8','4sfu_caudal_cruciate_bank','4delta_caudal_cruciate_bank')]
out=[]
for i,(paper,mid,label,neighbor) in enumerate(jobs):
 d=json.loads((FM/paper/'figures'/mid/'rois.json').read_text());old=next(r for r in d['rois'] if r['label']==label);other=next(r for r in d['rois'] if r['label']==neighbor);name='shared_edge_'+str(i);inp=OUT/'candidates'/(name+'.txt');dest=inp.with_suffix('.json')
 def serial(ps):return str(len(ps))+'\n'+'\n'.join(str(len(p))+'\n'+'\n'.join(str(x)+' '+str(y) for x,y in p) for p in ps)+'\n'
 inp.write_text(serial(old['polygons'])+serial(other['polygons']));subprocess.run([JAVA,str(OUT/'scripts/PolygonDifference.java'),str(inp),str(dest)],check=True)
 new=deepcopy(old);new['polygons']=json.loads(dest.read_text());assert len(new['polygons'])==len(old['polygons']),name
 preview(paper,mid,old,new,name)
 out.append(dict(paper=paper,map_id=mid,label=label,old=old,new=new,kind='revision',image=name+'.jpg',note='Aligned the encroaching shared edge with the source-refined '+neighbor+' border. Exact polygon difference removes the overlap on this shared edge; all remaining original vertices are preserved. This is a border correction, not a tissue exclusion or a new field.'))
(OUT/'shared_edge_candidates.json').write_text(json.dumps(out,indent=2)+'\n')
