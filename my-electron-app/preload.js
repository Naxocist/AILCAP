const { contextBridge, ipcRenderer } = require('electron')


contextBridge.exposeInMainWorld('API', {
    select: () => ipcRenderer.invoke('select')
})
  

    