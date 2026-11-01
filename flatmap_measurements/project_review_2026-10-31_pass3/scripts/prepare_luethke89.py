from pass3_helpers import *
p='Luethke_etal_1989'
# Anchors picked separately on each source. Panels 3 and 4 reveal the same-case envelope under the dense labels of panels 1 and 2.
anchors={
1:[[309,192],[352,197],[390,211],[426,231],[462,255],[492,282],[519,318],[539,354],[551,395],[557,440],[555,485],[548,528],[530,570],[513,599],[489,623],[466,632],[441,628],[421,617],[400,596],[378,566],[359,541],[338,515],[322,489],[305,461],[288,433],[268,405],[252,377],[236,345],[222,316],[217,290],[219,260],[229,234],[250,213],[278,198]],
2:[[302,195],[342,199],[383,214],[419,234],[453,258],[483,287],[510,322],[530,357],[542,398],[548,442],[546,487],[536,531],[521,568],[504,603],[480,625],[456,633],[432,630],[411,619],[389,599],[371,571],[352,546],[330,519],[312,492],[298,467],[280,440],[261,412],[244,385],[231,354],[218,326],[211,302],[210,279],[217,248],[231,225],[257,207],[280,198]],
3:[[307,188],[345,190],[385,206],[421,227],[455,251],[487,279],[514,311],[534,347],[548,389],[555,430],[554,474],[546,519],[533,560],[515,591],[492,616],[470,627],[447,627],[425,617],[406,600],[383,575],[365,549],[345,523],[327,495],[309,467],[290,438],[272,411],[256,383],[239,352],[227,327],[218,303],[216,280],[224,253],[236,231],[255,211],[278,196]],
4:[[306,188],[342,193],[382,207],[414,226],[444,247],[470,272],[496,298],[516,325],[531,356],[540,400],[544,448],[541,488],[534,522],[523,560],[516,588],[499,611],[481,629],[457,637],[434,636],[415,629],[395,612],[379,591],[361,564],[340,538],[321,511],[304,485],[285,454],[265,427],[250,404],[236,375],[222,346],[215,321],[211,290],[214,266],[222,239],[239,216],[266,197],[288,190]]}
# R outer dashes; closure follows A-I boundary rather than internal tracer patches.
outer={1:[[539,354],[576,385],[611,416],[644,452],[675,489],[711,532],[740,578],[762,625],[774,659],[773,681],[755,705],[725,726],[692,737],[661,741],[629,735],[597,724],[562,706],[530,682],[500,651],[489,623]],2:[[530,357],[571,388],[606,420],[637,455],[668,492],[702,534],[732,577],[753,622],[764,660],[764,683],[746,710],[717,732],[683,745],[650,748],[617,742],[586,729],[555,711],[522,686],[494,652],[480,625]],3:[[534,347],[575,379],[609,413],[643,449],[673,488],[706,530],[737,573],[758,619],[768,654],[765,683],[746,706],[716,724],[684,736],[651,740],[618,735],[586,723],[555,708],[524,681],[494,646],[492,616]],4:[[531,356],[568,386],[601,416],[631,451],[663,490],[696,531],[727,575],[749,619],[760,655],[758,686],[739,709],[710,731],[679,742],[646,746],[616,740],[585,727],[554,711],[523,687],[486,649],[481,629]]}
for i,a in anchors.items():
 m=f'fig06_panel{i}';ai=curve(a,closed=True)
 note='Smooth printed A-I envelope retraced independently on this panel. L-in-circles, tracer squares/stars/dots and the injection patch are internal annotations. Fig6 panels 3 and 4 show the same tamarin 87-44 hemisphere with less superimposed label and support the hidden left arc in panels 1 and 2; no other animal supplies geometry. Short symbol gaps bridged along source tangents. Scale and repeated-view status retained.'
 candidate(p,m,'A-I',[ai],note)
 # Reuse exactly the dense A-I run between the two source R junctions.
 start=next(k for k,x in enumerate(ai) if x==[float(t) for t in outer[i][0]])
 end=next(k for k,x in enumerate(ai) if x==[float(t) for t in outer[i][-1]])
 shared=ai[start:end+1]
 rp=curve(outer[i])+list(reversed(shared))[1:]
 candidate(p,m,'R',[rp],'R envelope follows the printed dashed outer boundary, bridging inter-dash gaps. Its A-I border is the identical corrected A-I run. Tracer patches are included tissue; Fig6 panels 3/4 confirm the same-case border under the dense marks in panels 1/2. Existing repeated-view and calibration restrictions retained.')
