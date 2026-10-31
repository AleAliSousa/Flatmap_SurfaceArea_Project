from prepare_precision import *
from copy import deepcopy
CH=[]
def pts(s):return [list(map(float,p.split(','))) for p in s.split()]
def add(paper,mid,label,polygons,note,extent=None,new=False):
 d=json.loads((FM/paper/'figures'/mid/'rois.json').read_text());old=next((r for r in d['rois'] if r['label']==label),None)
 assert new == (old is None),(paper,mid,label)
 r=deepcopy(old) if old else dict(label=label,extent=extent,polygons=[])
 r['polygons']=polygons
 if extent:r['extent']=extent
 name=paper+'__'+mid+'__'+str(len(CH))+'_final'
 preview(paper,mid,old or dict(polygons=[]),r,name)
 CH.append(dict(paper=paper,map_id=mid,label=label,old=old,new=r,note=note,kind='addition' if new else 'revision',image=name+'.jpg'))
def candidate(paper,mid,idx):
 c=next(x for x in json.loads((OUT/(paper+'_candidates.json')).read_text()) if x['map_id']==mid and x['index']==idx)
 add(paper,mid,c['label'],c['polygons'],'Enlarged source/old/candidate comparison: follows the printed compartment perimeter more closely, retaining internal lettering and symbols. White-component extraction, short pixel-gap closing where used, half-pixel coordinate correction, 0.5-pixel simplification. Native print resolution still limits precision.')
for mid,inds in {'fig09_case1_motor_fields':[1,2,7], 'fig10_case2_motor_fields':[7], 'fig14_case6':[0,1,2,3,4,5,6,7,8,9,12], 'fig15_case9':[0,1,2,4,5,6,7], 'fig16AB_case7':[1,2,3,5,6,7,8], 'fig16CD_case8':[0,2,4,5,7,8]}.items():
 for i in inds:candidate('Ghosh_1997',mid,i)
for mid,inds in {'fig07A_320_sensory':[2,5],'fig07B_320_S1_subregions':[5,6],'fig08A_310R_S1':[3,4],'fig08C_320L_S1':[3]}.items():
 for i in inds:candidate('Remple_etal_2006',mid,i)
def seeded(paper,mid,label,seed,extent='surface_component',threshold=190):
 a=labels(paper,mid,threshold);cid=a[seed[1],seed[0]];assert cid>0
 mask=a==cid;assert mask.sum()<a.size*.3
 poly=mask_outline(mask,paper+'__'+mid+'__new_'+label,expand=1,close=2)
 add(paper,mid,label,[poly],'Previously omitted, source-labelled closed compartment. Identified by comparison with adjacent panels/cases in the same paper; perimeter extracted from this panel only. Internal labels and tracer dots retained. This is a component, not a whole-region or whole-hemisphere total.',extent,new=True)
# Closed medial components above the exposed-surface/bank division; same labels as adjacent cases.
for mid,items in {'fig14_case6':[('3a_medial_component',(280,170)),('3b_medial_component',(330,200)),('area1_medial_component',(365,220))], 'fig15_case9':[('3a_medial_component',(320,250)),('3b_medial_component',(350,295)),('area1_medial_component',(350,345)),('3a_coronal_bank',(1030,1240)),('3b_coronal_bank',(1120,1240)),('area1_coronal_bank',(1220,930)),('area2_coronal_bank',(1210,1100))]}.items():
 for label,seed in items:seeded('Ghosh_1997',mid,label,seed,'sulcal_component' if 'bank' in label else 'surface_component')
# Direct manual source tracing; insets distinguish the internal folds from areal limits.
add('Burman_etal_2008','fig09A_CJ58R_flatmap','V1',[pts('258,486 270,484 282,485 296,489 310,495 329,505 350,520 370,537 390,555 410,574 427,594 437,612 442,625 443,637 439,649 432,660 417,675 401,690 382,702 365,714 343,725 320,737 297,748 276,757 258,763 246,764 228,763 211,760 194,756 173,752 150,749 128,747 106,744 86,742 69,738 57,733 49,725 43,715 36,702 31,685 28,668 26,650 25,632 25,614 26,596 30,580 37,565 46,554 58,545 74,536 92,529 111,523 132,518 154,515 176,512 194,507 215,501 237,493')], 'Fig.9 anatomical inset identifies both V1ca and V1op in the detached occipital lobe. Restored the entire drawn V1 lobe; continuous internal fold lines no longer split V1 or assign its opercular portion to V2. Other marmoset maps used only as topology guides. Pixel-only; no scale borrowed.')
d=json.loads((FM/'Burman_etal_2008/figures/fig09A_CJ58R_flatmap/rois.json').read_text());r=next(r for r in d['rois'] if r['label']=='V2')
add('Burman_etal_2008','fig09A_CJ58R_flatmap','V2',[r['polygons'][2]],'Removed two components that actually belong to the V1 lobe (Fig.9 inset: V1ca/V1op). Retained only the existing main-map V2 strip; its ventral continuation is unresolved, so this is explicitly partial and excluded from whole-field comparisons.','partial')
add('Beck_Kaas_1998','fig09','DM visible fragment',[pts('26,90 28,83 34,76 42,69 52,61 65,54 78,47 91,40 104,34 118,28 132,24 148,20 164,17 181,14 198,12 212,11 226,10 218,25 208,44 198,65 187,86 177,107 167,130 156,152 146,177 135,201 123,227 109,252 95,277 81,302 66,335 63,317 61,299 60,279 57,258 54,237 50,217 45,197 40,178 36,160 31,142 28,126 25,110 24,99')],'Manually retraced at enlargement across annotation interruptions; removed glyph-shaped detours and followed the visible gray DM perimeter. Fig.10 is a same-species topology guide only. The source itself describes uncertain borders; retain provisional interpretation.')
add('Krubitzer_2009','fig07_macaque','M/POd',[pts('1045,612 1023,609 1003,608 981,607 966,609 955,615 949,622 946,632 946,642 950,654 957,665 968,677 984,689 990,679 999,671 1012,665 1028,663 1042,663 1062,666 1057,647 1051,625 1048,612')],'Replaced a tiny contour around a letter in the M/POd label with the actual source field envelope between PIP, V3d and V2. Short upper-right print gap bridged along the printed continuation. Krubitzer & Dooley 2013 macaque map used for topological orientation only; parcellations are not assumed identical.')
# The squirrel M field is an independently visible filled silhouette, separate from SI.
add('Krubitzer_1998','fig14D_summary','M',[pts('605,228 618,245 634,265 653,285 673,306 691,327 703,345 710,360 709,374 703,386 695,392 676,396 650,397 624,397 600,398 607,384 608,365 606,345 605,326 603,305 602,285 603,264 603,244')],'Recovered the clearly bounded black M silhouette. Luethke et al. 1988 squirrel case maps corroborate the M/SI arrangement; no geometry or scale transferred. Comparative illustration only, not a new animal or whole cortical denominator.','complete',new=True)
# Save proposed changes separately; applying is an explicit final script option after visual review.
(OUT/'proposed_changes.json').write_text(json.dumps(CH,indent=2)+'\n')
print('Prepared',len(CH),'changes;',sum(x['kind']=='addition' for x in CH),'new fields')
