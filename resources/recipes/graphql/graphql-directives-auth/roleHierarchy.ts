// roleHierarchy.ts — Role hierarchy utility for auth directives
// Standalone module with no external dependencies, safe to test in isolation.

const roleHierarchy: Record<string, number> = {
  VIEWER: 0,
  EDITOR: 1,
  ADMIN: 2,
};

export function hasRole(userRole: string, requiredRole: string): boolean {
  return (roleHierarchy[userRole] ?? -1) >= (roleHierarchy[requiredRole] ?? 999);
}

export { roleHierarchy };
