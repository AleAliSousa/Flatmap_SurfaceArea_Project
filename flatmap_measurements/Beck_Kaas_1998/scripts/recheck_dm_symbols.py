"""Source-guided DM contours; no intensity flood filling through tracer symbols."""
from pathlib import Path
import json,zipfile,sys,copy
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review/dm_recheck_2026-10-31';OUT.mkdir(exist_ok=True)
if (OUT/'applied_changes.json').exists():raise SystemExit('Already applied. Use build_dm_recheck_review.py or rebuild_all.py; originals are archived.')
def pts(s):return [list(map(float,x.split(','))) for x in s.split()]
def smooth(p):
 p=np.array(p,float);out=[]
 for i in range(len(p)-1):
  a=p[max(0,i-1)];b=p[i];c=p[i+1];d=p[min(len(p)-1,i+2)]
  for t in np.linspace(0,1,max(3,int(np.linalg.norm(c-b)/2)),endpoint=False):
   out.append((.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)).tolist())
 return out+[p[-1].tolist()]
def contour(a,b):return smooth(pts(a))+smooth(pts(b))[1:-1]
specs={
'fig09':dict(label='DM',extent='complete',poly=contour('222,12 201,13 178,16 154,21 130,27 109,35 88,44 67,54 47,65 32,77 24,89 21,102 24,121 29,143 35,165 41,186 46,208 51,230 56,251 57,273 59,294 62,314 67,331','67,331 80,308 94,282 108,257 121,231 131,207 140,182 146,158 152,138 163,116 176,92 190,67 206,39 222,12'),inferred=[pts('112,34 119,31 127,28'),pts('150,143 147,155 145,163')],note='Faint gray DM envelope followed continuously across superimposed tracer symbols and injection outlines. The small ellipses/triangle/square/cross/circles are annotations, not areal boundaries. Short hidden continuations across the upper fold mark and right injection are interpolated. Both DM ends join the V2 boundary inside the inset; previous blanket frame-clipping/partial classification was incorrect. Complete means the published drawn envelope, not independently validated anatomical certainty.'),
'fig06':dict(label='DM',extent='complete',poly=contour('340,92 318,92 294,97 268,103 242,110 214,120 187,131 162,143 140,157 121,174 106,192 98,210 95,230 95,245 97,263 103,284 108,300 118,325 132,350 147,375 165,400 185,425 205,450 225,475 246,500 271,525 302,550 318,560 327,565 338,570 347,575','347,575 346,550 345,525 343,500 343,475 341,450 340,425 338,400 336,375 336,350 334,325 331,300 329,275 326,250 326,225 326,200 329,175 331,150 336,125 341,100 340,92'),inferred=[pts('95,245 97,263 103,284')],note='Added the visible closed DM envelope. The left edge continues behind the Fluororuby injection oval between approximately (95,245) and (103,284), a short smooth interpolation supported by the visible tangents above and below. Do not follow the three overlapping injection ellipses. Both ends meet the DM/V2 boundary inside the panel. Compared with Fig7 (same species, different case) and Fig9 (different species) for line meaning/topology only; no geometry or scale copied.'),
'fig04':dict(label='DM estimated envelope',extent='approximate_complete',poly=contour('295,77 269,78 243,78 217,77 192,74 168,70 145,68 124,73 104,85 84,108 66,143 55,183 54,226 60,270 65,300 70,325 75,350 81,375 89,400 97,425 108,450 120,475 135,500 150,525 168,550 187,575 207,600 230,625 254,650 265,660 276,670 291,682','291,682 284,654 277,620 272,586 271,551 273,515 278,480 286,444 295,410 305,375 315,341 323,309 330,277 334,246 334,214 332,186 327,158 317,130 307,103 295,77'),inferred=[smooth(pts('104,85 84,108 66,143 55,183 54,226 60,270'))],note='Added an explicitly inferred DM envelope. The large WGA-HRP injection obscures the left boundary between approximately (104,85) and (60,270). That interval is a smooth tangent-guided reconstruction, not an observed line; the injection ellipse is not used as DM boundary. Fig3 is a same-species topology check only. Approximate_complete excludes this from complete-field summaries by default; no unique hidden border can be recovered from this illustration.'),
'fig07':dict(label='DM estimated envelope',extent='approximate_complete',poly=contour('294,97 270,94 247,89 223,84 199,80 187,80 173,85 163,90 151,100 144,110 138,120 134,130 132,140 129,150 127,160 124,190 122,223 123,257 127,291 137,337 146,364 159,391 179,419 203,449 228,477 255,508 286,539 289,544','289,544 290,508 291,475 293,442 294,408 296,375 297,341 298,307 297,273 296,239 295,205 294,171 294,138 294,113 294,97'),inferred=[smooth(pts('126,160 124,190 122,223 123,257 127,291 137,337')),pts('286,539 289,544 290,537')],note='Added an explicitly inferred DM envelope. The WGA-HRP injection masks the left border from approximately (126,160) to (137,337). Smooth continuation is a hypothesis constrained by visible endpoints/tangents, not an observed areal edge. The injection ellipse extends into VPP and must not define DM. A small lower-right drawing gap is closed to the V2 boundary. Fig6 supplies same-species topological context, not copied coordinates. Approximate_complete is excluded from complete-field summaries by default.')}
# Use a straight final join across the tiny lower-right print gap; avoid spline overshoot at the cusp.
p7=specs['fig07']['poly'];i=p7.index([286.,539.]);j=p7.index([289.,544.]);p7[i+1:j]=[]
specs['fig07']['inferred'][-1]=[[286,539],[289,544],[289.031,542.888]]
changes=[]
for mid,s in specs.items():
 d=json.loads((ROOT/'figures'/mid/'rois.json').read_text());old=copy.deepcopy(d);new=dict(label=s['label'],polygons=[s['poly']],extent=s['extent'],boundary_note=s['note'],tracing_method='Manual source-border anchors with piecewise Catmull-Rom interpolation; injection/tracer marks explicitly ignored; 2026-10-31 DM recheck',interpolated_border_segments=s['inferred'],geometry_review=dict(date='2026-10-31',status='provisional_source_reviewed' if s['extent']=='complete' else 'inferred_boundary_not_observed',note=s['note']))
 if mid in ['fig04','fig07']:new.update(status='inferred_boundary_estimate_not_observed',analysis_eligible=False)
 d['rois']=[new];d['unmeasured']=[r for r in d['unmeasured'] if r['label'] not in ['DM','DM visible fragment']]
 if mid in ['fig04','fig07']:d['unmeasured'].append(dict(label='DM observed complete boundary',status='not_measurable',reason='The hidden boundary is not uniquely observed. An explicitly inferred DM estimated envelope is saved separately; see its orange/dashed interval.'))
 for r in d['unmeasured']:
  if r['label']=='V2':r['reason']='Only the DM-facing V2 boundary is shown; the outer V2 extent lies outside the inset. A complete V2 area cannot be recovered.'
  if r['label']=='VPP':r['reason']='VPP is a location label next to injection sites; its complete outer field boundaries are not supplied.'
 d['review_note']='DM-symbol recheck 2026-10-31 supersedes older blanket exclusions and symbol-following contours; see review/dm_recheck_2026-10-31/index.html.'
 changes.append(dict(map_id=mid,old=old,new=d,note=s['note']))
