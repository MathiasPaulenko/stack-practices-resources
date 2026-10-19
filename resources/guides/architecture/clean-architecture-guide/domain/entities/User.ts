import { Email } from '../valueobjects/Email';
import { UserId } from '../valueobjects/UserId';
import { UserStatus } from '../valueobjects/UserStatus';

// Entity: enterprise business rules. No ORM, no HTTP, no JSON concerns.
export class User {
  private constructor(
    readonly id: UserId,
    private email: Email,
    private status: UserStatus
  ) {}

  static create(email: Email): User {
    return new User(UserId.generate(), email, UserStatus.PENDING);
  }

  // Rebuilds a persisted user without re-running creation invariants.
  static reconstitute(id: UserId, email: Email, status: UserStatus): User {
    return new User(id, email, status);
  }

  activate(): void {
    this.status = UserStatus.ACTIVE;
  }

  isActive(): boolean {
    return this.status === UserStatus.ACTIVE;
  }

  get emailAddress(): string {
    return this.email.value;
  }

  get statusValue(): UserStatus {
    return this.status;
  }
}
