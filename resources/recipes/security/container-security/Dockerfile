# Hardened multi-stage Dockerfile — distroless runtime
# Build tools and dev dependencies never reach the final image.

FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build

FROM gcr.io/distroless/nodejs20-debian12 AS production
# Distroless: no shell, no package manager, non-root uid 65532
COPY --from=builder --chown=65532:65532 /app/node_modules /app/node_modules
COPY --from=builder --chown=65532:65532 /app/dist /app/dist
WORKDIR /app

USER 65532:65532
EXPOSE 3000
CMD ["dist/server.js"]
