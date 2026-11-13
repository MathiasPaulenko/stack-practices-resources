import { z } from 'zod';

export const createPostSchema = z.object({
  title: z.string()
    .min(3, 'Title must be at least 3 characters')
    .max(200, 'Title must be at most 200 characters')
    .trim(),
  content: z.string()
    .min(10, 'Content must be at least 10 characters')
    .max(50000, 'Content is too long')
    .trim(),
  tags: z.array(z.string().min(1).max(30).trim())
    .min(1, 'At least one tag is required')
    .max(10, 'Maximum 10 tags allowed'),
  publishedAt: z.iso.datetime()
    .optional()
    .refine(
      (date) => !date || new Date(date) > new Date(),
      'Published date must be in the future'
    ),
});

export const updateUserSchema = z.object({
  name: z.string().min(1).max(100).trim().optional(),
  bio: z.string().max(500).trim().optional(),
  website: z.url('Must be a valid URL').optional().or(z.literal('')),
});

export const eventSchema = z.object({
  startDate: z.iso.datetime(),
  endDate: z.iso.datetime(),
}).refine(
  (data) => new Date(data.endDate) > new Date(data.startDate),
  { message: 'End date must be after start date', path: ['endDate'] }
);

export type FieldError = { field: string; message: string };
export type ValidationResult<T> =
  | { success: true; data: T }
  | { success: false; errors: FieldError[] };

export function validateInput<T>(
  schema: z.ZodType<T>,
  input: unknown
): ValidationResult<T> {
  const result = schema.safeParse(input);
  if (result.success) {
    return { success: true, data: result.data };
  }
  const errors = result.error.issues.map((issue) => ({
    field: issue.path.join('.'),
    message: issue.message,
  }));
  return { success: false, errors };
}
