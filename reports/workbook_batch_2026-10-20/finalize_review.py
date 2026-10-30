#!/usr/bin/env python3
"""Build the batch review from saved canonical geometry and native measurements."""
from pathlib import Path
import collections, csv, hashlib, html, json, subprocess, sys

ROOT = Path(__file__).resolve().parents[2]
REPORT = Path(__file__).resolve().parent
BASE = ROOT / 'flatmap_measurements'
PAPERS = sorted(json.loads((REPORT / 'inventory.json').read_text()))
ESC = html.escape

NOTES = {
    'Brecht_Freiwald_2012': 'Figure 3a–d: human, macaque, mouse and naked mole-rat illustrative maps, all right hemispheres. S1-face is a subset of S1 and must not be added to it. Human, macaque and mole-rat use their own printed bars. The mouse flatmap has no unambiguously assigned local bar and remains pixel-only. The independent gray outline is schematic tissue, not a certified animal neocortex denominator.',
    'Catania_Remple_2002': 'Figure 2 is case 4: eight somatotopic compartments and their S1 union. Compartments and the union are non-additive. Figure 4A/B are comparative drawings with local 2 mm and 1 mm bars; they are not extra identified animals. Recording dots do not establish a closed S2/PV border in figure 2. Figure 4C is a section photograph with lesion sites, without an independently closed areal perimeter.',
    'Haug_1987': 'All 13 numbered figures were assessed. Statistical graphs and cross-sectional cortical histology do not provide planar field envelopes. No ROI or surface area was inferred from the workbook, reported volume, thickness, regression or graphs. The measurement tables are intentionally empty.',
    'Krubitzer_2009': 'Figures 4, 5 and 7 yield eleven illustrative views. Figure 4 is unscaled. Figures 5 and 7 use their printed local bars. Motor, parietal and small visual boundaries were inspected at enlargement; CM/MM is retained as a combined field where the printed divider is absent. Named parent domains explicitly include their child fields and are non-additive. Open background regions are NA rather than flood-filled through boundary gaps.',
    'Krubitzer_Dooley_2013': 'Fourteen illustrative views cover figures 1, 2, 6C, 7 and 8A. Figure 7 somatotopic drawings are pixel-only. Other views use the applicable printed bars. The ghost bat is Macroderma gigas; developmental fruit-bat panels do not change that identification. FST subdivisions without separate closed borders remain NA. Enucleated-opossum domains explicitly include the named child fields; these are not additive observations or independent specimens.',
    'Krubitzer_Prescott_2018': 'Six illustrative views cover figures 2, 4, 8C and 9A. Printed scale bars are used independently of other publications. Figure 8C is the ghost bat Macroderma gigas and mouse comparison; A/B are developmental/body-morphology images. Combined multimodal envelopes overlap their explicitly named subregions and must not be summed. These published summaries are not newly identified animals.',
    'Mayer_etal_2019': 'Eight views represent four identified left-hemisphere cases, identified by the source as Sapajus spp. Figures 1/2 measure the sampled M1 response territory, not complete M1. Figure 5 measures sampled digit/toe territory, a digit union and printed-color components within the source M1 limits. Color components estimate visible color shares: they do not reproduce the authors’ exact half-tile allocation for mixed responses (PDF page 6), and stripe edges are not anatomical field borders. All these observations are partial and excluded from complete-field means. White electrode circles remain tissue; larger no-response/unsampled gaps are retained. The four figure 10 threshold recodings are repeated views of the same maps. No whole-M1 total is inferred.',
    'Rosa_etal_1993': 'Six right-hemisphere case maps (figures 5A–10A) and two composite schematics (3C, 11) are measured. Case-map bars are 10 mm, without shrinkage correction; schematics remain pixel-only. Source taxonomy is Cebus apella. Thick tissue/sulcal outlines and black/striped tracer deposits are not substituted for thin areal boundaries. V1 envelopes include their internal sulcal and tracer marks. External POm leaders identify medial compartments in cases 2/3. LIP and MST are combined where subdivisions are not separately traced. Thirty-five case-field boundaries remain needs_anatomical_review with NA area; other absent or non-independent outlines have explicit reasons. These are defensible provisional contours, not a completed anatomical parcellation.',
    'VanEssen_2005': 'Figure 9A/B are right-hemisphere PALS-B12 atlas layouts, not identified individual animals. There is no local physical bar or valid areal-distortion correction, so results remain pixels only. External leaders and enlarged color boundaries were used for BA24, narrow cortical bands, V2d/V3/V3a/V7/LO and orbitofrontal labels. BA33 is not independently resolved. Literal s/l/r/m labels and an unidentified yellow cut component are not assigned invented area identities. Two one-pixel border slivers exceed the drafting reconciler’s fractional cutoff but have no overlap after the native two-pixel interior erosion audit.',
    'Wilkinson_2021': 'Figure 4 is an unscaled human atlas adaptation. Seven field/component observations include the cut V1 pieces, visual domains, S1, M1 and SII. M1 follows the black boundary; red leader lines are annotations. No scale is borrowed from Van Essen and Drury or from a different paper. This atlas view supplies no independent animal or complete-neocortex denominator.'
}
PANEL_NOTES = {
    ('Brecht_Freiwald_2012','3'): 'Panels a–d are measured separately.',
    ('Catania_Remple_2002','4'): 'Panels A/B are measured. C is a flattened-section photograph with lesion markers but no independently closed field perimeter.',
    ('Krubitzer_Dooley_2013','6'): 'Panel C mouse/bat cortical maps are measured; A/B show development and forelimb morphology, not cortical field surfaces.',
    ('Krubitzer_Dooley_2013','8'): 'Panel A cortical maps are measured; B is a connectivity illustration, not another independent areal reconstruction.',
    ('Krubitzer_Prescott_2018','8'): 'Panel C cortical maps are measured; A/B show developmental/body morphology, not cortical field surfaces.',
    ('Krubitzer_Prescott_2018','9'): 'Panel A cortical maps are measured; B shows connectivity rather than another independent field-area observation.',
    ('Rosa_etal_1993','3'): 'C is the planar schematic; A/B show folded/partly exposed cortical anatomy, not an additional planar surface measurement.',
    ('VanEssen_2005','9'): 'A/B flat atlases are measured. C–I are folded/spherical/registration representations, not independent flat field areas.'
}
for fig in range(5,11):
    PANEL_NOTES[('Rosa_etal_1993',str(fig))] = 'Panel A is the planar case map. B shows parasagittal sections and is excluded from cortical surface-area measurement.'

