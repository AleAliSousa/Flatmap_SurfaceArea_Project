from pathlib import Path
import json,sys
import cv2,numpy as np
from PIL import Image,ImageDraw
ROOT=Path('/Users/crossmodal/Library/CloudStorage/OneDrive-AllenInstitute/Flatmap_SurfaceArea_Project')
CFG=Path('/tmp/m1_new_papers/views.json')
def smooth(c,sigma=1.2,step=3):
 p=c.reshape(-1,2).astype(float)
 if len(p)<8:return p.tolist()
 rad=4;x=np.arange(-rad,rad+1);k=np.exp(-x*x/(2*sigma*sigma));k/=sum(k)
 q=sum(np.roll(p,i,axis=0)*v for i,v in zip(range(-rad,rad+1),k))
 q=q[::step];return np.round(q,2).tolist()
def fill(mask,minarea=40):
 cs,_=cv2.findContours(mask.astype('uint8'),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);out=np.zeros(mask.shape,np.uint8)
 for c in cs:
  if cv2.contourArea(c)>=minarea:cv2.drawContours(out,[c],0,1,-1)
 return out

def snap_ink(points,a,radius):
 p=np.asarray(points,float); tangent=np.roll(p,-2,axis=0)-np.roll(p,2,axis=0);n=np.stack([-tangent[:,1],tangent[:,0]],axis=1);n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-6)
 offsets=np.arange(-radius,radius+1,dtype=float);xy=p[:,None,:]+n[:,None,:]*offsets[None,:,None]
 gray=cv2.cvtColor(a,cv2.COLOR_RGB2GRAY).astype(np.float32)/255;gray=cv2.GaussianBlur(gray,(3,3),.6)
 val=cv2.remap(gray,xy[:,:,0].astype(np.float32),xy[:,:,1].astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
 costs=val+.0025*offsets[None,:]**2
 costs=np.concatenate([costs,costs,costs]);m=len(offsets);prior=costs[0].copy();back=np.zeros(costs.shape,np.int16)
 trans=.04*(offsets[:,None]-offsets[None,:])**2;trans[np.abs(offsets[:,None]-offsets[None,:])>3]=1e6
 for i in range(1,len(costs)):
  mat=prior[:,None]+trans;back[i]=np.argmin(mat,axis=0);prior=costs[i]+mat[back[i],np.arange(m)];prior-=prior.min()
 inds=np.zeros(len(costs),int);inds[-1]=prior.argmin()
 for i in range(len(costs)-1,0,-1):inds[i-1]=back[i,inds[i]]
 off=offsets[inds[len(p):2*len(p)]];off=sum(np.roll(off,k)*w for k,w in [(-2,.1),(-1,.2),(0,.4),(1,.2),(2,.1)])
 return p+n*off[:,None]

def segment(a,reg):
 h,w=a.shape[:2]; hsv=cv2.cvtColor(a,cv2.COLOR_RGB2HSV).astype(float);H,S,V=cv2.split(hsv)
 typ=reg['type']
 if typ=='color':
  x,y=reg['seed']; xi,yi=round(x*2),round(y*2); rad=reg.get('sample_radius',5); patch=a[max(0,yi-rad):yi+rad+1,max(0,xi-rad):xi+rad+1]; pc=patch.reshape(-1,3); ph=cv2.cvtColor(patch,cv2.COLOR_RGB2HSV).reshape(-1,3); good=(ph[:,1]>35)&(ph[:,2]>90); pc=pc[good] if good.sum()>=5 else pc[ph[:,2]>30]; sample_rgb=np.median(pc,axis=0).astype(np.uint8); sample=cv2.cvtColor(sample_rgb.reshape(1,1,3),cv2.COLOR_RGB2HSV)[0,0].astype(float); hd=np.abs(H-sample[0]);hd=np.minimum(hd,180-hd)
  mask=(hd<reg.get('hue_tol',9))&(S>reg.get('sat_min',40))&(V>reg.get('value_min',50))
  if 'sat_range' in reg:mask&=(S>=reg['sat_range'][0])&(S<=reg['sat_range'][1])
  if 'rgb_tol' in reg:mask=np.linalg.norm(a.astype(float)-sample_rgb.astype(float),axis=2)<reg['rgb_tol']
 elif typ=='colored_union':mask=(S>reg.get('sat_min',35))&(V>reg.get('value_min',80))
 elif typ=='tile_union':
  mask=((S>25)&(V>80))|((S<=25)&(V>100)&(V<220));mask=cv2.morphologyEx(mask.astype('uint8'),cv2.MORPH_OPEN,np.ones((3,3),np.uint8)).astype(bool)
 elif typ=='palette':
  dist=np.stack([np.linalg.norm(a.astype(float)-np.array(c),axis=2) for c in reg['palette']],axis=2);white_distance=np.linalg.norm(a.astype(float)-255,axis=2);mask=(dist.argmin(axis=2)==reg['color_index'])&(dist.min(axis=2)<reg.get('tolerance',65))&(dist.min(axis=2)<white_distance*.9)&(S>15)&(V>75)
 elif typ=='dark':mask=np.max(a,axis=2)<reg.get('threshold',100)
 elif typ=='outline_fill':mask=np.min(a,axis=2)<reg.get('threshold',230)
 elif typ=='white':
  mask=np.min(a,axis=2)>reg.get('threshold',165)
 elif typ=='manual':
  mask=np.zeros((h,w),np.uint8);p=np.array(reg['points'])*2
  if reg.get('curve'):
   q=[]
   for i in range(len(p)):
    a0,a1,a2,a3=p[(i-1)%len(p)],p[i],p[(i+1)%len(p)],p[(i+2)%len(p)]
    if i in reg.get('sharp_indices',[]):a0=2*a1-a2
    if (i+1)%len(p) in reg.get('sharp_indices',[]):a3=2*a2-a1
    for t in np.linspace(0,1,max(3,int(np.linalg.norm(a2-a1))),endpoint=False):q.append(.5*((2*a1)+(-a0+a2)*t+(2*a0-5*a1+4*a2-a3)*t*t+(-a0+3*a1-3*a2+a3)*t*t*t))
   p=np.array(q)
  if reg.get("snap_ink_radius"):p=snap_ink(p,a,reg["snap_ink_radius"])
  cv2.fillPoly(mask,[np.round(p).astype(np.int32)],1);return mask
 if reg.get('box'):
  x0,y0,x1,y1=[round(v*2) for v in reg['box']];sel=np.zeros((h,w),bool);sel[y0:y1,x0:x1]=True;mask&=sel
 mask=mask.astype(np.uint8)
 for box in reg.get('exclude_boxes',[]):
  x0,y0,x1,y1=[round(z*2) for z in box];mask[y0:y1,x0:x1]=0
 if typ=='white' and reg.get('barrier_close'):
  k=reg['barrier_close'];mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((k,k),np.uint8))
 close=reg.get('close',3)
 if close:mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(close,close)))
 for line in reg.get('barriers',[]):cv2.polylines(mask,[np.round(np.array(line)*2).astype(np.int32)],False,0,reg.get('barrier_width',3))
 if reg.get('gate'):
  g=np.zeros((h,w),np.uint8);cv2.fillPoly(g,[np.round(np.array(reg['gate'])*2).astype(np.int32)],1);mask &= g
 if typ in ['white','outline_fill'] or reg.get('select_seed'):
  if typ=='outline_fill':mask=fill(mask,reg.get('minarea',40))
  _,labs,stats,_=cv2.connectedComponentsWithStats(mask)
  if 'seed' in reg:
   x,y=reg['seed'];lab=labs[round(y*2),round(x*2)]
   if lab==0 or stats[lab,cv2.CC_STAT_AREA]<reg.get('min_seed_area',100) or stats[lab,cv2.CC_STAT_AREA]>h*w*.55:
    eligible=mask.copy()
    for tiny in np.where((stats[:,cv2.CC_STAT_AREA]<reg.get('min_seed_area',100))|(stats[:,cv2.CC_STAT_AREA]>h*w*.55))[0]:eligible[labs==tiny]=0
    ys,xs=np.where(eligible); idx=np.argmin((xs-x*2)**2+(ys-y*2)**2); lab=labs[ys[idx],xs[idx]]
    if (xs[idx]-x*2)**2+(ys[idx]-y*2)**2>35**2:raise ValueError('Seed far outside mask '+reg['label'])
   mask=(labs==lab).astype(np.uint8)
  else:
   lab=1+np.argmax(stats[1:,cv2.CC_STAT_AREA]);mask=(labs==lab).astype(np.uint8)
 if reg.get('preserve_holes'):
  full=fill(mask,reg.get('minarea',40));holes=full & (1-mask);n,ll,ss,_=cv2.connectedComponentsWithStats(holes)
  for j in range(1,n):
   if ss[j,cv2.CC_STAT_AREA]>reg.get('hole_minarea',100):full[ll==j]=0
  return full
 return fill(mask,reg.get('minarea',40))

