// [openseadragon]
let viewer = null
function viewer_setup() {
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

    imageSmoothingEnabled: false,
    minPixelRatio: 1
  });
}

viewer_setup()
let file = undefined
const content = document.getElementById("content")
const fileInput = document.getElementById('fileInput');
const buttons = document.getElementById('buttons');

function replaceContent(newContent) {
  content.removeChild(content.firstElementChild);
  content.appendChild(newContent)
}

async function openFile(file) {
  // console.log('Selected file:', file);
  const fileName = file.name;
  const fileExtension = fileName.split('.').pop().toLowerCase();
  // console.log('Selected file:', fileName);
  // console.log('File extension:', fileExtension);

  // normal images
  if (['png', 'jpg', 'jpeg'].includes(fileExtension)) {
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

  viewer.open(tf);
}


fileInput.addEventListener('change', () => {

  while(buttons.firstChild) {
    buttons.removeChild(buttons.firstChild)
  }

  file = fileInput.files[0];
  showDeepzoom()
  // openFile(file)
});


function showDeepzoom() {
  const outerDiv = document.createElement('div');
  outerDiv.className = 'flex bg-black flex-col grow-[1] h-[100vh]';
  const innerDiv = document.createElement('div');
  innerDiv.id = 'dz';
  innerDiv.className = 'cursor-grab active:cursor-grabbing box-border w-full h-full';
  outerDiv.appendChild(innerDiv);

  replaceContent(outerDiv)

  viewer_setup()
  openFile(file)
}


// -------------------------------------------------------------------------------------------------------------------

// back to viewer
const manualBtn = document.createElement('button');
manualBtn.type = 'button';
manualBtn.className = 'mt-2 btn btn-warning';
manualBtn.textContent = 'back to viewer';
manualBtn.onclick = showDeepzoom

// result 
const resBtn = document.createElement('button');
resBtn.type = 'button';
resBtn.className = 'mt-2 btn btn-success';
resBtn.textContent = 'show results';
resBtn.onclick = showImages


// spinner
const spinner = document.createElement('div');
spinner.className = 'mr-2';
spinner.id = 'spinner'
const spinnerDiv = document.createElement('div');
spinnerDiv.className = 'spinner-border spinner-border-sm';
spinnerDiv.setAttribute('role', 'status');
const span = document.createElement('span');
span.className = 'sr-only';
span.textContent = 'Loading...';
spinnerDiv.appendChild(span);
spinner.appendChild(spinnerDiv);


// let images = ['D:/OneDrive-CMU/Desktop_Dell/PROJECT/NSC2024/AILCAP/my-app/js/assets/cropped_predicted/0_0.png']
let images = []


function showImages() {
  const imgContainer = document.createElement('div');
  imgContainer.className = 'p-2 flex flex-wrap justify-around gap-[20px] overflow-y-scroll w-full';
  imgContainer.id = 'img-container';

  replaceContent(imgContainer)

  for (let i = 0; i < images.length; i++) {
    const img = document.createElement('img');
    img.className = "w-[200px] h-[200px]"
    img.src = images[i];

    imgContainer.appendChild(img)
  }
}

const run_script = () => {
  const file_path = file.path
  console.log("current file path :", file_path)

  const progress = document.getElementById("progress")
  progress.style.width = '0%'

  images = []

  // Create loading spinner
  const loading = document.getElementById('loading');
  loading.insertBefore(spinner, loading.firstChild)

  // Send file path to script.py
  window.api.process(file_path)
  window.api.onMessage((path) => {
    if(path === 'done') {
      const spinner = document.getElementById("spinner");
      spinner.remove();

      buttons.appendChild(manualBtn)
      buttons.appendChild(resBtn)
      return 
    }

    console.log(path)
    let p = Math.floor((images.push(path)/64) * 100)
    console.log(p)
    progress.style.width = `${p}%`

  })
}
