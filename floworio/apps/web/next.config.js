/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverComponentsExternalPackages: ["@remotion/renderer", "@remotion/bundler"],
  },
  env: {
    API_URL: process.env.API_URL || "http://localhost:8000",
  },
  images: {
    domains: ["localhost"],
  },
  webpack: (config) => {
    config.externals = [...(config.externals || []), { canvas: "canvas" }];
    return config;
  },
};

module.exports = nextConfig;
