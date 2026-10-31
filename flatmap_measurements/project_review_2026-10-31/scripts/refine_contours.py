"""Source-reviewed candidates; --apply archives every affected dataset before mutation."""
from pathlib import Path
import json, sys, subprocess, zipfile, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from prepare_candidates import flood, largest
ROOT=Path(__file__).resolve().parents[3]; FM=ROOT/'flatmap_measurements'
OUT=Path(__file__).resolve().parents[1]; C=OUT/'candidates'
JAVA='/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home/bin/java'
IJ='/Applications/Fiji.app/jars/ij-1.54p.jar'

def rdp(p, eps=.85):
 p=np.array(p,float)
 if len(p)<3:return p.tolist()
 v=p[-1]-p[0]; dist=np.linalg.norm(p-p[0],axis=1) if np.dot(v,v)==0 else np.abs(v[0]*(p[:,1]-p[0,1])-v[1]*(p[:,0]-p[0,0]))/np.linalg.norm(v)
 i=int(dist.argmax())
 return rdp(p[:i+1],eps)[:-1]+rdp(p[i:],eps) if dist[i]>eps else [p[0].tolist(),p[-1].tolist()]

def outline(mask,name):
 t=C/(name+'.tif'); j=C/(name+'.json');Image.fromarray(mask.astype('uint8')*255).save(t)
 subprocess.run([JAVA,'-Djava.awt.headless=true','--class-path',IJ,str(OUT/'scripts/MaskOutline.java'),str(t),str(j)],check=True,stdout=subprocess.DEVNULL)
 p=np.array(json.loads(j.read_text()),float)-.5
 # Split the ring in two before simplifying so no degenerate closed chord is used.
 k=len(p)//2
 return rdp(p[:k+1])+rdp(np.vstack([p[k:],p[:1]]))[1:-1]

def filled(paper,mid,inset=2,repair=None):
 a=np.asarray(Image.open(FM/paper/'figures'/mid/'source.tif').convert('L'))<150
 if repair:
  im=Image.fromarray(a);draw=ImageDraw.Draw(im)
  for line in repair:draw.line(line,fill=1,width=3)
  a=np.asarray(im)
 comp=largest(a);outside=flood(~np.pad(comp,1),(0,0))[1:-1,1:-1]
 return np.asarray(Image.fromarray((~outside).astype('uint8')*255).filter(ImageFilter.MinFilter(2*inset+1)))>0

def points(s):return [list(map(float,p.split(','))) for p in s.split()]

changes=[]
def add(paper,mid,label,polygons,note):
 f=FM/paper/'figures'/mid/'rois.json';d=json.loads(f.read_text());roi=next(r for r in d['rois'] if r['label']==label)
 changes.append(dict(paper=paper,map_id=mid,label=label,polygons=polygons,note=note,old_polygons=roi['polygons']))

for mid,label in [('fig10A','PV'),('fig10B','PV'),('fig07A','S2')]:
 repair=[[(1033,121),(1034,132)]] if mid=='fig10A' else None
 mask=filled('Beck_etal_1996',mid,2,repair)
 add('Beck_etal_1996',mid,label,[outline(mask,'refined_Beck_'+mid)],'Outer printed field envelope followed; all internal body-part compartments retained. Ink mask was hole-filled, shifted to the stroke centre and simplified within 0.85 source pixels.'+(' A short print gap at the right tip (1033,121)–(1034,132) was bridged along the visible continuation in a working mask only.' if repair else ''))

frost={
'9213':'''51,55 66,56 79,52 85,47 99,30 118,15 128,29 138,37 150,42 165,42 182,38 195,37 202,38 209,45 214,58 216,72 214,88 213,100 217,110 232,115 244,120 251,130 254,141 251,150 244,160 234,170 232,177 237,185 248,195 257,204 262,213 261,224 255,234 249,238 241,239 231,237 211,231 191,224 196,214 197,205 194,197 189,190 181,186 174,184 162,184 141,186 116,188 94,188 78,187 65,188 50,191 39,193 27,190 20,186 16,180 14,171 14,160 16,151 20,144 30,134 40,125 47,117 51,108 53,96 53,75''',
'9321':'''20,98 45,97 54,94 59,90 60,53 78,53 89,51 96,46 101,38 106,25 110,21 116,18 125,18 134,22 139,29 142,40 147,48 155,53 166,56 186,57 203,59 214,64 220,72 223,83 224,104 223,129 221,153 221,177 220,197 217,204 211,209 199,212 186,211 177,209 168,204 160,198 153,194 147,198 138,205 128,211 117,214 109,214 100,211 101,196 100,187 96,181 88,177 77,175 61,173 61,149 60,143 57,139 51,138 41,138 29,136 22,134 20,119''',
'9324':'''24,25 26,17 30,14 43,12 60,12 76,12 90,13 95,15 98,18 99,31 100,48 102,64 103,74 107,79 116,81 128,81 134,83 137,88 139,101 139,121 139,144 138,164 136,184 133,191 127,194 114,194 107,193 103,191 101,188 101,180 101,174 100,170 97,166 92,163 85,161 76,160 66,159 52,159 38,159 27,159 24,156 24,142 25,119 26,99 26,80 25,60 24,43'''}
for case,s in frost.items():
 add('Frost_etal_2000','fig04_'+case+'_distal_forelimb','S1_distal_forelimb',[points(s)],'Manually refined on enlarged source, following visible envelope curves and concavities; recording symbols and annotation leaders are not borders. '+('Labelled arm strip remains excluded.' if case=='9213' else 'Closed distal-forelimb envelope retained.'))

