from prepare_precision import *
from copy import deepcopy
ch=json.loads((OUT/'proposed_changes.json').read_text())
# Make extent of the two bank subdivisions explicit: fundus is a component boundary here, not an areal boundary.
for c in ch:
 if c['paper']=='Ghosh_1997' and c['kind']=='addition' and c['label'] in ['3a_coronal_bank','3b_coronal_bank']:
  c['label']=c['label'].replace('_coronal_bank','_ventral_coronal_bank');c['new']['label']=c['label'];c['new']['extent']='sulcal_component';c['note']+=' This ROI is the ventral-bank component below fSCor only. The fundus is not an areal limit; the dorsal-bank component is not included.'
 if c['paper']=='Beck_Kaas_1998':
  p=c['new']['polygons'][0]
  for q in p:
   if q[0]>110 and q[1]<180:q[0]-=max(0,6*(180-q[1])/170)
 if c['paper']=='Krubitzer_1998':
  im=Image.open(FM/c['paper']/'figures'/c['map_id']/'source.tif').convert('L');guide=Image.fromarray(mask_region(c['new'],im.size).astype('uint8')*255).filter(ImageFilter.MaxFilter(13));mask=(np.asarray(im)<90)&(np.asarray(guide)>0)
  # A bounded filled silhouette: retain the white M lettering inside the field.
  from prepare_candidates import largest
  mask=largest(mask);mask=~flood(~np.pad(mask,1),(0,0))[1:-1,1:-1]
  mask=np.asarray(Image.fromarray(mask.astype('uint8')*255).filter(ImageFilter.MinFilter(3)))>0
  c['new']['polygons']=[mask_outline(mask,'squirrel_M_refined',expand=0,close=1)]
# Manual source-column coordinates from the inspected enlarged Remple preview; explicitly include medial cap.
paper='Remple_etal_2006';mid='fig07A_320_sensory';idx=3
cand=next(x for x in json.loads((OUT/(paper+'_candidates.json')).read_text()) if x['map_id']==mid and x['index']==idx)
d=json.loads((FM/paper/'figures'/mid/'rois.json').read_text());old=d['rois'][idx];im=Image.open(FM/paper/'figures'/mid/'source.tif');p=np.vstack(old['polygons']+cand['polygons']);lo=np.maximum(0,np.floor(p.min(axis=0)-20));hi=np.minimum(im.size,np.ceil(p.max(axis=0)+21));w,h=hi-lo;ratio=min(420/w,700/h);off=(430-round(w*ratio))//2
coords='76,123 76,114 83,108 94,107 107,111 121,116 139,121 154,130 168,145 184,160 195,193 205,229 214,266 220,301 231,346 244,389 248,422 248,458 250,485 259,517 274,541 293,563 316,590 337,614 349,635 351,650 347,670 340,691 330,711 320,724 309,729 298,727 286,720 274,710 254,688 234,663 214,635 195,609 175,579 155,548 138,520 127,501 127,484 134,462 145,440 154,418 159,397 157,377 150,345 146,315 141,282 135,248 125,214 110,185 94,160 83,141'
poly=[[(float(x)-off)/ratio+lo[0],(float(y)-70)/ratio+lo[1]] for x,y in (v.split(',') for v in coords.split())];new=deepcopy(old);new['polygons']=[poly]
ch.append(dict(paper=paper,map_id=mid,label=old['label'],old=old,new=new,note='Manually followed the enlarged complete printed 3b contour, including its medial cap. Medial-wall fold line treated as internal, not an areal border. Fig.7B and the same-case Fig.11 supply identity/topology checks only; no geometry transferred.',kind='revision',image='Remple_S1_manual_final.jpg'))
for c in ch:preview(c['paper'],c['map_id'],c['old'] or dict(polygons=[]),c['new'],Path(c['image']).stem)
(OUT/'proposed_changes.json').write_text(json.dumps(ch,indent=2)+'\n')
print(len(ch),'proposed')
