const AWS = require('aws-sdk');
const s3 = new AWS.S3();

const BUCKET = 'mediaflow-uploads-969430605054';

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers };
  }

  try {
    const { action, ...params } = JSON.parse(event.body);

    switch (action) {
      case 'initiate':
        return await initiateMultipart(params, headers);
      case 'getUploadUrl':
        return await getUploadUrl(params, headers);
      case 'complete':
        return await completeMultipart(params, headers);
      case 'abort':
        return await abortMultipart(params, headers);
      default:
        throw new Error('Invalid action');
    }
  } catch (error) {
    console.error('Multipart error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ success: false, message: error.message })
    };
  }
};

async function initiateMultipart({ key, contentType, metadata }, headers) {
  const params = {
    Bucket: BUCKET,
    Key: key,
    ContentType: contentType,
    Metadata: metadata || {}
  };

  const result = await s3.createMultipartUpload(params).promise();
  
  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({
      success: true,
      uploadId: result.UploadId,
      key: result.Key
    })
  };
}

async function getUploadUrl({ key, uploadId, partNumber }, headers) {
  const params = {
    Bucket: BUCKET,
    Key: key,
    PartNumber: partNumber,
    UploadId: uploadId,
    Expires: 3600
  };

  const uploadUrl = s3.getSignedUrl('uploadPart', params);
  
  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({
      success: true,
      uploadUrl,
      partNumber
    })
  };
}

async function completeMultipart({ key, uploadId, parts }, headers) {
  const params = {
    Bucket: BUCKET,
    Key: key,
    UploadId: uploadId,
    MultipartUpload: {
      Parts: parts.map(part => ({
        ETag: part.etag,
        PartNumber: part.partNumber
      }))
    }
  };

  const result = await s3.completeMultipartUpload(params).promise();
  
  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({
      success: true,
      location: result.Location,
      key: result.Key
    })
  };
}

async function abortMultipart({ key, uploadId }, headers) {
  const params = {
    Bucket: BUCKET,
    Key: key,
    UploadId: uploadId
  };

  await s3.abortMultipartUpload(params).promise();
  
  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({ success: true })
  };
}