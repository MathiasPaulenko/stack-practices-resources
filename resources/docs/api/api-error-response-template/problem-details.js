/**
 * problem-details.js — RFC 9457 error middleware for Express
 *
 * Mount LAST, after all routes:
 *   const { ApiError, problemDetails } = require('./problem-details');
 *   app.use(problemDetails);
 *
 * Throw from handlers:
 *   throw new ApiError(422, 'https://api.example.com/errors/unprocessable',
 *     'Unprocessable Content', "Cannot schedule delivery for a past date.");
 *
 * Validation errors:
 *   throw new ApiError(400, 'https://api.example.com/errors/validation-failed',
 *     'Validation Failed', '3 fields failed validation.', [
 *       { field: 'email', message: 'must be a valid email address', code: 'invalid_format' },
 *     ]);
 */

class ApiError extends Error {
  constructor(status, type, title, detail, errors) {
    super(detail || title);
    this.status = status;
    this.type = type;
    this.title = title;
    this.errors = errors;
  }
}

const BASE_URI = process.env.API_ERRORS_BASE_URI || 'https://api.example.com/errors';

function problemDetails(err, req, res, next) { // eslint-disable-line no-unused-vars
  const isApiError = err instanceof ApiError;
  const status = isApiError ? err.status : 500;

  // Full context goes to logs, never to the client
  if (status >= 500) {
    console.error({ requestId: req.id, err });
  }

  res.status(status).type('application/problem+json').json({
    type: isApiError ? err.type : `${BASE_URI}/internal`,
    title: isApiError ? err.title : 'Internal Server Error',
    status,
    detail: status >= 500
      ? `An unexpected error occurred. Reference request ID ${req.id} when contacting support.`
      : err.message,
    instance: req.originalUrl,
    timestamp: new Date().toISOString(),
    ...(err.errors && { errors: err.errors }),
    request_id: req.id,
  });
}

module.exports = { ApiError, problemDetails };
