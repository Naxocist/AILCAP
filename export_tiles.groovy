import qupath.lib.images.servers.LabeledImageServer

def imageData = getCurrentImageData()

// Define output path (relative to project)
def name = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())

double spatialCalibration = imageData.getServer().getPixelCalibration().getAveragedPixelSize()

println "Spatial Calibration is " + spatialCalibration + " µm"

// Define output resolution
double requestedPixelSize = 0.2441
def factors = [1, 2, 5, 10] as int[]

for (int i = 0; i < 4; i++) {
    def factor = factors[i]
    def folder = factor.toString()
    println "Extracting downsample x" + factor + " of " + name
    
    def pathOutput = buildFilePath(PROJECT_BASE_DIR, 'export', '512', folder)
    mkdirs(pathOutput)
    
//    double downsample = requestedPixelSize / spatialCalibration
    double downsample = factor

    // Create an ImageServer where the pixels are derived from annotations
    def labelServer = new LabeledImageServer.Builder(imageData)
    //    .backgroundLabel(0) // Specify background label (usually 0 or 255)
        .downsample(downsample)    // Choose server resolution; this should match the resolution at which tiles are exported
        .addLabel('lepidic', 0)     
        .addLabel('acinar', 1)
        .addLabel('solid', 2)
        .addLabel('micropapillary', 3)
        .addLabel('papillary', 4)
        .multichannelOutput(true)  // If true, each label is a different channel (required for multiclass probability)
        .build()
    
    // Create an exporter that requests corresponding tiles from the original & labeled image servers
    new TileExporter(imageData)
        .downsample(downsample)     // Define export resolution
        .imageExtension('.tif')     // Define file extension for original pixels (often .tif, .jpg, '.png' or '.ome.tif')
        .tileSize(512)
        .labeledServer(labelServer) // Define the labeled image server to use (i.e. the one we just built)
        .annotatedTilesOnly(true)  // If true, only export tiles if there is a (labeled) annotation present
        .overlap(100)               // Define overlap, in pixel units at the export resolution    .exportJSON(true)
        .labeledImageSubDir("\\masks")
        .imageSubDir("\\images")
        
        .writeTiles(pathOutput)    // Write tiles to the specified directory
    
    // The overlap is already included in the tile size 
}


print 'Done!'