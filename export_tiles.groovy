import qupath.lib.images.servers.LabeledImageServer

def imageData = getCurrentImageData()

// Define output path (relative to project)
def name = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
def pathOutput = buildFilePath(PROJECT_BASE_DIR, 'export', name)
def subPathOutput = buildFilePath(PROJECT_BASE_DIR, 'export', name, 'masks')
mkdirs(pathOutput)
mkdirs(subPathOutput)


// Create an ImageServer where the pixels are derived from annotations
def labelServer = new LabeledImageServer.Builder(imageData)
//    .backgroundLabel(0) // Specify background label (usually 0 or 255)
//    .downsample(downsample)    // Choose server resolution; this should match the resolution at which tiles are exported
    .addLabel('lepidic', 0)     
    .addLabel('acinar', 1)
    .addLabel('micropapillary', 2)
    .multichannelOutput(true)  // If true, each label is a different channel (required for multiclass probability)
    .build()

// Create an exporter that requests corresponding tiles from the original & labeled image servers
new TileExporter(imageData)
//    .downsample(downsample)     // Define export resolution
    .imageExtension('.tif')     // Define file extension for original pixels (often .tif, .jpg, '.png' or '.ome.tif')
//    .tileSize(306)              // Define size of each tile, in pixels
    .tileSize(512)
    .labeledServer(labelServer) // Define the labeled image server to use (i.e. the one we just built)
    .annotatedTilesOnly(true)  // If true, only export tiles if there is a (labeled) annotation present
//    .overlap(25)
    .overlap(100)               // Define overlap, in pixel units at the export resolution    .exportJSON(true)
    .labeledImageSubDir("\\masks")
    .imageSubDir("\\images")
    
    .writeTiles(pathOutput)    // Write tiles to the specified directory

// The overlap is already included in the tile size 
print 'Done!'