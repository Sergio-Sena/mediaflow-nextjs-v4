/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: [
      'videos.sstechnologies-cloud.com',
      'd2we88koy23cl4.cloudfront.net',
      'video-streaming-sstech-v3.s3.amazonaws.com'
    ],
  },
  env: {
    AWS_REGION: process.env.AWS_REGION,
    AWS_ACCESS_KEY_ID: process.env.AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY: process.env.AWS_SECRET_ACCESS_KEY,
    JWT_SECRET: process.env.JWT_SECRET,
  }
}

module.exports = nextConfig