paper='Manger_etal_2002';mid='fig06right';d=json.loads((FM/paper/'figures'/mid/'rois.json').read_text());p=d['rois'][0]['polygons']
# Replace only the internal-body-part detour; retain both original gyral components.
new=p[0][:37]+points('260,450 240,452 220,456 201,460 187,464 196,447 202,429 207,410 209,397 207,382 202,365 194,348 185,335')+p[0][61:]
add(paper,mid,'PPr mapped extent',[new,p[1]],'Corrected lateral-gyrus component to the thick PPr boundary, retaining the ventral-trunk compartment previously cut out by following thin internal somatotopy lines. Figure 6 caption and somatotopic-representation text identify these internal body-part divisions. Sulcal strip and truncation at panel limits remain excluded; this is still a partial mapped extent.')

paper='Krubitzer_1998';mid='fig11B';mask=filled(paper,mid,3)
divider=points('831,162 836,199 841,233 849,267 861,304 875,334 895,361 918,384 944,404')
im=Image.new('1',(mask.shape[1],mask.shape[0]));ImageDraw.Draw(im).polygon([(0,0),(831,0)]+[tuple(p) for p in divider]+[(944,810),(0,810)],fill=1);left=np.asarray(im)
for label,m in [('Vc',mask&left),('Vr',mask&~left)]:
 add(paper,mid,label,[outline(m,'refined_Krubitzer11B_'+label)],'Corrected to thick outer Vc/Vr envelope and their shared boundary; thin upper/lower visual-field subdivisions, recording sites and labels are internal. Figure 11 caption identifies a simplified map and receptive-field progressions. Illustrative/repeated geometry remains pixel-only and does not establish an independent animal or physical area.')

for ch in changes:
 folder=FM/ch['paper']/'figures'/ch['map_id'];im=Image.open(folder/'source.tif').convert('RGB');draw=ImageDraw.Draw(im)
 for p in ch['polygons']:draw.line([tuple(x) for x in p]+[tuple(p[0])],fill='#00b6e0',width=2)
 if im.width<600:im=im.resize((im.width*3,im.height*3))
 name=ch['paper']+'__'+ch['map_id']+'__'+ch['label'].replace(' ','_');ch['candidate_image']=name+'.png';im.save(C/(name+'.png'))
(OUT/'candidate_changes.json').write_text(json.dumps(changes,indent=2)+'\n')

if '--apply' in sys.argv:
 archive=OUT/'before';archive.mkdir(exist_ok=True)
 for paper in sorted({c['paper'] for c in changes}):
  z=archive/(paper+'.zip')
  if z.exists():raise RuntimeError('Archive already exists; prevent duplicate mutation: '+str(z))
  with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
   for f in (FM/paper).rglob('*'):
    if f.is_file() and not any(x in f.parts for x in ['revisions','__pycache__']):out.write(f,f.relative_to(FM/paper))
 for ch in changes:
  f=FM/ch['paper']/'figures'/ch['map_id']/'rois.json';d=json.loads(f.read_text());r=next(r for r in d['rois'] if r['label']==ch['label'])
  r['polygons']=ch['polygons'];r['boundary_note']=r.get('boundary_note','')+' Review 2026-10-31: '+ch['note']
  r['tracing_method']='Source-reviewed contour revision, 2026-10-31; see project_review_2026-10-31'
  r['geometry_review']={'date':'2026-10-31','status':'source_refined_provisional','note':ch['note']}
  f.write_text(json.dumps(d,indent=2)+'\n')
 (OUT/'applied_changes.json').write_text(json.dumps(changes,indent=2)+'\n')
 print('Archived and applied',len(changes),'regional contour revisions')
else:print('Prepared',len(changes),'candidates; no canonical geometry changed')
