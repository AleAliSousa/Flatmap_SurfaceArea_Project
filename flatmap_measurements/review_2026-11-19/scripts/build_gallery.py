#!/usr/bin/env python3
"""Build the static November 2026 flatmap correction review gallery.

Rerun from any directory with: python3 flatmap_measurements/review_2026-11-19/scripts/build_gallery.py
The unified area_changes.csv is the correction inventory; new rows appear on rerun.
"""

import csv
import html
import os
from collections import OrderedDict
from pathlib import Path
from urllib.parse import quote


REVIEW = Path(__file__).resolve().parents[1]
MEASUREMENTS = REVIEW.parent
OUT = REVIEW / "index.html"
CSV_FILES = (REVIEW / "area_changes.csv",)


def esc(value):
    return html.escape(str(value), quote=True)


def href(path):
    return quote(os.path.relpath(path, REVIEW).replace(os.sep, "/"), safe="/")


def link(path, label):
    if not path.is_file():
        return '<span class="missing">Unavailable: {}</span>'.format(esc(label))
    return '<a href="{}">{}</a>'.format(esc(href(path)), esc(label))


def image(path, alt):
    if not path.is_file():
        return '<p class="missing">Image unavailable: {}</p>'.format(esc(alt))
    return '<a href="{}" target="_blank" rel="noopener"><img src="{}" alt="{}" loading="lazy"></a>'.format(
        esc(href(path)), esc(href(path)), esc(alt)
    )


def value(row, key):
    return row.get(key, "").strip()


def number(value_text, digits=3, signed=False):
    try:
        x = float(value_text)
    except (TypeError, ValueError):
        return esc(value_text) if value_text else "—"
    return "{:{sign},.{digits}f}".format(x, sign="+" if signed else "", digits=digits)


def area(row, prefix):
    mm2 = value(row, prefix + "_area_mm2")
    if mm2 and mm2.upper() != "NA":
        return number(mm2) + " mm²"
    px2 = value(row, prefix + "_area_px2")
    if px2 and px2.upper() != "NA":
        return number(px2, 1) + " px²"
    return "—"


def paper_name(paper_id):
    return paper_id.replace("_etal_", " et al. ").replace("_", " ")


def read_changes():
    rows = []
    for csv_path in CSV_FILES:
        if not csv_path.is_file():
            continue
        with csv_path.open(newline="", encoding="utf-8-sig") as stream:
            for row in csv.DictReader(stream):
                if not value(row, "paper_id") or not value(row, "map_id"):
                    continue
                row["_csv"] = csv_path.name
                rows.append(row)
    return rows


def path_in_review(value_text):
    if not value_text:
        return None
    path = (REVIEW / value_text).resolve()
    if not path.is_relative_to(REVIEW):
        return None
    return path


def before_roi(row):
    explicit = path_in_review(value(row, "before_roi"))
    if explicit:
        return explicit
    return REVIEW / "before" / value(row, "paper_id") / "figures" / value(row, "map_id") / "rois.json"


def canonical_roi(row):
    explicit = value(row, "after_roi")
    if explicit:
        path = (MEASUREMENTS / explicit).resolve()
        if path.is_relative_to(MEASUREMENTS):
            return path
    return MEASUREMENTS / value(row, "paper_id") / "figures" / value(row, "map_id") / "rois.json"


def evidence_paths(row):
    single = path_in_review(value(row, "evidence"))
    if single:
        return [("Old red · corrected green", single)]
    items = []
    for key, title in (("before_tracing", "Before"), ("after_tracing", "After")):
        path = path_in_review(value(row, key))
        if path:
            items.append((title, path))
    return items


