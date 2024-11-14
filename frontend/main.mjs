import { app, BrowserWindow, Menu } from 'electron'
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
      isDev ? '../backend/dist/DjangoRestfulAPI.exe' : '../APIDataDir/DjangoRestfulAPI.exe'
    )
  } else {
    djangoExecutePath = path.join(
      __dirname, 
      isDev ? '../backend/dist/DjangoRestfulAPI' : '../APIDataDir/DjangoRestfulAPI'
    )
  }

  console.log(`[startDjangoServer] Django Execute Path: ${djangoExecutePath}`)

  if (!fs.existsSync(djangoExecutePath)) {
    console.error('No Django backend exe file found.')
    if (win) {
      win.webContents.send('django-status', { message: 'Django Restful API backend not found, application will close in 10 seconds!' })
    }
    setTimeout(() => {
      app.quit()
    }, 10000)
    return
  }

  djangoProcess = spawn(djangoExecutePath, ['runserver', '--noreload'], { stdio: 'inherit'})

  if (!djangoProcess) {
    console.error('Failed to spawn Django process.')
    if (win) {
      win.webContents.send('django-status', { message: 'Django Restful API backend fail to spawn, application will close in 10 seconds!' })
    }
    setTimeout(() => {
      app.quit()
    }, 10000)
    return
  }

  djangoProcess.on('error', (err) => {
    console.error(`[Django server error] ${err}`)
    if (win) {
      win.webContents.send('django-status', { message: 'Django Restful API backend error, application will close in 10 seconds!' })
    }
    setTimeout(() => {
      app.quit()
    }, 10000)
  })

  djangoProcess.on('exit', (code) => {
    if (code !== 0) {
      console.error(`Django backend process exited with error code ${code}`)
      if (win) {
        win.webContents.send('django-status', { message: `Django backend exit, error code: ${code}\napplication will close in 10 seconds!` })
      }
      setTimeout(() => {
        app.quit()
      }, 10000)
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
        { label: 'Open', click: () => console.log('Open clicked') },
        { label: 'Save', click: () => console.log('Save clicked') },
        { type: 'separator' },
        { label: 'Exit', role: 'quit' }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { label: 'Undo', role: 'undo' },
        { label: 'Redo', role: 'redo' },
        { type: 'separator' },
        { label: 'Cut', role: 'cut' },
        { label: 'Copy', role: 'copy' },
        { label: 'Paste', role: 'paste' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { label: 'Reload', accelerator: 'Ctrl+R', click: () => win.reload() },
        { label: 'Toggle Developer Tools', accelerator: 'Ctrl+Shift+I', click: () => win.webContents.toggleDevTools() },
        { label: 'Actual Size', accelerator: 'Ctrl+0', role: 'resetzoom' },
        { label: 'Zoom In', accelerator: 'Ctrl+Plus', role: 'zoomin' },
        { label: 'Zoom Out', accelerator: 'Ctrl+-', role: 'zoomout' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        { label: 'Learn More', click: () => console.log('Learn More clicked') }
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
    if (win) {
      if (djangoProcess) {
        djangoProcess.kill()
        console.log('[win.onclose] Django backend process killed.')
      }
      killDjangoProcess()
      console.log('[win.onclose] Django exe process killed.')
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
