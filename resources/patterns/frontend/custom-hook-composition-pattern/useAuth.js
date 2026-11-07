import { createContext, useContext } from 'react';

// In a real app this context is created and provided by an AuthProvider.
export const AuthContext = createContext(null);

/**
 * Reads the auth context and throws a clear error outside the provider.
 * Note the guard checks the *value* returned by useContext, not the
 * context object itself.
 */
export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  const { user, token, login, logout, isLoading } = context;
  return { user, token, login, logout, isLoading, isAuthenticated: !!user };
}

export default useAuth;
