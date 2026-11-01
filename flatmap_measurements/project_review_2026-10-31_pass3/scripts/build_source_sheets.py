from pathlib import Path
import csv,json,math,hashlib,re
from PIL import Image,ImageDraw,ImageFont
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parents[3];FM=ROOT/'flatmap_measurements';OUT=Path(__file__).resolve().parents[1];S=OUT/'source_sheets';S.mkdir(exist_ok=True);P=OUT/'source_pages';P.mkdir(exist_ok=True)
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',17);small=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',14);allrows=[];sheets=[];baseline=[]
for root in sorted(FM.iterdir()):
 if not (root/'source/paper.pdf').exists():continue
 inv=root/'documentation/figure_inventory.csv'
 if not inv.exists():inv=root/'documentation/paper_figure_inventory.csv'
 rows=list(csv.DictReader(inv.open())) if inv.exists() else []
 pagefig={}
 for r in rows:
  v=r.get('pdf_page',r.get('pdf_pages',r.get('page','')))
  pages=[]
  for part in re.split(r'[,;]',str(v)):
   nums=re.findall(r'\d+',part)
   if len(nums)==2 and re.search(r'[-–—]',part):pages.extend(range(int(nums[0]),int(nums[1])+1))
   elif len(nums)==1:pages.append(int(nums[0]))
  for page in pages:pagefig.setdefault(page,[]).append(str(r.get('figure','')))
 for f in sorted((root/'figures').glob('*/rois.json')):
  d=json.loads(f.read_text());baseline.append(dict(paper_id=root.name,map_id=f.parent.name,path=str(f.relative_to(FM)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),roi_count=len(d['rois']),unmeasured=d.get('unmeasured',[])))
  if d.get('pdf_page'):pagefig.setdefault(int(d['pdf_page']),[]).append(str(d.get('figure','')))
 # Catch figure continuation pages omitted by the original one-row-per-figure inventories.
 pdf=pdfium.PdfDocument(root/'source/paper.pdf')
 for idx in range(len(pdf)):
  tp=pdf[idx].get_textpage();txt=tp.get_text_range();tp.close()
  for match in re.finditer(r'(?mi)^\s*(?:fig(?:ure)?\.?)\s*(\d+)\s*[.(:]',txt):pagefig.setdefault(idx+1,[]).append(match.group(1))
 if not pagefig:
  pdf.close();continue
 cards=[]
 for page in sorted(pagefig):
  source=root/'review/source_pages'/f'page{page:02}.png'
  if not source.exists():
   if pdf is None:pdf=pdfium.PdfDocument(root/'source/paper.pdf')
   source=P/f'{root.name}__p{page:03}.png';im=pdf[page-1].render(scale=1.4).to_pil();im.save(source)
  else:im=Image.open(source).convert('RGB')
  card=Image.new('RGB',(680,925),'white');dr=ImageDraw.Draw(card);label=f'{root.name} / PDF {page} / Fig '+','.join(sorted(set(pagefig[page])));dr.text((8,8),label,font=small,fill='black');im.thumbnail((664,885));card.paste(im,((680-im.width)//2,35));cards.append((page,card));allrows.append(dict(paper_id=root.name,pdf_page=page,figures=';'.join(sorted(set(pagefig[page]))),source_image=str(source.relative_to(FM)),status='pending_visual_screening'))
 for start in range(0,len(cards),4):
  group=cards[start:start+4];sheet=Image.new('RGB',(1360,925*math.ceil(len(group)/2)),'#dce6e2')
  for i,(_,card) in enumerate(group):sheet.paste(card,((i%2)*680,(i//2)*925))
  name=root.name+f'_{start//4+1:02}.jpg';sheet.save(S/name,quality=90);sheets.append(dict(paper_id=root.name,sheet=name,pages=[x[0] for x in group]))
 if pdf:pdf.close()
(OUT/'source_sheets.json').write_text(json.dumps(sheets,indent=2)+'\n');((OUT/'baseline.json').write_text(json.dumps(baseline,indent=2)+'\n') if not (OUT/'baseline.json').exists() else None);(OUT/'source_page_inventory.json').write_text(json.dumps(allrows,indent=2)+'\n');print(len(allrows),'source pages,',len(sheets),'source sheets',flush=True)