def main():
    rows = read_changes()
    grouped = OrderedDict()
    for row in rows:
        grouped.setdefault((value(row, "paper_id"), value(row, "map_id")), []).append(row)

    cards = []
    toc = []
    for index, ((paper_id, map_id), group) in enumerate(grouped.items(), 1):
        card_id = "view-{:02d}".format(index)
        toc.append('<a href="#{}">{} · {}</a>'.format(card_id, esc(paper_name(paper_id)), esc(map_id)))
        first = group[0]
        roi = canonical_roi(first)
        fig_dir = roi.parent
        source = fig_dir / "source_preview.png"
        trace = fig_dir / "tracing.png"
        evidence = OrderedDict()
        for row in group:
            for label, path in evidence_paths(row):
                evidence[str(path)] = (label, path)

        change_rows = []
        for row in group:
            before_area = area(row, "before")
            after_area = area(row, "after")
            delta = number(value(row, "delta_percent"), 2, signed=True)
            change_rows.append(
                "<tr><th scope=\"row\">{label}</th><td>{extent}</td><td>{before}</td>"
                "<td>{after}</td><td class=\"delta\">{delta}%</td></tr>".format(
                    label=esc(value(row, "label")), extent=esc(value(row, "extent") or "—"),
                    before=before_area, after=after_area, delta=delta
                )
            )
        reasons = list(OrderedDict.fromkeys(value(row, "reason") for row in group if value(row, "reason")))
        reason_html = " ".join("<p>{}</p>".format(esc(reason)) for reason in reasons)
        evidence_html = "".join(
            '<figure><div class="image-frame">{}</div><figcaption>{}</figcaption></figure>'.format(
                image(path, "{} {} correction evidence: {}".format(paper_id, map_id, label)), esc(label)
            ) for label, path in evidence.values()
        )
        before_links = list(OrderedDict.fromkeys(before_roi(row) for row in group))
        before_html = " · ".join(link(path, "Before ROI JSON") for path in before_links if path)
        cards.append(
            '<article class="card" id="{id}"><div class="card-heading"><div><p class="eyebrow">View {index:02d}</p>'
            '<h2>{paper} <span>{map}</span></h2></div><div class="file-links">{roi_link} · {before_links}</div></div>'
            '<div class="pair"><figure><div class="image-frame">{source}</div><figcaption>Published source</figcaption></figure>'
            '<figure><div class="image-frame">{trace}</div><figcaption>Current tracing</figcaption></figure></div>'
            '<div class="evidence">{evidence}</div><table><thead><tr><th>ROI</th><th>Extent</th><th>Before area</th>'
            '<th>After area</th><th>Change</th></tr></thead><tbody>{changes}</tbody></table>'
            '<div class="reason">{reason}</div><p class="verify">{verification}</p></article>'.format(
                id=card_id, index=index, paper=esc(paper_name(paper_id)), map=esc(map_id),
                roi_link=link(roi, "Current ROI JSON"), before_links=before_html,
                source=image(source, "{} {} published source".format(paper_id, map_id)),
                trace=image(trace, "{} {} current tracing".format(paper_id, map_id)),
                evidence=evidence_html or '<p class="missing">No separate correction image saved.</p>',
                changes="".join(change_rows), reason=reason_html,
                verification=esc(" · ".join(OrderedDict.fromkeys(
                    value(row, "verification") for row in group if value(row, "verification")
                )))
            )
        )

    page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Flatmap tracing review · 19 Nov 2026</title>
