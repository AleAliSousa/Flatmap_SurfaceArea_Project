#!/usr/bin/env python3
"""Rebuild saved ImageJ geometry, R summaries and precision review without changing source contours."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--java');ap.add_argument('--ij-jar');a=ap.parse_args();root=Path(__file__).resolve().parents[1]
 old=json.loads((root/'documentation/validation.json').read_text())
 subprocess.run([sys.executable,str(root/'scripts/audit_vertices.py')],check=True)
 cmd=[sys.executable,str(root/'scripts/measure_flatmaps.py'),'--rebuild']
 if a.java:cmd+=['--java',a.java]
 if a.ij_jar:cmd+=['--ij-jar',a.ij_jar]
 subprocess.run(cmd,check=True)
 subprocess.run([sys.executable,str(root/'scripts/audit_geometry.py')],check=True)
 subprocess.run(['Rscript','scripts/export_summary.R'],cwd=root,check=True)
 subprocess.run([sys.executable,str(root/'scripts/build_precision_review.py')],check=True)
 v=json.loads((root/'documentation/validation.json').read_text())
 if 'precision_audit' in old:v['prior_precision_audit']=old['precision_audit']
 v.update(full_dataset_recheck_date='2026-10-16',geometry_overlap_audit='passed; no overlap after removing shared-border raster slivers',anatomical_certification=False)
 (root/'documentation/validation.json').write_text(json.dumps(v,indent=2)+'\n')
 files=[p for n in ['source','figures','data','scripts','review','documentation'] for p in (root/n).rglob('*') if p.is_file() and p.name!='checksums.json' and '__pycache__' not in p.parts]
 (root/'documentation/checksums.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
 subprocess.run([sys.executable,str(root/'scripts/measure_flatmaps.py'),'--verify'],check=True)
 print(root.name,'final rebuild passed')
if __name__=='__main__':main()
