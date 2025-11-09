import { NextRequest, NextResponse } from 'next/server'
import { exec } from 'child_process'
import { promisify } from 'util'
import fs from 'fs'
import path from 'path'

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File
    
    if (!file || !file.name.endsWith('.ts')) {
      return NextResponse.json({ success: false, message: 'Invalid file' }, { status: 400 })
    }

    const tempDir = path.join(process.cwd(), 'temp')
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true })
    }

    const inputPath = path.join(tempDir, file.name)
    const outputPath = path.join(tempDir, file.name.replace('.ts', '.mp4'))

    const buffer = Buffer.from(await file.arrayBuffer())
    fs.writeFileSync(inputPath, buffer)

    await execAsync(`"C:\\ffmpeg\\bin\\ffmpeg.exe" -i "${inputPath}" -c copy "${outputPath}"`)

    const convertedBuffer = fs.readFileSync(outputPath)

    fs.unlinkSync(inputPath)
    fs.unlinkSync(outputPath)

    return new NextResponse(convertedBuffer, {
      headers: {
        'Content-Type': 'video/mp4',
        'Content-Disposition': `attachment; filename="${file.name.replace('.ts', '.mp4')}"`,
      },
    })

  } catch (error: any) {
    return NextResponse.json({ success: false, message: error.message }, { status: 500 })
  }
}
