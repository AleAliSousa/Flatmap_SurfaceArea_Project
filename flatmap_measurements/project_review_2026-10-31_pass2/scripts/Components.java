import ij.IJ;import ij.ImagePlus;import java.io.*;
public class Components{
 public static void main(String[] args)throws Exception{
  ImagePlus im=IJ.openImage(args[0]);int w=im.getWidth(),h=im.getHeight(),n=w*h,threshold=Integer.parseInt(args[2]);int[] labels=new int[n],queue=new int[n];
  for(int y=0;y<h;y++)for(int x=0;x<w;x++){int c=im.getProcessor().getPixel(x,y);int r=(c>>16)&255,g=(c>>8)&255,b=c&255;labels[y*w+x]=(r+g+b)/3>=threshold?0:-1;}
  int id=0;for(int pos=0;pos<n;pos++)if(labels[pos]==0){id++;int head=0,tail=0;queue[tail++]=pos;labels[pos]=id;while(head<tail){int p=queue[head++],x=p%w,y=p/w;int[] ns={x>0?p-1:-1,x<w-1?p+1:-1,y>0?p-w:-1,y<h-1?p+w:-1};for(int q:ns)if(q>=0&&labels[q]==0){labels[q]=id;queue[tail++]=q;}}}
  try(DataOutputStream out=new DataOutputStream(new BufferedOutputStream(new FileOutputStream(args[1])))){out.writeInt(w);out.writeInt(h);out.writeInt(id);for(int label:labels)out.writeInt(label);}
 }
}
