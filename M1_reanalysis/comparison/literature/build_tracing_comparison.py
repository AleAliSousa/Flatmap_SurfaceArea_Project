from pathlib import Path
import csv,html,openpyxl
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
FIELDS=['species','source','figure_case','record_type','S1_mm2','face_or_orofacial_mm2','V1_mm2','A1_mm2','cortical_outline_mm2','face_percent_S1','S1_percent_outline','definition_note','calibration_note','source_csv','source_ROIs']
def blank(**kw):return {k:kw.get(k,'') for k in FIELDS}
def data(p,m):return {r['label']:r for r in csv.DictReader((ROOT/'flatmap_measurements'/p/'data/measurements.csv').open()) if r['map_id']==m}
def val(d,k):
 try:return float(d[k]['area_mm2'])
 except (KeyError,ValueError):return ''
def roi(p,m):return 'flatmap_measurements/'+p+'/figures/'+m+'/rois.json'
def tracing(p,m,species,source,case,labels,note):
 d=data(p,m);r=blank(species=species,source=source,figure_case=case,record_type='existing flatmap tracing',definition_note=note,calibration_note=next(iter(d.values()))['scale_note'],source_csv='flatmap_measurements/'+p+'/data/measurements.csv',source_ROIs=roi(p,m))
 for col,lab in labels.items():r[col]=val(d,lab)
 if isinstance(r['S1_mm2'],float) and isinstance(r['face_or_orofacial_mm2'],float):r['face_percent_S1']=100*r['face_or_orofacial_mm2']/r['S1_mm2']
 if isinstance(r['S1_mm2'],float) and isinstance(r['cortical_outline_mm2'],float):r['S1_percent_outline']=100*r['S1_mm2']/r['cortical_outline_mm2']
 return r
w=openpyxl.load_workbook(ROOT/'M1_reanalysis/M1 surface measurements for reanalysis.xlsx',data_only=True);wr={r[0]:r for r in list(w.active.values)[1:] if r[0] is not None}
rows=[]
for sp,sids in [('Homo sapiens',{'S1_mm2':61,'face_or_orofacial_mm2':62,'V1_mm2':57,'A1_mm2':60,'cortical_outline_mm2':63}),('Heterocephalus glaber',{'S1_mm2':69,'face_or_orofacial_mm2':70,'cortical_outline_mm2':71})]:
 r=blank(species=sp,source='Brecht & Freiwald 2012',figure_case='Fig 3a' if sp=='Homo sapiens' else 'Fig 3d',record_type='original workbook',definition_note='Schematic; workbook human S1/3b retains ambiguous field equivalence.',calibration_note='Original workbook calibration provenance unresolved; see review.')
 for k,sid in sids.items():r[k]=wr[sid][5]
 r['face_percent_S1']=100*r['face_or_orofacial_mm2']/r['S1_mm2'];r['S1_percent_outline']=100*r['S1_mm2']/r['cortical_outline_mm2'];rows.append(r)
for mp,sp,fig in [('fig03a_human','Homo sapiens','Fig 3a'),('fig03d_naked_mole_rat','Heterocephalus glaber','Fig 3d')]:
 rows.append(tracing('Brecht_Freiwald_2012',mp,sp,'Brecht & Freiwald 2012',fig,{'S1_mm2':'S1','face_or_orofacial_mm2':'S1_face','V1_mm2':'V1','A1_mm2':'A1','cortical_outline_mm2':'drawn_cortical_outline'},'Illustrative drawing; face is a subset of S1. Outline is not a certified biological neocortex denominator. All tracings provisional.'))
