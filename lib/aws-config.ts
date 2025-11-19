// AWS Configuration for Mediaflow
export const AWS_CONFIG = {
  API_BASE_URL: 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod',
  
  ENDPOINTS: {
    AUTH: '/auth/login',
    FILES: '/files',
    UPLOAD: '/upload/presigned',
    CLEANUP: '/cleanup',
    BULK_DELETE: '/files/bulk-delete',
    USERS: '/users/list'
  },
  
  BUCKETS: {
    UPLOADS: 'mediaflow-uploads-969430605054',
    PROCESSED: 'mediaflow-processed-969430605054',
    FRONTEND: 'mediaflow-frontend-969430605054'
  },
  
  REGION: 'us-east-1'
};

// Helper function to build full API URLs
export const getApiUrl = (endpoint: keyof typeof AWS_CONFIG.ENDPOINTS) => {
  return `${AWS_CONFIG.API_BASE_URL}${AWS_CONFIG.ENDPOINTS[endpoint]}`;
};