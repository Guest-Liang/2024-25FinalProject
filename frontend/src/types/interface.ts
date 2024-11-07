// interface.ts
export interface EncodedImageResponse {
  message: string
  results: EncryptResult[]
}

export interface EncryptResult {
  status: string
  EncodedImagePath: string
}


export interface DecodedFileResponse {
  message: string
  results: DecryptResult[]
}

export interface DecryptResult {
  status: string
  DecryptedFilePath: string
}


export interface DownloadLink {
  name: string
  url: string
  originalName: string
}
