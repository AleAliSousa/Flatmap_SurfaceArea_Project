#!/usr/bin/env python3
"""Rebuild canonical measurements, summaries, source assessment review and final hashes."""
import argparse,csv,hashlib,html,json,shutil,subprocess,sys
from pathlib import Path
import pypdfium2 as pdfium
from measure_flatmaps import METADATA,write_csv,digest

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--java');ap.add_argument('--ij-jar');a=ap.parse_args()
 root=Path(__file__).resolve().parents[1]
 manifest=json.loads((root/'source/manifest.json').read_text())
 if digest(root/'source/paper.pdf')!=manifest['source_sha256']:raise ValueError('Source PDF checksum changed')
 inv=list(csv.DictReader((root/'documentation/figure_inventory.csv').open()))
 figs={int(x['figure']) for x in inv};defs=list((root/'figures').glob('*/rois.json'))
 if defs:
  subprocess.run([sys.executable,'-B',str(root/'scripts/audit_vertices.py')],check=True)
  cmd=[sys.executable,'-B',str(root/'scripts/measure_flatmaps.py'),'--rebuild']
  if a.java:cmd+=['--java',a.java]
  if a.ij_jar:cmd+=['--ij-jar',a.ij_jar]
  subprocess.run(cmd,check=True)
  subprocess.run([sys.executable,'-B',str(root/'scripts/audit_geometry.py')],check=True)
  v=json.loads((root/'documentation/validation.json').read_text());v['geometry_overlap_audit']='passed; no undeclared interior overlaps; explicitly declared parent/subregion pairs are non-additive'
 else:
  if not inv or any(x['processing_status']!='assessed_excluded' for x in inv):raise ValueError('No ROIs, but source assessment does not explicitly exclude all figures')
  fields=METADATA+['scale_length_mm','scale_length_px','source_roi_file','label','is_outline','extent','area_px2','area_mm2','percent_of_drawn_neocortex','percent_of_drawn_outline','sensitivity_low_mm2','sensitivity_high_mm2','status','boundary_note']
  write_csv(root/'data/measurements.csv',[],fields)
  write_csv(root/'data/view_index.csv',[],METADATA+['measured_fields','unmeasured_fields'])
  write_csv(root/'data/hemisphere_summary.csv',[],['map_id','species','specimen','figure','neocortex_pixels','neocortex_mm2'])
  v=dict(processed_views=0,measured_fields=0,unmeasured_fields=0,native_imagej_roundtrip='not_applicable; no eligible specimen ROI',anatomical_review='not_applicable; all figures excluded',reference_comparison='not_requested')
  (root/'review/gallery.html').write_text('<!doctype html><meta charset="utf-8"><title>Figure assessment</title><style>body{font:16px Arial;max-width:1100px;margin:32px auto}img{max-width:95%}td{padding:10px;border-bottom:1px solid #ddd}</style><h1>No eligible individual specimen flatmaps</h1><p>Measurement and summary tables have zero observations. No ImageJ ROI was invented from a schematic or projected view.</p>')
 rscript=shutil.which('Rscript')
 if not rscript:raise RuntimeError('Base R/Rscript is needed for summaries')
 subprocess.run([rscript,'scripts/export_summary.R'],cwd=root,check=True)
 # Separate review previews: these are not the canonical measurement crops/calibration.
 pdf=pdfium.PdfDocument(root/'source/paper.pdf');dest=root/'review/source_pages';dest.mkdir(exist_ok=True)
 for page in sorted({int(x['pdf_page']) for x in inv}):
  im=pdf[page-1].render(scale=1.2).to_pil();im.thumbnail((900,1250));im.save(dest/f'page{page:02}.png')
 marker='<!-- all-figure-assessment -->';gp=root/'review/gallery.html';s=gp.read_text().split(marker)[0]
 s+=marker+'<hr><h1>All-figure source assessment</h1><p>'+html.escape(root.name)+f': {len(figs)} numbered figures assessed; {v["measured_fields"]} field/fragment measurements. '
 s+='Saved observations, where present, are provisional. No certified complete-neocortex denominator is available.</p><p><a href="../documentation/figure_inventory.csv">Figure inventory</a> · <a href="../documentation/methods.md">Methods and limits</a> · <a href="../data/measurements.csv">Measurements</a> · <a href="../data/field_area_summary.csv">Complete-field absolute-area summary</a></p>'
 for x in inv:
  label='Figure '+x['figure']+(' '+x['panel'] if x['panel'] else '')+' — '+x['processing_status']
  s+='<details><summary>'+html.escape(label)+'</summary><p>'+html.escape(x['interpretation']+'. '+x['reason_or_result'])+'</p>'
  if x['linked_main_map']:s+='<p>Main maps: '+html.escape(x['linked_main_map'])+'</p>'
  s+=f'<p>PDF page{x["pdf_page"]}; review preview only.</p><img style="max-width:95%" src="source_pages/page{int(x["pdf_page"]):02}.png" alt="Original source page"></details>'
 gp.write_text(s)
 pending=sum(1 for f in defs for r in json.loads(f.read_text()).get('unmeasured',[]) if r.get('status')=='not_yet_digitized')
 unresolved=sum(1 for f in defs for r in json.loads(f.read_text()).get('unmeasured',[]) if r.get('status')=='needs_anatomical_review')
 v.update(not_yet_digitized_fields=pending,pending_anatomical_review_fields=unresolved,fully_digitized=(pending+unresolved==0),all_numbered_figures_assessed=True,numbered_figures_assessed=len(figs),assessment_status=('eligible_views_digitized_provisional' if v['measured_fields'] else 'assessed_no_defensible_field_contours') if defs else 'no_eligible_specimen_flatmaps',whole_neocortex_summary='unavailable; no independently established complete-neocortex view',source_visual_review='completed; anatomical certification pending' if defs else 'all source figures and captions inspected')
 if pending:v['assessment_status']='partially_digitized; named fields remain pending'
 elif unresolved:v['assessment_status']='defensible contours measured; unresolved anatomical boundaries remain NA'
 (root/'documentation/validation.json').write_text(json.dumps(v,indent=2)+'\n')
 manifest.update(processing_status=v['assessment_status'],numbered_figures_assessed=len(figs));(root/'source/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for f in (root/'figures').glob('*/draft.png'):f.unlink()
 revision_review=root/'scripts/review_line_refinement.py'
 if revision_review.exists():
  subprocess.run([sys.executable,'-B',str(revision_review)],check=True)
  gp.write_text(gp.read_text().replace('<hr><h1>All-figure', '<p><a href="line_refinement.html">Refined contours: enlarged source toggles and before/after comparison</a></p><hr><h1>All-figure'))
 subprocess.run([sys.executable,'-B',str(root/'scripts/build_precision_review.py')],check=True)
 gp.write_text(gp.read_text()+'<p><a href="precision_review.html">Enlarged source-toggle precision review</a></p>')
 files=[p for name in ['source','figures','data','scripts','review','documentation'] for p in (root/name).rglob('*') if p.is_file() and p.name!='checksums.json' and '__pycache__' not in p.parts]
 (root/'documentation/checksums.json').write_text(json.dumps({str(p.relative_to(root)):digest(p) for p in files},indent=2)+'\n')
 subprocess.run([sys.executable,'-B',str(root/'scripts/measure_flatmaps.py'),'--verify'],check=True)
 print(root.name,': final rebuild and verification passed',flush=True)
if __name__=='__main__':main()
