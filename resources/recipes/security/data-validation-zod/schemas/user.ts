// Basic user schema — Zod 4 API.
// Run: npx tsx schemas/user.ts  (or: node --experimental-strip-types schemas/user.ts)
import { z } from 'zod';

export const UserSchema = z.object({
  id: z.uuid(),
  email: z.email(),
  name: z.string().min(2).max(50),
  age: z.number().int().min(0).max(150),
  role: z.enum(['user', 'admin', 'moderator']),
  isActive: z.boolean().default(true),
  createdAt: z.coerce.date(),
});

export type User = z.infer<typeof UserSchema>;

export const PasswordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .refine((val) => /[A-Z]/.test(val), 'Password must contain an uppercase letter')
  .refine((val) => /[0-9]/.test(val), 'Password must contain a number')
  .refine((val) => /[^a-zA-Z0-9]/.test(val), 'Password must contain a special character');

const valid = UserSchema.safeParse({
  id: crypto.randomUUID(),
  email: 'admin@example.com',
  name: 'Admin',
  age: 34,
  role: 'admin',
  createdAt: '2026-01-15T10:00:00Z',
});

if (!valid.success) {
  console.error(valid.error.issues);
  process.exit(1);
}
console.log('Valid user:', valid.data.email, '| isActive default:', valid.data.isActive);
console.log('Rejects bad email:', !UserSchema.safeParse({ email: 'nope' }).success);
