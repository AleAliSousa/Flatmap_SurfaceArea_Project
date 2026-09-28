"""Rebuild or verify all saved whole, partial and summary views through one workflow.

Canonical inputs: source/paper.pdf, source/manifest.json, figures/figNN/rois.json.
Figure 20 uses the same code as every other figure. Per-figure raster settings
remain in its JSON to preserve all original scientific measurements.
"""
from pathlib import Path
import argparse,base64,csv,hashlib,html,io,json,math,shutil,subprocess,sys,tempfile,zipfile
import numpy as np
import pypdfium2 as pdfium
from PIL import Image,ImageDraw,ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'; FIGURES=ROOT/'figures'; REVIEW=ROOT/'review'; DOCS=ROOT/'documentation'
TOTALS={}
def folder(f): return FIGURES/(f if isinstance(f,str) else f'fig{f:02d}')
def all_maps(): return sorted(p.parent.name for p in FIGURES.glob('*/rois.json'))
def definition(f): return json.loads((folder(f)/'rois.json').read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def total_mask(f):
    if f in TOTALS: return TOTALS[f]
    d=definition(f)
    if 'map_id' in d:
        size=Image.open(folder(f)/'source.tif').size
        if d.get('whole_manual_polygon'): return poly_mask([d['whole_manual_polygon']],size[::-1])>=.5
        return np.ones(size[::-1],dtype=bool)
    with zipfile.ZipFile(folder(f)/'Masks.tif.zip') as z:
        with Image.open(io.BytesIO(z.read(z.namelist()[0]))) as im:
            im.seek(0);return np.array(im)>0



PALETTE={'17':'#0072b2','18':'#56b4e9','DM':'#e69f00','DI':'#cc79a7','DL':'#009e73','MT':'#d55e00','MST':'#8a5ab5','FST':'#d6a000','3b':'#208b87','3a':'#8e6f3e','1':'#576fa6','2':'#bd6259','SII':'#4871b2','PV/IG':'#ad5865','PV':'#ad5865','AI':'#55853b','FEF':'#956497','FV':'#3c8aa2','Motor & Premotor':'#808040','C':'#9a613c'}

RANGES={
 'Saimiri sciureus':{'17':[13.7,19.9],'18':[6.5,9.4],'DL':[3.4,5.7],'DM':[1.2,1.8],'DI':[.9,1.4],'FST':[2.4,3.2],'MT':[1.1,1.6],'MST':[1.1,1.8]},
 'Aotus trivirgatus':{'17':[6.7,18.4],'18':[5.,9.2],'DL':[2.2,4.2],'DM':[1.5,2.4],'DI':[1.3,1.8],'FST':[1.2,2.1],'MT':[1.3,2.1],'MST':[1.1,1.8]},
 'Callithrix jacchus':{'17':[15.7,22.3],'18':[7.5,9.6],'DL':[3.1,4.4],'DM':[1.1,1.8],'DI':[1.7,2.8],'FST':[1.7,2.7],'MT':[1.5,2.3],'MST':[1.1,1.7]},
 'Galago senegalensis':{'17':[13.5,19.6],'18':[4.4,8.0],'DL':[2.,2.9],'DM':[.6,1.2],'DI':[.7,1.4],'FST':[1.8,2.7],'MT':[1.9,2.5],'MST':[1.4,2.2]}}

def morph(mask,r,erode):
    h,w=mask.shape;p=np.pad(mask,r,constant_values=False);out=np.ones_like(mask) if erode else np.zeros_like(mask)
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            if dx*dx+dy*dy<=r*r:
                q=p[r+dy:r+dy+h,r+dx:r+dx+w]
                if erode:out &= q
                else:out |= q
    return out

def whole_mask(im,d):
    ink=Image.fromarray(np.uint8(np.array(im.convert('L'))<d['threshold'])*255).copy()
    draw=ImageDraw.Draw(ink)
    for line in d.get('whole_repairs',[]):draw.line([tuple(p) for p in line],fill=255,width=2)
    if d['barrier_dilation_px']:ink=ink.filter(ImageFilter.MaxFilter(2*d['barrier_dilation_px']+1))
    white=Image.fromarray(255-np.array(ink)).copy();ImageDraw.floodfill(white,(0,0),127)
    enclosed=Image.fromarray(np.uint8(np.array(white)!=127)*255).copy()
    selected=np.zeros_like(np.array(enclosed),dtype=bool)
    for seed in d['whole_seeds']:
        part=enclosed.copy();ImageDraw.floodfill(part,tuple(seed),128);selected |= np.array(part)==128
    selected=morph(selected,d['edge_inset_px'],True)
    # Remove small arrow/letter components disconnected by the stroke inset.
    pruned=np.zeros_like(selected)
    for seed in d['whole_seeds']:
        component=Image.fromarray(np.uint8(selected)*255).copy()
        if not selected[seed[1],seed[0]]:raise ValueError(f'Whole-tissue seed is outside mask: {seed}')
        ImageDraw.floodfill(component,tuple(seed),128);pruned |= np.array(component)==128
    for polygon in d.get('whole_exclusions',[]):pruned &= poly_mask([polygon],pruned.shape)<.5
    return pruned

def poly_mask(polys,shape,ss=3):
    h,w=shape;im=Image.new('L',(w*ss,h*ss));draw=ImageDraw.Draw(im)
    for poly in polys:draw.polygon([(round((x+.5)*ss),round((y+.5)*ss)) for x,y in poly],fill=255)
    return np.array(im,dtype=np.float32).reshape(h,ss,w,ss).mean(axis=(1,3))/255

def measure(d):
    f=d['figure'];im=Image.open(folder(f)/'source.tif').convert('RGB');total=whole_mask(im,d)
    if d.get('whole_manual_polygon'):
        total=poly_mask([d['whole_manual_polygon']],total.shape)>=.5
    calibrated=bool(d.get('scale_endpoints_px'))
    n=int(total.sum());bar=math.dist(*d['scale_endpoints_px']) if calibrated else float('nan');factor=(d['scale_length_mm']/bar)**2
    assert n>20000,f'Figure {f}: open contour / incomplete component ({n} px)'
    TOTALS[f]=total
    base=dict(figure=f,pdf_page=d['pdf_page'],printed_page=d['printed_page'],specimen=d['specimen'],species=d['species_as_reported'],hemisphere='not assigned',scale_length_mm=d['scale_length_mm'],scale_length_px=bar,source_roi_file=f'../figures/fig{f:02d}/rois.json')
    lo=(d['scale_length_mm']/(bar+2))**2;hi=(d['scale_length_mm']/(bar-2))**2
    rows=[dict(base,label='Neocortex outline',area_px2=n,area_mm2=n*factor,percent_of_drawn_neocortex=100.,sensitivity_low_mm2=float(morph(total,1,True).sum())*lo,sensitivity_high_mm2=float(morph(total,1,False).sum())*hi,status='provisional image-derived estimate',boundary_note='Total drawn tissue, repaired at documented small scan gaps if needed; no shrinkage correction.')]
    rgba=im.convert('RGBA');masks=[];audit=[]
    for r in d['rois']:
        frac=poly_mask(r['polygons'],total.shape,d.get('supersample',3));unclipped=float(frac.sum());frac*=total;px=float(frac.sum());mask=frac>=.5;masks.append(mask)
        outside=unclipped-px
        if outside/max(unclipped,1)>.03 and not r.get('clip_to_tissue'):audit.append(f"{r['label']}: {outside/unclipped:.1%} of polygon clipped at tissue border")
        rows.append(dict(base,label=r['label'],area_px2=px,area_mm2=px*factor,percent_of_drawn_neocortex=100*px/n,sensitivity_low_mm2=float(morph(mask,2,True).sum())*lo,sensitivity_high_mm2=float((morph(mask,2,False)&total).sum())*hi,status='provisional image-derived estimate',boundary_note=r['boundary_note']))
        color=PALETTE.get(r['label'],'#9670b0');rgb=[int(color[i:i+2],16) for i in (1,3,5)];a=np.zeros((im.height,im.width,4),dtype=np.uint8);a[mask]=rgb+[55];a[mask&~morph(mask,1,True)]=rgb+[255];rgba=Image.alpha_composite(rgba,Image.fromarray(a))
    for r in d['unmeasured']:rows.append(dict(base,label=r['label'],area_px2='',area_mm2='',percent_of_drawn_neocortex='',sensitivity_low_mm2='',sensitivity_high_mm2='',status='not measurable from complete field boundary',boundary_note=r['reason']))
    edge=np.zeros((im.height,im.width,4),dtype=np.uint8);edge[total&~morph(total,1,True)]=[0,125,135,255];rgba=Image.alpha_composite(rgba,Image.fromarray(edge))
    # Calibration endpoints are shown separately from areal outlines.
    dr=ImageDraw.Draw(rgba)
    for x,y in d.get('scale_endpoints_px',[]):dr.line([(x-4,y),(x+4,y)],fill='#c00035',width=1);dr.line([(x,y-4),(x,y+4)],fill='#c00035',width=1)
    rgba.convert('RGB').save(folder(f)/'tracing.png')
    overlaps=[]
    for i in range(len(masks)):
        for j in range(i+1,len(masks)):
            inter=morph(masks[i],1,True)&morph(masks[j],1,True);count=int(inter.sum())
            if count>5:overlaps.append(dict(a=d['rois'][i]['label'],b=d['rois'][j]['label'],interior_overlap_px=count))
    if not calibrated:
        audit.append(d.get('scale_note','Missing scale line; absolute areas unavailable.'))
        for row in rows:
            for key in ['area_mm2','sensitivity_low_mm2','sensitivity_high_mm2','scale_length_px']:row[key]=''
            if row['area_px2']!='':row['status']='provisional pixels and proportions only; no visible calibration line'
    summary=dict(figure=f,specimen=d['specimen'],total_area_mm2=n*factor if calibrated else None,total_pixels=n,scale_length_px=bar if calibrated else None,measured_fields=len(d['rois']),missing_fields=len(d['unmeasured']),warnings=audit,overlaps=overlaps)
    return rows,summary

def write_csv(path,rows):
    with path.open('w',newline='') as fp:
        writer=csv.DictWriter(fp,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def n(v,places=1):return f'{float(v):.{places}f}' if v!='' else 'unavailable'

def datauri(path):
    out=io.BytesIO()
    with Image.open(path) as im: im.convert('RGB').save(out,format='PNG')
    return 'data:image/png;base64,'+base64.b64encode(out.getvalue()).decode()

def maskuri(mask):
    out=io.BytesIO();Image.fromarray(np.uint8(mask)*255).save(out,format='PNG')
    return 'data:image/png;base64,'+base64.b64encode(out.getvalue()).decode()


def render_sources():
    manifest=json.loads((ROOT/'source/manifest.json').read_text())
    pdf=ROOT/'source/paper.pdf'
    if digest(pdf)!=manifest['source_sha256']:
        raise ValueError('Source PDF differs from the digitized original; check registration before reusing ROIs.')
    doc=pdfium.PdfDocument(str(pdf))
    for d in manifest['crops']:
        im=doc[d['pdf_page']-1].render(scale=d['pdf_render_scale']).to_pil().convert('RGB').crop(tuple(d['crop_xyxy']))
        if list(im.size)!=d['source_size']:im=im.resize(tuple(d['source_size']),Image.Resampling.LANCZOS)
        # ImageJ adds calibration and a reversible overlay during export below.
        im.save(folder(d.get('map_id',d['figure']))/'source.tif')

def save_checksums():
    hashes={str(p.relative_to(ROOT)):digest(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in ['.DS_Store','checksums.json']}
    (DOCS/'checksums.json').write_text(json.dumps(hashes,indent=2)+'\n')

def verify_checksums():
    for name,expected in json.loads((DOCS/'checksums.json').read_text()).items():
        if not (ROOT/name).is_file() or digest(ROOT/name)!=expected:
            raise ValueError('File changed since the last rebuild: '+name)

def row_metadata(d,label):
    main='map_id' not in d
    roi=next((r for r in d['rois'] if r['label']==label),{})
    return dict(map_id=d.get('map_id',f"fig{d['figure']:02d}"),panel=d.get('panel',''),
        view_type=d.get('view_type','whole_hemisphere'),extent=roi.get('extent','complete') if roi else 'complete' if label=='Neocortex outline' else 'schematic_outline' if label==d.get('outline_label') else 'unmeasured',
        hemisphere_relation=d.get('hemisphere_relation','injected hemisphere'),linked_main_map=d.get('linked_main_map',''),
        specimen_link_status=d.get('specimen_link_status','main_reconstructed_case'),repeat_of=d.get('repeat_of',''),relationship_note=d.get('relationship_note',''),
        include_in_whole_hemisphere_summary=main,outline_scope=d.get('outline_scope','whole_drawn_neocortex'),
        percent_of_drawn_outline='',scale_note=d.get('scale_note','Own figure scale bar.'),
        scale_reference_map=d.get('scale_reference_map',''))

def measure_view(d):
    mid=d['map_id'];im=Image.open(folder(mid)/'source.tif').convert('RGB');total=total_mask(mid);TOTALS[mid]=total
    ends=d['scale_endpoints_px'];bar=math.dist(*ends) if ends else None;mm=d['scale_length_mm'];factor=(mm/bar)**2 if bar else None
    lo=(mm/(bar+2))**2 if bar else None;hi=(mm/(bar-2))**2 if bar else None
    base=dict(figure=d['figure'],pdf_page=d['pdf_page'],printed_page=d['printed_page'],specimen=d['specimen'],species=d['species_as_reported'],hemisphere='not assigned',scale_length_mm=mm or '',scale_length_px=bar or '',source_roi_file=f'../figures/{mid}/rois.json')
    selections=[];has_outline=bool(d.get('outline_label'))
    if has_outline:selections.append((d['outline_label'],total.astype(np.float32),'Schematic drawn tissue outline; not a measured experimental hemisphere.'))
    selections += [(r['label'],poly_mask(r['polygons'],total.shape,d.get('supersample',3))*total,r['boundary_note']) for r in d['rois']]
    rgba=im.convert('RGBA');rows=[];masks=[];warnings=[]
    for label,frac,note in selections:
        mask=frac>=.5;px=float(frac.sum());assert px>0,(mid,label)
        r=dict(base,label=label,area_px2=px,area_mm2=px*factor if factor else '',percent_of_drawn_neocortex='',
               sensitivity_low_mm2=float(morph(mask,2,True).sum())*lo if lo else '',
               sensitivity_high_mm2=float((morph(mask,2,False)&total).sum())*hi if hi else '',
               status='provisional image-derived estimate' if factor else 'uncalibrated schematic; pixels and proportions only',boundary_note=note)
        r.update(row_metadata(d,label));r['percent_of_drawn_outline']=100*px/float(total.sum()) if has_outline else '';rows.append(r)
        if label==d.get('outline_label'):continue
        masks.append((label,mask))
        color=PALETTE.get(label,'#9670b0');rgb=[int(color[i:i+2],16) for i in (1,3,5)];a=np.zeros((*mask.shape,4),dtype=np.uint8)
        a[mask]=rgb+[55];a[mask&~morph(mask,1,True)]=rgb+[255];rgba=Image.alpha_composite(rgba,Image.fromarray(a))
    for r in d['unmeasured']:
        row=dict(base,label=r['label'],area_px2='',area_mm2='',percent_of_drawn_neocortex='',sensitivity_low_mm2='',sensitivity_high_mm2='',status='boundary not measurable',boundary_note=r['reason'])
        row.update(row_metadata(d,r['label']));rows.append(row)
    if has_outline:
        a=np.zeros((*total.shape,4),dtype=np.uint8);a[total&~morph(total,1,True)]=[0,125,135,255];rgba=Image.alpha_composite(rgba,Image.fromarray(a))
    if not d.get('scale_endpoints_external'):
        draw=ImageDraw.Draw(rgba)
        for x,y in ends:draw.line([(x-4,y),(x+4,y)],fill='#c00035');draw.line([(x,y-4),(x,y+4)],fill='#c00035')
    rgba.convert('RGB').save(folder(mid)/'tracing.png')
    overlaps=[]
    for i,(la,a) in enumerate(masks):
        for lb,b in masks[i+1:]:
            count=int((morph(a,1,True)&morph(b,1,True)).sum())
            if count>5:overlaps.append(dict(a=la,b=lb,interior_overlap_px=count))
    return rows,dict(map_id=mid,figure=d['figure'],specimen=d['specimen'],total_area_mm2=float(total.sum())*factor if factor and has_outline else None,
        total_pixels=int(total.sum()) if has_outline else None,scale_length_px=bar,measured_fields=len(d['rois']),missing_fields=len(d['unmeasured']),warnings=warnings,overlaps=overlaps)

def export_imagej(rows,args):
    jars=sorted(Path('/Applications/Fiji.app/jars').glob('ij-[0-9]*.jar'))
    jar=Path(args.ij_jar) if args.ij_jar else (jars[0] if len(jars)==1 else None)
    if jar is None or not jar.is_file():raise FileNotFoundError('Specify --ij-jar with the installed ImageJ JAR path.')
    with tempfile.TemporaryDirectory(prefix='kk1990_masks_') as temp:
        tmp=Path(temp);jobs=[]
        for mid in all_maps():
            d=definition(mid);whole=total_mask(mid);ends=d['scale_endpoints_px'];size=d['scale_length_mm']/math.dist(*ends) if ends else 1.;unit='mm' if ends else 'pixel'
            saved={r['label']:r for r in rows if r['map_id']==mid}
            selections=[]
            label=d.get('outline_label') if 'map_id' in d else 'Neocortex outline'
            if label:selections.append((label,whole))
            selections += [(r['label'],(poly_mask(r['polygons'],whole.shape,d.get('supersample',3))*whole)>=.5) for r in d['rois']]
            if not selections:jobs.append([mid,-1,'',str(folder(mid)/'source.tif'),'',size,unit,0,'#007d87'])
            for i,(label,mask) in enumerate(selections):
                p=tmp/f'{mid}_{i:02d}.png';Image.fromarray(np.uint8(mask)*255).save(p)
                jobs.append([mid,i,label,str(folder(mid)/'source.tif'),str(p),size,unit,saved[label]['area_px2'],PALETTE.get(label,'#007d87' if i==0 else '#9670b0')])
        jobfile=tmp/'jobs.tsv'
        with jobfile.open('w',newline='') as fp:
            writer=csv.writer(fp,delimiter='\t');writer.writerow(['map_id','index','label','source','mask','pixel_size','unit','original_pixels','color']);writer.writerows(jobs)
        subprocess.run([args.java,'-Djava.awt.headless=true','-cp',str(jar),str(ROOT/'scripts/ImageJIO.java'),str(jobfile),str(FIGURES),str(DOCS)],check=True)
    checks=list(csv.DictReader((DOCS/'imagej_measurements.tsv').open(),delimiter='\t'));worst=max(checks,key=lambda r:abs(float(r['pixel_difference_percent'])))
    return dict(native_ROIs=len(checks),all_mask_ROI_TIFF_roundtrips_exact=all(r['roi_roundtrip_pixels_equal']=='true' for r in checks),
        calibrated_views=sum(bool(definition(m)['scale_endpoints_px']) for m in all_maps()),
        uncalibrated_views=[m for m in all_maps() if not definition(m)['scale_endpoints_px']],
        largest_binary_vs_fractional_difference_percent=abs(float(worst['pixel_difference_percent'])),largest_difference_map=worst['map_id'],
        largest_difference_label=worst['label'],runtime=(DOCS/'imagej_runtime.txt').read_text().strip(),gui_interaction_tested=False)

def build_review(rows,audits):
    maps=[];hemispheres=[];views=[];comparisons=[];scales=[]
    crops={d.get('map_id',f"fig{d['figure']:02d}"):d for d in json.loads((ROOT/'source/manifest.json').read_text())['crops']}
    for mid in all_maps():
        d=definition(mid);rr=[r for r in rows if r['map_id']==mid];audit=next(x for x in audits if x['map_id']==mid);main='map_id' not in d
        meta=row_metadata(d,'');outline=next((r for r in rr if r['label'] in ['Neocortex outline','Drawn schematic outline']),None)
        item=dict(map_id=mid,figure=d['figure'],panel=d.get('panel',''),pdf_page=d['pdf_page'],printed_page=d['printed_page'],specimen=d['specimen'],species=d['species_as_reported'],view_type=meta['view_type'],hemisphere_relation=meta['hemisphere_relation'],linked_main_map=meta['linked_main_map'],specimen_link_status=meta['specimen_link_status'],repeat_of=meta['repeat_of'],relationship_note=meta['relationship_note'],include_in_whole_hemisphere_summary=main,measured_fields=len(d['rois']),partial_fields=sum(r.get('extent')=='partial' for r in d['rois']),unmeasured_labels=len(d['unmeasured']),outline_scope=meta['outline_scope'],drawn_outline_mm2=outline['area_mm2'] if outline else '',calibration=d.get('scale_note','Own figure scale bar.'),source_image=f'../figures/{mid}/source.tif',traced_image=f'../figures/{mid}/tracing.png',roi_vertices=f'../figures/{mid}/rois.json')
        views.append(item)
        if main:
            hemispheres.append(dict(figure=d['figure'],pdf_page=d['pdf_page'],printed_page=d['printed_page'],specimen=d['specimen'],species=d['species_as_reported'],neocortex_mm2=outline['area_mm2'],neocortex_pixels=outline['area_px2'],measured_fields=len(d['rois']),unmeasured_labels=len(d['unmeasured']),calibration='visible scale line' if d['scale_endpoints_px'] else 'line absent; proportions only',source_image=item['source_image'],traced_image=item['traced_image'],roi_vertices=item['roi_vertices'],status='provisional, trace review required'))
            for row in rr:
                if row['label'] in RANGES[row['species']] and row['percent_of_drawn_neocortex']!='':
                    low,high=RANGES[row['species']][row['label']];pct=float(row['percent_of_drawn_neocortex'])
                    comparisons.append(dict(figure=d['figure'],specimen=row['specimen'],species=row['species'],field=row['label'],digitized_percent=pct,printed_species_min=low,printed_species_max=high,within_species_range=low<=pct<=high,comparison_type='species range only; Table 1 case identities not matched'))
        maps.append(dict(map_id=mid,metadata=d,view=item,rows=rr,source=datauri(folder(mid)/'source.tif'),trace=datauri(folder(mid)/'tracing.png'),mask=maskuri(total_mask(mid)),size=list(Image.open(folder(mid)/'source.tif').size)))
        c=crops[mid];ends=d['scale_endpoints_px'];bar=math.dist(*ends) if ends else None;points=bar/(c['resize_scale']*c['pdf_render_scale']) if bar else None
        scales.append(dict(map_id=mid,figure=d['figure'],specimen=d['specimen'],bar_tissue_mm=d['scale_length_mm'],bar_in_saved_image_pixels=bar,resize_scale=c['resize_scale'],bar_length_pdf_points=points,bar_length_printed_mm=points*25.4/72 if points else None,tissue_mm_per_pdf_point=d['scale_length_mm']/points if points else None,status=d.get('scale_note','measured own scale stroke') if bar else 'no visible scale stroke; not calibrated'))
    write_csv(DATA/'hemisphere_summary.csv',hemispheres);write_csv(DATA/'view_index.csv',views);write_csv(DOCS/'table1_range_check.csv',comparisons);write_csv(DOCS/'scale_comparison.csv',scales)
    build_html(maps);build_pdf(maps)
    return dict(views=len(maps),original_hemispheres=len(hemispheres),additional_views=len(maps)-len(hemispheres),traced_fields=sum(len(m['metadata']['rois']) for m in maps),whole_outlines=len(hemispheres),schematic_outlines=sum(bool(m['metadata'].get('outline_label')) for m in maps),absolute_area_rows=sum(r['area_mm2']!='' for r in rows),pixel_area_rows=sum(r['area_px2']!='' for r in rows),partial_area_rows=sum(r['extent']=='partial' for r in rows),unmeasured_rows=sum(r['area_px2']=='' for r in rows),range_checks=len(comparisons),outside_species_range=sum(not r['within_species_range'] for r in comparisons))

def build_html(maps):
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krubitzer &amp; Kaas 1990 · tracing review</title>
<style>*{box-sizing:border-box}body{font:15px/1.5 system-ui,sans-serif;color:#183243;background:#f2f5f7;margin:0}header,main,footer{max-width:1450px;margin:auto;padding:22px}h1{font-size:27px}h2{font-size:19px}a{color:#12688c}.card{background:white;padding:18px;border:1px solid #dce5e9;border-radius:9px;margin:15px 0}.bar{display:flex;gap:18px;align-items:center;flex-wrap:wrap}.views{display:grid;grid-template-columns:1fr 1fr;gap:18px}.frame{position:relative}.frame img{width:100%;display:block}.frame .overlay,.frame svg{position:absolute;inset:0;width:100%;height:100%}.frame svg{pointer-events:none}table{width:100%;border-collapse:collapse;font-size:13px}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}td.num{text-align:right;white-space:nowrap}tr.active{background:#d7edf7}tr[data-label]{cursor:pointer}.alert{background:#fff0d7;border-left:4px solid #ce8b29;padding:12px}.small{font-size:13px;color:#4f6675}select,button{font:inherit;padding:7px;max-width:100%}@media(max-width:800px){.views{grid-template-columns:1fr}header,main{padding:12px}}</style>
<header><h1>Krubitzer &amp; Kaas (1990): images and editable tracings</h1><p>Whole hemispheres, partial sections, opposite hemispheres, magnified views and summary drawings. Estimates are provisional and require anatomical review.</p><div class="bar"><a href="../data/measurements.csv">Measurements CSV</a><a href="../data/view_index.csv">View and specimen index</a><a href="../data/hemisphere_summary.csv">Original hemisphere summary</a><a href="comparison.pdf">Comparison PDF</a><a href="../README.md">Instructions</a></div></header>
<main><section class="card"><div class="bar"><label>View <select id="view"></select></label><label>Trace opacity <input id="opacity" type="range" min="0" max="1" step=".05" value="1"></label><button id="clear">Clear highlight</button></div><h2 id="title"></h2><p id="meta"></p><p id="scope" class="alert"></p><p id="scale" class="small"></p><div class="views"><div><h2>Published image</h2><div class="frame"><img id="source" alt="Published panel"></div></div><div><h2>Saved trace</h2><div class="frame"><img id="base" alt="Published panel beneath trace"><img class="overlay" id="trace" alt="Saved area tracing"><svg id="highlight"></svg></div></div></div><p class="small">Red crosses mark local scale endpoints. Turquoise outlines represent whole drawn tissue only where defined. Scale for all Figure 10 panels comes from B, as explicitly stated in the caption. Tracer marks and white arrows are not subtracted from cortical fields.</p><p id="files" class="bar"></p></section><section class="card"><h2>Measurements</h2><p id="detail">Select a field to highlight its saved contour.</p><div style="overflow:auto"><table><thead><tr><th>Field</th><th>Extent</th><th>mm²</th><th>% drawn outline</th><th>Boundary / limitation</th></tr></thead><tbody id="rows"></tbody></table></div></section></main><footer>Partial fields have no whole-neocortex denominator. Schematic percentages describe only the drawing. Repeated views must not be summed or counted as independent specimens. No tissue-shrinkage correction.</footer>
<script>const maps=MAPS_DATA;const $=s=>document.getElementById(s);const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const num=x=>x===''?'—':Number(x).toFixed(2);let current;
for(const m of maps){const o=document.createElement('option');o.value=m.map_id;o.textContent=m.map_id+' · '+m.view.specimen+' · '+m.view.species; $('view').appendChild(o);}
function highlight(label){document.querySelectorAll('tr[data-label]').forEach(r=>r.classList.toggle('active',r.dataset.label===label));const r=current.rows.find(r=>r.label===label);$('detail').textContent=r?label+' — '+r.boundary_note:'Select a field to highlight its saved contour.';const svg=$('highlight');svg.setAttribute('viewBox','0 0 '+current.size.join(' '));svg.innerHTML='';const roi=current.metadata.rois.find(r=>r.label===label);if(roi)svg.innerHTML='<defs><mask id="tissue"><image width="'+current.size[0]+'" height="'+current.size[1]+'" href="'+current.mask+'"/></mask></defs><g mask="url(#tissue)">'+roi.polygons.map(p=>'<polygon points="'+p.map(q=>q.join(',')).join(' ')+'" fill="#ffcc33" fill-opacity=".12" stroke="#b40042" stroke-width="2"/>').join('')+'</g>';}
function render(){current=maps.find(m=>m.map_id===$('view').value);const d=current.metadata,v=current.view; $('title').textContent=current.map_id+' · '+v.species+' · '+v.specimen;$('meta').textContent='PDF page '+v.pdf_page+' / printed '+v.printed_page+' · '+v.hemisphere_relation+' · '+v.measured_fields+' traced fields';$('scope').textContent=v.view_type.replaceAll('_',' ')+' — '+(v.view_type==='whole_hemisphere'?'Original individual-case reconstruction.':v.outline_scope==='schematic_tissue'?'Illustrative drawing; not an independent specimen measurement.':'Local view; no total-neocortex area or percentage.')+' '+v.relationship_note;$('scale').textContent=(d.scale_endpoints_px.length?d.scale_length_mm+' mm bar. ':'No physical calibration. ')+(d.scale_note||'Own figure scale.')+((d.linked_main_map)?' Linked main reconstruction: '+d.linked_main_map+'.':'');$('source').src=current.source;$('base').src=current.source;$('trace').src=current.trace;$('rows').innerHTML=current.rows.map(r=>'<tr data-label="'+esc(r.label)+'"><td>'+esc(r.label)+'</td><td>'+esc(r.extent)+'</td><td class="num">'+num(r.area_mm2)+'</td><td class="num">'+num(r.percent_of_drawn_outline)+'</td><td>'+esc(r.boundary_note)+'</td></tr>').join('');document.querySelectorAll('tr[data-label]').forEach(r=>r.onclick=()=>highlight(r.dataset.label));$('files').innerHTML=['source.tif','tracing.png','rois.json',...(v.measured_fields?['RoiSet.zip','Masks.tif.zip']:[])].map(f=>'<a href="../figures/'+current.map_id+'/'+f+'">'+f+'</a>').join('');highlight(null);}
$('view').onchange=render;$('opacity').oninput=()=>$('trace').style.opacity=$('opacity').value;$('clear').onclick=()=>highlight(null);$('view').value='fig25A';render();</script></html>'''
    (REVIEW/'gallery.html').write_text(page.replace('MAPS_DATA',json.dumps(maps,separators=(',',':'))))

def build_pdf(maps):
    from reportlab.lib.utils import simpleSplit
    w,h=landscape(A3);pdf=canvas.Canvas(str(REVIEW/'comparison.pdf'),pagesize=(w,h));pdf.setTitle('Krubitzer & Kaas 1990: source and trace review')
    for i,m in enumerate(maps):
        d=m['metadata'];v=m['view'];mid=m['map_id']
        pdf.setFillColorRGB(.08,.18,.24);pdf.setFont('Helvetica-Bold',18);pdf.drawString(24,h-31,f"{mid} | {v['species']} | {v['specimen']}")
        pdf.setFont('Helvetica',10);pdf.drawString(24,h-49,f"PDF p.{v['pdf_page']} / printed p.{v['printed_page']} | {v['view_type']} | PROVISIONAL manual digitization")
        scope='Whole drawn hemisphere' if v['view_type']=='whole_hemisphere' else 'Illustrative drawing; not an independent specimen' if v['outline_scope']=='schematic_tissue' else 'Partial/local view; no whole-neocortex denominator'
        pdf.drawString(24,h-65,scope+' | '+v['hemisphere_relation'])
        cw=430;top=h-100;maxh=h-195
        for ix,name in enumerate(['source.tif','tracing.png']):
            x=24+ix*445;im=Image.open(folder(mid)/name).convert('RGB');k=min(cw/im.width,maxh/im.height)
            pdf.setFont('Helvetica-Bold',10);pdf.drawString(x,top+9,'Published source' if ix==0 else 'Saved tracing')
            pdf.drawImage(ImageReader(im),x+(cw-im.width*k)/2,top-im.height*k,width=im.width*k,height=im.height*k)
        x=927;y=top;pdf.setFont('Helvetica-Bold',9);pdf.drawString(x,y,'Field');pdf.drawRightString(w-68,y,'mm2');pdf.drawRightString(w-22,y,'% outline');y-=18
        for r in m['rows']:
            label=r['label'].replace('Neocortex outline','Total outline').replace('Drawn schematic outline','Schematic outline')
            if r['extent']=='partial':label+=' *'
            pdf.setFont('Helvetica',8);pdf.drawString(x,y,label);pdf.drawRightString(w-68,y,n(r['area_mm2'],2) if r['area_mm2']!='' else '--');pdf.drawRightString(w-22,y,n(r['percent_of_drawn_outline'],2) if r['percent_of_drawn_outline']!='' else '--');y-=15
        notes=['* Visible fragment, not whole field.','Blank values mean unavailable.','See CSV/JSON for boundary notes.','ROI ZIP and masks preserve all traces.','No shrinkage correction.']
        for note in notes:pdf.drawString(x,y-13,note);y-=12
        text=v['relationship_note']+' '+(d.get('scale_note','Own figure scale bar.'))
        pdf.setFont('Helvetica',9)
        for j,line in enumerate(simpleSplit(text,'Helvetica',9,w-48)[:4]):pdf.drawString(24,70-j*12,line)
        pdf.drawRightString(w-24,20,f'{i+1} / {len(maps)}');pdf.showPage()
    pdf.save()

def verify():
    rows=list(csv.DictReader((DATA/'measurements.csv').open()));audits=json.loads((DOCS/'validation.json').read_text())['measurement_audit']
    assert {r['map_id'] for r in rows}==set(all_maps())
    selections=0
    for mid in all_maps():
        d=definition(mid);rr=[r for r in rows if r['map_id']==mid];main='map_id' not in d
        assert len({r['label'] for r in rr})==len(rr)
        assert Image.open(folder(mid)/'source.tif').size==Image.open(folder(mid)/'tracing.png').size
        outline=next((r for r in rr if r['label'] in ['Neocortex outline','Drawn schematic outline']),None)
        for r in rr:
            assert (DATA/r['source_roi_file']).resolve()==(folder(mid)/'rois.json').resolve()
            if not r['area_px2']:
                assert not r['area_mm2'] and not r['percent_of_drawn_neocortex'];continue
            px=float(r['area_px2']);assert px>0
            if outline:
                den=float(outline['area_px2']);assert px<=den and math.isclose(float(r['percent_of_drawn_outline']),100*px/den,rel_tol=1e-9)
            else:assert not r['percent_of_drawn_neocortex'] and not r['percent_of_drawn_outline']
            if not main:assert not r['percent_of_drawn_neocortex']
            if d['scale_endpoints_px']:
                factor=(d['scale_length_mm']/math.dist(*d['scale_endpoints_px']))**2;area=float(r['area_mm2']);assert math.isclose(area,px*factor,rel_tol=1e-9)
                assert float(r['sensitivity_low_mm2'])<=area<=float(r['sensitivity_high_mm2']),(mid,r['label'],'sensitivity')
            else:assert r['area_mm2']==''
        def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        polys=[(r['label'],p) for r in d['rois'] for p in r['polygons']]
        if d.get('whole_manual_polygon'):polys.append(('outline',d['whole_manual_polygon']))
        for label,p in polys:
            for i in range(len(p)):
                a,b=p[i],p[(i+1)%len(p)]
                for j in range(i+2,len(p)):
                    if i==0 and j==len(p)-1:continue
                    c,e=p[j],p[(j+1)%len(p)]
                    assert not(cross(a,b,c)*cross(a,b,e)<0 and cross(c,e,a)*cross(c,e,b)<0),(mid,label,'self-intersection',i,j)
        count=len(d['rois'])+bool(outline);selections+=count
        if count:
            with zipfile.ZipFile(folder(mid)/'RoiSet.zip') as z:
                assert z.testzip() is None and len(z.namelist())==count
                assert all(z.read(name)[:4]==b'Iout' for name in z.namelist())
    assert all(not a['overlaps'] for a in audits), 'Interior ROI overlap; inspect validation.json'
    assert len([r for r in rows if r['label']=='Neocortex outline'])==13
    assert all(not a['overlaps'] for a in audits if a['map_id'] in {f'fig{f}' for f in range(12,25)})
    print(f'Verified: {len(all_maps())} views, {selections} selections, calibration, scope, proportions, registration and polygon geometry.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    action=parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--rebuild',action='store_true',help='Regenerate baseline images, measurements, review and ImageJ exports from saved JSON traces.')
    action.add_argument('--verify',action='store_true',help='Check geometry, measurements and saved file hashes without changing files.')
    action.add_argument('--zip',type=Path,metavar='PATH',help='Create a portable ZIP outside this folder without rebuilding.')
    parser.add_argument('--java',default='/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home/bin/java')
    parser.add_argument('--ij-jar',default=None)
    args=parser.parse_args()
    if args.zip:
        target=args.zip.resolve()
        if target.is_relative_to(ROOT) or target.exists():raise ValueError('Choose a new ZIP filename outside this dataset folder.')
        verify_checksums()
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for name in json.loads((DOCS/'checksums.json').read_text()):z.write(ROOT/name,str(Path(ROOT.name)/name))
            z.write(DOCS/'checksums.json',str(Path(ROOT.name)/'documentation/checksums.json'))
        print('Saved',target);return
    if args.verify:
        verify_checksums();verify();return
    render_sources();rows=[];audits=[]
    for mid in all_maps():
        d=definition(mid)
        if 'map_id' in d:rr,aa=measure_view(d)
        else:
            rr,aa=measure(d);TOTALS[mid]=TOTALS[d['figure']]
            for row in rr:
                row.update(row_metadata(d,row['label']))
                row['percent_of_drawn_outline']=row['percent_of_drawn_neocortex']
            aa['map_id']=mid
        rows.extend(rr);audits.append(aa)
    write_csv(DATA/'measurements.csv',rows)
    imagej=export_imagej(rows,args);summary=build_review(rows,audits)
    (DOCS/'validation.json').write_text(json.dumps(dict(summary=summary,measurement_audit=audits,imagej=imagej),indent=2)+'\n')
    verify();save_checksums();print(json.dumps(summary,indent=2))

if __name__=='__main__':main()

