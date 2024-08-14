import qupath.lib.images.servers.LabeledImageServer

def imageData = getCurrentImageData()

// Define output path (relative to project)
def name = GeneralTools.stripExtension(imageData.getServer().getMetadata().getName())

double spatialCalibration = imageData.getServer().getPixelCalibration().getAveragedPixelSize()

def SIZE = 512 // height * width

println "Spatial Calibration is " + spatialCalibration + " µm"


// Define output resolution
double requestedPixelSize = spatialCalibration

def factors = [1, 1.5, 2, 4] as double[]

for (int i = 0; i < 3; i++) {
    def factor = factors[i]
    def folder = factor.toString()
    println "Extracting downsample x" + factor + " of " + name
    
    def outputPath = buildFilePath(PROJECT_BASE_DIR, 'export', SIZE.toString(), folder)
    mkdirs(outputPath)
    
//    double downsample = requestedPixelSize / spatialCalibration
    double downsample = factor

    // Create an ImageServer where the pixels are derived from annotations
    def labelServer = new LabeledImageServer.Builder(imageData)
        .backgroundLabel(0)         // Specify background label (usually 0 or 255)
        .downsample(downsample)     // Choose server resolution; this should match the resolution at which tiles are exported

        .addLabel('solid', 1)     
        .addLabel('micropapillary', 2)
        // .addLabel('lepidic', 0)     
        // .addLabel('acinar', 1)
        // .addLabel('papillary', 3)

        // If true, each label is a different channel (required for multiclass probability)
        .multichannelOutput(true)   
        .build()
    
    // Create an exporter that requests corresponding tiles from the original & labeled image servers
    new TileExporter(imageData)
        .downsample(downsample)     // Define export resolution
        .imageExtension('.tif')     // Define file extension for original pixels (often .tif, .jpg, '.png' or '.ome.tif')
        .tileSize(SIZE)

        // Define the labeled image server to use (i.e. the one we just built)
        .labeledServer(labelServer) 

        // If true, only export tiles if there is a (labeled) annotation present
        .annotatedTilesOnly(true)   

        // Define overlap, in pixel units at the export resolution    .exportJSON(true)
        .overlap((SIZE/8).toInteger())                

        .labeledImageSubDir("/masks")
        .imageSubDir("/images")
        
        .writeTiles(outputPath)     // Write tiles to the specified directory

    // The overlap is already included in the tile size 
}


print 'Done!'