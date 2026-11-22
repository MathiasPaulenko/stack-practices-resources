// controller/UserController.ts
import type { User, UserModel } from './UserModel';

export class UserController {
  constructor(private model: UserModel) {}

  async loadUsers(): Promise<void> {
    const res = await fetch('/api/users');
    const users = await res.json();
    this.model.setUsers(users);
  }

  search(query: string): User[] {
    return this.model.getFilteredUsers(query);
  }

  sort(field: keyof User, direction: 'asc' | 'desc'): User[] {
    return this.model.getSortedUsers(field, direction);
  }
}
