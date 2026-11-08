// Zod user validation schema — run with: npx tsx user_schema.ts
import { z } from 'zod';

export const UserSchema = z.object({
  email: z.string().email(),
  age: z.number().int().min(18).max(120),
  role: z.enum(['user', 'admin', 'moderator']),
  tags: z.array(z.string()).max(10),
});

export type User = z.infer<typeof UserSchema>;

// Demo: validate a payload and print the result
const payload = { email: 'a@b.com', age: 30, role: 'admin', tags: [] };
const result = UserSchema.safeParse(payload);

if (!result.success) {
  console.error('Invalid:', result.error.flatten());
  process.exit(1);
}
console.log('Valid user:', result.data.email, result.data.role);

// Failing case
const bad = UserSchema.safeParse({ email: 'not-an-email', age: 10, role: 'x' });
console.log('Rejects bad input:', !bad.success);
