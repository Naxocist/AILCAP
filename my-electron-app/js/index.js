// [openseadragon]
var viewer =  OpenSeadragon({
    id: "dz",
    prefixUrl: "../openseadragon/images/",
    minZoomImageRatio: 0.01,
    visibilityRatio: 0,
    crossOriginPolicy: "Anonymous",
    ajaxWithCredentials: true,
    sequenceMode: true,
    animationTime: 0.5,
    zoomPerScroll: 1.7,

    showNavigator: true,
    navigatorPosition: "BOTTOM_RIGHT", 
    navigatorSizeRatio: 0.2,

    visibilityRatio: 0.8,
    constrainDuringPan: true,

    minZoomLevel: 0.7,
    defaultZoomLevel:	0.7,
  });

const fileInput = document.getElementById('fileInput');

fileInput.addEventListener('change', async () => {
  const file = fileInput.files[0];
  console.log('Selected file:', file);
  viewer.close();

  let tf = await OpenSeadragon.GeoTIFFTileSource.getAllTileSources(file, {
    logLatency: false,
  });

  viewer.open(tf)
});
