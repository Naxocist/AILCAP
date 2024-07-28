const { app, BrowserWindow, dialog, ipcMain } = require("electron");
const { join } = require("path")

let win;

app.whenReady().then(main);

function main() {
  win = new BrowserWindow({ 
    width: 800, 
    height: 600, 
    autoHideMenuBar: true,
    show: false,
    webPreferences: {
      preload: join(__dirname, './js/preload.js') // Load the preload script
    }
  })

  win.loadFile('./html/index.html')
  win.webContents.openDevTools();
  win.on('ready-to-show', win.show)
}

ipcMain.on("process", (event, args) => {
  const { spawn } = require("node:child_process");

  const py = spawn('python', ['./js/script.py', args]);

  // on python output
  py.stdout.on("data", function (data) {
    msg = data.toString()
    win.webContents.send("message", msg)
  });

  py.stderr.on('data', (data) => {
    console.error(`Error: ${data}`);
  });
  
  py.stdout.on("end", function () {
    console.log("script.py terminated!")
    win.webContents.send("message", "done");
  })
})
