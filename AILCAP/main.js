const {app, BrowserWindow, dialog, ipcMain} = require('electron');
const path = require('node:path')


let win;

function createWindow() {

  win = new BrowserWindow({ 
    show: false,
    width: 800, 
    height: 600, 
    webPreferences: {
      preload: path.join(__dirname, './js/preload.js'), // Load the preload script
    }
  })
  

  win.loadFile('./html/index.html')
  // let contents = win.webContents;
  // console.log(contents)

  win.webContents.openDevTools();

  win.once('ready-to-show', () => {
    win.show()
  })

  win.on('closed', () => {
    win = null
  });
}


const processSVS = (path) => new Promise((resolve, reject) => {

  const { spawn } = require('node:child_process');

  console.log("Data sent to python script: ", path);

  const python_process = spawn('python', ['python/extracting_svs.py', path]);

  python_process.stdout.on('data', data => {
    console.log("Python script DONE!")
    lst = data.toString().split('\n')
    console.log("Data received from python script:", lst);
    resolve()
  })
})

const handleSelect = () => new Promise((resolve, reject) => {
  dialog.showOpenDialog(win, {
    properties: ['openFile'],
    filters: [{ name: 'ScanScope Virtual Slide', extensions: ['svs'] }]
  })
    .then(result => {

      if (result.canceled) {
        reject('cancel');
        return ;
      }

      const path = result.filePaths[0];

      processSVS(path).then(resolve);
      // resolve();
    })
    .catch(err => {
      console.log(err);
      reject("ERROR!")
    })
})


app.whenReady().then(() => {
  ipcMain.handle('select', handleSelect)
  createWindow()
})

// For Mac
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
