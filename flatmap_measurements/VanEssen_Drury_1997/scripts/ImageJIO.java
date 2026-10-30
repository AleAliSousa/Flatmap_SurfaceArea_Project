import ij.IJ;
import ij.ImagePlus;
import ij.ImageStack;
import ij.gui.Overlay;
import ij.gui.Roi;
import ij.io.FileSaver;
import ij.io.RoiDecoder;
import ij.io.RoiEncoder;
import ij.measure.Calibration;
import ij.measure.Measurements;
import ij.plugin.filter.ThresholdToSelection;
import ij.process.ByteProcessor;
import ij.process.ImageProcessor;
import java.awt.Color;
import java.nio.file.*;
import java.util.*;
import java.util.zip.*;
import java.io.*;

/** Native ImageJ export and pixel-exact ROI/TIFF read-back verification. */
public class ImageJIO {
    static void check(boolean condition, String message) {
        if (!condition) throw new IllegalStateException(message);
    }
    static void checkCalibration(ImagePlus im, double pixelSize, String unit) {
        Calibration c = im.getCalibration();
        check(Math.abs(c.pixelWidth-pixelSize)<Math.max(1e-8,Math.abs(pixelSize)*1e-6) && Math.abs(c.pixelHeight-pixelSize)<Math.max(1e-8,Math.abs(pixelSize)*1e-6),
              "Calibration changed on disk: "+im.getTitle());
        check(c.getUnit().equals(unit), "Unit changed on disk: "+c.getUnit());
    }
    static ByteProcessor rasterize(Roi roi, int w, int h) {
        ByteProcessor result = new ByteProcessor(w,h);
        result.setValue(255);
        result.fill(roi);
        return result;
    }
    static void samePixels(ImageProcessor a, ImageProcessor b, String description) {
        check(a.getWidth()==b.getWidth() && a.getHeight()==b.getHeight(),description+" size mismatch");
        for(int i=0;i<a.getPixelCount();i++)
            check(a.get(i)==b.get(i),description+" pixel mismatch at "+i);
    }
    public static void main(String[] args) throws Exception {
        Path jobs = Paths.get(args[0]);
        Path output = Paths.get(args[1]);
        Path diagnostics = Paths.get(args[2]);
        List<String> lines = Files.readAllLines(jobs);
        Map<String,List<String[]>> groups = new LinkedHashMap<>();
        for (String line:lines.subList(1,lines.size())) {
            String[] r=line.split("\t",-1);
            groups.computeIfAbsent(r[0], k->new ArrayList<>()).add(r);
        }
        StringBuilder report=new StringBuilder("map_id\troi_index\tlabel\tarea_pixels\tarea_calibrated\tunit\toriginal_fractional_pixels\tpixel_difference_percent\troi_roundtrip_pixels_equal\n");
        int total=0;
        for (Map.Entry<String,List<String[]>> entry:groups.entrySet()) {
            String fig=entry.getKey(); List<String[]> rows=entry.getValue(); String[] first=rows.get(0);
            Path folder=output.resolve(fig); Files.createDirectories(folder);
            double pixelSize=Double.parseDouble(first[5]); String unit=first[6];
            ImagePlus source=IJ.openImage(first[3]); check(source!=null,"Cannot open source");
            Calibration calibration=new Calibration(); calibration.pixelWidth=pixelSize;
            calibration.pixelHeight=pixelSize; calibration.setUnit(unit); source.setCalibration(calibration);
            source.setProperty("Info", "Cortical flatmap view "+fig+". Provisional manual traces. "
                +(unit.equals("pixel")?"No scale line: pixel units only.":"Calibration provenance is in rois.json. No shrinkage correction.")
                +" Overlay and RoiSet.zip contain the same editable selections; do not import both.");
            if (Integer.parseInt(first[1])<0) {
                source.setOverlay((Overlay)null);
                check(new FileSaver(source).saveAsTiff(folder.resolve("source.tif").toString()),"Source save failed");
                ImagePlus reread=IJ.openImage(folder.resolve("source.tif").toString());
                checkCalibration(reread,pixelSize,unit);
                samePixels(source.getProcessor(),reread.getProcessor(),"Untraced source "+fig);
                System.out.println("View "+fig+": calibrated source retained; no defensible field ROI");
                continue;
            }
            Overlay overlay=new Overlay();
            ImageStack masks=new ImageStack(source.getWidth(),source.getHeight());
            ArrayList<ImageProcessor> expected=new ArrayList<>();
            try(ZipOutputStream zip=new ZipOutputStream(Files.newOutputStream(folder.resolve("RoiSet.zip")))) {
                for(String[] row:rows) {
                    int index=Integer.parseInt(row[1]); String label=row[2];
                    ImagePlus mask=IJ.openImage(row[4]); check(mask!=null,"Cannot open mask");
                    ImageProcessor ip=mask.getProcessor(); expected.add(ip.duplicate());
                    ip.setThreshold(255,255,ImageProcessor.NO_LUT_UPDATE);
                    Roi roi=new ThresholdToSelection().convert(ip); check(roi!=null,"Empty mask");
                    String name=String.format("%02d %s",index,label);
                    roi.setName(name); roi.setPosition(0); roi.setStrokeColor(Color.decode(row[8])); roi.setStrokeWidth(1);
                    byte[] bytes=RoiEncoder.saveAsByteArray(roi);
                    Roi decoded=new RoiDecoder(bytes,name).getRoi();
                    samePixels(ip,rasterize(decoded,source.getWidth(),source.getHeight()),"ROI "+fig+" "+name);
                    zip.putNextEntry(new ZipEntry(String.format("%02d_%s.roi",index,label.replaceAll("[^A-Za-z0-9_-]","_"))));
                    zip.write(bytes); zip.closeEntry();
                    overlay.add(roi); ip.resetThreshold(); masks.addSlice(name,ip);
                }
            }
            overlay.drawLabels(false); overlay.drawNames(true); source.setOverlay(overlay);
            check(new FileSaver(source).saveAsTiff(folder.resolve("source.tif").toString()),"Source save failed");
            ImagePlus maskStack=new ImagePlus("Masks.tif",masks); maskStack.setCalibration(calibration.copy());
            check(new FileSaver(maskStack).saveAsZip(folder.resolve("Masks.tif.zip").toString()),"Mask save failed");
            ImagePlus reread=IJ.openImage(folder.resolve("source.tif").toString());
            checkCalibration(reread,pixelSize,unit); samePixels(source.getProcessor(),reread.getProcessor(),"Source TIFF "+fig);
            check(reread.getOverlay()!=null && reread.getOverlay().size()==rows.size(),"Missing TIFF overlay");
            ImagePlus maskRead=IJ.openImage(folder.resolve("Masks.tif.zip").toString());
            check(maskRead!=null && maskRead.getStackSize()==rows.size(),"Mask stack size mismatch");
            checkCalibration(maskRead,pixelSize,unit);
            try(ZipFile zip=new ZipFile(folder.resolve("RoiSet.zip").toFile())) {
                Enumeration<? extends ZipEntry> entries=zip.entries(); int i=0;
                while(entries.hasMoreElements()) {
                    ZipEntry ze=entries.nextElement(); byte[] bytes=zip.getInputStream(ze).readAllBytes();
                    Roi roi=new RoiDecoder(bytes,ze.getName()).getRoi(); String[] row=rows.get(i);
                    samePixels(expected.get(i),rasterize(roi,source.getWidth(),source.getHeight()),"ZIP ROI "+fig+" "+i);
                    samePixels(expected.get(i),maskRead.getStack().getProcessor(i+1),"Mask TIFF "+fig+" "+i);
                    samePixels(expected.get(i),rasterize(reread.getOverlay().get(i),source.getWidth(),source.getHeight()),"Overlay "+fig+" "+i);
                    reread.setRoi(roi); double area=reread.getStatistics(Measurements.AREA).area;
                    int pixels=0; ImageProcessor m=expected.get(i);
                    for(int p=0;p<m.getPixelCount();p++) if(m.get(p)==255) pixels++;
                    double readSize=reread.getCalibration().pixelWidth;
                    check(Math.abs(area-pixels*readSize*readSize)<1e-7,"Measured area differs: fig "+fig+" ROI "+i+" got "+area+" expected "+(pixels*readSize*readSize));
                    double original=Double.parseDouble(row[7]);
                    report.append(fig+"\t"+row[1]+"\t"+row[2]+"\t"+pixels+"\t"+area+"\t"+(unit.equals("mm")?"mm^2":"pixel^2")+"\t"+original+"\t"+(100*(pixels-original)/original)+"\ttrue\n");
                    i++; total++;
                }
                check(i==rows.size(),"ZIP count mismatch");
            }
            System.out.println("Figure "+fig+": "+rows.size()+" selections, TIFF calibration and all pixels verified");
        }
        Files.writeString(diagnostics.resolve("imagej_measurements.tsv"),report);
        Files.writeString(diagnostics.resolve("imagej_runtime.txt"),"ImageJ "+IJ.getVersion()+"; Java "+System.getProperty("java.version")+"; "+total+" ROIs verified\n");
    }
}
