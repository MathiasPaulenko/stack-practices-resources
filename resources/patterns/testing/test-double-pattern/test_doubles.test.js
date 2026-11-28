// Test doubles in jest: stub, spy, fake, mock — same examples as the article.
class UserService {
  constructor(repo) { this.repo = repo; }
  async getName(id) {
    const user = await this.repo.findById(id);
    if (!user) throw new Error('not found');
    return user.name;
  }
}

class FakeUserRepository {
  constructor() { this.users = new Map(); this.nextId = 1; }
  async create(name, email) {
    const user = { id: this.nextId, name, email };
    this.users.set(this.nextId, user);
    this.nextId += 1;
    return user;
  }
  async findById(id) { return this.users.get(id) || null; }
  async count() { return this.users.size; }
}

test('stub returns canned user', async () => {
  const repo = { findById: jest.fn().mockResolvedValue({ id: 1, name: 'Alice' }) };
  const name = await new UserService(repo).getName(1);
  expect(name).toBe('Alice');
  expect(repo.findById).toHaveBeenCalledWith(1);
});

test('spy records send call', () => {
  const email = { send: jest.fn() };
  email.send({ to: 'alice@x.com', subject: 'Order #42 completed' });
  expect(email.send).toHaveBeenCalledTimes(1);
  expect(email.send).toHaveBeenCalledWith({ to: 'alice@x.com', subject: 'Order #42 completed' });
});

test('fake create and find', async () => {
  const repo = new FakeUserRepository();
  const user = await repo.create('Alice', 'alice@x.com');
  const found = await repo.findById(user.id);
  expect(found.name).toBe('Alice');
  expect(await repo.count()).toBe(1);
});

test('mock verifies exact call', async () => {
  const repo = { findById: jest.fn().mockResolvedValue({ id: 1, name: 'Alice' }) };
  await new UserService(repo).getName(1);
  expect(repo.findById).toHaveBeenCalledWith(1);
});
