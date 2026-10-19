"""Read-only geometry/summary/asset checks; invoke per-paper saved-file/area verification without refreshing their hashes."""
from pathlib import Path
import csv,json,hashlib,re,subprocess,sys,tempfile
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
B=Path(__file__).resolve().parents[1];LOG=Path(tempfile.gettempdir())/'flatmap_dataset_verification';LOG.mkdir(exist_ok=True); results=[];changed={r['paper'] for r in csv.DictReader((B/'full_dataset_recheck_contours.csv').open())};issues=[]
# Verify local assets on the new comprehensive pages, including editable native links.
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.add(a['id'])
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
htmls=[B/'review_full_dataset_audit.html']+list(B.glob('*/review/full_dataset_audit.html'))
for f in htmls:
 p=Links();p.feed(f.read_text())
 for link in p.links:
  u=urlsplit(link)
  if u.scheme or not u.path:continue
  target=(f.parent/unquote(u.path)).resolve()
  if not target.is_file():issues.append(f'Missing asset: {f.relative_to(B)} -> {link}')
 # Check syntax of the one script in the source-review pages.
 scripts=re.findall(r'<script>(.*?)</script>',f.read_text(),re.S)
 for i,s in enumerate(scripts):
  tmp=LOG/'check_review.js';tmp.write_text(s);r=subprocess.run(['node','--check',str(tmp)],capture_output=True,text=True)
  if r.returncode:issues.append(f'{f.name}: {r.stderr}')
for root in sorted(B.iterdir()):
 if not(root/'source/paper.pdf').exists():continue
 name=root.name;defs={f.parent.name:json.loads(f.read_text()) for f in (root/'figures').glob('*/rois.json')};mfile=root/'data/measurements.csv';rows=list(csv.DictReader(mfile.open()));by={(r['map_id'],r['label']):r for r in rows}
 if len(by)!=len(rows):issues.append(name+': duplicate measurement labels')
 for mid,d in defs.items():
  for r in d['rois']:
   row=by.get((mid,r['label']))
   if row is None or row.get('area_px2') in [None,'NA','']:issues.append(name+': missing measured ROI '+mid+' '+r['label'])
  if name in changed:
   for n in ['RoiSet.zip','Masks.tif.zip','source.tif','tracing.png']:
    if d['rois'] and not(root/'figures'/mid/n).exists():issues.append(name+': missing native '+mid+'/'+n)
 selection=root/'data/summary_case_selection.csv';nselection=0
 if selection.exists():
  selection=list(csv.DictReader(selection.open()));nselection=len(selection);keys=[]
  for s in selection:
   key=tuple(s[k] for k in ['species','specimen','label']);keys.append(key);d=defs[s['map_id']];roi=next(r for r in d['rois'] if r['label']==s['label'])
   if re.search('illustrative|summary|composite|schematic|atlas',d.get('view_type',''),re.I):issues.append(name+': illustration enters animal summary')
   if re.search('unresolved',d.get('specimen_link_status',''),re.I):issues.append(name+': unresolved identity enters summary')
   if roi.get('extent','complete')!='complete':issues.append(name+': partial enters complete-field summary')
   if d.get('specimen')!=s['specimen']:issues.append(name+': summary specimen mismatch')
  if len(set(keys))!=len(keys):issues.append(name+': repeated animal/field in summary')
 v=json.loads((root/'documentation/validation.json').read_text());hashes=json.loads((root/'documentation/checksums.json').read_text())
 script=root/'scripts/measure_flatmaps.py'
 if not script.exists():script=root/'scripts/rebuild.py'
 r=subprocess.run([sys.executable,str(script),'--verify'],capture_output=True,text=True)
 (LOG/(name+'.log')).write_text(r.stdout+r.stderr)
 if r.returncode:issues.append(name+': saved-area/hash verification failed: '+(r.stdout+r.stderr)[-1000:])
 results.append(dict(paper=name,geometry_changed=name in changed,saved_contours=sum(len(d['rois']) for d in defs.values()),measurement_rows=len(rows),independent_case_field_selections=nselection,checksum_files=len(hashes),saved_area_hash_verification='passed' if not r.returncode else 'failed',native_readback=v.get('native_imagej_roundtrip','prior accepted geometry retained')))
 print(name,r.returncode,'verified',len(hashes),'files',flush=True)
stats=json.loads((B/'full_dataset_recheck_stats.json').read_text())
if sum(r['saved_contours'] for r in results)!=stats['current_contours']:issues.append('Project contour total differs from current canonical geometry')
if stats['previous_contours']+stats['added_observations']-stats['withdrawn_observations']!=stats['current_contours']:issues.append('Project added/withdrawn contour accounting mismatch')
report={'date':'2026-10-16','papers':len(results),'source_reviews_checked':len(htmls),'issues':issues,'results':results,'anatomical_certification':False}
(B/'full_dataset_recheck_validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'papers':len(results),'issues':issues},indent=2));sys.exit(bool(issues))
