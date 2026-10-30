#!/usr/bin/env python3
"""Inventory canonical definitions and publish human-authored visual findings.

This script does not infer anatomy or modify measurement inputs/outputs.
"""
import csv
import hashlib
import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'missing_region_audit_2026-10-20'

def csv_write(path, rows, fields):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def main():
    findings_doc = json.loads((OUT / 'visual_findings.json').read_text())
    findings = findings_doc['findings']
    action_file = OUT / 'action_results.json'
    actions = json.loads(action_file.read_text()) if action_file.exists() else None
    action_map = {(r['paper'], r['map_id']): r for r in actions['results']} if actions else {}
    reviewed = {(r['paper'], r['map_id']) for r in findings}
    papers, views, missing, hashes = [], [], [], {}
    for paper in sorted(ROOT.iterdir()):
        if not (paper / 'source/paper.pdf').is_file():
            continue
        pv, nr, nu, pending, unstated = 0, 0, 0, 0, 0
        for path in sorted((paper / 'figures').glob('*/rois.json')):
            raw = path.read_bytes()
            d = json.loads(raw)
            mid = path.parent.name
            rois, na = d.get('rois', []), d.get('unmeasured', [])
            digest = hashlib.sha256(raw).hexdigest()
            hashes[str(path.relative_to(ROOT))] = digest
            pv += 1
            nr += len(rois)
            nu += len(na)
            for u in na:
                status = u.get('status') or 'status_not_recorded'
                pending += status == 'not_yet_digitized'
                unstated += status == 'status_not_recorded'
                missing.append(dict(paper=paper.name, map_id=mid,
                    pdf_page=d.get('pdf_page'), label=u.get('label', ''),
                    saved_status=status, saved_reason=u.get('reason', '')))
            views.append(dict(paper=paper.name, map_id=mid, pdf_page=d.get('pdf_page'),
                roi_count=len(rois), unmeasured_count=len(na),
                labels='; '.join(r.get('label', '') for r in rois),
                targeted_visual_review=(paper.name, mid) in reviewed,
                canonical_sha256=digest))
        papers.append(dict(paper=paper.name, saved_views=pv, roi_count=nr,
            unmeasured_entries=nu, not_yet_digitized=pending, status_not_recorded=unstated,
            visually_checked_views=sum(p == paper.name for p, m in reviewed)))
    assert len(reviewed) == len(findings), 'Duplicate review entry'
    known = {(r['paper'], r['map_id']) for r in views}
    assert reviewed <= known, 'Review references a missing definition'
    for r in findings:
        folder = ROOT / r['paper'] / 'figures' / r['map_id']
        for filename in ['rois.json', 'source.tif', 'tracing.png']:
            assert (folder / filename).is_file(), folder / filename
    csv_write(OUT / 'paper_inventory.csv', papers, list(papers[0]))
    csv_write(OUT / 'view_inventory.csv', views, list(views[0]))
    csv_write(OUT / 'saved_unmeasured_entries.csv', missing, list(missing[0]))
    csv_write(OUT / 'visual_findings.csv', findings, list(findings[0]))
    stats = dict(date=findings_doc['date'], papers=len(papers), saved_views=len(views),
        saved_rois=sum(r['roi_count'] for r in papers), saved_unmeasured_entries=len(missing),
        explicit_not_yet_digitized=sum(r['not_yet_digitized'] for r in papers),
        targeted_visual_views=len(reviewed), targeted_visual_papers=len({p for p,m in reviewed}),
        findings_by_disposition=dict(Counter(r['disposition'] for r in findings)),
        measurement_geometry_changed=bool(actions))
    if actions:
        stats['executed_actions'] = len(actions['results'])
        stats['added_contours'] = actions['added_contours']
        stats['revised_contours'] = actions['revised_contours']
    (OUT / 'summary.json').write_text(json.dumps(stats, indent=2) + '\n')
    (OUT / 'canonical_input_sha256.json').write_text(json.dumps(hashes, indent=2) + '\n')
    titles = dict(missing_tracing='Missing tracing', inventory_gap='Inventory gap',
        candidate='Needs closer boundary review', no_new_omission_found='No new omission established',
        source_limit_supported='Source limitation supported')
    priority = {k: i for i,k in enumerate(titles)}
    ordered = sorted(findings, key=lambda r: (priority[r['disposition']], r['paper'], r['map_id']))
    e = html.escape
    cards = []
    for n,r in enumerate(ordered):
        base = '../'+r['paper']+'/figures/'+r['map_id']+'/'
        source_url = base + 'source_preview.png'
        if not (ROOT/r['paper']/'figures'/r['map_id']/'source_preview.png').exists():
            from PIL import Image
            preview_dir = OUT/'source_previews'
            preview_dir.mkdir(exist_ok=True)
            preview_name = r['paper']+'_'+r['map_id']+'.png'
            with Image.open(ROOT/r['paper']/'figures'/r['map_id']/'source.tif') as im:
                im.convert('RGB').save(preview_dir/preview_name)
            source_url = 'source_previews/'+preview_name
        definition = json.loads((ROOT/r['paper']/'figures'/r['map_id']/'rois.json').read_text())
        pdf = '../'+r['paper']+'/source/paper.pdf#page='+str(definition.get('pdf_page',1))
        execution = action_map.get((r['paper'], r['map_id']))
        execution_html = ('<p style="padding:12px;background:#e0f3e8"><b>Action completed:</b> '+e(execution['outcome'])+'</p>') if execution else ''
        action_label = 'Original action (now assessed)' if execution else 'Next action'
        cards.append(f'''<article data-status="{e(r['disposition'])}">
        <span class="tag {e(r['disposition'])}">{e(titles[r['disposition']])}</span>
        <h2>{e(r['paper'])} / {e(r['map_id'])}</h2>{execution_html}<p><b>{e(r['regions'])}</b></p>
        <p>{'<b>Initial audit observation:</b> ' if execution else ''}{e(r['evidence'])}</p><p><b>{action_label}:</b> {e(r['next_action'])}</p>
        <p><a href="{e(pdf)}">Source PDF</a> · <a href="{e(base)}rois.json">Saved definition</a> ·
        <a href="{e(source_url)}">Full source image</a> · <a href="{e(base)}tracing.png">Full tracing</a></p>
        <details><summary>Compare source and current tracing</summary>
        <div class="pair"><figure><figcaption>Source</figcaption><img loading="lazy" src="{e(source_url)}" alt="Source {e(r['paper'])} {e(r['map_id'])}"></figure>
        <figure><figcaption>Current tracing</figcaption><img loading="lazy" src="{e(base)}tracing.png" alt="Current tracing {e(r['paper'])} {e(r['map_id'])}"></figure></div></details></article>''')
    table = ''.join('<tr>'+''.join('<td>'+e(str(r[k]))+'</td>' for k in papers[0])+'</tr>' for r in papers)
    options = '<option value="all">All findings</option>'+''.join(f'<option value="{k}">{e(v)}</option>' for k,v in titles.items())
    page = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Missing-region review · 20 October 2026</title><style>
    body{{font:16px/1.55 system-ui,sans-serif;background:#f3f5f7;color:#182735;max-width:1300px;margin:32px auto;padding:0 22px}}
    h1{{font-size:32px}}h2{{font-size:20px}}a{{color:#075f89}}article,.intro{{background:white;padding:24px;margin:20px 0;border:1px solid #d8e1e7;border-radius:10px}}
    .tag{{font-size:13px;font-weight:bold;padding:5px 10px;border-radius:4px;background:#e6eef2}}.missing_tracing{{background:#ffe7be}}.inventory_gap{{background:#ffe0d4}}.candidate{{background:#fff4ca}}
    .pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}figure{{margin:0}}img{{width:100%;height:auto}}summary{{cursor:pointer}}table{{border-collapse:collapse;font-size:13px;width:100%}}td,th{{padding:8px;text-align:left;border-bottom:1px solid #ddd}}.scroll{{overflow:auto}}select{{font:inherit;padding:9px}}[hidden]{{display:none}}
    @media(max-width:750px){{.pair{{grid-template-columns:1fr}}}}
    </style><h1>Missing-region review</h1><p>20 October 2026 · <a href="../tracing_method.md">Reusable tracing method</a> · <a href="README.md">Scope and findings</a></p>
    <div class="intro"><p><b>Inventory:</b> {stats['papers']} papers, {stats['saved_views']} saved views, {stats['saved_rois']} ROIs. <b>Visual inspection:</b> {stats['targeted_visual_views']} selected views across {stats['targeted_visual_papers']} other papers.</p>
    <p>Five views contain clear missing tracings; one has a missing component in the inventory. Other findings require closer boundary assessment or support existing source limitations. These are review findings, not newly measured areas.</p>
    <p>The {len(missing)} saved unmeasured entries include partial fields, contextual labels, unavailable totals and repeated views. They are not {len(missing)} recoverable fields. Seventeen of the {stats['explicit_not_yet_digitized']} explicit pending entries are the unfinished Krubitzer &amp; Kaas (1993) fig05 pilot.</p>
    <p>This is a targeted visual audit, not a fresh visual certification of all 304 views or all published figures. No canonical ROIs, scale endpoints or measured areas were changed. Kaas (2011) and Zilles (1985) have no saved ROI definitions; their existing exclusion records were read, but their source figures were not re-reviewed here. Felleman (1991) is covered by the preceding correction.</p>
    <p><a href="paper_inventory.csv">Paper inventory</a> · <a href="view_inventory.csv">All saved views</a> · <a href="saved_unmeasured_entries.csv">Saved unmeasured entries</a> · <a href="visual_findings.csv">Review queue</a> · <a href="summary.json">Counts</a></p></div>
    <label for="status">Show </label><select id="status">{options}</select>{''.join(cards)}
    <details><summary>Complete paper inventory</summary><div class="scroll"><table><thead><tr>{''.join('<th>'+e(k.replace('_',' '))+'</th>' for k in papers[0])}</tr></thead><tbody>{table}</tbody></table></div></details>
    <script>document.getElementById('status').addEventListener('change',function(){{document.querySelectorAll('article').forEach(a=>a.hidden=this.value!=='all'&&a.dataset.status!==this.value);}});</script></html>'''
    if actions:
        page = page.replace('<h1>Missing-region review</h1>', '<h1>Missing-region review — actions completed</h1><div class="intro"><b>28 contours added; one existing contour revised.</b> All 22 listed actions now have recorded outcomes. <a href="../review_missing_region_actions.html">Open the new before/source/after review and area changes</a>. Original audit observations are retained below for provenance; current images and inventories reflect the corrections.</div>')
        page = page.replace('Five views contain clear missing tracings; one has a missing component in the inventory. Other findings require closer boundary assessment or support existing source limitations. These are review findings, not newly measured areas.', 'The five omission views have been processed, the missing S component inventoried, and candidate borders reassessed. Twenty-seven complete-envelope additions and one approximate V envelope are saved. Illustrative drawings remain excluded from animal means; the approximate V is excluded from complete-field means.')
        page = page.replace(f'Seventeen of the {stats["explicit_not_yet_digitized"]} explicit pending entries are the unfinished Krubitzer &amp; Kaas (1993) fig05 pilot.', 'The fig05 pilot entries have been assessed individually: area 17 was added and unresolved boundaries now have specific source-limit reasons.')
        page = page.replace('No canonical ROIs, scale endpoints or measured areas were changed.', 'Canonical ROIs and measured areas were updated for accepted corrections. Scale endpoints and specimen identities were preserved.')
    (OUT/'index.html').write_text(page)
    md = '''# Missing-region audit — 20 October 2026

This pass records the improved tracing method and checks other files for omissions. No measurement geometry or area tables were changed.

## Scope

- Machine inventory: all 21 paper folders, 304 saved view definitions and 1,088 ROI records.
- Targeted visual inspection: 22 views across 18 papers besides Felleman & Van Essen. The queue below records every inspected view and the result. Source captions were additionally consulted for the Krubitzer (1995) comparative maps, Krubitzer et al. (1995) fig19, Lyon et al. (1998) fig04 and Beck & Kaas (1998) fig04.
- Kaas (2011) and Zilles (1985): existing exclusion documentation read; no new source-figure inspection. Felleman (1991): the preceding correction is the worked example.
- The 1,178 saved unmeasured entries are neither unique fields nor confirmed omissions. The 18 explicit `not_yet_digitized` entries consist of 17 pilot fields in Krubitzer & Kaas (1993) fig05 and one grouped hippocampal/subicular entry in Felleman fig02. Legacy entries without a status remain explicitly marked `status_not_recorded` in this audit.

## Main findings

Five views contain clear missing tracings: Krubitzer & Kaas (1993) fig05; Krubitzer (1995) fig01 macaque and marmoset; Krubitzer et al. (1995) fig19; and Krubitzer (1998) fig14F. Start with area 17, the FST/FEF/FV/R leader targets, the enclosed V region and the dark M field. Other fields listed on the same rows still require their own boundary decisions.

Lyon (1998) fig04A also has a second S component absent from both the ROIs and the missing-region list. Enlarged inspection shows its border interrupted at the tissue cut: this is an inventory omission, not a claim that a complete field can already be measured. This illustrates why missing-region assessment must distinguish an unrecorded component from a recoverable total area.

The old generic “small print,” “dark fill” and “overprinted lettering” reasons were too broad for several comparative figures. Their compartments must be reviewed individually. Conversely, open borders, projection lines, recording windows and diffuse histological staining remain real limits.

## Review and reproducibility

[Open the image review and prioritized queue](index.html). [Reusable tracing method](../tracing_method.md).

`visual_findings.json` is the human-authored assessment ledger. `visual_findings.csv` is its tabular copy. `view_inventory.csv` and `saved_unmeasured_entries.csv` retain the saved state, including old reasons that this audit disputes. They do not silently relabel canonical inputs. `canonical_input_sha256.json` records all inventoried definitions.

Run `python3 flatmap_measurements/scripts/audit_missing_regions.py` from the project to regenerate inventories and the review from the current definitions and the saved assessment ledger. The script does not discover anatomical borders. If geometry changes later, reassess the findings rather than assuming this dated ledger still describes the new traces.

Before retracing, preserve the affected paper, then update canonical JSON, areas, native ImageJ outputs, summaries and visual review together. Do not merely change an NA status without rebuilding the associated measurement records. No claim of complete anatomical review of the entire dataset is made here.
'''
    if actions:
        md = f'''# Missing-region audit and executed actions — 20 October 2026

All 22 listed actions now have outcomes. **{actions['added_contours']} contours were added and {actions['revised_contours']} existing contour revised**, across {actions['modified_views']} modified views in {actions['modified_papers']} papers. Source-limited candidates retain explicit NA with field-specific reasons. This is not an exhaustive new anatomical certification of the dataset.

[New before/source/after review and areas](../review_missing_region_actions.html) · [Audit with completed-action outcomes](index.html) · [Action results](action_results.csv) · [Area changes](action_measurement_changes.csv).

The additions comprise 25 illustrative-map fields, two complete specimen-field observations, and one approximate echidna V contour. Enlarged inspection revealed an undrawn V boundary interval among recording symbols, correcting the initial audit's description of it as fully enclosed. The interpolated V is excluded from complete-field means. Illustrations and repeated views do not create additional animals. Source scales, crops and specimen identities were preserved.

Current inventory: {stats['papers']} papers, {stats['saved_views']} saved views, {stats['saved_rois']} ROI records and {len(missing)} unmeasured entries. These are records, not independent specimens. The original visual inspection covered 22 selected views across 18 other papers. Kaas (2011) and Zilles (1985) were documentation-only checks; Felleman (1991) was the preceding correction.

`visual_findings.json` preserves the original human-authored findings. `action_results.json` records their execution. CSV inventories and canonical SHA-256 records reflect the current definitions. The [original audit snapshot](../_backups/missing_region_actions_2026-10-20/missing_region_audit_2026-10-20/README.md) and affected paper snapshots remain under `_backups/missing_region_actions_2026-10-20/`.

Rebuild affected papers with their existing `scripts/rebuild_all.py`, then run `flatmap_measurements/scripts/build_missing_region_actions_review.py` and `flatmap_measurements/scripts/audit_missing_regions.py` to refresh the project reviews. Canonical geometry is in each `rois.json`; no scratch fitting script is required. The review generators do not infer anatomical borders.
'''
    (OUT/'README.md').write_text(md)
    print(json.dumps(stats, indent=2))

if __name__ == '__main__':
    main()
