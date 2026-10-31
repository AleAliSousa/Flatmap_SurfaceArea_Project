from pathlib import Path
import csv, re, json, math, collections, html
import openpyxl
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
wb=openpyxl.load_workbook(ROOT/'M1_reanalysis/M1 surface measurements for reanalysis.xlsx',data_only=True)
DATA={p.parent.parent.name:list(csv.DictReader(p.open())) for p in (ROOT/'flatmap_measurements').glob('*/data/measurements.csv')}
def num(x):
 try:return float(x)
 except (ValueError,TypeError):return None
def selection(r):
 sid,sp,field,*_=r; ref=str(r[8]); f=str(field).strip(); note=''
 if f=='mef': f='MEF'
 if sid in [331,332]:return 'VanEssen_Drury_1997',None,[],'Multiple cited papers/figures; cannot identify which tracing produced the value. Resolve provenance before numeric pairing.'
 if '/' in f and 'cortex' in f:return None,None,[], 'Dimensionless cortex ratio stored in Area (mm2); numerator and denominator provenance must be checked separately.'
 if 'Haug' in ref:return 'Haug_1987',None,[], 'Histology/statistical source, not a planar field map. Regression estimates are not independent traced measurements.'
 if 'Wilkinson' in ref:
  return 'Wilkinson_2021','fig04_human',{'M1':['M1'],'V1':['V1'],'3,1,2':['S1_areas2_1_3b_3a'],'S2':['SII']}.get(f,[]),'Unscaled atlas. S1 total includes 3a,3b,1,2; individual subfields/cut pieces not separately recorded.'
 if 'Van Essen 2005' in ref:
  a={21:['BA41','BA42'],22:['BA4'],31:['BA17'],32:['BA18'],33:['BA3','BA1','BA2'],41:['BA6'],43:['BA41'],44:['BA42']}
  b={23:['MTplus'],25:['V1_dorsal','V1_ventral_cut'],26:['V1_dorsal'],27:['V1_ventral_cut'],28:['V2d','V2v'],29:['V2d'],30:['V2v'],34:['VP'],35:['V3'],36:['V4v'],37:['V3a'],38:['V7'],39:['V8'],40:['LO']}
  return 'VanEssen_2005','fig09A_Brodmann' if sid in a else 'fig09B_visuotopic_orbitofrontal',a.get(sid,b.get(sid,[])),'Pixel-only atlas; no valid local physical calibration/areal distortion correction. BA41+42 is not strictly A1; MTplus is broader than MT.'
 if 'Brecht' in ref:
  m='fig03a_human' if 'Homo' in sp else ('fig03b_macaque' if sp=='Macaque' else 'fig03d_naked_mole_rat')
  lab={'Cortex':'drawn_cortical_outline','S1/3b':'S1','S1 face':'S1_face'}.get(f,f)
  return 'Brecht_Freiwald_2012',m,[lab],('Workbook cites Fig 1; candidate sensory flatmap is Fig 3; reference correction needs confirmation. ' if sid in [327,330] else '')+'Schematic drawing comparison; caption defines human/macaque S1 as putative 3a+3b, not isolated 3b; outline is not a certified biological neocortex denominator.'
 if 'Felleman' in ref:
  lab={'M1':['4'],'A1':['AI'],'S1/3b':['3b'],'MST':['MSTd','MSTl'],'MSTI':['MSTl'],'V4v, V4d':['V4'],'ER':['ER posterior','ER anterior'],'subicular':['Subicular / hippocampal subdivisions'],'CA1':['Subicular / hippocampal subdivisions'],'CA3':['Subicular / hippocampal subdivisions']}.get(f,[f])
  return 'Felleman_VanEssen_1991','fig02',lab,'Composite macaque map; source species recorded only as Macaca. ER sum includes both components; workbook component extent unresolved.'+(' Workbook note combines motor fields; not equivalent to area 4.' if sid==353 else '')
 if 'Krubitzer & Dooley' in ref:
  lab={'S1/3b':['3b'],'FST':['FSTd','FSTv'],'V3':['V3d','V3v'],'V4':['DL/V4_dorsal','DL/V4_ventral']}.get(f,[f])
  return 'Krubitzer_Dooley_2013','fig01_macaque',lab,'Illustrative map reused from Krubitzer 2009 Fig 7; not another animal. Cortex outline not traced as a certified denominator.'
 if 'Krubitzer & Kaas' in ref:
  lab={'V1':['17'],'V2':['18'],'M1':['Motor'],'premotor':['Premotor'],'PV':['PV/IG'],'S1/3b':['3b'],'neocortex':['Neocortex outline']}.get(f,[f])
  return 'Krubitzer_Kaas_1990','fig12',lab,('Workbook cites Fig 2; Fig 12 is only a candidate corresponding summary; confirm citation. ' if sid>=428 else '')+'PV/IG is broader than literal PV; summary map does not add an animal.'
 if 'Rosa' in ref:
  m='fig05A_case1' if '5A' in ref else 'fig11_schematic'
  return 'Rosa_etal_1993',m,[{'DM':'DM_V3A','M1':'Motor/M1','S1':'Somatosensory'}.get(f,f)],'Fig 11 schematic has no scale; do not transfer specimen scale from Fig 5A without verified geometric correspondence.'
 if 'Mayer' in ref:
  case=re.search(r'15-0[1-4]',str(r[11])); candidates=[v for v in DATA['Mayer_etal_2019'] if v['label']=='M1_sampled_response_territory' and (not case or v['specimen']==case[0])]
  return 'Mayer_etal_2019',None,[], 'Whole M1 is not closed. Existing sampled response territory is partial, not equivalent to workbook M1. Source identifies Sapajus spp., not confirmed Cebus apella. Related areas (mm2): '+ '; '.join(v['specimen']+' '+v['area_mm2'] for v in candidates)
 if 'Van' in ref and '1997' in ref:return 'VanEssen_Drury_1997',None,[],'No uniform biological area calibration; need original surface mesh and per-tile areas. Multi-reference rows do not identify a unique source figure.'
 return None,None,[],'No corresponding source dataset in flatmap_measurements; cited paper/table/figure and measurement definition needed.'
