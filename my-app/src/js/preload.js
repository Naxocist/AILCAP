const { contextBridge, ipcRenderer } = require("electron")

const WINDOW_API = {
    process: (message) => ipcRenderer.send("process", message),
    onMessage: (callback) => ipcRenderer.on("message", (event, args) => {
        callback(args)
    }),
    onError: (callback) => ipcRenderer.on("error", (event, args) => {
        callback(args)
    })
}

contextBridge.exposeInMainWorld('api', WINDOW_API)
  

    