// Express validation middleware + field-level error formatter — Zod 4 API.
import { z } from 'zod';
import type { NextFunction, Request, Response } from 'express';

export function formatZodErrors(error: z.ZodError): Record<string, string> {
  const formatted: Record<string, string> = {};

  error.issues.forEach((issue) => {
    const path = issue.path.join('.');
    formatted[path] = issue.message;
  });

  return formatted;
}

export function validateBody<S extends z.ZodType>(schema: S) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);

    if (!result.success) {
      return res.status(400).json({
        errors: formatZodErrors(result.error),
      });
    }

    // res.locals is the idiomatic Express channel for per-request data
    res.locals.validatedBody = result.data;
    next();
  };
}

// Usage:
//   app.post('/users', validateBody(UserSchema), (req, res) => {
//     const user = res.locals.validatedBody as User;
//   });
