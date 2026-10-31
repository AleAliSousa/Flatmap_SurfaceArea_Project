from prepare_precision import *
import csv,io,html.parser,urllib.parse,re,shutil
changes=json.loads((OUT/'applied_changes.json').read_text());papers=sorted({c['paper'] for c in changes});overlaps=list(csv.DictReader((OUT/'validation/overlap_changes.csv').open()));checks=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cross(a,b,c):return (b[...,0]-a[...,0])*(c[...,1]-a[...,1])-(b[...,1]-a[...,1])*(c[...,0]-a[...,0])
for c in changes:
 f=FM/c['paper']/'figures'/c['map_id']/'rois.json';d=json.loads(f.read_text());r=next(r for r in d['rois'] if r['label']==c['label']);assert r==c['applied_new'];size=np.array(Image.open(f.parent/'source.tif').size)
 for poly in r['polygons']:
  p=np.array(poly,float);q=np.roll(p,-1,0);assert len(p)>=3 and np.isfinite(p).all() and (p>=0).all() and (p<size).all()
  for i in range(len(p)):
   js=np.arange(i+2,len(p));js=js[~((i==0)&(js==len(p)-1))]
   hit=(cross(p[i],q[i],p[js])*cross(p[i],q[i],q[js]) < -1e-8)&(cross(p[js],q[js],p[i])*cross(p[js],q[js],q[i]) < -1e-8)
   assert not hit.any(),(c['paper'],c['map_id'],c['label'],i,js[hit])
for paper in papers:
 root=FM/paper;cs=[c for c in changes if c['paper']==paper];z=zipfile.ZipFile(OUT/'before'/(paper+'.zip'));assert hashlib.sha256(z.read('source/paper.pdf')).hexdigest()==digest(root/'source/paper.pdf')
 review=dict(date='2026-10-31',pass_number=2,changed_regions=[dict(map_id=c['map_id'],label=c['label'],kind=c['kind'],note=c['note']) for c in cs],scope='All project views screened at overview resolution; changed regions reviewed enlarged. Anatomical certification remains pending.',source_pdf_unchanged=True,native_imagej_roundtrip='passed',remaining_interior_overlap_diagnostics=[r for r in overlaps if r['paper_id']==paper],project_review='../project_review_2026-10-31_pass2/index.html',no_new_calibration_or_denominator=True)
 (root/'documentation/second_pass_review.json').write_text(json.dumps(review,indent=2)+'\n')
 # Document changed figure counts without erasing previous historical action notes.
 if paper=='Krubitzer_1998':
  inv=root/'documentation/figure_inventory.csv';rs=list(csv.DictReader(inv.open()));marker=' Second precision pass 2026-10-31:'
  for row in rs:
   if row['figure']=='14':row['reason_or_result']=row['reason_or_result'].split(marker)[0]+marker+' squirrel summary M added in fig14D_summary. This is an illustrative field, not an independent animal. Current measurements and the second-pass review are authoritative for counts.'
  with inv.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
 gallery=root/'review/gallery.html';s=gallery.read_text();marker='<!-- second-pass-review -->';end='<!-- /second-pass-review -->';s=re.sub(re.escape(marker)+'.*?'+re.escape(end),'',s,flags=re.S)
 link=marker+'<p style="padding:16px;background:#fff0cc"><a href="../../project_review_2026-10-31_pass2/index.html?paper='+paper+'">Second precision pass: source/before/after comparisons and remaining limitations</a></p>'+end
 s=s.replace('<body>','<body>'+link,1) if '<body>' in s else s+link;gallery.write_text(s)
 files=[p for name in ['source','figures','data','scripts','review','documentation'] for p in (root/name).rglob('*') if p.is_file() and p.name!='checksums.json' and '__pycache__' not in p.parts]
 (root/'documentation/checksums.json').write_text(json.dumps({str(p.relative_to(root)):digest(p) for p in files},indent=2)+'\n')
 result=subprocess.run([sys.executable,'-B',str(root/'scripts/measure_flatmaps.py'),'--verify'],capture_output=True,text=True);assert result.returncode==0,(paper,result.stdout,result.stderr)
 checks.append(dict(paper_id=paper,verify='passed',output=result.stdout.strip(),source_pdf_unchanged=True));print(paper,'final verification passed',flush=True)
# All provisional Burman rejections must survive the new geometry.
burman=[r for f in (FM/'Burman_etal_2008/figures').glob('*/rois.json') for r in json.loads(f.read_text())['rois']];assert len(burman)==24 and all(r.get('status')=='rejected_pending_retrace' and r.get('analysis_eligible') is False for r in burman)
# Static document/link and JavaScript syntax checks; no browser automation bypass.
class Links(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ['href','src'] and v:self.links.append(v)
missing=[];js_count=0;node=shutil.which('node')
for page in [OUT/'index.html',*sorted((OUT/'views').glob('*.html'))]:
 text=page.read_text();parser=Links();parser.feed(text)
 for u in parser.links:
  link=urllib.parse.urlparse(u)
  if not link.scheme and link.path and not (page.parent/urllib.parse.unquote(link.path)).exists():missing.append((str(page),u))
 if node:
  for script in re.findall(r'<script[^>]*>(.*?)</script>',text,re.S):
   tmp=Path('/private/tmp/flatmap_pass2_check.js');tmp.write_text(script);p=subprocess.run([node,'--check',str(tmp)],capture_output=True,text=True);assert p.returncode==0,(page,p.stderr);js_count+=1
assert not missing,missing
assert all(int(r['after_interior_overlap_px'])==0 for r in overlaps if r['paper_id']=='Ghosh_1997')
result=dict(final_native_verification=checks,changed_region_bounds_and_crossings='passed',saved_geometry_matches_review_log=True,Burman_24_rejections_preserved=True,local_html_references='passed',inline_script_syntax_checks=js_count,browser_render_check='not_run; browser tool rejected local file URL protocol',overlap_diagnostic='Cat shared-edge interior overlaps resolved; Remple Fig7A residual4pixels and Burman V1/V2 residual15pixels remain explicitly documented; Remple Fig8 parent/subregion overlap intentional.',cross_project_analysis_snapshots='not recomputed; publication measurements and second-pass review are current')
(OUT/'validation/final_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('All final checks passed; JS scripts:',js_count,flush=True)
