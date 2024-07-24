const { contextBridge, ipcRenderer } = require('electron')
// import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld('API', {
    select: () => ipcRenderer.invoke('select')
})
  

    