import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Use local Lambda simulation for now
    const result = await handleMultipartAction(body);
    
    return NextResponse.json(result, { 
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      }
    });
    
  } catch (error) {
    console.error('Multipart API error:', error);
    return NextResponse.json(
      { success: false, message: 'Internal server error' },
      { status: 500 }
    );
  }
}

async function handleMultipartAction(body: any) {
  const { action } = body;
  
  switch (action) {
    case 'initiate':
      return { 
        success: true, 
        uploadId: `upload_${Date.now()}`,
        key: body.key 
      };
    case 'getUploadUrl':
      // Generate presigned URL for multipart
      const response = await fetch('/api/upload/presigned-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: body.key,
          contentType: 'application/octet-stream'
        })
      });
      const urlData = await response.json();
      return {
        success: true,
        uploadUrl: urlData.uploadUrl,
        partNumber: body.partNumber
      };
    case 'complete':
      return { success: true, key: body.key };
    case 'abort':
      return { success: true };
    default:
      throw new Error('Invalid action');
  }
}

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
}