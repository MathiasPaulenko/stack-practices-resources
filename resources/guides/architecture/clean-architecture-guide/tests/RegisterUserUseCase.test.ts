import { RegisterUserUseCase } from '../application/usecases/RegisterUserUseCase';
import { RegisterUserCommand } from '../application/dto/RegisterUserCommand';
import { InMemoryUserRepository } from '../infrastructure/persistence/InMemoryUserRepository';
import { SpyEmailService } from '../infrastructure/email/SpyEmailService';
import { User } from '../domain/entities/User';
import { Email } from '../domain/valueobjects/Email';

// Use-case tests swap the ports for in-memory fakes.
// No database, no network, no container — < 50ms each.
describe('RegisterUserUseCase', () => {
  let repo: InMemoryUserRepository;
  let mailer: SpyEmailService;
  let useCase: RegisterUserUseCase;

  beforeEach(() => {
    repo = new InMemoryUserRepository();
    mailer = new SpyEmailService();
    useCase = new RegisterUserUseCase(repo, mailer);
  });

  test('registers a new user and sends welcome email', async () => {
    const result = await useCase.execute(new RegisterUserCommand('test@example.com'));
    expect(result.isSuccess()).toBe(true);
    expect(mailer.sentEmails).toHaveLength(1);
  });

  test('rejects a duplicate email', async () => {
    repo.add(User.create(Email.create('test@example.com')));
    const result = await useCase.execute(new RegisterUserCommand('test@example.com'));
    expect(result.isFailure()).toBe(true);
    expect(mailer.sentEmails).toHaveLength(0);
  });
});
