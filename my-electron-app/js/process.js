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
    zoomPerScroll: 1.7
  });

const fileInput = document.getElementById('fileInput');

fileInput.addEventListener('change', function() {
  const file = fileInput.files[0];
  console.log('Selected file:', file);
  viewer.close();

  let tiffTileSources = OpenSeadragon.GeoTIFFTileSource.getAllTileSources(file, {
    logLatency: false,
  });

  tiffTileSources.then( tf => viewer.open(tf))
});


// const view = async () => {

//     const path = 'D:/NSC2024_dataset/svs/S58-03668 B.svs'

//     let tiffTileSources = await OpenSeadragon.GeoTIFFTileSource.getAllTileSources(path, {
//       logLatency: true,
//     });

//     var test = OpenSeadragon.Viewer({
//         id: 'dz',
//         crossOriginPolicy: "Anonymous",
//         ajaxWithCredentials: true,
//         prefixUrl: "../openseadragon/images/",
//         tileSources: tiffTileSources,
//         // animationTime: 0,
//         // zoomPerScroll: 1.7
//     });

//     // const viewer = new OpenSeadragon.Viewer({
//     //   id: 'dz',
//     //   crossOriginPolicy: "Anonymous",
//     //   ajaxWithCredentials: true,
//     //   tileSources: tiffTileSources,
//     // });
// }

// // view()

