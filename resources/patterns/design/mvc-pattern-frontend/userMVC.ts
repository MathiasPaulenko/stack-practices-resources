// userMVC.ts — Model and Controller in one module for the Vue example.
// Equivalent to combining UserModel.ts and UserController.ts.

export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

export class UserModel {
  private users: User[] = [];

  setUsers(users: User[]) {
    this.users = users;
  }

  getFilteredUsers(query: string): User[] {
    if (!query) return this.users;
    const lower = query.toLowerCase();
    return this.users.filter(u =>
      u.name.toLowerCase().includes(lower) ||
      u.email.toLowerCase().includes(lower)
    );
  }

  getSortedUsers(field: keyof User, direction: 'asc' | 'desc'): User[] {
    return [...this.users].sort((a, b) => {
      const cmp = String(a[field]).localeCompare(String(b[field]));
      return direction === 'desc' ? -cmp : cmp;
    });
  }
}

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
