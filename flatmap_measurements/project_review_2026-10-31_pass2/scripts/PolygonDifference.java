import java.awt.geom.*;import java.nio.file.*;import java.util.*;
class PolygonDifference {
 static Area read(Scanner s){Area a=new Area();int n=s.nextInt();for(int k=0;k<n;k++){int m=s.nextInt();Path2D.Double p=new Path2D.Double();for(int i=0;i<m;i++){double x=s.nextDouble(),y=s.nextDouble();if(i==0)p.moveTo(x,y);else p.lineTo(x,y);}p.closePath();a.add(new Area(p));}return a;}
 public static void main(String[] args)throws Exception{Scanner s=new Scanner(Files.readString(Path.of(args[0])));s.useLocale(Locale.US);Area a=read(s),b=read(s);a.subtract(b);PathIterator it=a.getPathIterator(null);ArrayList<ArrayList<String>> polys=new ArrayList<>();ArrayList<String> cur=null;double[] c=new double[6];while(!it.isDone()){int t=it.currentSegment(c);if(t==0){cur=new ArrayList<>();polys.add(cur);}if(t==0||t==1)cur.add("["+c[0]+","+c[1]+"]");it.next();}String out="["+String.join(",",polys.stream().map(p->"["+String.join(",",p)+"]").toList())+"]";Files.writeString(Path.of(args[1]),out);}
}
