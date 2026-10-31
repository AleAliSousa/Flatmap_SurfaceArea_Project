from prepare_precision import *
ch=json.loads((OUT/'proposed_changes.json').read_text())
c=next(c for c in ch if c['paper']=='Remple_etal_2006' and c['map_id']=='fig07A_320_sensory' and c['label']=='S1_3b')
cand=next(x for x in json.loads((OUT/'Remple_etal_2006_candidates.json').read_text()) if x['map_id']==c['map_id'] and x['index']==3)
im=Image.open(FM/c['paper']/'figures'/c['map_id']/'source.tif');p=np.vstack(c['old']['polygons']+cand['polygons']);lo=np.maximum(0,np.floor(p.min(axis=0)-20));hi=np.minimum(im.size,np.ceil(p.max(axis=0)+21));w,h=hi-lo;ratio=min(420/w,700/h);off=(430-round(w*ratio))//2
# Replace only the medial-wall chord of the inspected boundary-following candidate.
cap=np.array([[76,123],[76,114],[83,108],[94,107],[107,111],[121,116],[139,121],[154,130],[168,145],[184,160]],float)
cap=(cap-np.array([off,70]))/ratio+lo
poly=np.array(cand['polygons'][0]);c['new']['polygons']=[np.vstack([poly[:177],cap[::-1],poly[207:]]).tolist()]
c['note']='Followed the printed outer 3b contour with source-image boundary extraction, then manually replaced the medial-wall chord with the visible medial cap. The medial-wall fold line is internal, not an areal border. Fig.7B and same-case Fig.11 supply identity/topology checks only; no geometry transferred.'
preview(c['paper'],c['map_id'],c['old'],c['new'],Path(c['image']).stem)
(OUT/'proposed_changes.json').write_text(json.dumps(ch,indent=2)+'\n')
