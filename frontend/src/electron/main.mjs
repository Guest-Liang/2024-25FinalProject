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
let currentLanguage = 'en-US' // 默认语言

/**
 * @param {*} filename
 * @returns
 * 读取 JSON 文件
 */
function loadJsonFile(filename) {
  let filePath
  if (process.platform === 'win32') {
    filePath = path.join(__dirname, `../locales/${filename}`)
  } else if (process.platform === 'linux') {
    filePath = path.normalize(path.join('/', __dirname, `../locales/${filename}`))
    filePath = decodeURIComponent(filePath)
  } else {
    console.log('Unsupported platform.')
    filePath = path.join(__dirname, `../locales/${filename}`)
    exit(1)
  }

  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'))
  } catch (error) {
    console.error(`[loadJsonFile] Failed to load ${filename}:`, error)
    return {}
  }
}
let langMenu = loadJsonFile(`${currentLanguage}.json`)
const languageNames = loadJsonFile('languages.json')

/**
 * 退出Django进程
 */
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

/**
 * 启动Django服务
 */
function startDjangoServer() {
  // sometimes use dev mode
  if (process.platform === 'win32') {
    djangoExecutePath = path.join(
      __dirname,
      isDev
        ? '../../../backend/dist/windows/DjangoRestfulAPI.exe'
        : '../../../APIDataDir/DjangoRestfulAPI.exe'
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

/**
 * 创建窗口
 */
function createWindow() {
  let preloadPath
  if (process.platform === 'win32') {
    preloadPath = path.join(__dirname, 'preload.mjs')
  } else if (process.platform === 'linux') {
    preloadPath = path.normalize(path.join('/', __dirname, 'preload.mjs'))
    preloadPath = decodeURIComponent(preloadPath)
  } else {
    console.log('Unsupported platform.')
    exit(1)
  }
  win = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 500,
    minHeight: 300,
    icon: path.normalize(path.join(process.platform === 'linux'? '/': '', __dirname, '../assets/GuestLianglogo.png')),
    webPreferences: {
      preload: preloadPath,
      devTools: true,
      nodeIntegration: true,
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
  if (isDev) {
    console.log('[createWindow] Dev mode, remember run backend manually.')
  } else {
    startDjangoServer()
  }

  updateMenu() // 初始化菜单
  setupContextMenu() // 右键菜单

  win.on('closed', () => {
    win = null
  })
}

/**
 * 动态构建菜单
 */
function buildMenu() {
  return [
    {
      label: langMenu.Electron.file,
      submenu: [
        {
          label: langMenu.Electron.clearCache,
          click: () => {
            const win = BrowserWindow.getFocusedWindow()
            if (win) {
              win.webContents.session.clearCache().then(() => {
                dialog.showMessageBox({
                  type: 'info',
                  title: langMenu.Electron.cacheClearedTitle,
                  message: langMenu.Electron.cacheCleared,
                  buttons: ['OK']
                })
              })
            }
          }
        },
        { type: 'separator' },
        { label: langMenu.Electron.exit, role: 'quit' }
      ]
    },
    {
      label: langMenu.Electron.edit,
      submenu: [
        { label: langMenu.Electron.cut, role: 'cut' },
        { label: langMenu.Electron.copy, role: 'copy' },
        { label: langMenu.Electron.paste, role: 'paste' },
      ]
    },
    {
      label: langMenu.Electron.language,
      submenu: Object.keys(languageNames).map((lang) => ({
        label: languageNames[lang], // 动态获取语言名称
        type: 'radio',
        checked: currentLanguage === lang,
        click: () => changeLanguage(lang)
      }))
    },
    {
      label: langMenu.Electron.help,
      submenu: [
        {
          label: langMenu.Electron.about,
          click: () => {
            dialog.showMessageBox({
              type: 'info',
              title: langMenu.Electron.about,
              message: langMenu.Electron.aboutMessage,
              detail: langMenu.Electron.aboutDetail,
              buttons: ['OK']
            })
          }
        },
        {
          label: langMenu.Electron.toggleDevTools,
          accelerator: 'F12',
          click: () => win.webContents.openDevTools({ mode: 'detach' })
        }
      ]
    }
  ]
}

/**
 * 更新菜单
 */
function updateMenu() {
  const menu = Menu.buildFromTemplate(buildMenu())
  Menu.setApplicationMenu(menu)
}

/**
 * 切换语言，通知 Vue
 * @param {string} lang - 语言代码，'en-US' 或 'zh-CN'
 */
function changeLanguage(lang) {
  currentLanguage = lang
  langMenu = loadJsonFile(`${lang}.json`)
  updateMenu()
  console.log('[Electron] Sending change-language IPC event to Vue:', lang) // 记录 IPC 发送情况
  if (win) {
    win.webContents.send('change-language', lang) // 发送事件给 Vue
    console.log(currentLanguage === 'en-US' ? `[changeLanguage] Language changed to ${lang}` : `[changeLanguage] 语言已切换为 ${lang}`)
  } else {
    console.error('[Electron] No window found for IPC event') // 窗口可能丢失
  }
}

/**
 * 右键菜单
 */
function setupContextMenu() {
  win.webContents.on('context-menu', (event, params) => {

    const contextMenu = Menu.buildFromTemplate([
      { label: langMenu.Electron.reload || 'Reload', click: () => win.reload() },
      { label: langMenu.Electron.copy || 'Copy', role: 'copy', enabled: params.editFlags.canCopy },
      { label: langMenu.Electron.paste || 'Paste', role: 'paste', enabled: params.editFlags.canPaste },
      { type: 'separator' },
      {
        label: langMenu.Electron.customAction || 'Custom Action',
        click: () => {
          console.log(langMenu.Electron.customActionMessage || 'Custom action triggered!')
        }
      }
    ])
    contextMenu.popup(win)
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
    if (isDev) {
      console.log('[before-quit] Development mode, no need to kill Django process.')
    } else {
      killDjangoProcess()
      console.log('[before-quit] Django process killed.')
    }
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
