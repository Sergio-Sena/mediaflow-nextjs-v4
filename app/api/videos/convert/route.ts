import { NextRequest, NextResponse } from 'next/server'
import jwt from 'jsonwebtoken'

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'

interface ConvertRequest {
  fileKey: string
  outputFormats: string[]
  quality: 'low' | 'medium' | 'high'
}

export async function POST(request: NextRequest) {
  try {
    const authHeader = request.headers.get('authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'Token não fornecido' }, { status: 401 })
    }

    const token = authHeader.substring(7)
    
    try {
      jwt.verify(token, JWT_SECRET)
    } catch {
      return NextResponse.json({ error: 'Token inválido' }, { status: 401 })
    }

    const { fileKey, outputFormats, quality }: ConvertRequest = await request.json()

    if (!fileKey || !outputFormats?.length) {
      return NextResponse.json({ 
        error: 'fileKey e outputFormats são obrigatórios' 
      }, { status: 400 })
    }

    const conversionJob = {
      jobId: `job_${Date.now()}`,
      status: 'SUBMITTED',
      inputFile: fileKey,
      outputFormats,
      quality,
      createdAt: new Date().toISOString(),
      estimatedTime: outputFormats.length * 2
    }

    const qualitySettings = {
      low: { bitrate: '1000k', resolution: '720p' },
      medium: { bitrate: '2500k', resolution: '1080p' },
      high: { bitrate: '5000k', resolution: '1440p' }
    }

    const outputs = outputFormats.map(format => ({
      format,
      settings: qualitySettings[quality],
      outputKey: `converted/${fileKey.split('.')[0]}_${quality}.${format}`,
      status: 'QUEUED'
    }))

    return NextResponse.json({
      success: true,
      job: { ...conversionJob, outputs },
      message: 'Conversão iniciada com sucesso'
    })

  } catch (error) {
    console.error('Erro na conversão:', error)
    return NextResponse.json({ error: 'Erro interno do servidor' }, { status: 500 })
  }
}

export async function GET(request: NextRequest) {
  try {
    const authHeader = request.headers.get('authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'Token não fornecido' }, { status: 401 })
    }

    const token = authHeader.substring(7)
    
    try {
      jwt.verify(token, JWT_SECRET)
    } catch {
      return NextResponse.json({ error: 'Token inválido' }, { status: 401 })
    }

    const { searchParams } = new URL(request.url)
    const jobId = searchParams.get('jobId')

    if (!jobId) {
      const mockJobs = [
        {
          jobId: 'job_1704067200000',
          status: 'COMPLETED',
          inputFile: 'videos/sample1.mp4',
          progress: 100,
          createdAt: new Date(Date.now() - 3600000).toISOString(),
          completedAt: new Date(Date.now() - 1800000).toISOString()
        },
        {
          jobId: 'job_1704070800000',
          status: 'IN_PROGRESS',
          inputFile: 'videos/sample2.mov',
          progress: 65,
          createdAt: new Date(Date.now() - 1800000).toISOString()
        }
      ]

      return NextResponse.json({ success: true, jobs: mockJobs })
    }

    const mockJob = {
      jobId,
      status: Math.random() > 0.5 ? 'COMPLETED' : 'IN_PROGRESS',
      inputFile: 'videos/sample.mp4',
      progress: Math.floor(Math.random() * 100),
      outputs: [
        {
          format: 'mp4',
          status: 'COMPLETED',
          outputKey: 'converted/sample_medium.mp4',
          downloadUrl: 'https://example.com/converted/sample_medium.mp4'
        }
      ],
      createdAt: new Date(Date.now() - 1800000).toISOString()
    }

    return NextResponse.json({ success: true, job: mockJob })

  } catch (error) {
    console.error('Erro ao buscar job:', error)
    return NextResponse.json({ error: 'Erro interno do servidor' }, { status: 500 })
  }
}