METHOD = '''The source PDF is retained with a SHA-256 manifest. Source figures were rendered at four pixels per PDF point. Each crop, printed calibration and editable polygon is recorded in `figures/<map_id>/rois.json`; these saved coordinates are the authoritative measurement inputs.

External leaders were followed to their tissue endpoints. Lettering, numerals, recording circles, tracer deposits and internal shading were retained within anatomical envelopes. Source-guided curves used dense points and local smoothing at approximately one rendered pixel. Nearby dark ink could refine a guide within a bounded normal search; it could not choose an anatomical identity. Dark filled regions were traced at their external boundary rather than treating a white letter as the field. Color separation rejected white background and used local palette/shade information. Short gaps were bridged only where the visible neighboring border supported continuation. Approximate and partial observations retain those extent labels.

Adjacent manual guides were checked for overlap. Only narrow conflicts were reconciled to a common edge; broad conflicts required source review and a corrected perimeter. Exclusion polygons reuse inspected neighboring borders where needed. Explicit parent/subregion overlaps are allowed and non-additive; undeclared interior overlap fails validation. Thin shared-edge raster slivers are reported separately. Neither a successful geometry test nor dense vertices establish anatomical certainty.

Area is computed from the saved geometry at fourfold supersampling. Millimetres squared require an applicable printed bar; unscaled results remain pixels squared with NA physical area. Native ImageJ TIFF calibration, editable ROI ZIPs and saved masks were reopened and checked. Source-toggle reviews display both outer and dashed exclusion boundaries. Complete-field absolute summaries exclude partial/approximate, illustrative and unresolved observations. No view in this batch establishes a certified whole-neocortex denominator; no workbook numeric estimates were used.
'''

def rows(path):
    with path.open(newline='') as f: return list(csv.DictReader(f))