rows=[]
for excel_row,r in enumerate(list(wb.active.values)[1:],2):
 if r[1] is None:continue
 paper,mapid,labels,reason=selection(r)
 candidates=[v for v in DATA.get(paper,[]) if v.get('map_id')==mapid and v['label'] in labels]
 found={v['label'] for v in candidates}; complete=bool(labels) and all(l in found for l in labels)
 vals=[num(v['area_mm2']) for v in candidates]; px=[num(v['area_px2']) for v in candidates]
 a=sum(vals) if complete and all(x is not None for x in vals) else None
 p=sum(px) if complete and all(x is not None for x in px) else None
 old=num(r[5]);delta=100*(a-old)/old if a is not None and old not in [None,0] else None
 status='numeric drawing comparison' if delta is not None else ('existing geometry; mm2 unavailable' if p is not None else ('explicit unavailable measurement' if candidates else 'no equivalent row'))
 if r[0] in [353]:status='different field definition; diagnostic numbers only'
 if r[0] in [327,330] or 428<=r[0]<=441:status='citation mismatch; candidate comparison only'
 if r[0] in [58,59,47,48,91,92,118,119]:reason+=' Whole field is recorded, but workbook component is not separately tabulated; not an absent whole field. '
 if r[0] in [82,116,341]:reason+=' R is not a literal field in the selected table; source label identity needs inspection. '
 if r[0]==127:reason+=' SEF exists but is not silently substituted for MEF. '
 if r[0] in [105,133,182,45,56]:reason+=' Complete neocortex perimeter is not established; enclosing drawing cannot automatically serve as neocortex. '
 if not candidates and paper and labels:reason+=' Requested label/component absent from this figure table; do not substitute another field.'
 details=' | '.join(dict.fromkeys(v.get('boundary_note','') for v in candidates if num(v['area_mm2']) is None))
 rows.append(dict(excel_row=excel_row,source_row=r[0],species=r[1],field=r[2],workbook_value=r[5],reference=r[8],individual=r[11],dataset=paper,map_id=mapid,matched_labels=' + '.join(labels),flatmap_mm2=a,flatmap_px2=p,difference_mm2=a-old if a is not None and old is not None else None,difference_percent=delta,workbook_over_flatmap=old/a if old is not None and a not in [None,0] else None,status=status,reason=reason,measurement_detail=details,source_csv=f'flatmap_measurements/{paper}/data/measurements.csv' if paper else '',workbook_note=r[18],workbook_note2=r[19],calibration_review=r[21] if len(r)>21 else '',use_restriction=r[22] if len(r)>22 else ''))
with (OUT/'row_audit.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'audit_summary.json').write_text(json.dumps({'rows':len(rows),'statuses':dict(collections.Counter(r['status'] for r in rows))},indent=2))
# Portable browser table with filters; calculated values are generated from original source CSVs, not editable spreadsheet formula inputs.
cols=['source_row','species','field','workbook_value','flatmap_mm2','difference_percent','status','calibration_review','use_restriction','reason','measurement_detail','dataset','map_id','matched_labels']
esc=lambda x:html.escape('' if x is None else (f'{x:.4f}' if isinstance(x,float) else str(x)))
table='<table><thead><tr>'+''.join('<th>'+c+'</th>' for c in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(r[c])+'</td>' for c in cols)+'</tr>' for r in rows)+'</tbody></table>'
(OUT/'row_audit.html').write_text('<!doctype html><meta charset="utf-8"><title>M1 reanalysis comparison</title><style>body{font:14px Arial;margin:24px;color:#172c38}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #cbd5dc;vertical-align:top;min-width:95px}th{position:sticky;top:0;background:#e5eef4}input{padding:10px;width:500px}tr:nth-child(even){background:#f6f8fa}</style><h1>M1 reanalysis: row audit</h1><p>Difference = 100 × (flatmap − workbook) / workbook. Values compare drawing measurements, not independent biological replicates. See comparison_report.md for interpretation and paper requests. NA is never zero.</p><input placeholder="Filter species, reference, field, or reason" oninput="document.querySelectorAll(\'tbody tr\').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(this.value.toLowerCase()))">'+table)
print(json.dumps({'rows':len(rows),'statuses':dict(collections.Counter(r['status'] for r in rows))},indent=2))
for r in rows:
 if r['field']=='M1' or (r['dataset']=='Brecht_Freiwald_2012' and r['flatmap_mm2']):print(r['source_row'],r['field'],r['workbook_value'],r['flatmap_mm2'],r['difference_percent'])