# Closed drawn fields were incorrectly labelled fragments merely because the shared V2 line continues beyond DM.
for mid in ['fig10','fig12']:
 d=json.loads((ROOT/'figures'/mid/'rois.json').read_text());old=copy.deepcopy(d);r=d['rois'][0];r['label']='DM';r['extent']='complete';note='Extent re-audit: both DM endpoints join the DM/V2 boundary inside the inset. The continuation of that shared V2 line outside DM is not evidence that DM itself is cropped. Saved geometry unchanged; only the incorrect fragment classification/label is corrected. Complete denotes the published drawn field, whose anatomical borders remain provisional.';r['boundary_note']+=' DM-symbol recheck 2026-10-31: '+note;d['unmeasured']=[r for r in d['unmeasured'] if r['label']!='DM']
 for u in d['unmeasured']:
  if u['label']=='V2':u['reason']='The entire V2 field is not enclosed in this inset; only its shared boundary with DM is visible.'
 changes.append(dict(map_id=mid,old=old,new=d,note=note))
(OUT/'proposed_changes.json').write_text(json.dumps(changes,indent=2)+'\n')
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',18)
for c in changes:
 im=Image.open(ROOT/'figures'/c['map_id']/'source.tif').convert('RGB');panes=[]
 for title,d in [('Source',None),('Before this correction',c['old']),('Proposed',c['new'])]:
  t=im.copy();dr=ImageDraw.Draw(t)
  if d:
   for r in d['rois']:
    for p in r['polygons']:dr.line([tuple(v) for v in p]+[tuple(p[0])],fill='#008ea8',width=1)
    for p in r.get('interpolated_border_segments',[]):dr.line([tuple(v) for v in p],fill='#e47700',width=2)
  ratio=min(500/t.width,1000/t.height);t=t.resize((round(t.width*ratio),round(t.height*ratio)));can=Image.new('RGB',(520,1040),'white');can.paste(t,((520-t.width)//2,40));ImageDraw.Draw(can).text((10,10),title,font=font,fill='black');panes.append(can)
 full=Image.new('RGB',(1560,1080),'#e4edea');ImageDraw.Draw(full).text((10,10),c['map_id']+' — teal: field envelope; orange: interpolated/hidden boundary',font=font,fill='black')
 for i,p in enumerate(panes):full.paste(p,(i*520,40))
 full.save(OUT/(c['map_id']+'_comparison.png'))
if '--apply' in sys.argv:
 arc=ROOT.parent/'_backups/Beck_Kaas_1998_DM_symbols_2026-10-31.zip';assert not arc.exists(),'Archive exists; do not reapply.'
 with zipfile.ZipFile(arc,'w',zipfile.ZIP_DEFLATED) as z:
  for f in ROOT.rglob('*'):
   if f.is_file() and 'revisions' not in f.parts and '__pycache__' not in f.parts:z.write(f,f.relative_to(ROOT))
 for c in changes:
  f=ROOT/'figures'/c['map_id']/'rois.json';assert json.loads(f.read_text())==c['old'];f.write_text(json.dumps(c['new'],indent=2)+'\n')
 (OUT/'applied_changes.json').write_text(json.dumps(changes,indent=2)+'\n');print('Applied',len(changes),'view changes')
else:print('Prepared',len(changes),'view changes; not applied')
