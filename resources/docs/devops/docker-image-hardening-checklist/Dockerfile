# syntax=docker/dockerfile:1.6
# Hardened multi-stage Dockerfile — companion to
# https://stackpractices.com/docs/docker-image-hardening-checklist/

# ── Builder stage ──────────────────────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
# BuildKit secret mount: private npm registry auth, never baked into layers
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci --omit=dev
COPY . .
RUN npm run build

# ── Final stage — minimal attack surface ──────────────────────
# Pin by digest in production:
#   docker buildx imagetools inspect node:20-alpine
FROM node:20-alpine
WORKDIR /app

# Non-root user with numeric UID (K8s runAsNonRoot compatible)
RUN addgroup -S appuser -g 1001 && \
    adduser -S appuser -u 1001 -G appuser -h /home/appuser

COPY --from=builder --chown=1001:1001 /app/node_modules ./node_modules
COPY --from=builder --chown=1001:1001 /app/dist ./dist
COPY --from=builder --chown=1001:1001 /app/package.json ./

USER 1001:1001
EXPOSE 8080
CMD ["node", "dist/server.js"]
