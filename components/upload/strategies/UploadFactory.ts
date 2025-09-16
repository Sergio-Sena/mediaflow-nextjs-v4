import { UploadStrategy } from './UploadStrategy'
import { SmallFileUpload } from './SmallFileUpload'
import { LargeFileUpload } from './LargeFileUpload'

export class UploadFactory {
  private static readonly SIZE_THRESHOLD = 5 * 1024 * 1024 // 5MB

  static createStrategy(fileSize: number): UploadStrategy {
    if (fileSize > this.SIZE_THRESHOLD) {
      return new LargeFileUpload()
    } else {
      return new SmallFileUpload()
    }
  }

  static getStrategyInfo(fileSize: number): { type: string; timeout: string; retries: number } {
    if (fileSize > this.SIZE_THRESHOLD) {
      return {
        type: 'LargeFile',
        timeout: '2h',
        retries: 5
      }
    } else {
      return {
        type: 'SmallFile',
        timeout: '5min',
        retries: 5
      }
    }
  }
}