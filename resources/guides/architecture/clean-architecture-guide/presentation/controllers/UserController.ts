import { RegisterUserUseCase } from '../../application/usecases/RegisterUserUseCase';
import { RegisterUserCommand } from '../../application/dto/RegisterUserCommand';

interface RegisterUserDto {
  email: string;
  password: string;
}

interface UserResponse {
  status: number;
  body: { id?: string; email?: string; error?: string };
}

// Adapter: translates HTTP DTOs into domain commands and results
// into HTTP responses. Keeps zero business logic.
export class UserController {
  constructor(private registerUser: RegisterUserUseCase) {}

  async register(dto: RegisterUserDto): Promise<UserResponse> {
    const result = await this.registerUser.execute(new RegisterUserCommand(dto.email));
    if (result.isFailure() || !result.value) {
      return { status: 400, body: { error: result.error ?? 'registration failed' } };
    }
    return { status: 201, body: { id: result.value.id.value, email: result.value.emailAddress } };
  }
}
