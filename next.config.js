/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['@aws-sdk/client-s3']
  },
  api: {
    bodyParser: {
      sizeLimit: '100mb'
    }
  }
}

module.exports = nextConfig