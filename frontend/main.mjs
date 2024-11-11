import { app, BrowserWindow, Menu } from 'electron'
import path from 'path'

const __dirname = path.dirname(new URL(import.meta.url).pathname)

let win

function createWindow() {
  win = new BrowserWindow({
    width: 1280,
    height: 720,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false,
      cache: 'no-store',
    }
  })

  // win.loadURL('http://localhost:5173') // dev, hot reload
  win.loadFile('./dist/index.html') // prod
  win.on('closed', () => {
    win = null
  })

  const menuTemplate = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Open',
          click: () => {
            console.log('Open clicked')
          }
        },
        {
          label: 'Save',
          click: () => {
            console.log('Save clicked')
          }
        },
        {
          type: 'separator'
        },
        {
          label: 'Exit',
          role: 'quit'
        }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        {
          label: 'Undo',
          role: 'undo'
        },
        {
          label: 'Redo',
          role: 'redo'
        },
        {
          type: 'separator'
        },
        {
          label: 'Cut',
          role: 'cut'
        },
        {
          label: 'Copy',
          role: 'copy'
        },
        {
          label: 'Paste',
          role: 'paste'
        }
      ]
    },
    {
      label: 'View',
      submenu: [
        {
          label: 'Reload',
          accelerator: 'Ctrl+R',
          click: () => {
            win.reload()  // 重新加载窗口
          }
        },
        {
          label: 'Toggle Developer Tools',
          accelerator: 'Ctrl+Shift+I',
          click: () => {
            win.webContents.toggleDevTools()  // 打开开发者工具
          }
        },
        {
          label: 'Actual Size',
          accelerator: 'Ctrl+0',
          role: 'resetzoom'
        },
        {
          label: 'Zoom In',
          accelerator: 'Ctrl+Plus',
          role: 'zoomin'
        },
        {
          label: 'Zoom Out',
          accelerator: 'Ctrl+-',
          role: 'zoomout'
        }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Learn More',
          click: () => {
            console.log('Learn More clicked')
          }
        }
      ]
    }
  ]

  // 生成并设置菜单
  const menu = Menu.buildFromTemplate(menuTemplate)
  Menu.setApplicationMenu(menu)
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
