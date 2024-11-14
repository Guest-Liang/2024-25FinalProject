import { app, BrowserWindow, Menu } from 'electron'
import path from 'path'
import { execFile, exec } from 'child_process'
import iconv from 'iconv-lite'


const __dirname = path.dirname(new URL(import.meta.url).pathname).slice(1)

let isDev = process.env.NODE_ENV === 'development'
let win
let djangoProcess
let djangoExePath


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

function startDjangoServer() {
  // sometimes use dev mode
  if (!isDev) {
    djangoExePath = path.join(__dirname, '../APIDataDir/DjangoRestfulAPI.exe')
  } else {
    djangoExePath = path.join(__dirname, '../backend/dist/DjangoRestfulAPI.exe')
  }

  djangoProcess = execFile(djangoExePath, ['runserver', '--noreload'], (error, stdout, stderr) => {
    if (error || stderr) {
      console.error(`[django server error] ${error || stderr}`)
      win.webContents.send('django-status', { message: 'Django Restful API backend failed to start, application will close in 10 seconds!' })
      setTimeout(() => {
        app.quit()
      }, 10000)
      return
    }
    console.log(`[django server stdout] ${stdout}`)
  })

  djangoProcess.stdout.on('data', (stdout) => {
    console.log(`[Django server stdout] ${iconv.decode(stdout, 'utf-8')}`)
  })

  djangoProcess.stderr.on('data', (stderr) => {
    console.error(`[Django server stderr] ${iconv.decode(stderr, 'utf-8')}`)
  })

  djangoProcess.on('error', (err) => {
    console.error(`[Django server error] ${err}`)
  })

  djangoProcess.on('exit', (code) => {
    console.log(`Django backend process exited with code ${code}`)
  })
}

function createWindow() {
  win = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 500,
    minHeight: 300,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false,
      cache: 'no-store',
    }
  })

  if (isDev) {
    win.loadURL('http://localhost:5173') // dev, hot reload
    console.log('[createWindow] Load dev server localhost:5173')
  } else {
    win.loadFile('./dist/index.html') // prod
    console.log('[createWindow] Load prod file ./dist/index.html')
  }

  console.log('[createWindow] Waiting window starting...')
  startDjangoServer()

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

  win.on('closed', () => {
    win = null
  })
}

app.whenReady().then(() => {
  createWindow()
  
  win.on('closed', () => {
    if (djangoProcess) {
      djangoProcess.kill()
      console.log('[win.onclose] Django backend process killed.')
    }
    killDjangoProcess()
    console.log('[win.onclose] Django exe process killed.')
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
    console.log('[before-quit] Django exe process killed.')
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
