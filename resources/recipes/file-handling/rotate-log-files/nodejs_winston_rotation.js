// Log rotation with winston and winston-daily-rotate-file.
// Install: npm install winston winston-daily-rotate-file

import winston from 'winston';
import DailyRotateFile from 'winston-daily-rotate-file';

// Size-based rotation with Winston
const sizeTransport = new winston.transports.File({
    filename: 'app.log',
    maxsize: 10 * 1024 * 1024,  // 10 MB
    maxFiles: 5,
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    )
});

// Daily rotation with compression and retention
const dailyTransport = new DailyRotateFile({
    filename: 'app-%DATE%.log',
    datePattern: 'YYYY-MM-DD',
    zippedArchive: true,
    maxSize: '20m',
    maxFiles: '30d',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    )
});

const logger = winston.createLogger({
    level: 'info',
    transports: [sizeTransport, dailyTransport]
});

// Optional: hook into rotation events for monitoring
dailyTransport.on('rotate', (oldFilename, newFilename) => {
    logger.info(`Rotated log: ${oldFilename} -> ${newFilename}`);
});

logger.info('application started');
