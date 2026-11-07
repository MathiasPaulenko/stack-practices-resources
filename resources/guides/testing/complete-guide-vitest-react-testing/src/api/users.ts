export interface User {
  id: number;
  name: string;
  email: string;
}

export async function fetchUser(id: number): Promise<User> {
  const res = await fetch(`${window.location.origin}/api/users/${id}`);
  if (!res.ok) throw new Error("Failed to load user");
  return res.json();
}
