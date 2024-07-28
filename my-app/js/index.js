// [openseadragon]


const fileInput = document.getElementById('fileInput');

let file = undefined
viewer =  OpenSeadragon({
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
  maxZoomLevel: 100,
  maxZoomPixelRatio: 100,
  defaultZoomLevel:	0.7,
});


fileInput.addEventListener('change', async () => {
  file = fileInput.files[0];
  console.log('Selected file:', file);

  const fileName = file.name;
  const fileExtension = fileName.split('.').pop().toLowerCase();
  
  // console.log('Selected file:', fileName);
  // console.log('File extension:', fileExtension);

  viewer.close()

  if (['png', 'jpg', 'jpeg'].includes(fileExtension)) {
    console.log("PNG!")
    viewer.open({
      type: "image",
      url: file.path,
      buildPyramid: false
    })
    return 
  }

  // .svs
  let tf = await OpenSeadragon.GeoTIFFTileSource.getAllTileSources(file, {
    logLatency: false,
  });

  viewer.open(tf)
});


function loadContent(html) {
  document.getElementById('content').innerHTML = html;
}


const test = () => {
  // const { spawn } = require('node:child_process');
  
  console.log("CLICK :", file_path)
}
