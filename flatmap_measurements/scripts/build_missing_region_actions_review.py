#!/usr/bin/env python3
"""Publish the executed audit actions from canonical geometry and rebuilt tables."""
import csv,html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'missing_region_audit_2026-10-20'
B=ROOT/'_backups/missing_region_actions_2026-10-20'
e=html.escape

def read_rows(p):
 return list(csv.DictReader(p.open()))
def main():
 actions=json.loads((A/'action_results.json').read_text());diff=[];cards=[]
 for result in actions['results']:
  paper,mid=result['paper'],result['map_id'];root=ROOT/paper
  if not (root/'documentation/missing_region_actions_2026-10-20.md').exists():continue
  if not (root/'review/missing_region_previous'/f'{mid}.png').exists():continue
  old={(r['map_id'],r['label']):r for r in read_rows(B/paper/'data/measurements.csv')}
  new={(r['map_id'],r['label']):r for r in read_rows(root/'data/measurements.csv')}
  table=[]
  for label in result['added']+result['revised']:
   before=old.get((mid,label),{});after=new[(mid,label)]
   item=dict(paper=paper,map_id=mid,label=label,change='added' if label in result['added'] else 'revised',extent=after.get('extent',''),before_area_px2=before.get('area_px2','NA'),after_area_px2=after.get('area_px2','NA'),before_area_mm2=before.get('area_mm2','NA'),after_area_mm2=after.get('area_mm2','NA'))
   diff.append(item)
   def fmt(v):
    try:return f'{float(v):.4f}'
    except (ValueError,TypeError):return 'NA'
   table.append('<tr><td>'+e(label)+'</td><td>'+e(item['extent'])+'</td><td>'+fmt(item['before_area_mm2'])+'</td><td>'+fmt(item['after_area_mm2'])+'</td></tr>')
  stem=paper+'/figures/'+mid+'/';oldimg=paper+'/review/missing_region_previous/'+mid+'.png'
  d=json.loads((root/'figures'/mid/'rois.json').read_text())
  links='<a href="'+stem+'rois.json">Canonical definition</a> · <a href="'+paper+'/documentation/missing_region_actions_2026-10-20.md">Decisions</a>'
  if (root/'figures'/mid/'RoiSet.zip').exists():links+=' · <a href="'+stem+'RoiSet.zip">Editable ImageJ ROIs</a>'
  cards.append('<article><h2>'+e(paper+' / '+mid)+'</h2><p>'+e(result['outcome'])+'</p><p>'+links+'</p><div class="controls"><button data-image="'+stem+'tracing.png" aria-pressed="true">After</button><button data-image="'+stem+'source_preview.png" aria-pressed="false">Source</button><button data-image="'+oldimg+'" aria-pressed="false">Before</button></div><a class="full" href="'+stem+'tracing.png"><img loading="lazy" src="'+stem+'tracing.png" alt="'+e(paper+' '+mid)+'"></a>'+('<table><thead><tr><th>Field</th><th>Extent</th><th>Before mm²</th><th>After mm²</th></tr></thead><tbody>'+''.join(table)+'</tbody></table>' if table else '')+'<details><summary>Remaining field limits ('+str(len(d['unmeasured']))+')</summary><ul>'+''.join('<li><b>'+e(u['label'])+'</b>: '+e(u['reason'])+'</li>' for u in d['unmeasured'])+'</ul></details></article>')
 with (A/'action_measurement_changes.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(diff[0]));w.writeheader();w.writerows(diff)
 summary_rows=[]
 for r in actions['results']:summary_rows.append(dict(paper=r['paper'],map_id=r['map_id'],status=r['status'],added='; '.join(r['added']),revised='; '.join(r['revised']),approximate='; '.join(r['approximate']),outcome=r['outcome']))
 with (A/'action_results.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(summary_rows[0]));w.writeheader();w.writerows(summary_rows)
 page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Completed missing-region actions</title><style>
 body{font:16px/1.55 system-ui,sans-serif;color:#182a35;background:#f3f6f7;max-width:1350px;margin:32px auto;padding:0 22px}h1{font-size:32px}h2{font-size:22px}article,.intro{background:white;border:1px solid #d9e2e7;border-radius:10px;padding:24px;margin:22px 0}a{color:#006387}img{max-width:100%;display:block;margin:16px auto}button{font:inherit;padding:7px 20px;border:1px solid #67838c;background:white;cursor:pointer}button[aria-pressed=true]{background:#153d50;color:white}.controls{display:flex;gap:8px}table{border-collapse:collapse;width:100%;margin:18px 0}th,td{text-align:left;padding:8px;border-bottom:1px solid #ddd}summary{cursor:pointer}</style>
 <h1>Completed missing-region actions</h1><p>20 October 2026 · <a href="missing_region_audit_2026-10-20/index.html">Audit and action ledger</a> · <a href="tracing_method.md">Tracing method</a></p>
 <div class="intro"><p><b>28 contours added; one existing MT contour corrected.</b> Eleven views updated across eight papers. All 22 listed actions have an outcome: added measurements or an explicit source-limit assessment.</p><p>Twenty-five additions are illustrative-map fields, two are complete specimen-field observations, and one (echidna V) is approximate. The approximate V boundary bridges an undrawn interval among recording symbols and is excluded from complete-field means. Illustrative maps remain excluded from animal means. Original calibration and specimen metadata are preserved.</p><p>Use <b>After / Source / Before</b> beneath each figure heading. Click the image to enlarge it. Area values describe these drawn views; the observation count is not an animal count.</p><p><a href="missing_region_audit_2026-10-20/action_measurement_changes.csv">Area changes</a> · <a href="missing_region_audit_2026-10-20/action_results.csv">All action outcomes</a></p></div>
 '''+''.join(cards)+'''<script>document.querySelectorAll('article').forEach(card=>{card.querySelectorAll('button').forEach(button=>button.addEventListener('click',()=>{card.querySelector('img').src=button.dataset.image;card.querySelector('.full').href=button.dataset.image;card.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));}));});</script></html>'''
 (ROOT/'review_missing_region_actions.html').write_text(page)
 # Update root counts from canonical definitions, leaving unrelated paper artifacts untouched.
 readme=ROOT.parent/'README.md';s=readme.read_text()
 import re
 for p in ROOT.iterdir():
  if not (p/'source/paper.pdf').exists():continue
  n=sum(len(json.loads(f.read_text())['rois']) for f in (p/'figures').glob('*/rois.json'))
  s=re.sub(r'(\| \['+re.escape(p.name)+r'\]\([^\n]+\) \| )\d+( \|)',lambda m:m.group(1)+str(n)+m.group(2),s)
 marker='<!-- missing-region-actions-completed -->'
 if marker not in s:s=s.replace('## Datasets and queue','## Datasets and queue\n\n'+marker+'\n[Completed missing-region actions: 28 additions and one corrected contour](flatmap_measurements/review_missing_region_actions.html). All listed audit actions now have recorded outcomes; unresolved source boundaries remain explicit NA.')
 readme.write_text(s)
 print('Published action review:',len(cards),'updated views;',len(diff),'added/revised measurement rows.')
if __name__=='__main__':main()
