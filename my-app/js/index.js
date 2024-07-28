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
const intrepret = document.getElementById('intrepret')
intrepret.classList.add("invisible")


function replaceContent(newContent) {
  content.removeChild(content.firstElementChild);
  content.appendChild(newContent)
}


async function openFile(path) {
  
  const fileExt = file ? file.name.split('.').pop().toLowerCase() : null;
  
  // .svs (file object)
  if (fileExt === '.svs') {
    
    let tf = await OpenSeadragon.GeoTIFFTileSource.getAllTileSources(file, {
      logLatency: false,
    });
    
    viewer.open(tf);
    return 
  }

  let ext = ""
  
  if (path === null) {
    path = file.path;
    ext = file.path.split('.').pop().toLowerCase();
  }else {
    ext = path.split('.').pop().toLowerCase();
  }

  ext = ext.trim().replace(/[\s\u200B-\u200D\uFEFF]/g, ''); // remove hidden character

  // normal images
  if (['png', 'jpg', 'jpeg'].includes(ext)) {
    viewer.open({
      type: "image",
      url: path,
      buildPyramid: false,
    })
    return 
  }

}


function showDeepzoom(path) {
  const outerDiv = document.createElement('div');
  outerDiv.className = 'flex bg-black flex-col grow-[1] h-[100vh]';
  const innerDiv = document.createElement('div');
  innerDiv.id = 'dz';
  innerDiv.className = 'cursor-grab active:cursor-grabbing box-border w-full h-full';
  outerDiv.appendChild(innerDiv);

  replaceContent(outerDiv)

  viewer_setup()
  openFile(path)
}


fileInput.addEventListener('change', () => {

  while(buttons.firstChild) {
    buttons.removeChild(buttons.firstChild)
  }

  file = fileInput.files[0];
  showDeepzoom(null)

});

// -------------------------------------------------------------------------------------------------------------------


// showDeepzoom('D:/OneDrive-CMU/Desktop_Dell/PROJECT/NSC2024/AILCAP/my-app/js/assets/dummy_cropped_predicted/0_0.png')

// back to viewer
const manualBtn = document.createElement('button');
manualBtn.type = 'button';
manualBtn.className = 'mt-2 btn btn-warning';
manualBtn.textContent = 'back to viewer';
manualBtn.onclick = () => showDeepzoom(file.path)

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
    img.className = "w-[200px] h-[200px] hover:cursor-pointer"
    img.src = images[i];
    img.onclick = () => showDeepzoom(images[i])

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

      intrepret.classList.remove("invisible")

      return 
    }

    if(path[0] == '#') {
      path = path.substring(1)
      const data = JSON.parse(path)
      console.log(data)

      const lepidic = document.getElementById('lepidic')
      lepidic.innerHTML = `lepidic: ${data['lepidic']} (${Math.floor(data['lepidic']/64 * 100)}%)`

      const acinar = document.getElementById('acinar')
      acinar.innerHTML = `acinar: ${data['acinar']} (${Math.floor(data['acinar']/64 * 100)}%)`

      const micro = document.getElementById('micro')
      micro.innerHTML = `micro: ${data['micro']} (${Math.floor(data['micro']/64 * 100)}%)`

      const pap = document.getElementById('pap')
      pap.innerHTML = `pap: ${data['pap']} (${Math.floor(data['pap']/64 * 100)}%)`

      const solid = document.getElementById('solid')
      solid.innerHTML = `solid: ${data['solid']} (${Math.floor(data['solid']/64 * 100)}%)`

      return 
    }

    console.log(path)
    let p = Math.floor((images.push(path)/64) * 100)
    console.log(p)
    progress.style.width = `${p}%`

  })
}