<style>
:root{color-scheme:light;--paper:#f7f5ef;--ink:#172b2b;--muted:#58666a;--line:#cad3ce;--accent:#17685d;--surface:#fffefa}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:var(--accent);text-underline-offset:3px}a:hover{text-decoration-thickness:2px}
.wrap{max-width:1420px;padding:0 24px;margin:auto}.hero{padding:44px 0 30px;border-bottom:1px solid var(--line);background:#edf1ec}
.eyebrow{text-transform:uppercase;letter-spacing:.15em;font-size:.72rem;font-weight:750;color:var(--accent);margin:0 0 8px}
h1{font-size:clamp(2rem,5vw,3.7rem);line-height:1.1;letter-spacing:-.035em;margin:0 0 13px}h2{font-size:1.45rem;line-height:1.2;margin:0}h2 span{color:var(--muted);font-weight:500}
.lede{max-width:830px;color:#3b4e4d;margin:0}.stats{display:flex;gap:10px;flex-wrap:wrap;margin:23px 0}.stats span{padding:8px 12px;border:1px solid #a5bdb3;border-radius:999px;background:#f8fbf8;font-size:.9rem;font-weight:650}
.scope{max-width:950px;color:#3b4e4d;font-size:.94rem}.scope p{margin:8px 0}.toc{display:flex;gap:8px;overflow-x:auto;padding:18px 0 23px;white-space:nowrap}.toc a{font-size:.86rem;background:#fff;border:1px solid var(--line);padding:7px 11px;border-radius:6px;text-decoration:none}
main{padding:8px 0 42px}.card{scroll-margin-top:18px;background:var(--surface);border:1px solid var(--line);border-radius:13px;padding:23px;margin:25px 0;box-shadow:0 2px 8px #1d31230b}
.card-heading{display:flex;justify-content:space-between;align-items:end;gap:16px;margin-bottom:18px}.file-links{font-size:.86rem;text-align:right}.pair,.evidence{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.evidence{margin-top:14px}.evidence:empty{display:none}
figure{margin:0;min-width:0}.image-frame{display:flex;align-items:center;justify-content:center;background:#e8ebe7;border:1px solid #d6ddd7;border-radius:7px;overflow:hidden;min-height:150px}.image-frame a{display:block;line-height:0}.image-frame img{display:block;max-width:100%;height:auto;max-height:460px;object-fit:contain}.evidence .image-frame img{max-height:430px}
figcaption{font-size:.79rem;color:var(--muted);padding:5px 2px 0;font-weight:650}table{width:100%;border-collapse:collapse;margin:20px 0 7px;font-variant-numeric:tabular-nums}th,td{border-bottom:1px solid #e1e6e0;padding:8px 10px;text-align:left}thead th{color:var(--muted);font-size:.75rem;text-transform:uppercase;letter-spacing:.06em}tbody th{font-weight:700}.delta{font-weight:700}.reason{max-width:1000px;color:#334747}.reason p{margin:8px 0}.verify{font-size:.78rem;color:var(--muted);margin:12px 0 0}.missing{font-size:.8rem;color:#985a37}
footer{padding:24px 0 45px;border-top:1px solid var(--line);color:var(--muted);font-size:.86rem}
@media(max-width:760px){.wrap{padding:0 14px}.card{padding:15px}.card-heading{display:block}.file-links{text-align:left;margin-top:8px}.pair,.evidence{grid-template-columns:1fr}table{font-size:.82rem}th,td{padding:7px 5px}.image-frame img{max-height:340px}}
</style></head><body>
<header class="hero"><div class="wrap"><p class="eyebrow">Surface-area project · correction record</p><h1>Tracing review</h1>
<p class="lede">Published source images, current editable tracings, and saved before/after evidence for the corrected outlines in the 19 November 2026 review.</p>
<div class="stats"><span>{roi_count} ROI corrections</span><span>{view_count} views</span><span>{paper_count} papers</span></div>
<div class="scope"><p><strong>Reading the images:</strong> red marks the prior contour and green the corrected contour in comparison images. Open any image for its full resolution. Area changes are calculated from the saved polygons; a negative change means the corrected area is smaller. Uncalibrated schematics show pixel area.</p>
<p><strong>Scope and uncertainty:</strong> this gallery records corrections, not a certification of every outline. Some published borders are thick, faint, interrupted, or inferred from staining; their reported extent and status remain in each ROI JSON. The <a href="source_coverage.md">source coverage</a>, <a href="line_proximity_method.md">screening method</a>, and <a href="technical_verification.csv">technical verification</a> document the wider pass.</p></div></div></header>
<nav class="wrap toc" aria-label="Corrected views">{toc}</nav><main class="wrap">{cards}</main>
<footer><div class="wrap">Generated from <a href="area_changes.csv">area_changes.csv</a>. Rerun <code>scripts/build_gallery.py</code> after that record changes.</div></footer>
</body></html>'''
    for key, content in (
        ("roi_count", len(rows)), ("view_count", len(grouped)),
        ("paper_count", len(set(value(row, "paper_id") for row in rows))),
        ("toc", "".join(toc)), ("cards", "".join(cards))
    ):
        page = page.replace("{" + key + "}", str(content))
    OUT.write_text(page, encoding="utf-8")
    print("Wrote {} ({} ROI corrections, {} views)".format(OUT, len(rows), len(grouped)))


if __name__ == "__main__":
    main()
