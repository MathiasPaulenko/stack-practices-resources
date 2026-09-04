// Repository Pattern — JavaScript implementation.

class User {
  constructor(id, name, role = "member") {
    this.id = id;
    this.name = name;
    this.role = role;
  }
}

class UserRepository {
  /** @abstract */
  getById(id) {
    throw new Error("Not implemented");
  }

  /** @abstract */
  findAll() {
    throw new Error("Not implemented");
  }

  /** @abstract */
  save(user) {
    throw new Error("Not implemented");
  }

  /** @abstract */
  delete(id) {
    throw new Error("Not implemented");
  }
}

class InMemoryUserRepository extends UserRepository {
  constructor() {
    super();
    this.users = new Map();
  }

  getById(id) {
    return this.users.get(id) ?? null;
  }

  findAll() {
    return Array.from(this.users.values());
  }

  save(user) {
    this.users.set(user.id, user);
  }

  delete(id) {
    return this.users.delete(id);
  }
}

class UserService {
  /** @param {UserRepository} repo */
  constructor(repo) {
    this.repo = repo;
  }

  promoteUser(id) {
    const user = this.repo.getById(id);
    if (!user) throw new Error("User not found");
    user.role = "admin";
    this.repo.save(user);
    return user;
  }
}

module.exports = { User, UserRepository, InMemoryUserRepository, UserService };
