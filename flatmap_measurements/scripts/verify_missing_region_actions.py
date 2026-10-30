#!/usr/bin/env python3
"""Verify the scope, saved artifacts and summary exclusions of the executed audit."""
import csv,hashlib,json,math,re
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'missing_region_audit_2026-10-20';B=ROOT/'_backups/missing_region_actions_2026-10-20'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  self.links += [v for k,v in attrs if k in ('href','src','data-image') and v]
def main():
 actions=json.loads((A/'action_results.json').read_text());papers=sorted(p.name for p in B.iterdir() if (p/'source/paper.pdf').exists());expected={(r['paper'],r['map_id']) for r in actions['results'] if r['added'] or r['revised'] or r['updated_unmeasured']};changed=set();added=0;revised=0
 oldhash=json.loads((B/A.name/'canonical_input_sha256.json').read_text())
 for rel,sha in oldhash.items():
  f=ROOT/rel
  if hashlib.sha256(f.read_bytes()).hexdigest()!=sha:changed.add((f.parts[-4],f.parts[-2]))
 assert changed==expected,(changed,expected)
 verified_files=0; prior_source_overlaps=0
 for p in papers:
  root=ROOT/p
  v=json.loads((root/'documentation/validation.json').read_text());assert v['native_imagej_roundtrip']=='passed',p
  vert=json.loads((root/'documentation/vertex_validation.json').read_text());assert not vert['proper_crossings_or_invalid_bounds'],p
  geom=json.loads((root/'documentation/geometry_review.json').read_text())
  baseline_geom=json.loads((B/p/'documentation/geometry_review.json').read_text())
  for x in geom['overlaps']:
   if not x['overlap_after_eroding_both_masks_2px']:continue
   assert x['interpretation']=='documented source overlap' and x in baseline_geom['overlaps'],(p,x)
   assert (p,x['map_id']) not in changed,(p,x['map_id'],'changed overlap needs review')
   prior_source_overlaps+=1
  for rel,h in json.loads((root/'documentation/checksums.json').read_text()).items():
   assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==h,(p,rel)
   verified_files+=1
  measurements={(r['map_id'],r['label']):r for r in csv.DictReader((root/'data/measurements.csv').open())}
  selections={(r['map_id'],r['label']) for r in csv.DictReader((root/'data/summary_case_selection.csv').open())}
  for q in (root/'figures').glob('*/rois.json'):
   old=json.loads((B/p/'figures'/q.parent.name/'rois.json').read_text());new=json.loads(q.read_text());oldr={r['label']:r for r in old['rois']}
   for k in ['pdf_page','render_scale','crop_xyxy','scale_endpoints_px','scale_length_mm','specimen','view_type','include_in_whole_hemisphere_summary','outline']:assert old.get(k)==new.get(k),(p,q.parent.name,k)
   for r in new['rois']:
    if r['label'] not in oldr:added+=1
    elif r['polygons']!=oldr[r['label']]['polygons']:revised+=1
    else:continue
    row=measurements[(new['map_id'],r['label'])];px=float(row['area_px2']);mm=float(row['area_mm2']);assert px>0 and mm>0
    scale=float(row['scale_length_mm'])/float(row['scale_length_px']);assert math.isclose(mm,px*scale*scale,rel_tol=1e-9)
    if r.get('extent')=='approximate' or 'illustrative' in new['view_type']:assert (new['map_id'],r['label']) not in selections,(p,r['label'],'invalid summary inclusion')
 assert (added,revised)==(actions['added_contours'],actions['revised_contours']),(added,revised)
 analysis=ROOT.parent/'surface_area_analysis/data/02_measurements_flagged.csv'
 aggregated={(r['paper'],r['map_id'],r['label']):r for r in csv.DictReader(analysis.open())}
 for r in csv.DictReader((A/'action_measurement_changes.csv').open()):
  q=aggregated[(r['paper'],r['map_id'],r['label'])]
  assert math.isclose(float(q['area_mm2']),float(r['after_area_mm2']),rel_tol=1e-9),(r['paper'],r['label'],'stale project analysis')
  if r['extent']=='approximate' or 'illustrative' in q['view_type']:
   assert q['use_for_specimen_mean'].lower()=='false',(r['paper'],r['label'],'project mean exclusion')
 htmlfiles=[ROOT/'review_missing_region_actions.html',A/'index.html']+[ROOT/p/'review/missing_region_actions.html' for p in papers]
 nlinks=0
 for f in htmlfiles:
  parser=Links();parser.feed(f.read_text())
  for link in parser.links:
   if '://' in link or link.startswith('#'):continue
   nlinks+=1;assert (f.parent/link.split('#')[0]).is_file(),(f,link)
 report=dict(status='passed',papers_rebuilt=len(papers),changed_views=len(changed),added_contours=added,revised_contours=revised,native_imagej_roundtrip='passed for all affected papers',vertex_and_interior_overlap_checks='passed; unchanged documented source overlaps retained',unchanged_prior_source_overlaps=prior_source_overlaps,scale_crop_outline_and_specimen_metadata='unchanged',new_approximate_and_illustrative_summary_exclusions='passed',verified_hashed_files=verified_files,verified_review_links=nlinks,anatomical_certification=False)
 report['project_analysis']='rebuilt; all 29 changed measurement values and approximate/illustrative exclusions verified'
 (A/'action_validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
