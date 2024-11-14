// preload.js
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electron', {
  listenDjangoStatus: (callback) => {
    ipcRenderer.on('django-status', callback)
  }
})
