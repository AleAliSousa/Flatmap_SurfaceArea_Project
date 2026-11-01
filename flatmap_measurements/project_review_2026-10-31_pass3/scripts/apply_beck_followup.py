from pass3_helpers import *
p='Beck_Kaas_1998';root=FM/p;out=root/'review/dm_recheck_2026-10-31';report=out/'followup_recheck.json'
if report.exists():raise SystemExit('Already applied')
archive(p);events=[];originalchanges=json.loads((out/'applied_changes.json').read_text());notes={}
for m in ['fig03','fig09','fig11']:
 old=get(p,m);d=copy.deepcopy(old);r=d['rois'][0]
 if m=='fig03':
  e=json.loads((OUT/'candidates'/'Beck_Kaas_1998__fig03__DM.json').read_text());assert old['rois'][0]==e['before'];r=e['after'];d['rois'][0]=r
  notes[m]='Follow-up recheck: residual right-border bends around the injection ovals removed. The DM/V2 continuation across the clustered symbols is now smooth and marked orange; all other vertices are retained.'
 elif m=='fig09':
  pp=r['polygons'][0];r['interpolated_border_segments'].append([q for q in pp[:12] if q[0]>=211])
  r['boundary_note']+=' Follow-up: the short upper-right gap between the faint arc and V2 junction is explicitly marked as interpolated; geometry unchanged.'
  notes[m]='Smooth DM contour retained after enlarged review. Orange now also identifies the short upper-right gap before the V2 junction; no geometry or area change.'
 else:
  pp=r['polygons'][0];dense=[]
  for a,b in zip(pp,pp[1:]+pp[:1]):
   a=np.array(a);b=np.array(b)
   for t in np.linspace(0,1,max(2,int(np.linalg.norm(b-a))),endpoint=False):dense.append((a+(b-a)*t).tolist())
  r['interpolated_border_segments']=[[q for q in dense if 352<=q[1]<=448 and q[0]<250],[q for q in dense if 490<=q[1]<=521 and q[0]<280],[q for q in dense if q[1]<=4]]
  r['boundary_note']+=' Follow-up: legend-hidden continuations (source y352–448 and y490–521) and the upper frame closure are explicitly marked in orange. These are not observed field borders. Geometry unchanged; this remains a partial contour, excluded from complete-field summaries.'
  notes[m]='Partial contour retained. The upper frame closure and both legend-obscured continuations are now marked orange. These hidden intervals cannot be certified as observed boundaries; no geometry or area change.'
 events.append(dict(paper_id=p,map_id=m,label=r['label'],before=old['rois'][0],after=copy.deepcopy(r),reason=notes[m],status='applied_after_visual_review'))
 (root/'figures'/m/'rois.json').write_text(json.dumps(d,indent=2)+'\n')
 if not any(c['map_id']==m for c in originalchanges):originalchanges.append(dict(map_id=m,old=old,new=d,note=notes[m]))
 for c in originalchanges:
  if c['map_id']==m:c['new']=d;c['note']=c.get('note','')+' '+notes[m]
(out/'applied_changes.json').write_text(json.dumps(originalchanges,indent=2)+'\n')
a=json.loads((OUT/'applied_changes.json').read_text());a.extend(events);(OUT/'applied_changes.json').write_text(json.dumps(a,indent=2)+'\n')
report.write_text(json.dumps(dict(date='2026-10-31',views_rechecked=['fig03','fig04','fig06','fig07','fig09','fig10','fig11','fig12'],geometry_changed=['fig03'],interpolation_display_added=['fig03','fig09','fig11'],notes=notes,native_verification='pending',anatomical_certification=False),indent=2)+'\n')
# Keep the same user-facing report current on every rebuild.
builder=root/'scripts/build_dm_recheck_review.py';s=builder.read_text();s=s.replace("rows=[];area=[];cards=[];all_images=[]", "followup_path=OUT/'followup_recheck.json'\nfollowup=json.loads(followup_path.read_text()) if followup_path.exists() else {}\nnotes.update(followup.get('notes',{}))\nrows=[];area=[];cards=[];all_images=[]")
s=s.replace("(OUT/'index.html').write_text(s)","if followup:\n s=s.replace('<h2>Why the other', '<p class=\\\"note\\\"><b>Additional recheck:</b> all eight insets re-inspected at enlargement. Fig3 injection-driven bends corrected; previously unmarked interpolation in Figs9/11 now shown. See <a href=\\\"followup_recheck.json\\\">follow-up verification</a>.</p><h2>Why the other')\n(OUT/'index.html').write_text(s)")
s=s.replace("(ROOT/'documentation/dm_symbol_recheck.md').write_text(md)","if followup:\n md+='\\n## Additional recheck\\n\\nAll eight insets were re-inspected at enlargement. Figure3 still had injection-driven bends on its right edge; these were replaced by a continuous local DM/V2 arc and marked as interpolated. Figure9’s short upper-right gap and Figure11’s legend-hidden/frame-closure segments are now explicitly shown in orange, without changing their geometry. Figures4/7 remain inferred estimates excluded from observed complete-field analysis, and Figure11 remains partial. Original state for this follow-up is archived in `../../project_review_2026-10-31_pass3/before/Beck_Kaas_1998.zip`.\\n'\n(ROOT/'documentation/dm_symbol_recheck.md').write_text(md)")
builder.write_text(s)
print('Beck follow-up applied; report updated on rebuild')
