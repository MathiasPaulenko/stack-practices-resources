// view/UserListView.tsx
import { useState, useEffect } from 'react';
import type { User } from './UserModel';
import type { UserController } from './UserController';

export function UserListView({ controller }: { controller: UserController }) {
  const [users, setUsers] = useState<User[]>([]);
  const [query, setQuery] = useState('');

  useEffect(() => {
    controller.loadUsers().then(() => {
      setUsers(controller.search(''));
    });
  }, [controller]);

  const handleSearch = (q: string) => {
    setQuery(q);
    setUsers(controller.search(q));
  };

  return (
    <div>
      <input
        type="search"
        value={query}
        onChange={e => handleSearch(e.target.value)}
        placeholder="Search users..."
      />
      <ul>
        {users.map(u => (
          <li key={u.id}>{u.name} — {u.email}</li>
        ))}
      </ul>
    </div>
  );
}
