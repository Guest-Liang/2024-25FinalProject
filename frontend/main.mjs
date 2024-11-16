import { app, BrowserWindow, Menu, dialog } from 'electron'
import path from 'path'
import { exec, spawn } from 'child_process'
import iconv from 'iconv-lite'
import fs from 'fs'


const __dirname = path.dirname(new URL(import.meta.url).pathname).slice(1)

let isDev = process.env.NODE_ENV === 'development'
let win
let djangoProcess
let djangoExecutePath

const killDjangoProcess = () => {
  let command
  if (process.platform === 'win32') {
    command = 'taskkill -F -IM DjangoRestfulAPI.exe'
  } else {
    command = 'pkill -f DjangoRestfulAPI'
  }

  exec(command, (error, stdout, stderr) => {
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
  if (process.platform === 'win32') {
    djangoExecutePath = path.join(
      __dirname, 
      isDev ? '../backend/dist/windows/DjangoRestfulAPI.exe' : '../APIDataDir/DjangoRestfulAPI.exe'
    )
  } else if (process.platform === 'linux') {
    djangoExecutePath = path.join(
      isDev
        ? path.normalize(path.join('/', __dirname, '../backend/dist/linux/'))
        : path.normalize(path.join(path.dirname(process.argv[0]), 'resources/')),
      'DjangoRestfulAPI'
    )
    djangoExecutePath = decodeURIComponent(djangoExecutePath)
  } else {
    console.log('Unsupported platform.')
    exit(1)
  }

  console.log(`[startDjangoServer] Django Execute Path: ${djangoExecutePath}`)

  if (!fs.existsSync(djangoExecutePath)) {
    console.error('No Django backend file found.')
    return
  }

  djangoProcess = spawn(djangoExecutePath, ['runserver', '--noreload'], { stdio: 'inherit'})

  if (!djangoProcess) {
    console.error('Failed to spawn Django process.')
    return
  }

  djangoProcess.on('error', (err) => {
    console.error(`[Django server error] ${err}`)
  })

  djangoProcess.on('exit', (code) => {
    if (code !== 0) {
      console.error(`Django backend process exited with error code ${code}`)
    } else {
      console.log('Django backend started successfully.')
    }
  })

  if (djangoProcess.stdout) {
    djangoProcess.stdout.on('data', (stdout) => {
      console.log(`[Django server stdout] ${iconv.decode(stdout, 'utf-8')}`)
    })
  }

  if (djangoProcess.stderr) {
    djangoProcess.stderr.on('data', (stderr) => {
      console.error(`[Django server stderr] ${iconv.decode(stderr, 'utf-8')}`)
    })
  }
}

function createWindow() {
  win = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 500,
    minHeight: 300,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      devTools: isDev,
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
    win.loadFile('./dist/index.html') // production
    console.log('[createWindow] Load prod file ./dist/index.html')
  }

  console.log('[createWindow] Waiting window starting...')
  startDjangoServer()

  const menuTemplate = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Clear Cache',
          click: () => {
            const win = BrowserWindow.getFocusedWindow()
            if (win) {
              win.webContents.session.clearCache().then(() => {
                dialog.showMessageBox({
                  type: 'info',
                  title: 'Cache Cleared',
                  message: 'Cache cleared successfully!',
                  buttons: ['OK']
                })
              })
            }
          },
        },
        { type: 'separator' },
        { label: 'Exit', role: 'quit' }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { label: 'Cut', role: 'cut' },
        { label: 'Copy', role: 'copy' },
        { label: 'Paste', role: 'paste' },
      ]
    },
    {
      label: 'View',
      submenu: [
        { label: 'Refresh', accelerator: 'F5', click: () => win.reload() },
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'About',
          click: () => {
            dialog.showMessageBox({
              type: 'info',
              title: 'About',
              message: 'This app was developed by Guest Liang.',
              detail: 'For more information, visit https://github.com/Guest-Liang.',
              buttons: ['OK']
            })
          },
        }
      ]
    }
  ]

  const menu = Menu.buildFromTemplate(menuTemplate)
  Menu.setApplicationMenu(menu)

  win.webContents.on('context-menu', (event, params) => {
    const contextMenu = Menu.buildFromTemplate([
      { label: 'Reload', click: () => win.reload() },
      { label: 'Copy', role: 'copy', enabled: params.editFlags.canCopy },
      { label: 'Paste', role: 'paste', enabled: params.editFlags.canPaste },
      { type: 'separator' },
      { label: 'Custom Action', click: () => {
          console.log('Custom action triggered!')
        }
      }
    ])
    contextMenu.popup(win)
  })

  win.on('closed', () => {
    win = null
  })
}

app.whenReady().then(() => {
  createWindow()
  
  win.on('closed', () => {
    if (win) {
      if (djangoProcess) {
        djangoProcess.kill()
        console.log('[win.onclose] Django backend process killed.')
      }
      killDjangoProcess()
      console.log('[win.onclose] Django process killed.')
    }
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
    console.log('[before-quit] Django process killed.')
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
