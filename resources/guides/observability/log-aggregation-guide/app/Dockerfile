FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY logger.js ./
RUN mkdir -p /var/log/app
CMD ["node", "logger.js"]
