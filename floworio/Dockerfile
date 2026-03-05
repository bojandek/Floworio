# Multi-stage build za Floworio
# Stage 1: Build Next.js frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/apps/web

# Kopiraj package files
COPY apps/web/package*.json ./

# Instaliraj zavisnosti
RUN npm ci

# Kopiraj source kod
COPY apps/web/ .

# Build aplikaciju
RUN npm run build

# Stage 2: Production image za frontend
FROM node:18-alpine AS frontend

WORKDIR /app

# Kopiraj samo potrebne fajlove iz builder stage-a
COPY --from=frontend-builder /app/apps/web/package*.json ./
COPY --from=frontend-builder /app/apps/web/.next ./.next
COPY --from=frontend-builder /app/apps/web/public ./public

# Instaliraj samo production zavisnosti
RUN npm ci --only=production

# Expose port
EXPOSE 3000

# Start aplikaciju
CMD ["npm", "start"]
