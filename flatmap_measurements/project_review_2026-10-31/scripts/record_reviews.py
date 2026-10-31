from pathlib import Path
import json,csv
OUT=Path(__file__).resolve().parents[1]
def record(paper, maps, clarity, fit, notes, improvement='', grade='B'):
 p=OUT/'assessments.json';data=json.loads(p.read_text());inventory=list(csv.DictReader((OUT/'inventory.csv').open()))
 selected=[r for r in inventory if r['paper_id']==paper and (maps=='*' or r['map_id'] in maps)]
 if maps!='*':assert len(selected)==len(maps),(paper,maps)
 for r in selected:
  traced=int(r['ROI_count'])+int(r['outline_count'])>0
  data[paper+'/'+r['map_id']]=dict(clarity=clarity,fit=fit if traced else 'no_saved_trace',notes=notes,improvement=improvement,grade=grade if traced else 'N',review_status='visual_reviewed',source_roi_sha256=r['source_roi_sha256'])
 p.write_text(json.dumps(data,indent=2)+'\n')
