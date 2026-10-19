import { User } from '../domain/entities/User';
import { Email } from '../domain/valueobjects/Email';
import { UserStatus } from '../domain/valueobjects/UserStatus';

// Pure domain tests: no database, no network, no mocks. < 10ms each.
describe('User', () => {
  test('create sets status to PENDING', () => {
    const user = User.create(Email.create('test@example.com'));
    expect(user.isActive()).toBe(false);
    expect(user.statusValue).toBe(UserStatus.PENDING);
  });

  test('activate sets status to ACTIVE', () => {
    const user = User.create(Email.create('test@example.com'));
    user.activate();
    expect(user.isActive()).toBe(true);
  });
});
