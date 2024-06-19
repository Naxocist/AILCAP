const {app, BrowserWindow, dialog, ipcMain} = require('electron')
const path = require('node:path')

let win;

function createWindow() {

  win = new BrowserWindow({ 
    show: false,
    width: 800, 
    height: 600, 
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // Load the preload script
    }
  })


  win.loadFile('./index.html')
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


const handleSelect = () => new Promise((resolve, reject) => {
  dialog.showOpenDialog(win, {
    properties: ['openFile'],
    filters: [{ name: 'ScanScope Virtual Slide', extensions: ['*'] }]
  })
    .then(result => {

      if (result.canceled) {
        reject('cancel')
      }

      resolve(result.filePaths[0]);
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
