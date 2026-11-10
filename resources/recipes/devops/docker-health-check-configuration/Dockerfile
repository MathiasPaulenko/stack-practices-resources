FROM node:20-alpine

WORKDIR /app

COPY server.js .
RUN apk add --no-cache curl

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
    CMD curl -f http://localhost:3000/health || exit 1

EXPOSE 3000

CMD ["node", "server.js"]
