// model/UserModel.ts
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
