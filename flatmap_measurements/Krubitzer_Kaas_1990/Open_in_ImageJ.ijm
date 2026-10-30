// Plugins > Macros > Run; select this file, then choose any figures/ view folder.
// Existing ROI Manager work is preserved: save/clear it yourself before loading.
requires("1.54a");
dir = getDirectory("Choose a figures/ view folder, e.g. fig26D");
if (!File.exists(dir + "source.tif"))
    exit("Choose a figures/ view folder containing source.tif.");
if (roiManager("count") > 0)
    exit("ROI Manager already contains selections. Save them, clear the list, then run this loader again.");
open(dir + "source.tif");
// Remove only the displayed duplicate overlay; source.tif on disk is unchanged.
run("Remove Overlay");
RoiManager.restoreCentered(false);
if (!File.exists(dir + "RoiSet.zip"))
    exit("Calibrated source opened. This panel has no defensible saved cortical ROI; create your own selection if desired.");
roiManager("open", dir + "RoiSet.zip");
roiManager("show all without labels");
getPixelSize(unit, pw, ph);
showStatus("Loaded " + roiManager("count") + " editable selections; " + pw + " " + unit + "/pixel");
