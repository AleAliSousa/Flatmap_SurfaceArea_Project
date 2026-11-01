from pass3_helpers import *
p='Burman_etal_2008';m='fig09A_CJ58R_flatmap'
# All coordinates on the original 1070 x 1004 raster; gray-band midline estimates.
# Four paths share identical junctions; no tracer perimeter is used.
a=curve([[729,268],[725,280],[729,294],[726,309],[742,318],[755,335],[760,346],[766,353]])
b=curve([[766,353],[783,359],[799,365],[811,376],[827,390],[844,405]])
c=curve([[701,277],[700,290],[700,302],[703,315],[701,321],[715,328],[723,345],[741,355],[756,364],[763,370],[762,380],[781,386],[788,391],[802,399],[816,412],[831,424],[844,433]])
d=curve([[666,286],[664,296],[671,313],[660,332],[676,345],[679,357],[700,373],[696,388],[703,399],[703,407],[733,412],[756,417],[778,425],[802,435],[828,441],[845,443],[854,439]])
e=curve([[772,259],[772,279],[786,284],[799,303],[801,316],[811,332],[818,340],[818,352],[831,366],[845,380]])+[[859.0,389.0],[844.0,405.0]]
polys={'M1_dorsal_component': a+b[1:]+list(reversed(e))[1:]+[[729,268]],'3a':[[701,277],[729,268]]+a[1:]+b[1:]+[[844,433]]+list(reversed(c))[1:],'3b':[[666,286],[701,277]]+c[1:]+[[854,439]]+list(reversed(d))[1:]}
for label,poly in polys.items():
 candidate(p,m,label,[poly], 'Retraced along the approximate centers of the published gray architectural uncertainty bands. Narrow ventral extensions retained; blue tracer patches ignored. M1/3a and 3a/3b use identical shared paths. The broad junction at the ventral tips is an explicit band-center estimate, not an observed sharp border. Dorsal component only: the upper edge follows the unfolding cut, not a complete field boundary. No physical scale established; held out of quantitative analysis.', extent='dorsal_component',status='provisional_gray_band_center_estimate',analysis_eligible=False, boundary_uncertainty='Gray bands have nonzero width. Midline convention does not resolve anatomical uncertainty; no numeric sensitivity limits computed.')
record(p,'All four saved views screened. Fig9 enlarged source: gray bands contain narrow M1/3a/3b extensions; tracer deposits are internal. Three shared-boundary candidates prepared. Fig6 motor contours need separate dashed-line review.',source=False)
record('Hinds_etal_2008','All 11 views and source figures screened. Pink V1 perimeter must be retained separately from fitted blue ellipse; green stars locally obscure the edge. No new independent field in probability/model panels. Enlarged LH4 source inspected; no automatic ellipse substitution.')
record('Luethke_etal_1988','All 14 saved views and all 19 source figures screened. Enlarged Fig12 shows M/S-I corner rounding and slight stroke drift; black tracer fields cannot substitute for auditory field borders. Fig1/2 whole-map panels omitted; Figs5–15 contain same case/hemisphere repeats, requiring source linkage. Summary Figs17–19 do not add independent cases.')
# Previously omitted premotor/frontal compartments: their gray-band envelopes are closed.
l=curve([[845,284],[846,295],[837,312],[848,334],[851,347],[855,359]])
j=curve([[855,359],[851,373]])+[[859.0,389.0]]
k=curve([[885,291],[888,300],[881,310],[879,318],[884,329],[883,344],[889,349]])
f=curve([[855,359],[872,358],[889,349]])
g=curve([[889,349],[910,336],[926,346]])
# Recover the already-inspected M1 / 6Dc path from its branch on the 6M band.
ix=e.index([786.0,284.0]);iy=e.index([859.0,389.0]);m1_dc=e[ix:iy+1]
newpolys={
'6Dc':curve([[786,284],[815,279],[845,284]])+l[1:]+j[1:]+list(reversed(m1_dc))[1:],
'6Dr':curve([[845,284],[863,286],[885,291]])+k[1:]+list(reversed(f))[1:]+list(reversed(l))[1:],
'8Ad':curve([[885,291],[917,294],[942,298],[936,309],[938,318],[946,338],[926,346]])+list(reversed(g))[1:]+list(reversed(k))[1:],
'8Av':f+g[1:]+curve([[926,346],[925,360],[918,380],[914,396],[891,393],[875,393],[859,389]])[1:]+list(reversed(j))[1:]}
for label,poly in newpolys.items():
 candidate(p,m,label,[poly],'Previously omitted closed frontal field. Approximate gray-band centers traced on CJ58R Fig9A; tracer deposits and solid fold lines are not region borders. Shared borders reuse the M1/6Dc/6Dr/8Ad/8Av paths. Wide multi-field junctions remain estimates within the printed uncertainty bands. Pixel-only, provisional and excluded from quantitative analysis; no scale borrowed.',extent='complete_drawn_field',status='provisional_gray_band_center_estimate',analysis_eligible=False,boundary_uncertainty='Band-center convention; broad junctions ambiguous. No numeric sensitivity limits computed.')
