import { app, BrowserWindow, Menu } from 'electron'
import path from 'path'
import { execFile, exec } from 'child_process'

process.env.NODE_OPTIONS = '--encoding=UTF-8';

const killDjangoProcess = () => {
  exec('taskkill -F -IM DjangoRestfulAPI.exe', (error, stdout, stderr) => {
    if (error) {
      console.error(`[killDjangoProcess] Error killing Django process: ${error}`)
      return
    }
    if (stderr) {
      console.error(`[killDjangoProcess] stderr: ${stderr}`)
      return
    }
    console.log(`[killDjangoProcess] stdout: ${stdout}`)
  })
}

const __dirname = path.dirname(new URL(import.meta.url).pathname).slice(1)

let isDev = true
let win
let djangoProcess
let djangoExePath

function createWindow() {
  win = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 500,
    minHeight: 300,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false,
      cache: 'no-store',
    }
  })

  // sometimes use dev mode
  if (!isDev) {
    djangoExePath = path.join(__dirname, '../APIDataDir/DjangoRestfulAPI.exe')
  } else {
    djangoExePath = path.join(__dirname, '../backend/dist/DjangoRestfulAPI.exe')
  }

  if (!isDev) {
    djangoProcess = execFile(djangoExePath, ['runserver', '--noreload'], (error, stdout, stderr) => {
      if (error) {
        console.error(`[django internal server error] ${error}`)
        return
      }
      if (stderr) {
        console.error(`[django internal server stderr] ${stderr}`)
        return
      }
      console.log(`[django internal server stdout] ${stdout}`)
    })

    djangoProcess.stdout.on('data', (stdout) => {
      console.log(`[Django server stdout] ${stdout.toString()}`)
    })

    djangoProcess.stderr.on('data', (stderr) => {
      console.error(`[Django server stderr] ${stderr.toString()}`)
    })

    djangoProcess.on('error', (err) => {
      console.error(`[Django server error] ${err}`)
    })

    djangoProcess.on('exit', (code) => {
      console.log(`Django backend process exited with code ${code}`)
    })

    win.loadFile('./dist/index.html') // prod
  } else {
    win.loadURL('http://localhost:5173') // dev, hot reload
  }

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

  const menu = Menu.buildFromTemplate(menuTemplate)
  Menu.setApplicationMenu(menu)
}

app.whenReady().then(() => {
  createWindow()
  
  win.on('closed', () => {
    if (djangoProcess) {
      djangoProcess.kill()
      console.log('[win.onclose] Django backend process killed.')
    }
    killDjangoProcess()
  })

  // listen SIGINT (Ctrl+C)
  process.on('SIGINT', () => {
    if (djangoProcess) {
      djangoProcess.kill()
      console.log('[SIGINT] Django backend process killed.')
    }
    app.quit()
  })

  app.on('before-quit', () => {
    if (djangoProcess) {
      djangoProcess.kill()
      console.log('[before-quit] Django backend process killed.')
    }
    killDjangoProcess()
  })

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