def run():
 cfg=json.loads(CFG.read_text());stats=[];errors=[]
 if len(sys.argv)>1:cfg=[v for v in cfg if v['paper'] in sys.argv[1:] or v['map_id'] in sys.argv[1:]]
 for v in cfg:
  paper=v['paper'];mid=v['map_id'];folder=ROOT/'flatmap_measurements'/paper/'figures'/mid;folder.mkdir(parents=True,exist_ok=True)
  a=np.array(Image.open('/tmp/m1_new_papers/crops/'+paper+'__'+mid+'.png').convert('RGB'));height,width=a.shape[:2]
  rois=[];masks={}
  for reg in v.get('regions',[]):
   if reg['type']=='union':mask=np.maximum.reduce([masks[l] for l in reg['members']])
   else:
    try:mask=segment(a,reg)
    except Exception as e:
     errors.append([paper,mid,reg['label'],str(e)]);continue
   for child in reg.get('include_regions',[]):mask=np.maximum(mask,masks[child])
   masks[reg['label']]=mask
   cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
   poly=[smooth(c,reg.get('sigma',1.2),reg.get('step',3)) for c in cs if cv2.contourArea(c)>=reg.get('minarea',40)]
   if not poly:
    errors.append([paper,mid,reg['label'],'Empty contour']);continue
   holes=[]
   if reg.get('preserve_holes'):
    hc,hh=cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    holes=[smooth(c) for j,c in enumerate(hc) if hh[0,j,3]>=0 and cv2.contourArea(c)>reg.get('hole_minarea',100)]
   rois.append(dict(label=reg['label'],polygons=poly,exclude_polygons=holes,extent=reg.get('extent','complete'),boundary_note=reg.get('note','Source-guided external field envelope; internal letters and recording symbols retained as tissue. Local smoothing at approximately one rendered pixel; provisional anatomical tracing.')))
  for reg in v.get('regions',[]):
   rr=next((r for r in rois if r['label']==reg['label']),None)
   if rr is not None:
    for lab in reg.get('exclude_regions',[]):
     other=next(r for r in rois if r['label']==lab);rr['exclude_polygons']+=other['polygons']
  outline=None
  if v.get('outline'):
   mask=segment(a,v['outline']);cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);outline=dict(label='drawn_cortical_outline',polygons=[smooth(c) for c in cs if cv2.contourArea(c)>40],boundary_note='Independent visible drawn envelope; illustrative/reconstructed tissue, not a certified whole-neocortex animal denominator.')
  meta=dict(map_id=mid,figure=v['figure'],panel=v.get('panel',mid),pdf_page=v['page'],printed_page=v.get('printed_page','not reported'),species=v['species'],specimen=v.get('specimen','illustrative summary; not an independent animal'),hemisphere=v.get('hemisphere','not reported'),view_type=v.get('view_type','illustrative_flatmap'),hemisphere_relation='not an additional independent specimen',linked_main_map='',repeat_of=v.get('repeat_of'),relationship_note=v.get('relationship_note','Published drawing measured independently; no transfer of workbook estimates or calibration from another paper.'),specimen_link_status=v.get('specimen_link_status','illustrative; excluded from animal means'),allowed_overlap_pairs=v.get('allowed_overlap_pairs',[]),include_in_whole_hemisphere_summary=False,outline_scope='schematic_tissue' if outline else 'none',render_scale=4,crop_xyxy=[round(n*2) for n in v['crop']],scale_endpoints_px=[[x*2,y*2] for x,y in v.get('scale',[])],scale_length_mm=v.get('scale_mm'),scale_note=v.get('scale_note','Local printed scale only; no inferred scale when absent.'),scale_reference_map=v.get('scale_reference_map'),supersample=4,outline=outline,rois=rois,unmeasured=v.get('unmeasured',[]))
  (folder/'rois.json').write_text(json.dumps(meta,indent=2)+'\n')
  im=Image.fromarray(a).resize((width//2,height//2));d=ImageDraw.Draw(im)
  for i,r in enumerate(rois):
   col=['#009e73','#0072b2','#d55e00','#cc79a7','#e69f00','#56b4e9'][i%6]
   for pts in r['polygons']:
    pts=[(x/2,y/2) for x,y in pts];d.line(pts+[pts[0]],fill=col,width=2)
    cen=np.mean(pts,axis=0);d.text(tuple(cen),r['label'],fill=col,stroke_width=1,stroke_fill='white')
  (Path('/tmp/m1_new_papers/drafts')).mkdir(exist_ok=True);im.save('/tmp/m1_new_papers/drafts/'+paper+'__'+mid+'.png');stats.append((paper,mid,len(rois)))
 print(stats); print('ERRORS',errors);Path('/tmp/m1_new_papers/build_errors.json').write_text(json.dumps(errors,indent=2))
if __name__=='__main__':run()
