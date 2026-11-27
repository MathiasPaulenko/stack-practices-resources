const logger = pino({
  redact: {
    paths: ['password', 'req.headers.authorization', '*.token', '*.ssn'],
    censor: '[REDACTED]'
  }
});
