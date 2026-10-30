import json,pypdfium2 as p
from pathlib import Path
from PIL import ImageDraw
cfg=json.loads(Path('/tmp/m1_new_papers/views.json').read_text());out=Path('/tmp/m1_new_papers/crops');out.mkdir(exist_ok=True);docs={}
for v in cfg:
 f=out/(v['paper']+'__'+v['map_id']+'.png')
 if f.exists():continue
 if v['paper'] not in docs:docs[v['paper']]=p.PdfDocument(Path('flatmap_measurements')/v['paper']/'source/paper.pdf')
 im=docs[v['paper']][v['page']-1].render(scale=4).to_pil().convert('RGB').crop(tuple(round(x*2) for x in v['crop']));im.save(f)
