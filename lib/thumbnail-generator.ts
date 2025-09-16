import { exec } from 'child_process'
import { promisify } from 'util'
import path from 'path'
import fs from 'fs'

const execAsync = promisify(exec)

export interface ThumbnailOptions {
  width?: number
  height?: number
  timeOffset?: string // e.g., '00:00:10' for 10 seconds
  quality?: number // 1-31, lower is better
}

export class ThumbnailGenerator {
  private static readonly DEFAULT_OPTIONS: Required<ThumbnailOptions> = {
    width: 320,
    height: 180,
    timeOffset: '00:00:05',
    quality: 2
  }

  /**
   * Generate thumbnail from video file using FFMPEG
   * @param videoPath Path to the video file
   * @param outputPath Path where thumbnail will be saved
   * @param options Thumbnail generation options
   */
  static async generateThumbnail(
    videoPath: string,
    outputPath: string,
    options: ThumbnailOptions = {}
  ): Promise<{ success: boolean; path?: string; error?: string }> {
    try {
      const opts = { ...this.DEFAULT_OPTIONS, ...options }
      
      // Ensure output directory exists
      const outputDir = path.dirname(outputPath)
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true })
      }

      // FFMPEG command to generate thumbnail
      const command = [
        'ffmpeg',
        '-i', `"${videoPath}"`,
        '-ss', opts.timeOffset,
        '-vframes', '1',
        '-vf', `scale=${opts.width}:${opts.height}`,
        '-q:v', opts.quality.toString(),
        '-y', // Overwrite output file
        `"${outputPath}"`
      ].join(' ')

      console.log('🎬 Generating thumbnail:', command)
      
      await execAsync(command)
      
      // Verify thumbnail was created
      if (fs.existsSync(outputPath)) {
        const stats = fs.statSync(outputPath)
        console.log(`✅ Thumbnail generated: ${outputPath} (${stats.size} bytes)`)
        return { success: true, path: outputPath }
      } else {
        throw new Error('Thumbnail file was not created')
      }
      
    } catch (error) {
      console.error('❌ Thumbnail generation failed:', error)
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      }
    }
  }

  /**
   * Generate thumbnail for video and upload to S3
   * @param videoFile Video file object
   * @param s3Key S3 key where thumbnail will be uploaded
   */
  static async generateAndUploadThumbnail(
    videoFile: File,
    s3Key: string
  ): Promise<{ success: boolean; thumbnailUrl?: string; error?: string }> {
    try {
      // Create temporary paths
      const tempDir = path.join(process.cwd(), 'temp')
      if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir, { recursive: true })
      }

      const videoTempPath = path.join(tempDir, `video_${Date.now()}_${videoFile.name}`)
      const thumbnailTempPath = path.join(tempDir, `thumb_${Date.now()}.jpg`)

      try {
        // Save video file temporarily
        const videoBuffer = Buffer.from(await videoFile.arrayBuffer())
        fs.writeFileSync(videoTempPath, videoBuffer)

        // Generate thumbnail
        const result = await this.generateThumbnail(videoTempPath, thumbnailTempPath)
        
        if (!result.success) {
          return { success: false, error: result.error }
        }

        // Upload thumbnail to S3
        const { mediaflowClient } = await import('./aws-client')
        const thumbnailBuffer = fs.readFileSync(thumbnailTempPath)
        const thumbnailKey = s3Key.replace(/\.[^.]+$/, '_thumb.jpg')
        
        const uploadResult = await mediaflowClient.uploadThumbnail(thumbnailKey, thumbnailBuffer.buffer)
        
        if (uploadResult.success) {
          return { 
            success: true, 
            thumbnailUrl: `https://mediaflow-uploads-969430605054.s3.amazonaws.com/${thumbnailKey}` 
          }
        } else {
          return { success: false, error: uploadResult.error }
        }

      } finally {
        // Cleanup temporary files
        try {
          if (fs.existsSync(videoTempPath)) fs.unlinkSync(videoTempPath)
          if (fs.existsSync(thumbnailTempPath)) fs.unlinkSync(thumbnailTempPath)
        } catch (cleanupError) {
          console.warn('⚠️ Cleanup warning:', cleanupError)
        }
      }

    } catch (error) {
      console.error('❌ Thumbnail generation and upload failed:', error)
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      }
    }
  }

  /**
   * Check if FFMPEG is available on the system
   */
  static async checkFFMPEGAvailability(): Promise<boolean> {
    try {
      await execAsync('ffmpeg -version')
      return true
    } catch {
      return false
    }
  }

  /**
   * Get video duration using FFPROBE
   */
  static async getVideoDuration(videoPath: string): Promise<number | null> {
    try {
      const command = `ffprobe -v quiet -show_entries format=duration -of csv=p=0 "${videoPath}"`
      const { stdout } = await execAsync(command)
      const duration = parseFloat(stdout.trim())
      return isNaN(duration) ? null : duration
    } catch {
      return null
    }
  }
}