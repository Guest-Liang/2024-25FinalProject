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

const menuConfig = {
  'en-US': {
    file: 'File',
    clearCache: 'Clear Cache',
    exit: 'Exit',
    edit: 'Edit',
    cut: 'Cut',
    copy: 'Copy',
    paste: 'Paste',
    language: 'Language',
    help: 'Help',
    about: 'About',
    aboutMessage: 'This app was developed by Guest Liang.',
    aboutDetail: 'For more information, visit https://github.com/Guest-Liang.',
    cacheCleared: 'Cache cleared successfully!',
    cacheClearedTitle: 'Cache Cleared',
    reload: 'Reload',
    customAction: 'Custom Action',
    customActionMessage: 'Custom action triggered!',
    toggleDevTools: 'Toggle Developer Tools'
  },
  'zh-CN': {
    file: '文件',
    clearCache: '清除缓存',
    exit: '退出',
    edit: '编辑',
    cut: '剪切',
    copy: '复制',
    paste: '粘贴',
    language: '语言',
    help: '帮助',
    about: '关于',
    aboutMessage: '此应用由 Guest Liang 开发',
    aboutDetail: '更多信息请访问 https://github.com/Guest-Liang',
    cacheCleared: '缓存清除成功！',
    cacheClearedTitle: '缓存已清除',
    reload: '重新加载',
    customAction: '自定义操作',
    customActionMessage: '自定义操作已触发！',
    toggleDevTools: '开发者工具'
  }
}

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
      isDev ? '../../../backend/dist/windows/DjangoRestfulAPI.exe' : '../../../APIDataDir/DjangoRestfulAPI.exe'
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
  win = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 500,
    minHeight: 300,
    webPreferences: {
      preload: path.join(__dirname, 'preload.mjs'),
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
  startDjangoServer()

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
  const langMenu = menuConfig[currentLanguage];

  return [
    {
      label: langMenu.file,
      submenu: [
        {
          label: langMenu.clearCache,
          click: () => {
            const win = BrowserWindow.getFocusedWindow()
            if (win) {
              win.webContents.session.clearCache().then(() => {
                dialog.showMessageBox({
                  type: 'info',
                  title: langMenu.cacheClearedTitle,
                  message: langMenu.cacheCleared,
                  buttons: ['OK']
                })
              })
            }
          }
        },
        { type: 'separator' },
        { label: langMenu.exit, role: 'quit' }
      ]
    },
    {
      label: langMenu.edit,
      submenu: [
        { label: langMenu.cut, role: 'cut' },
        { label: langMenu.copy, role: 'copy' },
        { label: langMenu.paste, role: 'paste' },
      ]
    },
    {
      label: langMenu.language,
      submenu: [
        {
          label: currentLanguage === 'en-US' ? 'English' : '英语',
          type: 'radio',
          checked: currentLanguage === 'en-US',
          click: () => changeLanguage('en-US')
        },
        {
          label: currentLanguage === 'en-US' ? 'Chinese' : '简体中文',
          type: 'radio',
          checked: currentLanguage === 'zh-CN',
          click: () => changeLanguage('zh-CN')
        }
      ]
    },
    {
      label: langMenu.help,
      submenu: [
        {
          label: langMenu.about,
          click: () => {
            dialog.showMessageBox({
              type: 'info',
              title: langMenu.about,
              message: langMenu.aboutMessage,
              detail: langMenu.aboutDetail,
              buttons: ['OK']
            })
          }
        },
        {
          label: langMenu.toggleDevTools,
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
 * @param {string} lang - 语言代码， 'en-US' 或 'zh-CN'
 */
function changeLanguage(lang) {
  currentLanguage = lang
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
    const langMenu = menuConfig[currentLanguage]

    const contextMenu = Menu.buildFromTemplate([
      { label: langMenu.reload || 'Reload', click: () => win.reload() },
      { label: langMenu.copy || 'Copy', role: 'copy', enabled: params.editFlags.canCopy },
      { label: langMenu.paste || 'Paste', role: 'paste', enabled: params.editFlags.canPaste },
      { type: 'separator' },
      {
        label: langMenu.customAction || 'Custom Action',
        click: () => {
          console.log(langMenu.customActionMessage || 'Custom action triggered!');
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
