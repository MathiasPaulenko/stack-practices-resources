import "server-only";

// Auth stub — in a real app this reads the session cookie through
// Auth.js/NextAuth, Clerk, or your provider of choice. It only ever runs on
// the server: Server Components can call it during render and Server Actions
// must call it before mutating anything.

export type SessionUser = {
  id: string;
  name: string;
  email: string;
  isAdmin: boolean;
};

export type Session = {
  user: SessionUser;
} | null;

const DEMO_USER: SessionUser = {
  id: "user-demo",
  name: "Demo User",
  email: "demo@stackpractices.dev",
  // Flip to false and submit the create form to see the "Unauthorized"
  // state returned by the Server Action.
  isAdmin: true,
};

export async function auth(): Promise<Session> {
  return { user: DEMO_USER };
}
