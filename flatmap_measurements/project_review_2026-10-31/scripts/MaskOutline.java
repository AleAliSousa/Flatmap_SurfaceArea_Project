import ij.IJ;
import ij.gui.Roi;
import ij.plugin.filter.ThresholdToSelection;
import ij.process.ImageProcessor;
import ij.process.FloatPolygon;
import java.nio.file.*;
public class MaskOutline {
 public static void main(String[] args) throws Exception {
  ImageProcessor p=IJ.openImage(args[0]).getProcessor();p.setThreshold(128,255,ImageProcessor.NO_LUT_UPDATE);
  Roi r=new ThresholdToSelection().convert(p);FloatPolygon f=r.getFloatPolygon();
  StringBuilder b=new StringBuilder("[");for(int i=0;i<f.npoints;i++){if(i>0)b.append(',');b.append('[').append(f.xpoints[i]).append(',').append(f.ypoints[i]).append(']');}b.append(']');Files.writeString(Path.of(args[1]),b.toString());
 }
}
