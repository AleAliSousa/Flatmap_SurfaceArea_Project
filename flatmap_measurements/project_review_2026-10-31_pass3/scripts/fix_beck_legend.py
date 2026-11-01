from pass3_helpers import *
p='Beck_Kaas_1998';m='fig11';root=FM/p;out=root/'review/dm_recheck_2026-10-31';d=get(p,m);r=d['rois'][0];old=copy.deepcopy(r);poly=r['polygons'][0]
if len(poly)!=176:raise SystemExit('Already applied or changed geometry')
seg=curve([poly[103],[256,520],[242,507],[225,493],poly[116]],step=1)
r['polygons']=[poly[:103]+seg+poly[117:]];r['interpolated_border_segments'][1]=[q for q in seg if 490<=q[1]<=521]
r['boundary_note']='Partial DM contour: upper border cut by the figure frame. Follow-up recheck: removed letter-shaped detours around the lower Diamidino Yellow legend by a smooth continuation between visible line segments; legend-hidden y352–448 and y490–521 intervals are inferred and marked orange, as is the upper frame closure. The rest of the geometry and local scale are retained. This remains partial and is excluded from complete-field summaries.'
preview(p,m,old,r,'Beck_Kaas_1998__fig11__legend')
(OUT/'candidates'/'beck_legend_definition.json').write_text(json.dumps(d,indent=2)+'\n')
