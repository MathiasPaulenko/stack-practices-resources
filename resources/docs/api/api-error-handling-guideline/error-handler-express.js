function errorHandler(err, req, res, next) {
  const errorId = `err_${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;
  const statusCode = err.statusCode || 500;
  const code = err.code || "INTERNAL_ERROR";

  const payload = {
    error: {
      id: errorId,
      code: code,
      message: statusCode >= 500
        ? "An internal error occurred. Please try again."
        : err.message,
      details: err.details || [],
      timestamp: new Date().toISOString(),
      path: req.path,
      retryable: err.retryable || false,
      documentation_url: `https://docs.example.com/errors/${code}`,
    },
  };

  if (statusCode >= 500) {
    logger.error({
      errorId,
      code,
      message: err.message,
      stack: err.stack,
      requestId: req.id,
      userId: req.user?.id,
      path: req.path,
      method: req.method,
    });
  } else {
    logger.warn({
      errorId,
      code,
      message: err.message,
      requestId: req.id,
      path: req.path,
    });
  }

  res.status(statusCode).json(payload);
}

class ApiError extends Error {
  constructor(code, message, statusCode, options = {}) {
    super(message);
    this.code = code;
    this.statusCode = statusCode;
    this.details = options.details || [];
    this.retryable = options.retryable || false;
  }
}

// Usage in route handlers
app.post("/v1/users", (req, res, next) => {
  if (!req.body.email || !req.body.email.includes("@")) {
    return next(new ApiError("INVALID_PARAMETER", "The 'email' field must be a valid email address.", 400, {
      details: [{ field: "email", issue: "invalid_format", value: req.body.email }],
    }));
  }
  res.status(201).json({ id: 1, email: req.body.email });
});

app.use(errorHandler);