r=tracing('Catania_Remple_2002','fig02_case4','Heterocephalus glaber','Catania & Remple 2002','Fig 2 / case 4, left',{'S1_mm2':'S1'},'Candidate broad orofacial sum = lower incisor + upper incisor + buccal cavity/tongue + chin + vibrissae/head. Definition may differ from Brecht S1-face. Whole-neocortex perimeter unavailable in this tracing; all geometry provisional.')
d=data('Catania_Remple_2002','fig02_case4');components=['S1_lower_incisor','S1_upper_incisor','S1_buccal_cavity_tongue','S1_chin','S1_vibrissae_head'];r['face_or_orofacial_mm2']=sum(val(d,k) for k in components);r['face_percent_S1']=100*r['face_or_orofacial_mm2']/r['S1_mm2'];rows.append(r)
rows.append(tracing('Catania_Remple_2002','fig04B_naked_mole_rat','Heterocephalus glaber','Catania & Remple 2002','Fig 4B summary',{'S1_mm2':'S1'},'Summary drawing, not identified as case 4 or an additional animal. Face and cortical outline not separately measured.'))
rows.append(blank(species='Heterocephalus glaber',source='Catania & Remple 2002',figure_case='Table 1 / case 4',record_type='published case values',S1_mm2=11.4,face_or_orofacial_mm2=7.3,cortical_outline_mm2=32.5,face_percent_S1=100*7.3/11.4,S1_percent_outline=100*11.4/32.5,definition_note='Face column is derived broad orofacial sum 3.5+1.8+1.2+0.8 from rounded published table values. Same case as Fig 2 tracing; not another observation.',source_csv='M1_reanalysis/comparison/literature/Catania_Remple_2002_published_cases.csv'))
for p,m,sp,source,case,labs,note in [
 ('VanEssen_2005','fig09A_Brodmann','Homo sapiens','Van Essen 2005','Fig 9A',{'S1_mm2':'BA3','V1_mm2':'BA17'},'Pixel geometry exists but no accepted physical calibration. BA3 differs from isolated 3b; BA17 is the anatomical V1 candidate. BA41/42 not silently equated to A1.'),
 ('VanEssen_2005','fig09B_visuotopic_orbitofrontal','Homo sapiens','Van Essen 2005','Fig 9B',{},'V1 dorsal and ventral pixel tracings exist; physical areas unavailable. No borrowed scale.'),
 ('Wilkinson_2021','fig04_human','Homo sapiens','Wilkinson 2021','Fig 4',{'S1_mm2':'S1_areas2_1_3b_3a','V1_mm2':'V1'},'Unscaled atlas geometry. S1 includes 3a,3b,1,2; not identical to isolated 3b. Face not separately delineated.'),
 ('Krubitzer_Dooley_2013','fig07D_naked_mole_rat','Heterocephalus glaber','Krubitzer & Dooley 2013','Fig 7D',{},'Unscaled teeth/body geometry exists; teeth is not whole face. No absolute mm2 accepted.')]:rows.append(tracing(p,m,sp,source,case,labs,note))
# Keep each species together, with the workbook and tracing first.
rows.sort(key=lambda r: 0 if r['species']=='Homo sapiens' else 1)
with (OUT/'Brecht_alongside_existing_tracings.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
esc=lambda v:html.escape(f'{v:.3f}' if isinstance(v,float) else str(v) if v!='' else '—')
cols=FIELDS[:-2]
table='<table><thead><tr>'+''.join('<th>'+c+'</th>' for c in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(r[c])+'</td>' for c in cols)+'</tr>' for r in rows)+'</tbody></table>'
(OUT/'Brecht_alongside_existing_tracings.html').write_text('<!doctype html><meta charset="utf-8"><title>Brecht alongside other tracings</title><style>body{font:14px Arial;margin:24px;color:#24343f}table{border-collapse:collapse}td,th{border:1px solid #ccd3d8;padding:9px;vertical-align:top;min-width:90px}th{background:#e6edf3;position:sticky;top:0}tr:nth-child(even){background:#f6f8fa}</style><h1>Brecht alongside existing tracings</h1><p>Areas in mm²; percentages in 0–100 units. A dash means unavailable, never zero. Rows include original workbook, current tracings and one published case reference. Oral/head sums are candidate comparisons to Brecht S1-face. Source reuse and repeated views do not add animals. No new tracings or scale transfers were made.</p>'+table)
assert len(rows)==11
assert abs(next(r for r in rows if r['figure_case']=='Fig 2 / case 4, left')['face_percent_S1']-62.377181001974556)<1e-8
print('Saved 11 comparison rows with figure/case identity, units, calibration notes and canonical ROI paths.')
