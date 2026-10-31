from pathlib import Path
import csv,json,hashlib,subprocess,sys,re
from html.parser import HTMLParser
ROOT=Path.cwd();FM=ROOT/'flatmap_measurements';OUT=FM/'recommended_M1_expansion_2026-10-31';ids=json.loads((OUT/'papers.json').read_text()).values();logs=[]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ['href','src']:self.links.append(v)
for paper in ids:
 root=FM/paper;rs=list(csv.DictReader((root/'data/measurements.csv').open()));measured={(r['map_id'],r['label']) for r in rs if r['area_px2']!='NA'}
 canonical=set();empty=[]
 for f in (root/'figures').glob('*/rois.json'):
  d=json.loads(f.read_text());canonical.update((d['map_id'],r['label']) for r in d['rois'])
  if not d['rois'] and not d.get('outline'):empty.append(d['map_id'])
 assert measured==canonical,(paper,'CSV/canonical labels mismatch')
 # The helper's source-only view needs no link to a nonexistent ROI archive.
 script=root/'scripts/measure_flatmaps.py';s=script.read_text();needle="    (root/'review/gallery.html').write_text(page.replace"
 if 'No field ROI —' not in s:
  insertion="    for v in views:\n        if v['measured_fields'] == 0 and v['outline_scope'] == 'none':\n            page = page.replace(f'<a href=\"../figures/{v[\"map_id\"]}/RoiSet.zip\">ImageJ ROIs</a> · ', 'No field ROI — ')\n"
  assert needle in s;s=s.replace(needle,insertion+needle);compile(s,str(script),'exec');script.write_text(s)
 gallery=root/'review/gallery.html';s=gallery.read_text()
 for mid in empty:s=s.replace(f'<a href="../figures/{mid}/RoiSet.zip">ImageJ ROIs</a> · ','No field ROI — ')
 gallery.write_text(s)
 vpath=root/'documentation/validation.json';v=json.loads(vpath.read_text());v['anatomical_review']=('rejected_pending_retrace: file integrity is not anatomical validation' if any(r['status']=='rejected_pending_retrace' for r in rs) else v.get('anatomical_review','provisional; pending anatomical review'));v['reference_comparison']='Frost same-case Table1 comparison saved in batch report; Bock and Halley source tables retained separately. No calibration fitted to reference values.' if paper in ['Frost_etal_2000','Bock_etal_2011','Halley_etal_2025'] else 'Not performed; no matched numeric reference used.';vpath.write_text(json.dumps(v,indent=2)+'\n')
 if not any(r['status']=='rejected_pending_retrace' for r in rs):
  (root/'documentation/review_notes.txt').write_text('2026-10-31: Source and tracing were visually inspected for every saved view. Final canonical ROI labels were checked against measurement rows. Large overlaps were reviewed: parent/child S1-face or M1-face, and intentional mixed-response pig grid support. Other overlaps are narrow shared-border raster effects. Native ImageJ exported ROI/mask/source read-back passed during rebuild. This verifies file integrity, not biological validity. See figure_inventory.csv, canonical boundary notes and the batch report for calibration and remaining-view limitations.\n')
 # Refresh the integrity ledger after adding final documentation and source-only HTML link fixes.
 files=[p for name in ['source','figures','data','scripts','review','documentation'] for p in (root/name).rglob('*') if p.is_file() and p.name!='checksums.json' and '__pycache__' not in p.parts]
 (root/'documentation/checksums.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
 r=subprocess.run([sys.executable,'scripts/measure_flatmaps.py','--verify'],cwd=root,capture_output=True,text=True);assert r.returncode==0,(paper,r.stderr);logs.append(paper+': '+r.stdout.strip());print(logs[-1],flush=True)
 parser=Links();parser.feed(gallery.read_text())
 for link in parser.links:
  if not re.match(r'^[a-z]+:',link) and not link.startswith('#'):assert (gallery.parent/link.split('#')[0]).exists(),(gallery,link)
parser=Links();parser.feed((OUT/'index.html').read_text())
for link in parser.links:
 if not re.match(r'^[a-z]+:',link) and not link.startswith('#'):assert (OUT/link.split('#')[0]).exists(),link
# All batch rows link to real canonical files and all published source-table rows are separate.
rows=list(csv.DictReader((OUT/'measurements.csv').open()));assert len({(r['paper_id'],r['map_id'],r['label']) for r in rows})==len(rows)
assert all(r['percent_of_drawn_neocortex']=='NA' for r in rows)
assert all(r['whole_M1_replacement_ready']=='False' for r in rows)
(OUT/'verification.txt').write_text('\n'.join(logs)+'\nAll local HTML links resolved. Batch keys unique; no invented whole-cortex denominator or certified whole-M1 replacement.\n')
print('All report/gallery links resolved; batch checks passed.')
