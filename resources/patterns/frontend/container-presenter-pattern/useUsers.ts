// useUsers.ts — custom hook playing the container role.
// Copy into your app's hooks folder; point fetch at a real API.
import { useState, useEffect, useCallback, useMemo } from 'react';

export interface User {
  id: number;
  name: string;
  email: string;
}

export function useUsers(apiUrl = '/api/users') {
  const [users, setUsers] = useState<User[]>([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(apiUrl);
      setUsers(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [apiUrl]);

  useEffect(() => { fetchUsers(); }, [fetchUsers]);

  const deleteUser = useCallback(async (userId: number) => {
    setUsers(prev => prev.filter(u => u.id !== userId));
    await fetch(`${apiUrl}/${userId}`, { method: 'DELETE' });
  }, [apiUrl]);

  // Derived view — never filter `users` itself or the full list is lost.
  const visibleUsers = useMemo(
    () => users.filter(u => u.name.toLowerCase().includes(query.toLowerCase())),
    [users, query]
  );

  return { users: visibleUsers, loading, error, deleteUser, setQuery, refetch: fetchUsers };
}
