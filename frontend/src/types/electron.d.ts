/* eslint-disable @typescript-eslint/no-explicit-any */
// src/types/electron.d.ts
declare global {
  interface Window {
    electron: {
      listenDjangoStatus: (callback: (event: any, data: { message: string }) => void) => void
    }
  }
}

export {}
