# Multi-stage build za Floworio Frontend
# Stage 1: Build Next.js frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Kopiraj package files
COPY floworio/apps/web/package*.json ./

# Instaliraj zavisnosti
RUN npm install

# Kopiraj source kod
COPY floworio/apps/web/ .

# Build aplikaciju
RUN npm run build

# Stage 2: Production image za frontend
FROM node:18-alpine

WORKDIR /app

# Kopiraj samo potrebne fajlove iz builder stage-a
COPY --from=frontend-builder /app/package*.json ./
COPY --from=frontend-builder /app/.next ./.next
COPY --from=frontend-builder /app/public ./public

# Instaliraj samo production zavisnosti
RUN npm ci --only=production

# Expose port
EXPOSE 3000

# Start aplikaciju
CMD ["npm", "start"]
