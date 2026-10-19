# syntax=docker/dockerfile:1.6
FROM node:20-alpine

WORKDIR /app
COPY get-secret.js .

# Build-time secret: mounted for this RUN only, never stored in image layers.
# Build with: docker build --secret id=npm_token,source=$HOME/.npmrc -t my-api .
RUN --mount=type=secret,id=npm_token \
    test -f /run/secrets/npm_token && echo "npm token mounted during build"

CMD ["node", "get-secret.js"]
