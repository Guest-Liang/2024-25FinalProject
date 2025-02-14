import { ipcRenderer, contextBridge } from 'electron'

contextBridge.exposeInMainWorld('electron', {
  changeLanguage: (callback) => {
    ipcRenderer.removeAllListeners('change-language') // 避免重复监听
    ipcRenderer.on('change-language', (_, lang) => callback(lang))
  }
})
