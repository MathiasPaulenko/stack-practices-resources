// Test container — overrides production registrations with fakes.
// Companion to https://stackpractices.com/recipes/dependency-injection/

import { DIContainer } from './di-container';

export class TestContainer extends DIContainer {
  constructor() {
    super();
    // Same keys as the production container, different implementations.
    this.registerSingleton('db', () => new InMemoryDatabase());
    this.registerSingleton('emailService', () => new FakeEmailService());
    this.registerScoped('userRepository', () => new InMemoryUserRepository());
    this.registerScoped('userService', () =>
      new UserService(this.resolve('emailService'), this.resolve('userRepository'))
    );
  }
}

// --- Usage with vitest/jest ---
//
// describe('UserService', () => {
//   let container: TestContainer;
//
//   beforeEach(() => {
//     container = new TestContainer();
//     container.beginScope();
//   });
//
//   afterEach(() => container.endScope());
//
//   it('sends welcome email on register', async () => {
//     const svc = container.resolve<UserService>('userService');
//     await svc.register('user@example.com', 'password');
//     const email = container.resolve<FakeEmailService>('emailService');
//     expect(email.sentEmails).toHaveLength(1);
//   });
// });
