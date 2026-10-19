import { User } from '../../domain/entities/User';
import { Email } from '../../domain/valueobjects/Email';
import { UserRepository } from '../../domain/repositories/UserRepository';
import { EmailService } from '../../domain/services/EmailService';
import { RegisterUserCommand } from '../dto/RegisterUserCommand';
import { Result } from '../results/Result';

// Use case: application business rule "register a user".
// Depends on ports only — never on Express, Knex, or SendGrid.
export class RegisterUserUseCase {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async execute(command: RegisterUserCommand): Promise<Result<User>> {
    const existing = await this.userRepository.findByEmail(command.email);
    if (existing) {
      return Result.failure('Email already registered');
    }

    const user = User.create(Email.create(command.email));
    await this.userRepository.save(user);
    await this.emailService.sendWelcome(user.emailAddress);

    return Result.success(user);
  }
}