def write_csv(path, data, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    records=[]; all_meas=[]; unresolved=[]; inventory=[]; cards=[]; fields_all=[]
    for paper in PAPERS:
        p=BASE/paper
        defs=[json.loads(f.read_text()) for f in sorted((p/'figures').glob('*/rois.json'))]
        inv=rows(p/'documentation/figure_inventory.csv')
        meas=rows(p/'data/measurements.csv')
        pending=[dict(paper=paper,map_id=d['map_id'],label=r['label'],status=r['status'],reason=r.get('reason','')) for d in defs for r in d.get('unmeasured',[]) if r['status'] in ['not_yet_digitized','needs_anatomical_review']]
        unresolved+=pending
        for x in inv:
            maps=[d for d in defs if str(d['figure'])==x['figure']]
            if maps:
                n=sum(len(d['rois']) for d in maps); q=sum(r['status']=='needs_anatomical_review' for d in maps for r in d.get('unmeasured',[]))
                x['processing_status']='digitized_with_unresolved_boundaries' if q else 'digitized_provisional'
                x['linked_main_map']=';'.join(d['map_id'] for d in maps)
                x['reason_or_result']=f'{len(maps)} measured view(s), {n} field/component observations; {q} boundaries remain NA for anatomical review. Illustrative, partial, repeated and unscaled restrictions apply.'
            note=PANEL_NOTES.get((paper,x['figure']))
            if note and note not in x['reason_or_result']: x['reason_or_result']+=' '+note
            inventory.append(dict(paper=paper,**x))
        write_csv(p/'documentation/figure_inventory.csv',inv,list(inv[0]))
        fields=[]
        for d in defs:
            for r in d['rois']:
                fields.append(dict(paper=paper,map_id=d['map_id'],figure=d['figure'],label=r['label'],status='measured_provisional',extent=r.get('extent','complete'),reason=r.get('boundary_note','')))
            for r in d.get('unmeasured',[]):
                fields.append(dict(paper=paper,map_id=d['map_id'],figure=d['figure'],label=r['label'],status=r['status'],extent='',reason=r.get('reason','')))
        fields_all+=fields
        write_csv(p/'documentation/field_inventory.csv',fields,['paper','map_id','figure','label','status','extent','reason'])
        measured=[m for m in meas if m['area_px2'] not in ['', 'NA'] and m['is_outline'].lower()!='true']
        rec=dict(paper=paper,numbered_figures=len({x['figure'] for x in inv}),views=len(defs),field_components=sum(len(d['rois']) for d in defs),calibrated_field_components=sum(m['area_mm2'] not in ['', 'NA'] for m in measured),pixel_only_field_components=sum(m['area_mm2'] in ['', 'NA'] for m in measured),unresolved_anatomical_boundaries=len(pending))
        assert len(measured)==rec['field_components'], (paper,len(measured),rec)
        records.append(rec); all_meas += [dict(paper=paper,**m) for m in meas]
        (p/'documentation/methods.md').write_text('# Measurement method and limits\n\n'+METHOD+'\n## Source-specific assessment\n\n'+NOTES[paper]+'\n\n[Field-by-field inventory](field_inventory.csv) · [All numbered figures](figure_inventory.csv) · [Source-toggle review](../review/precision_review.html)\n')
        (p/'README.md').write_text(f'# {paper}\n\n{rec["numbered_figures"]} numbered figures assessed; {rec["views"]} views and {rec["field_components"]} provisional field/component measurements saved. Counts are observations, including overlapping domains and repeated drawings, not animals.\n\n'+NOTES[paper]+'\n\n[Source-toggle review](review/precision_review.html) · [All-figure assessment](review/gallery.html) · [Measurements](data/measurements.csv) · [Methods](documentation/methods.md) · [Field inventory](documentation/field_inventory.csv)\n\nRebuild from saved geometry with `python scripts/rebuild_all.py --java /path/to/java --ij-jar /path/to/ij.jar`. Python requires numpy, Pillow and pypdfium2; summaries require base R. `python scripts/measure_flatmaps.py --verify` checks saved outputs. Geometry is editable in each `figures/<map_id>/rois.json` or the corresponding native ImageJ ROI ZIP; coordinate changes must be rebuilt before use.\n')
        val=json.loads((p/'documentation/validation.json').read_text())
        assert val.get('native_imagej_roundtrip')=='passed' or not defs, (paper,val.get('native_imagej_roundtrip'))
        val.update(pending_anatomical_review_fields=len(pending),not_yet_digitized_fields=sum(x['status']=='not_yet_digitized' for x in pending),fully_digitized=not pending,all_numbered_figures_assessed=True,numbered_figures_assessed=rec['numbered_figures'])
        if pending: val['assessment_status']='defensible contours measured; unresolved anatomical boundaries remain NA'
        (p/'documentation/validation.json').write_text(json.dumps(val,indent=2)+'\n')
        manifest=json.loads((p/'source/manifest.json').read_text());manifest['processing_status']=val['assessment_status'];(p/'source/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        subprocess.run([sys.executable,'-B',str(p/'scripts/build_precision_review.py')],check=True,stdout=subprocess.DEVNULL)
        # Refresh the assessment appendix, preserving the native gallery above it.
        gp=p/'review/gallery.html';s=gp.read_text().split('<!-- all-figure-assessment -->')[0]
        s+='<!-- all-figure-assessment --><hr><h1>All-figure source assessment</h1><p>'+ESC(NOTES[paper])+f'</p><p><a href="precision_review.html">Source-toggle precision review</a> · <a href="../documentation/field_inventory.csv">Field inventory</a></p>'
        for x in inv:
            s+=f'<details><summary>Figure {ESC(x["figure"])} — {ESC(x["processing_status"])}</summary><p>{ESC(x["reason_or_result"])}</p><img style="max-width:95%" src="source_pages/page{int(x["pdf_page"]):02}.png" alt="Source page"></details>'
        gp.write_text(s)
        card=f'<article><h2>{ESC(paper)}</h2><p class="count">{rec["views"]} views · {rec["field_components"]} field/components · {rec["calibrated_field_components"]} calibrated · {rec["pixel_only_field_components"]} pixels only</p><p>{ESC(NOTES[paper])}</p><p><a href="{paper}/review/precision_review.html">Inspect contours and source</a> · <a href="{paper}/review/gallery.html">All figures</a> · <a href="{paper}/data/measurements.csv">Measurements CSV</a> · <a href="{paper}/documentation/methods.md">Methods</a></p>'
        card+='<div class="views">'
        for d in defs:
            mid=d['map_id'];card+=f'<a href="{paper}/review/precision_review.html#{mid}"><img loading="lazy" src="{paper}/figures/{mid}/tracing.png" alt="{ESC(mid)}"><span>{ESC(mid)}</span></a>'
        card+='</div></article>';cards.append(card)
        files=[q for name in ['source','figures','data','scripts','review','documentation'] for q in (p/name).rglob('*') if q.is_file() and q.name!='checksums.json' and '__pycache__' not in q.parts]
        (p/'documentation/checksums.json').write_text(json.dumps({str(q.relative_to(p)):digest(q) for q in files},indent=2)+'\n')
        subprocess.run([sys.executable,'-B',str(p/'scripts/measure_flatmaps.py'),'--verify'],check=True,stdout=subprocess.DEVNULL)
        print(paper, 'final checksums and verification passed', flush=True)
    write_csv(REPORT/'paper_summary.csv',records,list(records[0]))
    write_csv(REPORT/'all_measurements.csv',all_meas,list(all_meas[0]))
    write_csv(REPORT/'unresolved_boundaries.csv',unresolved,['paper','map_id','label','status','reason'])
    write_csv(REPORT/'figure_inventory.csv',inventory,list(inventory[0]))
    write_csv(REPORT/'field_inventory.csv',fields_all,['paper','map_id','figure','label','status','extent','reason'])
    totals={k:sum(r[k] for r in records) for k in records[0] if k!='paper'}
    totals.update(papers=len(PAPERS),saved_output_verification='passed for all ten datasets',anatomical_certification=False,whole_neocortex_denominator_available=False)
    (REPORT/'validation.json').write_text(json.dumps(totals,indent=2)+'\n')
    unresolved_html=''.join(f'<tr><td>{ESC(r["paper"])}</td><td><a href="{r["paper"]}/review/precision_review.html#{r["map_id"]}">{ESC(r["map_id"])}</a></td><td>{ESC(r["label"])}</td><td>{ESC(r["reason"])}</td></tr>' for r in unresolved)
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Workbook PDF tracing review</title><style>body{font:16px/1.55 system-ui,sans-serif;color:#22313b;background:#f3f6f7;max-width:1400px;margin:30px auto;padding:0 24px}h1{font-size:34px}h2{font-size:23px}a{color:#086b81}article,.intro,details{background:white;padding:24px;margin:22px 0;border:1px solid #ccd9dd;border-radius:10px}.count{font-weight:650;color:#34515f}.views{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:15px}.views a{background:#f8fafb;border:1px solid #dae3e7;padding:8px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}.views img{width:100%;height:260px;object-fit:contain}.views span{font-size:14px}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-bottom:1px solid #d9e0e4;padding:8px;text-align:left;vertical-align:top}summary{cursor:pointer;font-weight:650}input[type=search]{width:100%;box-sizing:border-box;padding:12px;font-size:16px}small{color:#54636b}</style>
<h1>Workbook PDF tracing review</h1><div class="intro">'''
    page+=f'<p class="count">{totals["papers"]} PDFs · {totals["numbered_figures"]} numbered figures assessed · {totals["views"]} traced views · {totals["field_components"]} field/component measurements</p>'
    page+=f'<p>{totals["calibrated_field_components"]} observations have local calibration; {totals["pixel_only_field_components"]} remain in pixels. Counts include illustrative maps, partial response maps, components and overlapping parent/subregion observations; do not sum them or treat them as animal counts. No complete-neocortex denominator is established.</p>'
    page+='<p>Open a paper’s contour review, choose a region, and toggle the contour to compare it with the source. Dashed colored curves show excluded/shared boundaries. Orange denotes approximate contours; purple denotes partial territories. To request a correction, give the paper, map ID and field label, then describe the misplaced boundary or missing region. Editable ImageJ files are linked in each map.</p>'
    page+='<p><a href="../reports/workbook_batch_2026-10-20/all_measurements.csv">Combined measurements</a> · <a href="../reports/workbook_batch_2026-10-20/figure_inventory.csv">Every numbered figure and disposition</a> · <a href="../reports/workbook_batch_2026-10-20/README.md">Methods and validation</a></p></div>'
    page+=f'<details><summary>{len(unresolved)} unresolved anatomical boundaries — NA, not omitted or zero</summary><p>These require anatomical confirmation; geometric validation does not resolve them.</p><table><tr><th>Paper</th><th>Map</th><th>Field</th><th>Reason</th></tr>{unresolved_html}</table></details>'
    page+='<label>Filter papers or notes <input type="search" id="filter" placeholder="Paper, species, figure or limitation"></label>'+''.join(cards)
    page+='<script>document.querySelector("#filter").addEventListener("input",e=>{const q=e.target.value.toLowerCase();document.querySelectorAll("article").forEach(x=>x.hidden=!x.textContent.toLowerCase().includes(q))})</script></html>'
    (BASE/'review_workbook_batch_2026-10-20.html').write_text(page)
    (REPORT/'README.md').write_text('# Workbook PDF tracing batch\n\nCompleted source assessment on 21 October 2026. The queue directory is `papers_to_do/M1_surface_workbook_figure_references_2026-10-20/PDFs`.\n\n'+f'{totals["papers"]} papers, {totals["numbered_figures"]} numbered figures, {totals["views"]} traced views and {totals["field_components"]} provisional field/component measurements. {len(unresolved)} source boundaries remain explicit NA for anatomical review. Haug has no eligible planar field contours. Counts are not independent animals.\n\n[Open review](../../flatmap_measurements/review_workbook_batch_2026-10-20.html) · [Paper counts](paper_summary.csv) · [Measurements](all_measurements.csv) · [Unresolved boundaries](unresolved_boundaries.csv) · [Validation](validation.json)\n\n'+METHOD+'\n## Reproduction and drafting provenance\n\nThe canonical per-paper `rois.json` files include the accepted shared-border corrections. Rebuild them using each paper’s `scripts/rebuild_all.py`; this does not require OpenCV. The accompanying `views.json`, `build_batch.py`, `render_crops.py`, `reconcile_shared.py` and `fast_audit.py` are drafting provenance, not the authoritative final geometry. They contain original local cache paths and must not be run blindly: regenerating draft guides overwrites later accepted corrections. All temporary drafting conflicts are superseded by the final per-paper geometry audit and native verification. Backups under `documentation/pre_reconciliation` are earlier drafts, not additional measurements.\n\nThe saved exports were reopened through native ImageJ and checked against the canonical coordinates, masks and calibration. Final checksums were refreshed after documentation. This validates the files and geometry; anatomical certification remains pending.\n\nMayer color components are printed-color allocation estimates, not exact half-tile allocation or anatomical parcels; use the combined response territories for the sampled-area result. Every new view remains excluded from whole-hemisphere summaries.\n')
    (REPORT/'STATUS.txt').write_text('Source assessment and defensible provisional measurements exported and verified. See README.md and validation.json. 35 anatomical boundaries remain explicit NA for review.\n')
    print(json.dumps(totals),flush=True)

if __name__=='__main__': main()
