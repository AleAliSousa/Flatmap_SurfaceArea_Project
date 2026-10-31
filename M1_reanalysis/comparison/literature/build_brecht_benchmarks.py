from pathlib import Path
import csv,statistics
OUT=Path(__file__).resolve().parent
# Transcribed and visually checked against Catania & Remple (2002), Table 1,
# printed p.5695 / PDF p.4. Areas are rounded published mm2 per hemisphere.
rows=[]
for i,si,nc,inc,head,bucc,chin in [(1,10.6,39.8,2.9,2.5,1.1,.6),(2,7.9,25.3,2.4,1.7,.9,.8),(3,12.,37.2,4.2,1.8,1.6,.9),(4,11.4,32.5,3.5,1.8,1.2,.8)]:
 face=inc+head+bucc+chin
 rows.append(dict(case=i,S1_mm2=si,neocortex_mm2=nc,incisors_mm2=inc,head_vibrissae_mm2=head,buccal_cavity_mm2=bucc,chin_mm2=chin,derived_broad_orofacial_mm2=face,derived_S1_percent_neocortex=100*si/nc,derived_broad_orofacial_percent_S1=100*face/si,source='Catania & Remple 2002 Table 1 p5695',url='https://pmc.ncbi.nlm.nih.gov/articles/PMC122833/',note='Derived broad orofacial sum is a candidate comparator, not a proven match to Brecht S1-face; derived ratios use rounded published areas.'))
def save(name,records):
 with (OUT/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)
save('Catania_Remple_2002_published_cases.csv',rows)
bench=[]
def add(species,field,w,t,ref,sd,unit,source,url,interpretation):
 bench.append(dict(species=species,field=field,workbook=w,current_tracing=t,published_value=ref,published_SD=sd,unit=unit,workbook_difference_percent=100*(w/ref-1) if isinstance(ref,(int,float)) else '',tracing_difference_percent=100*(t/ref-1) if isinstance(ref,(int,float)) else '',source=source,url=url,interpretation=interpretation))
add('Homo sapiens','V1',2771,2850.5208333333335,2960,760,'mm2 per hemisphere','Hinds et al. 2008','https://pmc.ncbi.nlm.nih.gov/articles/PMC2733317/','Independent ex vivo V1 benchmark; both drawing estimates near published mean.')
add('Homo sapiens','cortical outline versus neocortex',66231,70517.57330246914,97300,'','mm2 per hemisphere','Van Essen et al. 2012','https://pubmed.ncbi.nlm.nih.gov/22047963/','MRI midthickness neocortex; drawn outline may differ in tissue coverage and distortion. Not a specimen match.')
add('Homo sapiens','A1 versus auditory core',174,194.71450617283952,'core rarely exceeds about 200; A1 somewhat more than half','','mm2 per hemisphere','Dick et al. 2012','https://pmc.ncbi.nlm.nih.gov/articles/PMC3531973/','Different scope: A1 is smaller than core; qualitative scale benchmark, no justified exact mean comparison.')
add('Homo sapiens','S1 / workbook S1-3b',1526,1704.3016975308644,'not verified','','mm2 per hemisphere','Search unresolved','','No matched published complete-field numeric benchmark verified; area 3b and combined S1 must be distinguished.')
add('Homo sapiens','S1-face',454,434.89583333333337,'not verified','','mm2 per hemisphere','Search unresolved','','No matched published complete face-domain numeric benchmark verified; functional activation extents are not automatically field areas.')
add('Heterocephalus glaber','S1',8.209,8.190564449432891,10.5,1.8,'mm2 per hemisphere','Catania & Remple 2002 Table 1','https://pmc.ncbi.nlm.nih.gov/articles/PMC122833/','Published range 7.9–12.0, n=4. Same source lineage may underlie Brecht; do not count as an independent replication.')
add('Heterocephalus glaber','cortical outline versus neocortex',26.682,26.254017013232513,33.7,6.4,'mm2 per hemisphere','Catania & Remple 2002 Table 1','https://pmc.ncbi.nlm.nih.gov/articles/PMC122833/','Published range 25.3–39.8, n=4. Within range; outline equivalence still needs source tracing.')
add('Heterocephalus glaber','S1 / cortex',100*8.209/26.682,100*8.190564449432891/26.254017013232513,31,'','percent','Catania & Remple 2002 Results','https://pmc.ncbi.nlm.nih.gov/articles/PMC122833/','31% is approximate reported percentage. Excellent descriptive agreement; not independent source validation.')
face=[r['derived_broad_orofacial_mm2'] for r in rows]
add('Heterocephalus glaber','S1-face versus broad orofacial candidate',5.301,5.067905245746691,statistics.mean(face),statistics.stdev(face),'mm2 per hemisphere','Derived from Catania & Remple 2002 Table 1','https://pmc.ncbi.nlm.nih.gov/articles/PMC122833/','Sum incisors + head/vibrissae + buccal cavity + chin within each case; values rounded at source. Definition match unresolved. Range 5.8–8.5.')
add('Heterocephalus glaber','S1-face / S1 versus broad orofacial candidate',100*5.301/8.209,100*5.067905245746691/8.190564449432891,30.8+18.7+11.5+7.5,'','percent','Sum of published category mean percentages, Catania & Remple 2002 Table 1','https://pmc.ncbi.nlm.nih.gov/articles/PMC122833/','68.5% is derived from rounded published means; not incisor-only 30.8%. Definition match unresolved.')
save('Brecht_human_molerat_benchmarks.csv',bench)
assert len(rows)==4 and len(bench)==10
print('Saved four published case records and ten comparison records.')
